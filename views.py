from flask import request, render_template, flash, send_from_directory
from photosandtext2 import app
from photosandtext2.models import Photo, Gallery
import os


@app.route('/')
def home():
    photos = Photo.query.all()
    return render_template("home.html", photos=photos)

@app.route('/photo/<photoID>')
def return_photo(photoID):
    photo = Photo.query.filter_by(id=photoID).first()
    return render_template("photo.html", photo=photo)

@app.route('/gallery/<gallerySlug>')
def return_gallery(gallerySlug):
    gallery = Gallery.query.filter_by(slug=gallerySlug).first()
    return render_template("gallery.html", gallery=gallery)

@app.route('/upload')
def upload_photo():
    return render_template("photoUpload.html")

@app.route('/media/photos/<path:filename>')
def render_image(filename):
    return send_from_directory(app.config['PHOTO_STORE'], filename)

@app.route('/media/crops/<path:filename>')
def render_crop(filename):
    return send_from_directory(app.config['CROP_STORE'], filename)