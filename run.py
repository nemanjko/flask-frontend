import boto3
from flask import Flask, render_template

app = Flask(__name__)
dynamodb = boto3.client('dynamodb', endpoint_url='http://localhost:8000')

@app.route('/')
@app.route('/index')
def index():
   return render_template('home/index.html')

@app.route('/dashboard')
def dashboard():
   return render_template('home/dashboard.html')
 
@app.route('/settings')
def settings():
   return render_template('home/settings.html')

@app.route('/logs')
def logs():
   return render_template('home/logs.html')
   
if __name__ == '__main__':
   app.run(debug = True)
   
