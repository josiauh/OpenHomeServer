"""
OpenHomeServer
You guessed it, it's a home server!
"""
import os
import mimetypes
import random
from flask import Flask, send_file, render_template, request, Response
app = Flask(__name__)

pin = "2763"

def isVideo(path):
    try:
        return mimetypes.guess_type(path)[0].startswith('video')
    except:
        return False

def getVideos():
    return [videoFile for videoFile in os.listdir("videos") if isVideo(os.path.join("videos", videoFile))]

@app.route("/uploadVideo", methods=["POST"])
def videoUpload():
    try:
        if 'video' in request.files and 'PIN' in request.form and request.form['PIN'] == pin:
            f = request.files["video"]
            f.save(os.path.join("videos", os.path.basename(f.filename)))
            return Response("Uploaded", 200)
        elif 'PIN' in request.form and request.form['PIN'] != pin:
            return Response("PIN disallowed", 401)
        elif 'PIN' in request.form and request.form['PIN'] == pin and 'video' not in request.files:
            return Response("Video not found", 400)
        else:
            return Response("Invalid request", 400)
    except Exception as e:
        return Response(f"Error: {str(e)}", 500)

@app.route("/")
def home():
    currVid = getVideos()[int(random.Random().random() * len(getVideos()))]
    print(currVid)
    return render_template("home.html", latestVideo=currVid)

@app.route("/video/<path:video>")
def videoPlayer(video):
    return render_template("videoPlayer.html", video=os.path.join("videos", video))

@app.route("/videoManager")
def videoManager():
    print(os.listdir("videos"))
    return render_template("videoManager.html", videos=getVideos())

@app.route("/videos/<path>")
def video(path):
    return send_file(os.path.join("videos", path))

@app.route("/style.css")
def stylesheet():
    return send_file("style.css")