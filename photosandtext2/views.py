from flask import request, redirect, url_for, render_template, send_from_directory, flash, jsonify
from werkzeug import secure_filename
from photosandtext2 import app
from photosandtext2.models.photo import Photo, Crop
from photosandtext2.utils.general import allowed_file

import os

#Serve photos from dev
if app.config['DEBUG']:
    @app.route('/media/<path:filename>')
    def send_file(filename):
        return send_from_directory('/Users/jared/Documents/PycharmProjects/photosandtext2/media', filename)

@app.route('/')
def home():
    crops = Crop.query.filter_by(name="home600")
    return render_template('home.html', crops=crops)

@app.route('/photo/<int:photo_id>')
def photo_view(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    return render_template('photo_view.html', photo=photo)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['PHOTO_STORE'], filename))
            photo = Photo(image=filename)
            photo.save()
            flash("Photo Uploaded")
            return jsonify({"photo":{"id":photo.id, "url":photo.url()}})
        else:
            flash("Something went wrong")
            return render_template('upload.html')
    else:
        return render_template('upload.html')