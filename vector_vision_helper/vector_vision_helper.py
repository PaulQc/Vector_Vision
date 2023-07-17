# Variables et méthodes en support à l'application "VectorVision"
# Paul Grenier
# 2023


class Messages(object):
    def __init__(self):
        """Définie les différents messages à fournir à l'utilisateur aux différentes étapes, soit:
         'initial', 'go', 'no_go' et 'fin'
         """
        self.message = {
            'try_to_connect': "<b><em>Bien reçu !</em></b> Voyons si Vector est disponible <br>" +
                              "pour votre requête. S'il s'arrête, c'est bon signe :<br>" +
                              "<em>C'est qu'il se prépare à vous répondre !</em>",
            'connected': "Placer l'image à environ 5cm devant Vector pour qu'il puisse<br>" +
                         " bien voir l'image que vous désirez qu'il interprète.<br><br>" +
                         "<small>Appuyer lorsque <em>prêt</em></small>",
            'connection_fail': "<b><em>Malheureusement</em></b>, <br>" +
                               " Vector ne répond pas aux commandes <em>il est têtu parfois !</em>" +
                               "<br><small>Vous serez redirigés vers la page d'accueil dans 5sec.</small>",
            'validate_picture': "Est-ce que cette image prise<br>" +
                                " par Vector est satisfaisante ?",
            'retake_picture': "Repositionnez l'image devant Vector <br>" +
                              "pour reprendre une image <br>" +
                              "<small>Appuyer lorsque prêt à <em>reprendre</em> l'image</small>",
            'analyse_picture': "Vector analyse l'image<br>" +
                               "et vous donnera ses observations sous peu",
            'analyse_result': "Voici le détail de l'analyse de l'image faite par Vector<br>" +
                              "Vous pouvez réécouter Vector ou retourner au début"
        }


class VectorStatus(object):
    def __init__(self):
        """Variable pour garder l'état de Vector, soit:
        'available' (= valeur initiale) et 'not_available' (si Vector est occupé ailleurs)
        """
        self.status = 'available'
        self.connection = ''  # 3 possibilité: active, close, unavailable


class VectorText(object):
    def __init__(self):
        """Définie les différents messages de Vector
        """
        self.text = {
            'take_picture': "Ok, I will take a picture in four, three, two, one zero",
            'picture_taken': "I got it",
            'image_description': "Here is what I understand from this picture",
            'image_text': "The image has the following text"
        }
