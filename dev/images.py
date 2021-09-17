from multiprocessing import Pool
from pathlib import Path
from PIL import Image, ExifTags
from os import system
#intern
from utils.date_fr import str_date_fr
from utils.folder import create_folder

th = 250
tcolor = (31, 30, 36)

def get_images_data(images: list) -> dict:
    return dict(Pool().map(operate_images, images))

def operate_images(infile: str) -> tuple:
    global th, tcolor
    filename = Path(infile).stem
    img = Image.open(infile)

    #size
    w, h = img.size
    tw = int(w * th / h)

    #exif
    img_exif = img.getexif()
    title = str_exif(0x9C9B, img_exif, "Sans titre")
    description = str_exif(0x9C9C, img_exif, '')
    tags = str_exif(0x9C9E, img_exif)

    #date
    datetime = filename.split('_')[0]
    date = str_date_fr(datetime)

    #data
    data = {'filename':filename, 'year':filename[:4], 'date': date, 'datetime': datetime,
        'size':(w, h), 'tsize':(tw, th), 'set':[], 'title':title, 'description':description, 'tags':tags}

    #create folders
    create_folder('../img/gallery')
    create_folder('../img/gallery/placeholder')
    create_folder('../img/gallery/responsive')
    create_folder('../img/gallery/thumbnail')

    #convert original to webp
    outfile = '../img/gallery/%s.webp' % (filename)
    if not Path(outfile).exists():
        img.save(outfile, format='WebP', quality=80, method=6)
        # system('cwebp -m 6 -q 80 -quiet -mt "%s" -o "%s"' % (infile, outfile))
        system('webpmux -set xmp image.xmp "%s" -o "%s"' % (outfile, outfile))
    
    #generate responsive images
    for nw in [320, 640, 808, 1024, 2048]:
        if w - nw < nw / 3:
            break
        data['set'].append(nw)
        outfile = '../img/gallery/responsive/%s_%d.webp' % (filename, nw)
        if not Path(outfile).exists():
            system('cwebp -m 6 -q 80 -resize %d 0 -quiet -mt "%s" -o "%s"' % (nw, infile, outfile))
            system('webpmux -set xmp image.xmp "%s" -o "%s"' % (outfile, outfile))
    
    #generate thumbnails images
    outfile = '../img/gallery/thumbnail/%s_thumbnail.webp' % (filename)
    if not Path(outfile).exists():
        system('cwebp -m 6 -q 80 -resize %d %d -quiet -mt "%s" -o "%s"' % (tw, th, infile, outfile))

    #generate placeholder images for thumbnails
    outfile = '../img/gallery/placeholder/%d.webp' % (tw)
    if not Path(outfile).exists():
        Image.new('RGB', (tw, th), tcolor).save(outfile, 'WebP', quality=1, method=6)

    img.close()
    return infile, data

def str_exif(key: str, exif: str, default='') -> str:
    if key in exif:
        return exif[key].decode('utf-16').rstrip('\x00')
    else:
        return default