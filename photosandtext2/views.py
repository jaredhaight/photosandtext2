from flask import request, redirect, url_for, render_template, send_from_directory, flash, jsonify
from werkzeug import secure_filename
from photosandtext2 import app, manager
from photosandtext2.models.photo import Photo, Crop, Gallery
from photosandtext2.utils.general import allowed_file

import os

#Serve photos from dev
if app.config['DEBUG']:
    @app.route('/media/<path:filename>')
    def send_file(filename):
        return send_from_directory('/Users/jared/Documents/PycharmProjects/photosandtext2/media', filename)

@app.route('/')
def home_view():
    crops = Crop.query.filter_by(name="home600")
    return render_template('home.html', crops=crops)

@app.route('/photo/<int:photo_id>')
def photo_view(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    return render_template('photo_view.html', photo=photo)

@app.route('/gallery/new')
def gallery_new_view():
    gallery = Gallery()
    gallery.save()
    return redirect(url_for('gallery_view', gallery_id=gallery.id))

@app.route('/gallery/<int:gallery_id>', methods=['GET', 'POST'])
def gallery_view(gallery_id):
    gallery = Gallery.query.get_or_404(gallery_id)
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['PHOTO_STORE'], filename))
            photo = Photo(image=filename)
            photo.gallery = gallery
            photo.save()
            flash("Photo Uploaded")
            return jsonify({"photo":{"id":photo.id, "url":photo.url()}})
        else:
            flash("Something went wrong")
            return render_template('upload.html', gallery=gallery)
    else:
        return render_template('upload.html', gallery=gallery)

#API Endpoints
manager.create_api(Photo, methods=['GET','POST','DELETE','PATCH'], url_prefix='/api/v1', collection_name='photos', results_per_page=20)
manager.create_api(Gallery, methods=['GET','POST','DELETE','PATCH'], url_prefix='/api/v1', collection_name='galleries', results_per_page=20)