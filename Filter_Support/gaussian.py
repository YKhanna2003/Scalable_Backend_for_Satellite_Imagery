import cv2
import numpy as np
from multiprocessing import Pool, cpu_count

def apply_gaussian_blur_chunk(chunk, kernel_size):
    # Apply Gaussian blur to a chunk of the image
    chunk_blurred = cv2.GaussianBlur(chunk, (kernel_size, kernel_size), 0)
    return chunk_blurred

def apply_gaussian_blur(image_path, output_path, chunk_size=100, kernel_size=5):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Unable to load the image.")
        return

    # Ensure the kernel size is valid and odd
    if kernel_size % 2 == 0:
        kernel_size += 1
    
    # Split the image into smaller chunks
    rows, cols = image.shape[:2]
    chunks = [image[row:row + chunk_size, col:col + chunk_size]
              for row in range(0, rows, chunk_size)
              for col in range(0, cols, chunk_size)]

    # Apply Gaussian blur using multiprocessing
    num_processes = cpu_count()
    with Pool(num_processes) as pool:
        chunk_blurred_list = pool.starmap(apply_gaussian_blur_chunk,
                                          [(chunk, kernel_size) for chunk in chunks])

    # Recombine the blurred chunks into the final image
    output_image = np.zeros_like(image)
    current_chunk = 0
    for row in range(0, rows, chunk_size):
        for col in range(0, cols, chunk_size):
            output_image[row:row + chunk_size, col:col + chunk_size] = chunk_blurred_list[current_chunk]
            current_chunk += 1

    # Save the final image with Gaussian blur applied
    cv2.imwrite(output_path, output_image)
    print("Gaussian blur applied and saved successfully.")

def gaussian_main(filepath):
    input_image_path = filepath
    output_image_path = "gaussian_blurred_image.jpg"
    
    kernel_size = int(input("Enter kernel size for Gaussian blur: "))
    apply_gaussian_blur(input_image_path, output_image_path, kernel_size=kernel_size)
