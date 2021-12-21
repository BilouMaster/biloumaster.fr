from pathlib import Path
from PIL import Image
from os import system
from glob import glob
#intern
from utils.folder import create_folder

th = 250
folders = list(glob('animation/*'))
create_folder('animation/temp')
for folder in folders:
    images = list(glob(folder + '/*'))
    animation_name = folder.split('/')[-1]
    for image in images:
        img = Image.open(image)
        w, h = img.size
        tw = int(w * th / h)
        filename = Path(image).stem
        for nw in [320, 640, 808, 1024, 2048]:
            if w - nw < nw / 3:
                break
            create_folder('animation/temp/%s_%d' % (animation_name, nw))
            outfile = 'animation/temp/%s_%d/%s.webp' % (animation_name, nw, filename)
            system('cwebp -m 6 -q 80 -resize %d 0 -quiet -mt "%s" -o "%s"' % (nw, image, outfile))
        create_folder('animation/temp/%s_thumbnail' % (animation_name))
        outfile = 'animation/temp/%s_thumbnail/%s.webp' % (animation_name, filename)
        system('cwebp -m 6 -q 80 -resize %d %d -quiet -mt "%s" -o "%s"' % (tw, th, image, outfile))
    infile = ' -d 150 '.join(images)
    create_folder('animation/output')
    outfile = 'animation/output/' + animation_name + '.webp'
    system('img2webp -m 4 -q 100 -mixed -d 150 %s -o "%s"' % (infile, outfile))
folders = list(glob('animation/temp/*'))
for folder in folders:
    images = list(glob(folder + '/*'))
    animation_name = folder.split('/')[-1]
    infile = ' -d 150 '.join(images)
    outfile = 'animation/output/' + animation_name + '.webp'
    system('img2webp -m 4 -q 100 -mixed -d 150 %s -o "%s"' % (infile, outfile))