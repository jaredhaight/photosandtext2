from PIL import Image, ImageOps
from PIL.ExifTags import TAGS
from decimal import Decimal
from datetime import datetime
from pat2_backend import app

PHOTO_STORE = app.config["PHOTO_STORE"]
CROP_STORE = app.config["CROP_STORE"]

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
    t_img.save(filename, 'JPEG', quality=90)

    return filename

def make_crop(image, cropName, height, width):
    slash = image.find('/')+1
    dot = image.find('.')
    filename = image[slash:dot]+'_'+cropName+'.jpg'
    t_img = Image.open(PHOTO_STORE+"/"+image)
    if width > t_img.size[0]:
        width = t_img.size[0]
    if height > t_img.size[1]:
        height = t_img.size[1]
    if width == 0:
        width = t_img.size[0] * height / t_img.size[1]
        t_img.thumbnail((width,height), Image.ANTIALIAS)
        t_img.save(CROP_STORE+'/'+filename, 'JPEG', quality=90)
        return filename
    if height == 0:
        height = t_img.size[1] * width / t_img.size[0]
        t_img.thumbnail((width,height), Image.ANTIALIAS)
        t_img.save(CROP_STORE+'/'+filename, 'JPEG', quality=90)
        return filename
    t_fit = ImageOps.fit(t_img, (height,width), Image.ANTIALIAS, 0, (0.5,0.5))
    t_fit.save(CROP_STORE+'/'+filename,"JPEG", quality=90)
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