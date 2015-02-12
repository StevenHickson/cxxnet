import os
import glob
import sys
from datetime import datetime
#from PIL import Image
#import PIL
import cv2

rotation_angles = [0, 45, 90, 135, 180, 225, 270, 315]

def rotate_and_invert(img, angle):
    dst = (255 - img)
    rows,cols = img.shape
    M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
    dst = cv2.warpAffine(dst, M, (cols, rows))
    return dst

def create_image_rotations(image):
    imgs = [ (rotate_and_invert(image,a), a) for a in rotation_angles]
    return imgs

if __name__ == '__main__':

    if len(sys.argv) >= 2:
        img_data = glob.glob(sys.argv[1])
    else:
        raise ValueError('Must pass directory of images as the first parameter')

    for foldername in img_data:
    #for foldername in os.listdir(folders):
        print 'Folder: %s' % foldername
	com = 'rm -rf ' + foldername + '/*_rot*'
	print com
	os.system(com)
        n_images = len(foldername)
        print 'Processing %i images' % n_images

        start_time = datetime.now()

        for imgf in os.listdir(foldername):
	    imgf = foldername + '/' + imgf
            #print 'File: %s' % imgf
            #img = Image.open(imgf)
            img = cv2.imread(imgf,cv2.IMREAD_GRAYSCALE)

            rimgs = create_image_rotations(img)
            spimgf = imgf.split('/')
            image_path = '/'.join(spimgf[:-1])
            image_file = spimgf[-1].split('.')[0]

            for rimg, rot in rimgs:
                cv2.imwrite(image_path + '/' + image_file + '_rot' + str(rot) + '.jpg', rimg)
            os.system('rm -f ' + imgf)

            #if ((i+1) % 10000) == 0:
            #    print 'Processed %i files in %is' % (i+1, (datetime.now() - start_time).seconds)
