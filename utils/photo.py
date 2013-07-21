from PIL import Image, ImageOps
from PIL.ExifTags import TAGS
from decimal import Decimal
from datetime import datetime
from photosandtext2 import app
from photosandtext2.models import Photo

PHOTO_STORE = app.config["PHOTO_STORE"]

def new_photo(photoFile):
    exif = get_exif(PHOTO_STORE+'/'+photoFile)
    photo = Photo(title=exif['date_taken'], image=photoFile)
    photo.save()
    return photo

def list_photos():
    photos = Photo.query.all()
    return photos

def resize_image(image, height, width):
    slash = image.name.find('/')+1
    dot = image.name.find('.')
    filename = CROP_STORE+str(image.name[slash:dot])+'_h'+str(height)+'_w'+str(width)+'.jpg'
    t_img = Image.open(image.path)
    if width == 0:
        width = t_img.size[0] * height / t_img.size[1]
    if height == 0:
        height = t_img.size[1] * width / t_img.size[0]
    t_img.thumbnail((width,height), Image.ANTIALIAS)
    t_img.save(filename, 'JPEG', quality=95)

    return filename

def make_thumbnail(image, height, width):
    slash = image.name.find('/')+1
    dot = image.name.find('.')
    filename = MEDIA_ROOT+'crops/'+str(image.name[slash:dot])+'_thumb_h'+str(height)+'_w'+str(width)+'.jpg'
    t_img = Image.open(image.path)
    t_fit = ImageOps.fit(t_img, (height,width), Image.ANTIALIAS, 0, (0.5,0.5))
    t_fit.save(filename,"JPEG", quality=95)

    return filename

def get_orientation(image):
        width = image.width
        height = image.height

        if width > height:
            return 'landscape'

        if width < height:
            return 'portrait'

#Get exif from image, return dict of results
def get_exif(image):
    ret = {}
    i = Image.open(image)
    info = i._getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
    try:
        iso = ret['ISOSpeedRatings']
    except:
        iso = None
    try:
        fnfirst,fnsec = ret['FNumber']
        aperture = Decimal(fnfirst)/Decimal(fnsec)
    except:
        aperture = None
    try:
        exif_a,exif_b = ret['ExposureTime']
        if exif_b == 1:
            shutter = '%s seconds'% (exif_a)
        else:
            shutter = '%s/%s'% (exif_a,exif_b)
    except:
        shutter = None
    try:
        ash,bsh = ret['FocalLength']
        focal = ash/bsh
    except:
        focal = None
    try:
        date_taken_seed = datetime.strptime(ret['DateTimeOriginal'], "%Y:%m:%d %H:%M:%S")
        date_taken = date_taken_seed.strftime("%Y-%m-%d %H:%M:%S")
    except:
        date_taken = None
    d = dict(iso=iso, aperture="f/"+str(aperture), shutter=shutter, focal=str(focal)+"mm", date_taken=date_taken)
    return d