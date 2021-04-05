import redis
import json
from flask import Flask, request, render_template

red = redis.Redis(
    host = 'redis-18308.c238.us-central1-2.gce.cloud.redislabs.com',
    port = 18308,
    password = 'ljLCe2nxalVGsAtde9nHglLiZJVMFVS7'
)

app = Flask(__name__)



@app.route('/reset', methods=['POST'])
@app.route('/main', methods=['POST'])
@app.route('/', methods=['POST', 'GET'])
def settingsPost():
    if request.method == "POST":
        
        settings_dict = {
            'host' : request.form['host'],
            'update_frequency' : request.form['update_frequency'],
            'text' : request.form['text'],
        }

        red.set('settings', json.dumps(settings_dict))
        
        return render_template("settings.html")

    else:
        return render_template("settings.html")

@app.route('/workspaces', methods=['POST', 'GET'])
def workspaces():
    if request.method == "POST":
        workspaces = json.loads(red.get('workspaces'))

        if type(workspaces) is not dict:
            workspaces = {}

        elif request.form['token'] not in workspaces.keys():
            workspaces[request.form['token']] = {}

        workspaces[request.form['token']][request.form['channel']] = list(request.form['tegs'].split(' '))
    
        red.set('workspaces', json.dumps(workspaces))
        
        return render_template("channels.html")
    
    else:
        return render_template("channels.html")

@app.route('/reset', methods=['GET'])
def reset():
    if request.method == "GET":
        settings_dict = {}
        workspaces = {}

        red.set('settings', json.dumps(settings_dict))
        red.set('workspaces', json.dumps(workspaces))

        return render_template("settings.html")
    
    else:
        return render_template("settings.html")

@app.route('/main', methods=['GET'])
def main():
    if request.method == "GET":
        return render_template("settings.html")

    else:
        return render_template("settings.html")
    

    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)