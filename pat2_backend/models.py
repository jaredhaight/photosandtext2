from flask import url_for
from pat2_backend import db, app
from utils.general import slugify
from utils.photo import get_exif, make_crop
from datetime import datetime

PHOTO_STORE = app.config["PHOTO_STORE"]
CROP_STORE = app.config["CROP_STORE"]

association_table = db.Table('photo_tag_association',
    db.Column('photo_id', db.Integer, db.ForeignKey('photo.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)

def init_dev():
    crop1 = CropSettings(name="thumb200",height=200,width=200)
    crop2 = CropSettings(name="thumb400",height=400,width=400)
    crop3 = CropSettings(name="home400",height=0,width=400)
    crop4 = CropSettings(name="display1280",height=0,width=1280)

    for crop in (crop1, crop2, crop3, crop4):
        db.session.add(crop)

    db.session.commit()


def create_crops(photo):
    """
    Used when a Photo object is saved. Any crops in the Crops Settings table that don't exist will be created.
    """
    cropTypes = CropSettings.query.all()
    for cropType in cropTypes:
        search = photo.crops.filter_by(name=cropType.name).first()
        if search is None:
            thumbnail = make_crop(photo.image, cropType.name, cropType.height, cropType.width)
            crop = Crop(name=cropType.name, file=thumbnail)
            photo.crops.append(crop)
    db.session.add(photo)
    db.session.commit()

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.Text, nullable=True)
    exif_iso = db.Column(db.String(10), nullable=True)
    exif_aperture = db.Column(db.String(10), nullable=True)
    exif_shutter = db.Column(db.String(10), nullable=True)
    exif_focal = db.Column(db.String(10), nullable=True)
    exif_date_taken = db.Column(db.DateTime, nullable=True)
    image = db.Column(db.String(256), nullable=False)
    raw_file = db.Column(db.String(256), nullable=True)
    orientation = db.Column(db.String(256), nullable=True)
    tags = db.relationship('Tag', secondary=association_table, backref=db.backref('photos', lazy='dynamic'))
    crops = db.relationship('Crop', backref=db.backref('photo'), lazy='dynamic')
    gallery_id = db.Column(db.Integer, db.ForeignKey('gallery.id'))
    permissions = db.Column(db.String(256), nullable=True)
    uploaded = db.Column(db.DateTime, nullable=True)
    updated = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Photo %r>' % self.id

    def path(self):
        return app.config["PHOTO_STORE"]+'/'+self.image

    def url(self):
        return app.config["PHOTO_BASE_URL"]+'/'+self.image

    def api_url(self):
        return url_for('api_photo', photoID=self.id, _external=True)

    def filename(self):
        return self.image

    def get_thumbnail(self, thumbnailName):
        crop = Crop.query.filter_by(photo_id=self.id, name=thumbnailName).first()
        return crop.url()

    def save(self):
        if self.uploaded is None:
            self.uploaded = datetime.utcnow()
        self.updated = datetime.utcnow()
        #Get EXIF
        exif = get_exif(PHOTO_STORE+"/"+self.image)
        self.exif_aperture = exif['aperture']
        self.exif_date_taken = exif['date_taken']
        self.exif_focal = exif['focal']
        self.exif_iso = exif['iso']
        self.exif_shutter = exif['shutter']
        db.session.add(self)
        db.session.commit()
        create_crops(self)

class Crop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'))
    name = db.Column(db.String(256))
    file = db.Column(db.String(256))

    def url(self):
        return app.config["CROP_BASE_URL"]+'/'+self.file

class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    slug = db.Column(db.String(256))
    date = db.Column(db.Date)
    photos = db.relationship('Photo', backref=db.backref('gallery'), lazy='dynamic')

    def api_url(self):
        return url_for('api_gallery', galleryID=self.id, _external=True)

    def save(self):
        if not self.date:
            self.date = datetime.utcnow().date()
        self.slug = slugify(self.name)
        db.session.add(self)
        db.session.commit()

class CropSettings(db.Model):
    """
    This table stores the details for the crops we want. We iterate through this
    when a photo is saved.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    height = db.Column(db.Integer)
    width = db.Column(db.Integer)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True)
    description = db.Column(db.Text)
    slug = db.Column(db.String(256), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag %r>' % self.name

    def site_url(self):
        return url_for('return_tag', tagSlug=self.slug, _external=True)

    def api_url(self):
        return url_for('api_tag', tagID=self.id)

    def save(self):
        self.name = self.name.lower()
        if (Tag.query.filter_by(name=self.name.lower()).count() > 0):
            return "A tag with this name already exists"
        slug = slugify(unicode(self.name))
        slugs = Tag.query.filter_by(slug=slug).count()
        if slugs > 0:
            self.slug = slug+unicode(slugs+1)
        else:
            self.slug = slug
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    longitude = db.Column(db.Numeric)
    latitude = db.Column(db.Numeric)