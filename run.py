import boto3
from flask import Flask, render_template, request, send_from_directory
from dashboard import get_dashboard_data
from logs import get_logs_data
from settings import get_settings_data

app = Flask(__name__)
dynamodb = boto3.client('dynamodb', endpoint_url='http://localhost:8000')

@app.route('/')
@app.route('/index')
def index():
   return render_template('home/index.html')

@app.route('/dashboard')
def dashboard():
   return render_template('home/dashboard.html', dashboard_data = get_dashboard_data(dynamodb))
 
@app.route('/settings', methods=('GET', 'POST'))
def settings():
   return render_template('home/settings.html', settings_data = get_settings_data(request, dynamodb))

@app.route('/logs')
def logs():
   return render_template('home/logs.html', logs_data = get_logs_data(request))

@app.route('/logs/download')
def logs_download():
   filename = request.args.get('filename')
   if '-' in filename:
      filename = filename.replace('-', '#')
   return send_from_directory(directory="../log/", path=filename)
   
if __name__ == '__main__':
   app.run(debug = True)
   
