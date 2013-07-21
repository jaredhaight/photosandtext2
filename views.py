from flask import request, render_template, flash, send_from_directory
from werkzeug import secure_filename
from utils.photo import new_photo
from photosandtext2 import app
from photosandtext2.models import Photo
import os


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    photos = Photo.query.all()
    return render_template("home.html", photos=photos)

@app.route('/photo/<photoID>')
def return_photo(photoID):
    photo = Photo.query.filter_by(id=photoID).first()
    return render_template("photo.html", photo=photo)


@app.route('/upload', methods=['GET','POST'])
def upload_photo():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['PHOTO_STORE'], filename))
            photo = new_photo(filename)
            return '{"status":"uploaded","title":photo.title,"thumbnail":photo.get_thumbnail("thumb400"),"photo":photo.url()}'
        else:
            flash('Failed Validation')
    return render_template("photoUpload.html")

@app.route('/media/photos/<path:filename>')
def render_image(filename):
    return send_from_directory(app.config['PHOTO_STORE'], filename)

@app.route('/media/crops/<path:filename>')
def render_crop(filename):
    return send_from_directory(app.config['CROP_STORE'], filename)