# Image Processor Documentation

The Image Processor is a Python class designed to perform various operations on images, such as dividing images into chunks, applying filters to chunks, combining chunks, and more. This README provides comprehensive documentation for the class and its functions.

## Getting Started

To use the Image Processor, follow these steps:

1. Create an instance of the ImageProcessor class by specifying the path to the original image:

   from image_processor import ImageProcessor

   Replace 'input_image.jpg' with your image file path
   processor = ImageProcessor("input_image.jpg")

2. Use this instance created to call the inbuilt functions from the class.
   - def print_original_path(self)
   - def divide_into_chunks(self,chunk_size)
   - def delete_chunks(self):
   - def apply_function_on_specific_chunks(self,chunk_id, custom_filter):
   - def apply_function_on_multiple_chunks(self,chunk_ids, custom_filter):
   - def print_chunk(self,chunk_id):
   - def return_map(self):
   - def combine_image(self):

## Functions
### Divide the original image into smaller chunks.
This function divides the original image into smaller chunks and saves them as individual files. Chunks are saved in the 'image_chunks' directory, and a text file called 'chunk_ids.txt' is created to store the IDs of the chunks.

    def divide_into_chunks(self,chunk_size):
        # ...

    - chunk_size (optional): Specify the size of each chunk.
    processor.divide_into_chunks(chunk_size=100)

### Delete Chunks
This function deletes chunks based on the IDs listed in 'chunk_ids.txt'.
    def delete_chunks(self):
        # ...

    processor.delete_chunks()

### Apply filter function on specific chunk
This function applies a custom filter function to a specific chunk identified by its ID. The filtered chunk is saved in the 'filtered_chunks' directory.

    def apply_function_on_specific_chunks(self,chunk_id, custom_filter):
        # ...
    - chunk_id: Specify the ID of the chunk.
    - custom_filter: Implement a custom filter function that takes a chunk as input and returns the filtered chunk.

    def custom_filter(chunk):
        Implement your custom filter logic here
        return chunk

    processor.apply_function_on_specific_chunk("chunk_0_0", custom_filter)

### Apply filter function on multiple chunks
This function applies a custom filter function to multiple chunks identified by their IDs.
    
    def apply_function_on_multiple_chunks(self,chunk_ids, custom_filter):
        # ...
    - chunk_ids: Specify a list of chunk IDs.
    - custom_filter: Implement a custom filter function that takes a chunk as input and returns the filtered chunk.

   chunk_ids = ["chunk_0_0", "chunk_1_0"]
   processor.apply_function_on_multiple_chunks(chunk_ids, custom_filter)

### Combining Chunks
This function combines the saved chunks to recreate the original image. It combines chunks both vertically and horizontally using hstack and vstack techniques.
    
    def combine_image(self):
        # ...

    processor.combine_chunks()

### Printing Chunks
This function displays an image associated with a specific chunk ID.

    def combine_image(self):
        # ...
    
    - chunk_id: Specify the chunk ID to display.
    processor.print_chunk("chunk_0_0")

# Filter API

This repository contains a collection of Python functions for various image processing tasks. These functions use the OpenCV library and provide different image filtering and manipulation techniques.

## Table of Contents:
1. Functions
    - Convert Image to Numpy Array
    - Salt and Pepper
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

## Functions:

Conversion to Array
Converts the image into array based on mode input, -1,0,1.

    -1  :- As it is.
    0   :- Black and White.
    1   :- Color.

    def array_image(input_image_path,mode,print_it=False):
        # ...
    
    - `input_image_path`: Path to the input image.
    - `mode`: Mode in which image is returned.
    - `print_it`: Print needed or not.

Salt and Pepper:
Applies a randomized salt and pepper filter to an image.

    def salt_and_pepper(input_image_path, output_image_path):
        # ...

    - `input_image_path`: Path to the input image.
    - `output_image_path`: Path to the output image.

Custom Filter:
Applies a custom filter to an image using a user-defined filter matrix.

    def custom_filter(input_image_path, output_image_path, custom_filter_path):
        # ...

    - `input_image_path`: Path to the input image.
    - `output_image_path`: Path to save the filtered output image.
    - `custom_filter_path`: Path to a text file containing the custom filter matrix.

Gaussian Filter:
Applies a Gaussian filter to an image for blurring or smoothing.

    def gaussian(input_image_path, output_image_path, kernel_size, sigma_x):
        # ...

    - `input_image_path`: Path to the input image.
    - `output_image_path`: Path to save the filtered output image.
    - `kernel_size`: Size of the Gaussian kernel (e.g., 3, 5, 7).
    - `sigma_x`: Standard deviation for Gaussian smoothing (use 0 for auto-calculation).

Median Filter:
Applies a median filter to an image for noise reduction.

    def median(input_image_path, output_image_path, kernel_size):
        # ...

    - `input_image_path`: Path to the input image.
    - `output_image_path`: Path to save the filtered output image.
    - `kernel_size`: Size of the median filter kernel.

Max Filter:
Applies a max filter (dilation) to an image.

    def max(input_image_path, output_image_path, kernel_size):
        # ...

    - `input_image_path`: Path to the input image.
    - `output_image_path`: Path to save the filtered output image.
    - `kernel_size`: Size of the max filter kernel.

