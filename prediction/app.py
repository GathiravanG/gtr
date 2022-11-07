from asyncio.windows_events import NULL
import json
from flask import Flask,jsonify, request
from flask import render_template
from flask import request, redirect, url_for,flash,Flask
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import ml as obj
app=Flask(__name__)

CORS(app)

@app.route('/', methods=['GET', 'POST'])
def essentials():
    return jsonify("GathiR")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLD = '\GTR24\predictor'
UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLD)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/uploadnow', methods=["GET" , "POST"])
def upload_file():
    
    file = request.files['file']
    file.filename = 'predict.csv'
    
    if file :
      print("hello")
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return json.dumps("uploaded")
    print("end")
    return "success"


@app.route('/column', methods=['GET','POST'])
def essential1():
    columnname = request.data
    print(columnname)
    return jsonify("Success")

@app.route('/period', methods=['POST'])
def essential2():
    predictingperiod = request.json
    print(predictingperiod)
    number=int(predictingperiod["period"])
    multiple=int(predictingperiod["target"])
    ans = number*multiple
    print(ans)
    obj.predictionCumEvaluation(ans)
    return jsonify("Success")
    

if __name__=='__main__':
    app.run(debug=True)