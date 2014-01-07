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
    crops = Crop.query.filter_by(name="home600")
    return render_template('home.html', crops=crops)

@app.route('/photo/<int:photo_id>')
def photo_view(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    return render_template('photo_view.html', photo=photo)