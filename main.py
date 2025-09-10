from flask import Flask, render_template, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import os

app = Flask(__name__)

token = ""

def fetch_token():
    global token
    url = "https://api.artsy.net/api/tokens/xapp_token?client_id=208b20e0a3e74e677cef&client_secret=87014948d402d1d0b9934dd621e5ab0f"
    response = requests.post(url)
    
    if response.status_code in [200, 201]:  
        data = response.json()
        token = data.get("token", "")  
    else:
        print(f"Failed to fetch token. Status code: {response.status_code}")


@app.route("/")
def root():
    return render_template("index.html")

@app.route('/api/search', methods=['GET'])
def search_artist():
    query = request.args.get('q')
    
    if not query:
        return jsonify({'error': 'No query provided'}), 400

    search_api_url = f"https://api.artsy.net/api/search?q={query}&size=10&type=artist"
    headers = {
        'X-XAPP-Token': token,
        'Content-Type': 'application/json',
    }
    
    try:
        response = requests.get(search_api_url, headers=headers)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/artist/<artist_id>', methods=['GET'])
def get_artist(artist_id):
    if not artist_id:
        return jsonify({'error': 'No artist ID provided'}), 400

    artist_api_url = f"https://api.artsy.net/api/artists/{artist_id}"
    headers = {
        'X-XAPP-Token': token,
        'Content-Type': 'application/json',
    }
    
    try:
        response = requests.get(artist_api_url, headers=headers)
        response.raise_for_status()  
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


fetch_token()

scheduler = BackgroundScheduler()
scheduler.add_job(fetch_token, 'interval', days=7)
scheduler.start()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
