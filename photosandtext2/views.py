from flask import request, redirect, url_for, render_template, send_from_directory, flash, jsonify
from flask.ext.login import login_user
from sqlalchemy import func, desc
from werkzeug import secure_filename
from photosandtext2 import app, manager, login_manager
from photosandtext2.models.photo import Photo, Crop, Gallery
from photosandtext2.models.user import User
from photosandtext2.utils.general import allowed_file, date_format
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
    header_background = Photo.query.filter_by(favorite=True).order_by(func.random()).first()
    galleries = Gallery.query.filter(Gallery.photos!=None)
    return render_template('home.html', galleries=galleries, header_background=header_background)

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
    return redirect('/gallery/edit/#/'+str(gallery.id))

@app.route('/gallery/<int:gallery_id>')
def gallery_view(gallery_id):
    gallery = Gallery.query.get_or_404(gallery_id)
    photos = gallery.photos.order_by(Photo.exif_date_taken)
    dates = date_format(photos[0].exif_date_taken, photos[-1].exif_date_taken)
    return render_template('gallery.html', gallery=gallery, photos=photos, dates=dates)

@app.route('/gallery/edit/')
def gallery_js_edit_view():
    return render_template('gallery_edit_js.html')

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
def include_url(result):
    photo = Photo.query.get(result["id"])
    result['url'] = photo.url()
    return result

def edit_crops_for_photo_api(result, **kw):
    photoObj = Photo.query.get(result["id"])
    cropsResult = dict()
    for crop in photoObj.crops:
        cropInfo = dict()
        cropInfo["height"] = crop.height
        cropInfo["width"] = crop.width
        cropInfo["url"] = crop.url()
        cropsResult[crop.name] =cropInfo
    result["crops"] = cropsResult
    return result

def remove_crops_for_photo_api(data, **kw):
    del data["crops"]
    pass

def include_crops_for_gallery_api(result, **kw):
    for photo in result["photos"]:
        photoObj = Photo.query.get(photo["id"])
        cropsResult = dict()
        for crop in photoObj.crops:
            cropInfo = dict()
            cropInfo["height"] = crop.height
            cropInfo["width"] = crop.width
            cropInfo["url"] = crop.url()
            cropsResult[crop.name] =cropInfo
        photo["crops"] = cropsResult
    return result

def remove_crops_for_gallery_api(data, **kw):
    newPhotos = []
    for photo in data["photos"]:
        del photo["crops"]
        newPhotos.append(photo)
    del data["photos"]
    data["photos"] = newPhotos
    pass

#Dont know if this counts as cheating or not.. kind of brute forcing file uploads into the API
@app.route('/api/v1/galleries/<int:gallery_id>/photos', methods=['POST'])
def gallery_upload_view(gallery_id):
    gallery = Gallery.query.get_or_404(gallery_id)
    resp = dict()
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['PHOTO_STORE'], filename))
        photo = Photo(image=filename)
        photo.gallery = gallery
        photo.save()
    resp['status'] = 'success'
    resp['id'] = photo.id
    return jsonify(resp)


manager.create_api(
    Photo,
    methods=['GET','POST','DELETE','PATCH','PUT'],
    url_prefix='/api/v1',
    collection_name='photos',
    results_per_page=20,
    preprocessors={
        'PUT_SINGLE':[remove_crops_for_photo_api]
    },
    postprocessors={
        'GET_SINGLE':[include_url,edit_crops_for_photo_api]
    }
)

manager.create_api(
    Gallery,
    methods=['GET','POST','DELETE','PATCH','PUT'],
    url_prefix='/api/v1',
    collection_name='galleries',
    results_per_page=20,
    preprocessors={
        'PUT_SINGLE':[remove_crops_for_gallery_api]
    },
    postprocessors={
        'GET_SINGLE':[include_crops_for_gallery_api]
    }
)