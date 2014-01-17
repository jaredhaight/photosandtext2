from flask import request, redirect, url_for, render_template, send_from_directory, flash, jsonify
from flask.ext.login import login_user
from werkzeug import secure_filename
from photosandtext2 import app, manager, login_manager
from photosandtext2.models.photo import Photo, Crop, Gallery
from photosandtext2.models.user import User
from photosandtext2.utils.general import allowed_file
from photosandtext2.forms import LoginForm

import os

#User loader for Flask-Login
@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)

#Serve photos from dev
if app.config['DEBUG']:
    @app.route('/media/<path:filename>')
    def send_file(filename):
        return send_from_directory('/Users/jared/Documents/PycharmProjects/photosandtext2/media', filename)

@app.route('/')
def home_view():
    galleries = Gallery.query.filter(Gallery.photos!=None)
    return render_template('home.html', galleries=galleries)

@app.route('/photo/<int:photo_id>')
def photo_view(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    return render_template('photo_view.html', photo=photo)

@app.route('/gallery/new')
def gallery_new_view():
    gallery = Gallery.query.filter_by(name=None, photos=None).first()
    if gallery is None:
        gallery = Gallery()
        gallery.save()
    return redirect(url_for('gallery_edit_view', gallery_id=gallery.id))

@app.route('/gallery/<int:gallery_id>')
def gallery_view(gallery_id):
    print "Got gallery id"
    gallery = Gallery.query.get_or_404(gallery_id)
    return render_template('gallery.html', gallery=gallery)

@app.route('/gallery/<int:gallery_id>/edit', methods=['GET', 'POST'])
def gallery_edit_view(gallery_id):
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
            return render_template('gallery_edit.html', gallery=gallery)
    else:
        return render_template('gallery_edit.html', gallery=gallery)

@app.route('/login', methods=['GET', 'POST'])
def login_view():
    form = LoginForm()
    if form.validate_on_submit():
        username, password = form.username.data, form.password.data
        user = User.query.filter_by(username=username,password=password).all()
        if len(user) > 0:
            login_user(user[0])
            return redirect(url_for('home_view'))
        flash('Username and password pair not found')
        return redirect(request.args.get("next") or url_for("home_view"))
    return render_template("login.html", form=form)

#API Endpoints
manager.create_api(Photo, methods=['GET','POST','DELETE','PATCH'], url_prefix='/api/v1', collection_name='photos', results_per_page=20)
manager.create_api(Gallery, methods=['GET','POST','DELETE','PATCH','PUT'], url_prefix='/api/v1', collection_name='galleries', results_per_page=20)