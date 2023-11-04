import cv2
import numpy as np
from multiprocessing import Pool, cpu_count

def apply_motion_blur_chunk(chunk, kernel_size, angle):
    motion_blur_kernel = np.zeros((kernel_size, kernel_size))
    motion_blur_kernel[int((kernel_size - 1) / 2), :] = np.ones(kernel_size)
    motion_blur_kernel /= kernel_size
    
    chunk_blurred = cv2.filter2D(chunk, -1, motion_blur_kernel)

    return chunk_blurred

def apply_motion_blur(image_path, output_path, chunk_size=100, kernel_size=15, angle=45):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Unable to load the image.")
        return

    rows, cols = image.shape[:2]
    chunks = [image[row:row + chunk_size, col:col + chunk_size]
              for row in range(0, rows, chunk_size)
              for col in range(0, cols, chunk_size)]

    num_processes = cpu_count()
    with Pool(num_processes) as pool:
        chunk_blurred_list = pool.starmap(apply_motion_blur_chunk,
                                          [(chunk, kernel_size, angle) for chunk in chunks])

    output_image = np.zeros_like(image)
    current_chunk = 0
    for row in range(0, rows, chunk_size):
        for col in range(0, cols, chunk_size):
            output_image[row:row + chunk_size, col:col + chunk_size] = chunk_blurred_list[current_chunk]
            current_chunk += 1

    cv2.imwrite(output_path, output_image)
    print("Motion blur applied and saved successfully.")

def motion_blur_main(filepath):
    input_image_path = filepath
    output_image_path = "motion_blurred_image.jpg"
    
    kernel_size = int(input("Enter kernel size for motion blur: "))
    apply_motion_blur(input_image_path, output_image_path, kernel_size=kernel_size)
