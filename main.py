import os, json, re
from flask import Flask, render_template, request, abort, Response, send_from_directory, jsonify

#custom module
from database import track_page

app = Flask(__name__)


#-------------------------------------------------------------------
# constants / variables
#-------------------------------------------------------------------

HOST = '::'
PORT = 8081


#-------------------------------------------------------------------
# helper functions
#-------------------------------------------------------------------

with open('static/favicon.ico', 'rb') as f:
    favicon_data = f.read()


with open('data/apps.json', 'r') as file:
    PROJECTS = json.load(file)

PROJECTS_NO_ADMIN = PROJECTS[:-1]


#-------------------------------------------------------------------
# content routes
#-------------------------------------------------------------------

@app.route('/projects')
def api_projects():
    admin_cookie = request.cookies.get('admin_cookie')
    access_cookie = request.cookies.get('access_cookie')
    if not access_cookie:
        abort(404)
    if admin_cookie:
        return jsonify(PROJECTS)
    return jsonify(PROJECTS_NO_ADMIN)  


@app.route('/')
def home():
    response = send_from_directory('templates', 'index.html')
    response.set_cookie('access_cookie', 'true')
    return response


@app.route('/apps/<app_name>.html')
def serve_app(app_name):
    return send_from_directory('apps', app_name + '.html')


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
    if re.match(r'^[\w/]+/\w+\.(jpg|jpeg|png|gif)$', path):
        return send_from_directory('img', path)
    abort(403) 
    

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