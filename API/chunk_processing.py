import numpy as np
import cv2
import os

def hstack_images(image_file_paths):
    """
    Stack a set of images horizontally (column-wise).

    Parameters:
        image_file_paths (list of str): List of file paths to the images to be horizontally stacked.

    Returns:
        numpy.ndarray: The horizontally stacked image.
    """
    # Load images and convert them to arrays
    images = [cv2.imread(file_path) for file_path in image_file_paths]

    # Check if the images were loaded successfully
    for i, image in enumerate(images):
        if image is None:
            raise ValueError(f"Failed to load image at path: {image_file_paths[i]}")

    # Check if the images have the same height (number of rows)
    num_rows = images[0].shape[0]
    for image in images:
        if image.shape[0] != num_rows:
            raise ValueError("Images must have the same height for hstack.")

    # Horizontally stack the images
    stacked_image = np.hstack(images)
    return stacked_image

def vstack_images(image_arrays):
    """
    Stack a set of images vertically (row-wise).

    Parameters:
        image_arrays (list of numpy.ndarray): List of image arrays to be vertically stacked.

    Returns:
        numpy.ndarray: The vertically stacked image.
    """
    # Check if the list is empty
    if not image_arrays:
        raise ValueError("No image arrays provided for vstack.")

    # Check if the image arrays have the same width (number of columns)
    num_columns = image_arrays[0].shape[1]
    for image in image_arrays:
        if image.shape[1] != num_columns:
            raise ValueError("Image arrays must have the same width for vstack.")

    # Vertically stack the images
    stacked_image = np.vstack(image_arrays)
    return stacked_image

