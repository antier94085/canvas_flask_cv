from flask import Flask
from edge import bp as edge
from image import bp as sendImage

def register(app: Flask):
    app.register_blueprint(edge)
    app.register_blueprint(sendImage)