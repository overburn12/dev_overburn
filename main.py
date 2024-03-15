import os, json, re
from flask import Flask, render_template, request, abort, Response, send_from_directory

#custom module
from database import track_page

app = Flask(__name__)


#-------------------------------------------------------------------
# constants / variables
#-------------------------------------------------------------------

HOST = '0.0.0.0'
PORT = 8081


#-------------------------------------------------------------------
# helper functions
#-------------------------------------------------------------------

with open('static/favicon.ico', 'rb') as f:
    favicon_data = f.read()


with open('data/apps.json', 'r') as file:
    PROJECTS = json.load(file)


#-------------------------------------------------------------------
# content routes
#-------------------------------------------------------------------

@app.route('/')
def home():
    return render_template('index.html', projects=PROJECTS)


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


@app.route('/img/<path:path>')
def serve_image(path):
    if not re.match(r'^[\w/]+/\w+\.(jpg|jpeg|png|gif)$', path):
        print(f"fpath failed: {path}")
        abort(404) 

    return send_from_directory('img', path)
    

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