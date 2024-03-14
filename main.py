from flask import Flask, render_template, request, jsonify, abort, Response, send_from_directory
import json

from database import track_page

app = Flask(__name__)

with open('static/favicon.ico', 'rb') as f:
    favicon_data = f.read()

@app.route('/')
def index():
    return "Welcome to overburn.dev"

@app.route('/favicon.ico')
def favicon():
    return Response(favicon_data, mimetype='image/vnd.microsoft.icon')

@app.after_request
def after_request(response):
    track_page(request, response)
    return response

@app.errorhandler(404)
def page_not_found(e):
    return "this page does not exist, sorry!", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)