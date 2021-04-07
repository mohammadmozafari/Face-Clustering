import math
import numpy as np
import matplotlib.pyplot as plt

def show_images(image_list):
    """
    Takes a list of images - 3d numpy arrays - and
    shows a larger image that contains all of them. 
    """
    sqroot = math.sqrt(len(image_list))
    cols = math.ceil(sqroot)
    rows = math.floor(sqroot)
    while cols * rows < len(image_list):
        rows += 1
    rows = cols if (cols * cols > len(image_list)) else (cols + 1)
    big_image = np.ones((rows * 112, cols * 112, 3)) * 255
    i, j = 0, 0
    for img in image_list:
        big_image[j*112:(j+1)*112, i*112:(i+1)*112, :] = img
        if i == cols - 1:
            i = 0
            j += 1
        else:
            i += 1

    fig = plt.figure()
    fig.set_size_inches(10, 8)
    plt.imshow(big_image.astype('int'))
    plt.axis('off')
    plt.show()
