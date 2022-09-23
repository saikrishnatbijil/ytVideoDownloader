import os
from flask import Flask, request, render_template, session, send_file
from pytube import YouTube
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'ki5388477h346553773hdf4'
app.config['SESSION_TYPE'] = 'filesystem'

links = ""

def setData(link):
    links = link
    return links

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        session['link'] = request.form.get("link")
        if not session['link'] == "":
            yt = YouTube(session['link'])
            print(setData(session['link']))
            return render_template("homer.html", title=yt.title, views=yt.views, url=yt.thumbnail_url)

    return render_template("index.html")


@app.route("/downloadvideo", methods=["GET", "POST"])
def downloadvideo():
    bufferer = BytesIO()
    yt = YouTube(session['link'])
    yd = yt.streams.get_highest_resolution()
    yd.stream_to_buffer(bufferer)
    bufferer.seek(0)
    return send_file(bufferer, as_attachment=True, download_name=yt.title+'.mp4', mimetype='video/mp4')
    # return send_file(bufferer, yd.download(), as_attachment=True, download_name=yt.title+'.mp4')


@app.route("/downloadaudio", methods=["GET", "POST"])
def downloadaudio():
    buffer = BytesIO()
    yt = YouTube(session['link'])
    # yd = yt.streams.get_highest_resolution()
    yd = yt.streams.filter(only_audio=True).first()
    new_file = yd.title + '.mp3'
    os.rename(yd.download(), new_file)
    yd.stream_to_buffer(buffer)
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=yt.title+'.mp3', mimetype='audio/mp3')
    # return send_file(yd.download(), as_attachment=True)    



if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)