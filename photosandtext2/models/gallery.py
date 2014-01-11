from photosandtext2 import db, app

class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    date = db.Column(db.Date)
    photos = db.relationship('Photo', backref=db.backref('gallery'), lazy='dynamic')
    created = db.Column(db.DateTime, nullable=True)
    updated = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return '<Gallery %r>' % self.name

    def api_url(self):
        return url_for('api_gallery', galleryID=self.id)

    def save(self):
        if not self.date:
            self.created = datetime.utcnow()
        self.updated = datetime.utcnow()
        self.slug = slugify(self.name)
        db.session.add(self)
        db.session.commit()