Min Filter:
Applies a min filter (erosion) to an image.

    def min(input_image_path, output_image_path, kernel_size):
        # ...

    - `input_image_path`: Path to the input image.
    - `output_image_path`: Path to save the filtered output image.
    - `kernel_size`: Size of the min filter kernel.

High-Pass Filter:
Applies a high-pass filter to an image to enhance edges and fine details.

    def high_pass(input_image_path, output_image_path, kernel_size):
        # ...

    - `input_image_path`: Path to the input image.
    - `output_image_path`: Path to save the filtered output image.
    - `kernel_size`: Size of the high-pass filter kernel.

Low-Pass Filter:
Applies a low-pass filter to an image to reduce noise and smooth the image.

    def low_pass(input_image_path, output_image_path, kernel_size):
        # ...

    - `input_image_path`: Path to the input image.
    - `output_image_path`: Path to save the filtered output image.
    - `kernel_size`: Size of the low-pass filter kernel.

Motion Blur:
Applies a motion blur effect to an image.

    def motion_blur(input_image_path, output_image_path, kernel_size):
        # ...

    - `input_image_path`: Path to the input image.
    - `output_image_path`: Path to save the motion-blurred output image.
    - `kernel_size`: Size of the motion blur kernel.

## Usage:

1. Clone this repository to your local machine:

    git clone https://github.com/your-username/image-processing-functions.git

2. Install the required libraries, preferably in a virtual environment.

3. Use the functions in your Python scripts as shown in the examples below.

## Examples:

Here are some examples of how to use the image processing functions:

    from API import image_filter

    # Example usage of custom filter
    image_filter.custom_filter("input_image.jpg", "custom_filtered_image.jpg", "custom_filter.txt")

    # Example usage of Gaussian filter
    image_filter.gaussian("input_image.jpg", "gaussian_filtered_image.jpg", kernel_size=5, sigma_x=0)

    # Example usage of median filter
    image_filter.median("input_image.jpg", "median_filtered_image.jpg", kernel_size=3)

    # Example usage of max filter
    image_filter.max("input_image.jpg", "max_filtered_image.jpg", kernel_size=5)

    # Example usage of min filter
    image_filter.min("input_image.jpg", "min_filtered_image.jpg", kernel_size=5)

    # Example usage of high-pass filter
    image_filter.high_pass("input_image.jpg", "high_pass_filtered_image.jpg", kernel_size=5)

    # Example usage of low-pass filter
    image_filter.low_pass("input_image.jpg", "low_pass_filtered_image.jpg", kernel_size=5)

    # Example usage of motion blur
    image_filter.motion_blur("input_image.jpg", "motion_blurred_image.jpg", kernel_size=15)

## Contributing:

If you have suggestions, improvements, or additional image processing functions to contribute, please feel free to open an issue or submit a pull request.

# Satellite Image Downloader and Location Selector
File:- rgb_download.py

This Python script provides functionalities to download satellite images from various sources based on user-defined coordinates or addresses. It also includes a location selector to choose specific locations and download corresponding satellite images.

## Features

- Download satellite images by specifying coordinates (latitude and longitude) and zoom level.
- Select locations by providing an address, view multiple locations, and download images accordingly.
- Customizable preferences for download sources, tile size, and more.

## Prerequisites

Before using the script, make sure you have the following prerequisites:

- Python 3.x
- Required Python libraries: numpy, requests, geopy, opencv-python

You can install these libraries using pip:

pip install numpy requests geopy opencv-python

## Usage

### Location Selector

To use the location selector for downloading satellite images:

1. Run the script.
2. Enter the location (address) you want to search for.
3. The script will display a list of matching locations with coordinates and addresses.
4. Select a location from the list by entering the corresponding S.No.
5. Enter the desired zoom level for the satellite image.
6. The script will download and save the satellite image.

### Specific Coordinate
Download a satellite image for specific coordinates.

    def specific_coordinate(BRlat, BRlon, TLlat, TLlon, zoom, output_file_name):
        # ...

    - `BRlat`: Latitude of Bottom Right for desired bounding box.
    - `BRlon`: Longitude of Bottom Right for desired bounding box.
    - `TLlat`: Latitude of Top Left for desired bounding box.
    - `TLlon`: Longitude of Top Left for desired bounding box.
    - `output_file_name`: Name for output file/saved file.
    - `zoom`: Zoom level for the bounding box.

### Location Listing
Location Listing based on address as an argument.

    def obtain_location_list(address):
        # ...
    - `address`: Latitude of Bottom Right for desired bounding box.
    Returns:- List of locations based on the address input.

## Preferences

You can customize the download preferences by modifying the preferences.json file. The following preferences are available:

- url: URL template for downloading satellite tiles.
- tile_size: Size of the satellite tiles (e.g., 256).
- tile_format: Format of the satellite tiles (e.g., 'jpg' or 'png').
- dir: Directory to store downloaded images.
- headers: HTTP headers for tile requests.
- tl: Top-left coordinate for downloading a specific region.
- br: Bottom-right coordinate for downloading a specific region.
- zoom: Zoom level for downloading a specific region.

## License

This script is released under the MIT License. See the LICENSE file for details.

## Acknowledgments

This script utilizes the geopy library for location data retrieval and the opencv-python library for image manipulation.

Feel free to contribute to this project, report issues, or suggest improvements.
