from flask import render_template, request
from flask import redirect, url_for
from PIL import Image
import os

from app.utils import pipeline_model

UPLOAD_PATH = "static/uploads"
PREDICT_PATH = "static/predict"

def base():
    return render_template("base.html")

def index():
    return render_template("index.html")

def faceapp():
    return render_template("faceapp.html")

def getwidth(path):
    img = Image.open(path)
    size = img.size
    aspect_ratio = size[0]/size[1]
    width = 250*aspect_ratio #250 given in gender.html
    return width


def gender():
    if request.method == "POST":
        img = request.files["image"]  #name/key given in gender.html = "image"
        filename = img.filename
        path = os.path.join(UPLOAD_PATH,filename)
        img.save(path)
        width = getwidth(path)
        out_path = os.path.join(PREDICT_PATH,"predict_"+filename)
        pipeline_model(path,filename)
        return render_template("gender.html",fileupload=True,img_name=filename,w= width)
        #img_name ll be passed to html page to display the uploaded image
    return render_template("gender.html",fileupload=False,img_name="python.png",w=250)