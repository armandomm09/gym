#Converts normalized coordinates (x_center, y_center, width, height) to pixel coordinates (x_min, y_min, x_max, y_max)
def normalized_to_pixels(box, image_width, image_height):
    x, y, w, h = box
    x_min = (x * image_width) - ((w * image_width) / 2)
    y_min = (y * image_height) - ((h * image_height) / 2)
    x_max = (x * image_width) + ((w * image_width) / 2)
    y_max = (y * image_height) + ((h * image_height) / 2)
    return x_min, y_min, x_max, y_max

#Converts pixel coordinates (x_min, y_min, x_max, y_max) to normalized coordinates (x_center, y_center, width, height)
def pixels_to_normalized_rel(pixel_coordinates, image_width, image_height):
    x_min, y_min, x_max, y_max = pixel_coordinates
    x = (x_min + ((x_max - x_min) / 2)) / image_width
    y = (y_min + ((y_max - y_min) / 2)) / image_height
    w = (x_max - x_min) / image_width
    h = (y_max - y_min) / image_height
    return x, y, w, h

def pixels_to_normalized_abs(pixel_coordinates, image_width, image_height):
    x_min, y_min, x_max, y_max = pixel_coordinates
    x = (x_min + ((x_max - x_min) / 2)) / image_width
    y = (y_min + ((y_max - y_min) / 2)) / image_height
    w = (x_max - x_min) / image_width
    h = (y_max - y_min) / image_height
    return x* image_width, y * image_height, w * image_width, h * image_height
