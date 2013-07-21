from photosandtext2 import db, app

association_table = db.Table('photo_gallery_association',
    db.Column('photo_id', db.Integer, db.ForeignKey('photo.id')),
    db.Column('gallery_id', db.Integer, db.ForeignKey('gallery.id'))
)

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=True)
    desc = db.Column(db.Text, nullable=True)
    exif_iso = db.Column(db.String(10), nullable=True)
    exif_aperture = db.Column(db.String(10), nullable=True)
    exif_shutter = db.Column(db.String(10), nullable=True)
    exif_focal = db.Column(db.String(10), nullable=True)
    exif_date_taken = db.Column(db.DateTime, nullable=True)
    image = db.Column(db.String(256), nullable=False)
    raw_file = db.Column(db.String(256), nullable=True)
    orientation = db.Column(db.String(256), nullable=True)
    galleries = db.relationship('Gallery', secondary=association_table, backref=db.backref('photos', lazy='dynamic'))
    crops = db.relationship('Crop')
    permissions = db.Column(db.String(256), nullable=True)
    created = db.Column(db.DateTime, nullable=True)
    updated = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Photo %r>' % self.title

    def photo_path(self):
        return app.config["PHOTO_STORE"]+'/'+self.image

    def photo_url(self):
        return app.config["PHOTO_BASE_URL"]+'/'+self.image

    def save(self):
        db.session.add(self)
        db.session.commit()

class Crop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'))
    name = db.Column(db.String(256))
    path = db.Column(db.String(256))

class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    description = db.Column(db.Text)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    longitude = db.Column(db.Numeric)
    latitude = db.Column(db.Numeric)