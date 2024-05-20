from flask import send_file, Blueprint

bp = Blueprint("image", __name__)

@bp.route('/image')
def getImage():
    return send_file('300DPI.png', mimetype='image/png')

@bp.route('/origin')
def getOrigin():
    return send_file('img.png', mimetype='image/png')

