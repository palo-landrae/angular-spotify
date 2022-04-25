from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify, make_response, render_template
from flask_cors import CORS
import requests
import os
import base64

dir_path = os.path.dirname(os.path.realpath(__file__))
static_path = os.path.join(dir_path, 'dist/angular-spotify')
template_path = os.path.join(dir_path,'dist/angular-spotify') 

app = Flask(__name__, static_url_path='/static', static_folder=static_path, template_folder=template_path)
CORS(app)

# urls
TOKEN_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1/'

# .env
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REFRESH_TOKEN = os.getenv('SPOTIFY_REFRESH_TOKEN')

def get_access_token():
    basic = base64.urlsafe_b64encode((f'{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}').encode())
    headers = {
        'Authorization': 'Basic %s' % basic.decode('ascii'),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': SPOTIFY_REFRESH_TOKEN 
    }
    access_token_response = requests.post(url=TOKEN_URL, data=payload, headers=headers)
    return access_token_response.json()

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/api/search_track")
def search_track():
    access_token = get_access_token().get('access_token')
    query = request.args.get('q')
    url = BASE_URL + f'search/?q={query}&type=track'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url=url, headers=headers)
    return make_response(jsonify(response.json()), 200)

@app.route("/api/get_track")
def get_track():
    access_token = get_access_token().get('access_token')
    track_id = request.args.get('id')
    url = BASE_URL + f'tracks/{track_id}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url=url, headers=headers)
    return make_response(jsonify(response.json()), 200)

if __name__ == '__main__':
    app.run(host='localhost', port=5000)
