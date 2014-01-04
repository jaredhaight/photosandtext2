from flask import render_template, send_from_directory
from photosandtext2 import app
from photosandtext2.models import Photo, Crop

#Serve photos from dev
if app.config['DEBUG']:
    @app.route('/media/<path:filename>')
    def send_foo(filename):
        return send_from_directory('/Users/jared/Documents/PycharmProjects/photosandtext2/media', filename)

@app.route('/')
def home():
    crops = Crop.query.filter_by(name="home400")
    return render_template('home.html', crops=crops)