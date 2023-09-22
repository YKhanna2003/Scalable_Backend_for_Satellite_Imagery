Image Processing API README

This repository contains a collection of Python functions for various image processing tasks. These functions use the OpenCV library and provide different image filtering and manipulation techniques.

Table of Contents:
1. Functions
    - Custom Filter
    - Gaussian Filter
    - Median Filter
    - Max Filter
    - Min Filter
    - High-Pass Filter
    - Low-Pass Filter
    - Motion Blur
2. Usage
3. Examples
4. Contributing
5. License

Functions:

Custom Filter:
Applies a custom filter to an image using a user-defined filter matrix.

    def apply_custom_filter(input_image_path, output_image_path, custom_filter_path):
        # ...

    - `input_image_path`: Path to the input image.
    - `output_image_path`: Path to save the filtered output image.
    - `custom_filter_path`: Path to a text file containing the custom filter matrix.

Gaussian Filter:
Applies a Gaussian filter to an image for blurring or smoothing.

    def apply_gaussian_filter(input_image_path, output_image_path, kernel_size, sigma_x):
        # ...

    - `input_image_path`: Path to the input image.
    - `output_image_path`: Path to save the filtered output image.
    - `kernel_size`: Size of the Gaussian kernel (e.g., 3, 5, 7).
    - `sigma_x`: Standard deviation for Gaussian smoothing (use 0 for auto-calculation).

Median Filter:
Applies a median filter to an image for noise reduction.

    def apply_median_filter(input_image_path, output_image_path, kernel_size):
        # ...

    - `input_image_path`: Path to the input image.
    - `output_image_path`: Path to save the filtered output image.
    - `kernel_size`: Size of the median filter kernel.

Max Filter:
Applies a max filter (dilation) to an image.

    def apply_max_filter(input_image_path, output_image_path, kernel_size):
        # ...

    - `input_image_path`: Path to the input image.
    - `output_image_path`: Path to save the filtered output image.
    - `kernel_size`: Size of the max filter kernel.

Min Filter:
Applies a min filter (erosion) to an image.

    def apply_min_filter(input_image_path, output_image_path, kernel_size):
        # ...

    - `input_image_path`: Path to the input image.
    - `output_image_path`: Path to save the filtered output image.
    - `kernel_size`: Size of the min filter kernel.

High-Pass Filter:
Applies a high-pass filter to an image to enhance edges and fine details.

    def apply_high_pass_filter(input_image_path, output_image_path, kernel_size):
        # ...

    - `input_image_path`: Path to the input image.
    - `output_image_path`: Path to save the filtered output image.
    - `kernel_size`: Size of the high-pass filter kernel.

Low-Pass Filter:
Applies a low-pass filter to an image to reduce noise and smooth the image.

    def apply_low_pass_filter(input_image_path, output_image_path, kernel_size):
        # ...

    - `input_image_path`: Path to the input image.
    - `output_image_path`: Path to save the filtered output image.
    - `kernel_size`: Size of the low-pass filter kernel.

Motion Blur:
Applies a motion blur effect to an image.

    def apply_motion_blur(input_image_path, output_image_path, kernel_size):
        # ...

    - `input_image_path`: Path to the input image.
    - `output_image_path`: Path to save the motion-blurred output image.
    - `kernel_size`: Size of the motion blur kernel.

Usage:
1. Clone this repository to your local machine:

    git clone https://github.com/your-username/image-processing-functions.git

2. Install the required libraries, preferably in a virtual environment:

    pip install -r requirements.txt

3. Use the functions in your Python scripts as shown in the examples below.

Examples:

Here are some examples of how to use the image processing functions:

    # Example usage of custom filter
    apply_custom_filter("input_image.jpg", "custom_filtered_image.jpg", "custom_filter.txt")

    # Example usage of Gaussian filter
    apply_gaussian_filter("input_image.jpg", "gaussian_filtered_image.jpg", kernel_size=5, sigma_x=0)

    # Example usage of median filter
    apply_median_filter("input_image.jpg", "median_filtered_image.jpg", kernel_size=3)

    # Example usage of max filter
    apply_max_filter("input_image.jpg", "max_filtered_image.jpg", kernel_size=5)

    # Example usage of min filter
    apply_min_filter("input_image.jpg", "min_filtered_image.jpg", kernel_size=5)

    # Example usage of high-pass filter
    apply_high_pass_filter("input_image.jpg", "high_pass_filtered_image.jpg", kernel_size=5)

    # Example usage of low-pass filter
    apply_low_pass_filter("input_image.jpg", "low_pass_filtered_image.jpg", kernel_size=5)

    # Example usage of motion blur
    apply_motion_blur("input_image.jpg", "motion_blurred_image.jpg", kernel_size=15)

Contributing:
If you have suggestions, improvements, or additional image processing functions to contribute, please feel free to open an issue or submit a pull request.

License:
This project is licensed under the MIT License - see the LICENSE file for details.
