from os import listdir
from os.path import isfile, join

from PIL import Image

mypath = 'lipsink_images'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

for fl in onlyfiles:
    im1 = Image.open('pres_file/5.jpg')
    im2 = Image.open(mypath + '/' + fl)
    im2 = im2.resize((453, 552))
    im1.paste(im2, (2500, 1100))
    im1.save('lipsink_images5/' + fl, quality=95)

    im1.close()
    im2.close()
