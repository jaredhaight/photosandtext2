from datetime import datetime
from flask import url_for
import os
from datetime import datetime

from photosandtext2 import db, app
from photosandtext2.utils.photo import get_image_info, make_crop
from photosandtext2.queue import low_queue, high_queue


PHOTO_STORE = app.config["PHOTO_STORE"]
CROP_STORE = app.config["CROP_STORE"]

association_table = db.Table('photo_tag_association',
    db.Column('photo_id', db.Integer, db.ForeignKey('photo.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)


def create_crops(photo):
    """
    Used when a Photo object is saved. Any crops in the Crops Settings table
    that don't exist will be created.
    """
    cropTypes = CropSettings.query.all()
    for cropType in cropTypes:
        #TODO - Make this smarter
        #search = photo.crops.filter_by(name=cropType.name).first()
        #if search is None:
        thumbnail = make_crop(photo.image, cropType.name, cropType.height, cropType.width)
        crop = Crop(name=cropType.name, file=thumbnail['filename'], height=thumbnail['height'], width=thumbnail['width'])
        crop.save()
        photo.crops.append(crop)
    photo.save()


def create_initial_crops(photo):
    crop1 = CropSettings.query.filter_by(name="thumb200").first()
    crop2 = CropSettings.query.filter_by(name="display_c").first()
    #TODO - This is a hack to make gallery thumbnails work.
    crop3 = CropSettings.query.filter_by(name="thumb400").first()
    cropTypes = (crop1,crop2,crop3)

    for cropType in cropTypes:
        thumbnail = make_crop(photo.image, cropType.name, cropType.height, cropType.width)
        crop = Crop(name=cropType.name, file=thumbnail['filename'], height=thumbnail['height'], width=thumbnail['width'])
        crop.save()
        photo.crops.append(crop)
    photo.save()

def update_exif(photo):
    print str(datetime.now())+" Photo "+str(photo.id)+": Updating EXIF"
    exif = get_image_info(PHOTO_STORE+"/"+photo.image)
    photo.exif_aperture = exif['aperture']
    photo.exif_date_taken = exif['date_taken']
    photo.exif_focal = exif['focal']
    photo.exif_iso = exif['iso']
    photo.exif_shutter = exif['shutter']
    photo.desc = exif['caption']
    photo.width = exif['width']
    photo.height = exif['height']
    photo.orientation = exif['orientation']
    photo.save()

def add_photo_to_gallery(gallery, photoId):
        photo = Photo.query.get(photoId)
        print str(datetime.now())+" Gallery "+str(gallery.id)+": Adding photo "+str(photo.id)
        photo.gallery = gallery
        if photo.location is None:
            photo.location = gallery.location
        photo.save()
        paged = gallery.photos.order_by(Photo.exif_date_taken).paginate(1,1000,False)
        gallery.update_positions()
        gallery.save()

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    desc = db.Column(db.UnicodeText, nullable=True)
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
    gallery_pos = db.Column(db.Integer, nullable=True)
    permissions = db.Column(db.String(256), nullable=True)
    uploaded = db.Column(db.DateTime, nullable=True)
    updated = db.Column(db.DateTime, nullable=True)
    height = db.Column(db.Integer, nullable=True)
    width = db.Column(db.Integer, nullable=True)
    favorite = db.Column(db.Boolean, nullable=True)
    location = db.Column(db.UnicodeText, nullable=True)

    def __repr__(self):
        return '<Photo %r>' % self.id

    def path(self):
        return app.config["PHOTO_STORE"]+'/'+self.image

    def url(self):
        return app.config["PHOTO_BASE_URL"]+'/'+self.image

    def api_url(self):
        return url_for('api_photo', photoID=self.id)

    def filename(self):
        return self.image

    def get_thumbnail(self, thumbnailName):
        crop = Crop.query.filter_by(photo_id=self.id, name=thumbnailName).first()
        return crop.url()

    def prepare_photo(self):
        if self.crops.first() is None:
            print str(datetime.now())+" Photo "+str(self.id)+": Creating Initial Crops"
            high_queue.enqueue(create_initial_crops, self)
            print str(datetime.now())+" Photo "+str(self.id)+": Creating Rest of Crops"
            low_queue.enqueue(create_crops, self)
        if self.exif_date_taken is None:
            low_queue.enqueue(update_exif, self)

    def save(self):
        print str(datetime.now())+" Photo: "+str(self.id)+": Photo.save() called"
        self.updated = datetime.utcnow()
        if self.uploaded is None:
            self.uploaded = datetime.utcnow()
        self.updated = datetime.utcnow()
        print str(datetime.now())+" Photo "+str(self.id)+": Commiting to DB"
        db.session.add(self)
        db.session.commit()

    def delete(self):
        if os.path.isfile(PHOTO_STORE+"/"+self.image):
            os.remove(PHOTO_STORE+"/"+self.image)
        db.session.delete(self)
        db.session.commit()

class Crop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'))
    gallery_id = db.Column(db.Integer, db.ForeignKey('gallery.id'))
    name = db.Column(db.String(256))
    file = db.Column(db.String(256))
    height = db.Column(db.Integer, nullable=True)
    width = db.Column(db.Integer, nullable=True)
    url = db.Column(db.String, nullable=True)

    def save(self):
        self.url = app.config["CROP_BASE_URL"]+'/'+self.file
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
        return url_for('return_tag', tagSlug=self.slug)

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

class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    description = db.Column(db.UnicodeText)
    date = db.Column(db.Date)
    photos = db.relationship('Photo', backref=db.backref('gallery'), lazy='dynamic')
    created = db.Column(db.DateTime, nullable=True)
    updated = db.Column(db.DateTime, nullable=True)
    location = db.Column(db.UnicodeText, nullable=True)
    thumbnails = db.relationship('Crop', backref=db.backref('gallery'), lazy='dynamic')

    def __repr__(self):
        return '<Gallery %r>' % self.name

    def api_url(self):
        return url_for('api_gallery', galleryID=self.id)

    def add_photo(self, photo):
        high_queue.enqueue(add_photo_to_gallery, self, photo.id)

    def update_thumbnails(self):
        print "Setting Thumbnails"
        thumbnail = self.photos.filter_by(favorite=True).first()
        if not thumbnail:
            thumbnail = self.photos.first()
        print "Thumbnail set as: "+str(thumbnail)
        self.thumbnails = thumbnail.crops

    def update_positions(self):
        paged = self.photos.order_by(Photo.exif_date_taken).paginate(1,1000,False)
        for photoItem in paged.items:
            print "Photo being arranged: "+str(photoItem.id)
            photoItem.gallery_pos = paged.items.index(photoItem)+1
            photoItem.save()

    def status(self):
        for photo in self.photos:
            if photo.crops.filter_by(name="thumb200").first() is None:
                return "Initial crops being created"
            if photo.crops.filter_by(name="display1280").first() is None:
                return "Other crops being created"
        return "Ready"

    def save(self):
        print "Gallery save called"
        if not self.date:
            self.created = datetime.utcnow()
        self.updated = datetime.utcnow()
        if self.photos.first() and not self.thumbnails.first():
            self.update_thumbnails()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        for photo in self.photos:
            photo.delete()
        db.session.delete(self)
        db.session.commit()
