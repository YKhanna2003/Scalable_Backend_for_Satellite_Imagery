import cv2
import numpy as np
import random

def add_noise(img):  
    row , col = img.shape
    number_of_pixels = random.randint(300, 10000)
    for i in range(number_of_pixels):
        y_coord=random.randint(0, row - 1)
        x_coord=random.randint(0, col - 1)
        img[y_coord][x_coord] = 255
    number_of_pixels = random.randint(300 , 10000)
    for i in range(number_of_pixels):
        y_coord=random.randint(0, row - 1)
        x_coord=random.randint(0, col - 1)
        img[y_coord][x_coord] = 0
    return img

def print_specific_image(img):
    cv2.imshow('Image Output',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Function:- Print Image
# Input:- Image Address, Mode and Printing or not
# 1 - Color, 0 - Grayscale, -1 - Unchanged (As-Is)
# Incase of Error NULL is returned

def array_image(input_image_path,mode,print_it=False):
    checker = [0,1,-1]
    if mode not in checker:
        return None
    img = cv2.imread(input_image_path,mode)
    if img is None:
        return None
    if print_it:
        print(img)
        print_specific_image(img)
    return img

# Function:- Salt and Pepper
# Input:- File Address and whether to print it or not
# Output:- Salt and Pepper image returned

def salt_and_pepper(input_image_path,output_image_path):
    img = cv2.imread(input_image_path,0)
    if img is None:
        return None
    rows = len(img)
    columns = len(img[0])
    salt_img=add_noise(img)
    cv2.imwrite(output_image_path, salt_img)

# Function:- Custom Filter Application
# Input:- File Addresses of input and output images, custom filter in text file
# Output:- File saved as output_image_path name

def custom_filter(input_image_path, output_image_path, custom_filter_path):
    image = cv2.imread(input_image_path)
    if image is None:
        raise ValueError("Image not found at the specified path.")
    try:
        with open(custom_filter_path, 'r') as file:
            custom_filter = []
            for line in file:
                values = [float(val) for val in line.strip().split()]
                custom_filter.append(values)
            custom_filter = np.array(custom_filter, dtype=np.float32)
    except Exception as e:
        raise ValueError(f"Error reading custom filter from file: {e}")
    filtered_image = cv2.filter2D(image, -1, custom_filter)
    cv2.imwrite(output_image_path, filtered_image)

# Function:- Gaussian Filter Application
# Input:- File Addresses of input and output images, kernel size and sigma (0 for auto correction)
# Output:- File saved as output_image_path name

def gaussian(input_image_path, output_image_path, kernel_size, sigma_x):
    image = cv2.imread(input_image_path)
    if image is None:
        raise ValueError("Image not found at the specified path.")
    blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigmaX=sigma_x)
    cv2.imwrite(output_image_path, blurred_image)

# Function:- Median, Max and Min Filter Application
# Input:- File Addresses of input and output images, kernel size.
# Output:- File saved as output_image_path name

def median(input_image_path, output_image_path, kernel_size):
    image = cv2.imread(input_image_path)
    if image is None:
        raise ValueError("Image not found at the specified path.")
    median_filtered_image = cv2.medianBlur(image, kernel_size)
    cv2.imwrite(output_image_path, median_filtered_image)

def max(input_image_path, output_image_path, kernel_size):
    image = cv2.imread(input_image_path)
    if image is None:
        raise ValueError("Image not found at the specified path.")
    kernel = np.ones((kernel_size, kernel_size), dtype=np.uint8)
    max_filtered_image = cv2.dilate(image, kernel)
    cv2.imwrite(output_image_path, max_filtered_image)

def min(input_image_path, output_image_path, kernel_size):
    image = cv2.imread(input_image_path)
    if image is None:
        raise ValueError("Image not found at the specified path.")
    kernel = np.ones((kernel_size, kernel_size), dtype=np.uint8)
    min_filtered_image = cv2.erode(image, kernel)
    cv2.imwrite(output_image_path, min_filtered_image)

# Function:- High and Low Pass Filter Application
# Input:- File Addresses of input and output images, kernel size.
# Output:- File saved as output_image_path name

def high_pass(input_image_path, output_image_path, kernel_size):
    image = cv2.imread(input_image_path)
    if image is None:
        raise ValueError("Image not found at the specified path.")
    low_pass_kernel = cv2.getGaussianKernel(kernel_size, 0)
    low_pass_filtered = cv2.filter2D(image, -1, low_pass_kernel)
    high_pass_filtered = image - low_pass_filtered
    cv2.imwrite(output_image_path, high_pass_filtered)

def low_pass(input_image_path, output_image_path, kernel_size):
    image = cv2.imread(input_image_path)
    if image is None:
        raise ValueError("Image not found at the specified path.")
    low_pass_kernel = cv2.getGaussianKernel(kernel_size, 0)
    low_pass_filtered = cv2.filter2D(image, -1, low_pass_kernel)
    cv2.imwrite(output_image_path, low_pass_filtered)

# Function:- Motion Blur Filter Application
# Input:- File Addresses of input and output images, kernel size.
# Output:- File saved as output_image_path name

def motion_blur(input_image_path, output_image_path, kernel_size):
    image = cv2.imread(input_image_path)
    if image is None:
        raise ValueError("Image not found at the specified path.")
    kernel = np.zeros((kernel_size, kernel_size), dtype=np.float32)
    center = (kernel_size - 1) / 2
    for i in range(kernel_size):
        kernel[i, int(center)] = 1.0 / kernel_size
    motion_blurred_image = cv2.filter2D(image, -1, kernel)
    cv2.imwrite(output_image_path, motion_blurred_image)