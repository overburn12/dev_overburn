import os
from flask import Flask, render_template, request, abort, Response, send_from_directory
from werkzeug.utils import secure_filename

#custom module
from database import track_page

app = Flask(__name__)


#-------------------------------------------------------------------
# constants
#-------------------------------------------------------------------

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
IMAGE_DIR = 'img/'

HOST = '0.0.0.0'
PORT = 8081


#-------------------------------------------------------------------
# helper functions
#-------------------------------------------------------------------

with open('static/favicon.ico', 'rb') as f:
    favicon_data = f.read()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def file_exists(filename):
    return os.path.exists(os.path.join(IMAGE_DIR, filename))


#-------------------------------------------------------------------
# content routes
#-------------------------------------------------------------------

@app.route('/')
def index():
    return "Welcome to overburn.dev"


@app.route('/robots.txt')
def robots_txt():
    content = "User-agent: *\nDisallow: /"
    return Response(content, mimetype='text/plain')


#-------------------------------------------------------------------
# image routes
#-------------------------------------------------------------------

@app.route('/favicon.ico')
def favicon():
    return Response(favicon_data, mimetype='image/vnd.microsoft.icon')


@app.route('/img/<path:image_name>')
def serve_image(image_name):
    image_name = secure_filename(image_name)
    
    if not allowed_file(image_name) or not file_exists(image_name):
        abort(404)
    try:
        return send_from_directory(IMAGE_DIR, image_name)
    except FileNotFoundError:
        abort(404)


#-------------------------------------------------------------------
# aux. routes
#-------------------------------------------------------------------

@app.after_request
def after_request(response):
    track_page(request, response)
    return response


@app.errorhandler(404)
def page_not_found(e):
    return "this page does not exist, sorry!", 404


#-------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)