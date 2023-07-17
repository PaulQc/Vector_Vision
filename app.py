
from flask import Flask, render_template, session
from vector_vision_helper import Messages, VectorText
from image_analysis import analyse_image

import anki_vector
from anki_vector.util import degrees
import numpy as np
import matplotlib.image
import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env

app = Flask(__name__)
app.secret_key = 'the random string for Vector in Quebec city'.encode('utf8')
app.vector_text = VectorText()
app.messages = Messages()
app.key = os.getenv("key")
app.endpoint = os.getenv("endpoint")

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Page d'entré pour l'interaction avec Vector
    """
    # La variable session['step] garde en mémoire de l'étape où l'utilisateur est rendu
    session['step'] = 'introduction'
    return render_template('index.html')


@app.route('/try_to_connect', methods=['GET', 'POST'])
def try_to_connect():
    """
    Méthode qui affiche le message que l'on essaie de se connecter à Vector
    et qui lance la méthode à cet effet
    """
    current_step = 'try_to_connect'
    session['step'] = current_step
    text = app.messages.message[current_step]
    return render_template('message.html', text=text, step=current_step)


@app.route('/trying_to_connect', methods=['GET', 'POST'])
def trying_to_connect():
    """
    Méthode pour essayer de se connecter à Vecteur
    Renvoi un message dépendamment si la connexion a pu être établie ou pas
    """
    app.robot = anki_vector.Robot(serial='00508611')
    try:
        app.robot.connect()
        current_step = 'connected'  # i.e. la connection a été établie
    except:
        print('Unable to connect to Vector')
        current_step = 'connection_fail'
    #
    session['step'] = current_step
    text = app.messages.message[current_step]
    return render_template('message.html', text=text, step=current_step)


@app.route('/take_picture', methods=['GET', 'POST'])
def take_picture():
    """
    Méthode pour prendre un image avec le robot Vector
    """
    vector_text = app.vector_text.text['take_picture']
    app.robot.behavior.set_head_angle(degrees(5))  # Positionne la tête de Vector
    app.robot.behavior.set_lift_height(1, duration=2.0)  # 1 = MAX_LIFT_HEIGHT_MM
    app.robot.behavior.say_text(vector_text)
    # Prend un photo
    image = app.robot.camera.capture_single_image()
    image = np.array(image.raw_image)
    # Sauve cette photo
    matplotlib.image.imsave('./static/current_picture.png', image)
    session['image_file'] = 'current_picture.png'
    # Confirme
    vector_text = app.vector_text.text['picture_taken']
    app.robot.behavior.say_text(vector_text)
    #
    current_step = 'validate_picture'
    session['step'] = current_step
    text = app.messages.message[current_step]
    return render_template('message.html', text=text, step=current_step, image_file=session['image_file'])


@app.route('/retake_picture', methods=['GET', 'POST'])
def retake_picture():
    """
    Méthode pour reprendre l'image à analyser
    """
    current_step = 'retake_picture'
    session['step'] = current_step
    text = app.messages.message[current_step]
    return render_template('message.html', text=text, step=current_step)


@app.route('/analyse_picture', methods=['GET', 'POST'])
def analyse_picture():
    """
    Méthode pour lancer indiquer que l'analyse de l'image qui a été prise par Vector est lancé
    """
    current_step = 'analyse_picture'
    session['step'] = current_step
    text = app.messages.message[current_step]
    image_file = session['image_file']
    return render_template('message.html', text=text, step=current_step, image_file=image_file)


@app.route('/analyse_result', methods=['GET', 'POST'])
def analyse_result():
    """
    Méthode pour analyser l'image et donner les résultats
    """
    path = './static/'
    filename = session['image_file']
    description, readtext = analyse_image(path, filename, app.key, app.endpoint)
    session['description'] = description
    session['readtext'] = readtext
    print("Description de l'image = ", description)
    print("Texte sur l'image = ", readtext)
    # Texte que Vector doit dire
    vector_text = app.vector_text.text['image_description']
    app.robot.behavior.say_text(vector_text)
    app.robot.behavior.say_text(description)
    if len(readtext) > 2:
        vector_text = app.vector_text.text['image_text']
        app.robot.behavior.say_text(vector_text)
        app.robot.behavior.say_text(readtext)
    current_step = 'analyse_result'
    session['step'] = current_step
    text = app.messages.message[current_step]
    image_file = "image_bbox.png"
    return render_template('message.html', text=text, step=current_step, image_file=image_file)


@app.route('/replay_analyse_result', methods=['GET', 'POST'])
def replay_analyse_result():
    """
    Méthode pour donner a nouveau les résultats de l'analyse
    """
    # Reload les résultats de l'analyse courrante
    description = session['description']
    readtext = session['readtext']
    #
    vector_text = app.vector_text.text['image_description']
    app.robot.behavior.say_text(vector_text)
    app.robot.behavior.say_text(description)
    if len(readtext) > 2:
        vector_text = app.vector_text.text['image_text']
        app.robot.behavior.say_text(vector_text)
        app.robot.behavior.say_text(readtext)

    current_step = 'analyse_result'
    session['step'] = current_step
    text = app.messages.message[current_step]
    image_file = session['image_file']
    return render_template('message.html', text=text, step=current_step, image_file=image_file)


@app.route('/recommencer', methods=['GET', 'POST'])
def recommencer():
    """
    Méthode qui met fin à la connexion et retourne à la page d'entré pour l'interaction avec Vector
    """
    app.robot.disconnect()
    # La variable session['step] garde en mémoire de l'étape où l'utilisateur est rendu
    session['step'] = 'introduction'
    return render_template('index.html')


if __name__ == "__main__":
    create_app().run()