class ImageProcessor:
    def __init__(self, original_image_path):
        self.__original_image_path = original_image_path
        self.__image = cv2.imread(self.__original_image_path)
        self.__filemap = {}
    def print_original_path(self):
        return self.__original_image_path
    def divide_into_chunks(self,chunk_size):
        """
        Divides an image into smaller chunks, assigns unique IDs, and saves each chunk with a unique name.
        Saves chunk IDs into a text file called chunk_ids.txt.

        Args:
        - image: A NumPy array representing the input image.
        - chunk_size: The size (in pixels) of each smaller chunk.

        Returns:
        - chunk_ids: A list containing unique IDs for each chunk.
        """
        image = self.__image
        # Check if the input image is a NumPy array
        if not isinstance(image, np.ndarray):
            raise ValueError("Input image must be a NumPy array.")

        # Get the dimensions of the input image
        image_height, image_width, channels = image.shape

        # Ensure that the chunk size is valid
        if chunk_size <= 0:
            raise ValueError("Invalid chunk size.")

        # Initialize variables
        chunk_ids = []
        chunk_counter = 0

        # Create a directory to save the chunks
        if not os.path.exists("image_chunks"):
            os.makedirs("image_chunks")

        for y in range(0, image_height, chunk_size):
            for x in range(0, image_width, chunk_size):
                # Calculate the dimensions for the current chunk
                chunk_height = min(chunk_size, image_height - y)
                chunk_width = min(chunk_size, image_width - x)

                # Extract a chunk from the image
                chunk = image[y:y+chunk_height, x:x+chunk_width]

                # Generate a unique ID for the chunk based on its position
                chunk_id = f"chunk_{x // chunk_size}_{y // chunk_size}"

                # Save the chunk as an image
                chunk_filename = os.path.join("image_chunks", f"{chunk_id}.png")
                cv2.imwrite(chunk_filename, chunk)
                self.__filemap[chunk_id] = chunk_filename

                # Append the unique ID to the list
                chunk_ids.append(chunk_id)

                chunk_counter += 1

        # Save chunk IDs to a text file
        with open("chunk_ids.txt", "w") as file:
            file.write("\n".join(chunk_ids))
        file.close()
        return chunk_ids
    def delete_chunks(self):
        """
        Deletes all the chunks whose IDs are listed in the chunk_ids.txt file.
        Returns True, if deletion was successful.
        """
        # Check if the chunk_ids.txt file exists
        if not os.path.exists("chunk_ids.txt"):
            print("chunk_ids.txt file not found.")
            return
        # Read chunk IDs from the text file
        with open("chunk_ids.txt", "r") as file:
            chunk_ids = file.read().splitlines()
        # Delete chunks based on their IDs
        for chunk_id in chunk_ids:
            #chunk_filename = os.path.join("image_chunks", f"{chunk_id}.png")
            chunk_filename = self.__filemap[chunk_id]
            if os.path.exists(chunk_filename):
                os.remove(chunk_filename)
                print(f"Deleted chunk: {chunk_id}")
        os.remove("chunk_ids.txt")

        # Check if the chunk_ids.txt file exists
        if not os.path.exists("filtered_chunk_ids.txt"):
            print("filtered_chunk_ids.txt file not found.")
            return
        # Read chunk IDs from the text file
        with open("filtered_chunk_ids.txt", "r") as file:
            chunk_ids = file.read().splitlines()
        # Delete chunks based on their IDs
        for chunk_id in chunk_ids:
            #chunk_filename = os.path.join("image_chunks", f"{chunk_id}.png")
            chunk_filename = self.__filemap[chunk_id]
            if os.path.exists(chunk_filename):
                os.remove(chunk_filename)
                print(f"Deleted chunk: {chunk_id}")
        os.remove("filtered_chunk_ids.txt")
        self.__filemap = {}
        return True
    def apply_function_on_specific_chunks(self,chunk_id, custom_filter):
        """
        Applies a custom filter on a specific image chunk and saves the result as a new image.

        Args:
        - chunk_id: The ID of the chunk to apply the filter on.
        - custom_filter: A function that takes an image (as a NumPy array) as input and applies the desired filter.
        """

        # Check if the chunk ID is valid
        if not chunk_id:
            print("Invalid chunk ID.")
            return

        # Load the chunk image
        #chunk_filename = os.path.join("image_chunks", f"{chunk_id}.png")
        chunk_filename = self.__filemap[chunk_id]
        if not os.path.exists(chunk_filename):
            print(f"Chunk '{chunk_id}' not found.")
            return

        chunk_image = cv2.imread(chunk_filename)

        # Apply the custom filter
        filtered_image = custom_filter(chunk_image)

        # Create the "filtered_chunks" folder if it doesn't exist
        if not os.path.exists("filtered_chunks"):
            os.makedirs("filtered_chunks")

        # Save the filtered image with a different name
        filtered_filename = os.path.join("filtered_chunks", f"{chunk_id}_filtered.png")
        filtered_chunk_id = "filtered_"+chunk_id
        self.__filemap[filtered_chunk_id]=filtered_filename
        cv2.imwrite(filtered_filename, filtered_image)
        print(f"Filtered chunk saved as '{filtered_filename}'")
        chunk_ids = []
        filtered_chunk_id=filtered_chunk_id+"\n"
        chunk_ids.append(filtered_chunk_id)
        with open("filtered_chunk_ids.txt", "a") as file:
             file.write("\n".join(chunk_ids))
        file.close()
        return True
    def apply_function_on_multiple_chunks(self,chunk_ids, custom_filter):
        """
        Applies a custom filter on multiple image chunks and saves the results as new images.

        Args:
        - chunk_ids: A list of chunk IDs to apply the filter on.
        - custom_filter: A function that takes an image (as a NumPy array) as input and applies the desired filter.
        """

        # Iterate over the provided chunk IDs
        for chunk_id in chunk_ids:
            self.apply_function_on_specific_chunks(chunk_id, custom_filter)
        return True
    def print_chunk(self,chunk_id):
        """
        Returns True if correct execution of function
        Prints the image associated with the given chunk ID.

        Args:
        - chunk_id: The ID of the chunk to be printed.
        """

        # Check if the chunk ID is valid
        if not chunk_id:
            print("Invalid chunk ID.")
            return

        # Construct the file path for the chunk image
        #chunk_filename = os.path.join("image_chunks", f"{chunk_id}.png")
        chunk_filename = self.__filemap[chunk_id]
        # Check if the chunk image file exists
        if not os.path.exists(chunk_filename):
            print(f"Chunk '{chunk_id}' is missing.")
            return

        # Load and display the chunk image
        chunk_image = cv2.imread(chunk_filename)
        cv2.imshow(f"Chunk {chunk_id}", chunk_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        True
    def return_map(self):
        return self.__filemap
    def combine_image(self):
        """
        Combines chunks to recreate the original image and saves it if all chunks are available.
        """
        with open("chunk_ids.txt", "r") as file:
            chunk_ids = file.read().splitlines()
        combined_chunks = {}
        temp_return = []
        for chunk_id in chunk_ids:
            filtered_key = "filtered_"+chunk_id
            if filtered_key in self.__filemap:
                chunk_filename = self.__filemap[filtered_key]
                temp_return.append(filtered_key)
            else:
                chunk_filename = self.__filemap[chunk_id]
                temp_return.append(chunk_id)
            if not os.path.exists(chunk_filename):
                print(f"Chunk '{chunk_id}' is missing.")
                return
            chunk = cv2.imread(chunk_filename)
            _, x, y = chunk_id.split('_')
            x, y = int(x), int(y)
            combined_chunks[(x, y)] = chunk
        if not combined_chunks:
            print("No chunks available to combine.")
            return
        i = 0
        final_image = {}
        final_image[i]=[]
        for chunks in temp_return:
            if chunks.endswith(str(i)):
                final_image[i].append(self.__filemap[chunks]) 
            else:
                i = i+1
                final_image[i]=[]
                final_image[i].append(self.__filemap[chunks])
        
        j = 0
        hstacked_images = []
        while j<=i:
            hstacked_images.append(hstack_images(final_image[j]))
            cv2.imwrite("stacked_image_{}.jpg".format(j), hstacked_images[j])
            j=j+1
        imgg=vstack_images(hstacked_images)
        cv2.imwrite("Final Image.jpg",imgg)
        return True 

"""
USAGE:-
if __name__ == "__main__":
    img = ImageProcessor("example.jpg")
    print(img.divide_into_chunks(100))
    def custom_filter(image):
        # Apply a custom filter (e.g., grayscale)
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print(img.apply_function_on_specific_chunks("chunk_0_0",custom_filter))
    print(img.apply_function_on_multiple_chunks(["chunk_0_1","chunk_0_2","chunk_0_3"],custom_filter))
    print(img.return_map())
    print(img.combine_image())
"""