import os
import cv2
from helper import erik_functions_files
import numpy as np
import shutil



# same size  and horizontally
def images_concatenate(list_2d):
    # return final image
    return cv2.vconcat([cv2.hconcat(list_h) for list_h in list_2d])

    # image resizing
    img1_s = cv2.resize(img1, dsize=(0, 0), fx=0.5, fy=0.5)

    # function calling
    img_tile = concat_vh([[img1_s, img1_s, img1_s],
                          [img1_s, img1_s, img1_s],
                          [img1_s, img1_s, img1_s]])
    # show the output image
    cv2.imshow('concat_vh.jpg', img_tile)


def image_split_save(image_cuts, path_image, dir_output=None):
    os.makedirs(dir_output, exist_ok=True)

    counter = 1

    # dir, filename_base, file_extension from full path
    dir_name, file_name, file_ext = erik_functions_files.path_split_from_path(path_image)

    if dir_output == None:
        dir_output = dir_name

    for image_cut in image_cuts:
        filename_new = file_name + '_' + str.zfill(str(counter),6) + file_ext
        path_save = os.path.join(dir_output, filename_new)
        cv2.imwrite(path_save, image_cut)
        counter +=1


# get crop from range of h,w with size
def get_crop(h_start,w_start, h_size,w_size):
    w_coord_start = (w_start * w_size)
    h_coord_start = (h_start * h_size)
    w_coord_end = (w_start+1) * w_size
    h_coord_end = (h_start+1) * h_size
    return w_coord_start,w_coord_end, h_coord_start, h_coord_end


# splits an image into smaller cuts in a gridlike fashion, it saves the slices if save_path is set to something
def image_split(path_image, size_split=64, save_path=None):
    # check if image exists on file
    if not(erik_functions_files.file_exists(path_image)): return False

    image_cuts = []
    image = cv2.imread(path_image)
    (h, w) = image.shape[:2]

    # compute the size for every cut
    h_cuts = int(h // size_split)
    w_cuts = int(w // size_split)

    for h_cut in range(h_cuts):
        for w_cut in range(w_cuts):
            w1, w2, h1, h2 = get_crop(h_cut, w_cut, size_split, size_split)
            image_cut = image[h1:h2,w1:w2]
            image_cuts.append(image_cut)

    if save_path != None:
        image_split_save(image_cuts, path_image, save_path)
    return image_cuts


# takes an array of images and splits them as a grid and saves the portions in a new directory
def split_images_into_new_dir(dir_images, dir_images_out, size):
    images = erik_functions_files.files_images_in_dir(dir_images)
    for path_image in images:
        #   def image_split(path_image, grid_size=2, save_path=None):
        image_split(path_image, size, dir_images_out)


def group_images_by_category_into_directorys(labels, label_names, path_images, dir_save):
    np_labels = np.array(labels)
    np_unique_labels = np.unique(np_labels)

    # create directorys
    for label in np_unique_labels:
        os.makedirs(dir_save, label)

    # copy the files
    for i in range(len(labels)):
        filename = os.path.basename(path_images[i])
        path_save_image = os.path.join(dir_save, labels[i], filename)
        shutil.copyfile(path_images[i], path_save_image)



'''
# splits an image into smaller cuts in a gridlike fashion, it saves the slices if save_path is set to something
# it crops the center portions
def image_split_crop(path_image, size_crop, save_path=None):
    # check if image exists on file
    if not(erik_functions_files.file_exists(path_image)): return False

    image_cuts = []
    image = cv2.imread(path_image)
    (h, w) = image.shape[:2]

    # compute the size for every cut
    h_numbers = int(h // size_crop)
    w_new = int(w // grid_size)

    for h_cut in range(grid_size):
        for w_cut in range(grid_size):
            image_cut = image[h_new * h_cut : h_new * (h_cut + 1), w_new * w_cut : w_new * (w_cut + 1)]
            image_cuts.append(image_cut)

    if save_path != None:
        image_split_save(image_cuts, path_image, save_path)
    return image_cuts
'''