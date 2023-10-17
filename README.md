# Scalable Backend for Satellite Imagery

The project involves providing the user access to multi-spectral satellite imagery, provide a filter infrastructure and allow the users to process the image in form of chunks. This allows the user to create efficient algorithms, include multiple processing technique and work with multiple spectral images.

## API Content

### Chunk Processing
File: chunk_processing.py
Description: API to divide and work on specific chunks of the image. This involves ImageProcessor class object creation with several functionalities to apply on chunks.
    
    The following are the functions offered:
        - def __init__(self, original_image_path)
        - def divide_into_chunks(self,chunk_size)
        - def delete_chunks(self)
        - def apply_function_on_specific_chunks(self,chunk_id, custom_filter)
        - def apply_function_on_multiple_chunks(self,chunk_ids, custom_filter)
        - def combine_image(self)

2. Image Filtering

    File: image_filter.py
    Description: API to allow the user to apply filters on chunks or whole image.
    The following are the functions offered:
        - def array_image(input_image_path,mode,print_it=False):
        - def salt_and_pepper(input_image_path, output_image_path):
        - def custom_filter(input_image_path, output_image_path, custom_filter_path):
        - def gaussian(input_image_path, output_image_path, kernel_size, sigma_x):
        - def median(input_image_path, output_image_path, kernel_size):
        - def max(input_image_path, output_image_path, kernel_size):
        - def min(input_image_path, output_image_path, kernel_size):
        - def high_pass(input_image_path, output_image_path, kernel_size):
        - def low_pass(input_image_path, output_image_path, kernel_size):
        - def motion_blur(input_image_path, output_image_path, kernel_size):

3. Multi-Spectral Satellite Image
    - File: 
        - multi_band_download.py
        - rgb_download.py
    
    Description: Satellite Imagery downloading facility to get the Multi-Band Imagery based on Geographical Information provided by the user.

Refer to the API folder for more detailed documentation.

## License

This script is released under the MIT License. See the LICENSE file for details.

## Acknowledgments

These scripts utilizes the geopy library for location data retrieval and the opencv-python library for image manipulation.
Source for USGS API:- https://github.com/yannforget/landsatxplore

Feel free to contribute to this project, report issues, or suggest improvements.