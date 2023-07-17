# Méthodes pour l'analyse d'image a l'aide de la plateforme Azure
# Adaptation de l'example contenu dans le SDK de Azure
# https://github.com/Azure-Samples/azure-ai-vision-sdk/tree/main/samples/python/image-analysis
# Paul Grenier
# 2023

import azure.ai.vision as visionsdk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches


def analyse_image(path, filename, key, endpoint):
    """
    Méthode pour l'analyse d'image avec Azure AI Vision. La méthode retourne la description ("caption")
    et le texte se trouvant dans l'image ("readtext"), le cas échéant.
    Une image "image_bbox.png" avec les bonding boxes et les labels est sauvegardée dans "path"
    :param path, filename : Chemin et nom du fichier de l'image, et Azure key and endpoint
    :return caption (str), readtext (str)
    """
    image_courante = path + filename

    """
    Analyze image from file, all features, synchronous (blocking)
    """
    service_options = visionsdk.VisionServiceOptions(endpoint, key)

    # Specify the image file on disk to analyze. sample.jpg is a good example to show most features
    vision_source = visionsdk.VisionSource(filename=image_courante)

    # Set the language and one or more visual features as analysis options
    analysis_options = visionsdk.ImageAnalysisOptions()

    # Mandatory. You must set one or more features to analyze.
    analysis_options.features = (
            visionsdk.ImageAnalysisFeature.CAPTION |
            visionsdk.ImageAnalysisFeature.DENSE_CAPTIONS |
            visionsdk.ImageAnalysisFeature.OBJECTS |
            visionsdk.ImageAnalysisFeature.PEOPLE |
            visionsdk.ImageAnalysisFeature.TEXT |
            visionsdk.ImageAnalysisFeature.TAGS
    )

    # Optional. Default is "en" for English. See https://aka.ms/cv-languages for a list of supported
    # language codes and which visual features are supported for each language.
    analysis_options.language = "en"

    # Optional. Default is "latest".
    analysis_options.model_version = "latest"

    # Optional, and only relevant when you select ImageAnalysisFeature.CAPTION.
    # Set this to "true" to get a gender neutral caption (the default is "false").
    analysis_options.gender_neutral_caption = False

    # Create the image analyzer object
    image_analyzer = visionsdk.ImageAnalyzer(service_options, vision_source, analysis_options)

    # Do image analysis for the specified visual features
    # This call creates the network connection and blocks until Image Analysis results
    # return (or an error occurred). Note that there is also an asynchronous (non-blocking)
    # version of this method: image_analyzer.analyze_async().
    result = image_analyzer.analyze()

    """
    Extract Bonding boxes
    """
    labels = []
    bboxes = []
    confidences = []
    if result.objects is not None:
        for object in result.objects:
            labels.append(object.name)
            bboxes.append([object.bounding_box.x, object.bounding_box.y,
                           object.bounding_box.w, object.bounding_box.h])
            confidences.append(object.confidence)
    # plot_bboxes(
    #     image_file=image_courante, bboxes=bboxes,
    #     xywh=True, labels=labels, confidences=confidences
    # )

    """
    Extract image caption and the read image text, if any  
    """
    if result.caption is not None:
        caption = result.caption.content
        print("Description : ", caption)
    readtext = ""
    if result.text is not None:
        for line in result.text.lines:
            readtext = readtext + line.content + " "
        print("Texte sur l'image : ", readtext)

    """
    Plot picture with bonding boxe
    Code provenant de : https://minibatchai.com/cv/detection/2021/07/03/BoundingBox.html
    que j'ai modifié
    """
    xywh = True  # True when the bounding box annotations specified as [xmin, ymin, width, height]

    fig = plt.figure()

    # add axes to the image
    ax = fig.add_axes([0, 0, 1, 1])

    # read and plot the image
    image = plt.imread(image_courante)
    plt.imshow(image)

    # Iterate over all the bounding boxes
    for i, bbox in enumerate(bboxes):
        if xywh:
            xmin, ymin, w, h = bbox
        else:
            xmin, ymin, xmax, ymax = bbox
            w = xmax - xmin
            h = ymax - ymin

        # add bounding boxes to the image
        box = patches.Rectangle(
            (xmin, ymin), w, h, edgecolor="red", facecolor="none"
        )

        ax.add_patch(box)

        if labels is not None:
            rx, ry = box.get_xy()
            # cx = rx  + box.get_width()/2.0
            # cy = ry  + box.get_height()/8.0
            # Change to be top and left justified  : Paul Grenier
            cx = rx
            cy = ry
            label = labels[i]
            if confidences is not None:
                label = label + ", {:2.0f}%".format(confidences[i] * 100)
            l = ax.annotate(
                label,
                (cx, cy),
                fontsize=8,
                fontweight="bold",
                color="white",
                ha='left',
                va='baseline'
            )
            # l.set_bbox(
            #   dict(facecolor='red', alpha=0.5, edgecolor='red')
            # )

    plt.axis('off')
    outfile = path + "image_bbox.png"
    fig.savefig(outfile)

    return caption, readtext

