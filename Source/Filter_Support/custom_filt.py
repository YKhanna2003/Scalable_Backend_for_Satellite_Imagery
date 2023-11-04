import multiprocessing
from PIL import Image

def read_filter_matrix_from_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

    filter_matrix = []
    for line in lines:
        values = [float(eval(val)) for val in line.strip().split()]
        filter_matrix.append(values)

    return filter_matrix

def apply_filter_chunk(image, filter_matrix, chunk_start, chunk_end, result_queue):
    width, height = image.size
    filter_size = len(filter_matrix)
    filter_radius = filter_size // 2

    chunk_filtered_pixels = []

    for x in range(chunk_start[0], chunk_end[0]):
        for y in range(chunk_start[1], chunk_end[1]):
            new_pixel = [0, 0, 0]

            for i in range(filter_size):
                for j in range(filter_size):
                    img_x = x + i - filter_radius
                    img_y = y + j - filter_radius

                    if img_x < 0 or img_x >= width or img_y < 0 or img_y >= height:
                        pixel = (0, 0, 0)
                    else:
                        pixel = image.getpixel((img_x, img_y))

                    for c in range(3):
                        new_pixel[c] += pixel[c] * filter_matrix[i][j]

            new_pixel = tuple(int(val) for val in new_pixel)
            chunk_filtered_pixels.append(((x, y), new_pixel))

    result_queue.put(chunk_filtered_pixels)

def apply_filter_parallel(image, filter_matrix, num_processes):
    width, height = image.size
    chunk_height = height // num_processes

    processes = []
    result_queue = multiprocessing.Queue()

    for i in range(num_processes):
        chunk_start = (0, i * chunk_height)
        chunk_end = (width, (i + 1) * chunk_height if i < num_processes - 1 else height)
        process = multiprocessing.Process(target=apply_filter_chunk, args=(image, filter_matrix, chunk_start, chunk_end, result_queue))
        processes.append(process)
        process.start()

    filtered_image = Image.new("RGB", (width, height))

    for _ in range(num_processes):
        chunk_filtered_pixels = result_queue.get()
        for pixel_coords, pixel_value in chunk_filtered_pixels:
            filtered_image.putpixel(pixel_coords, pixel_value)

    for process in processes:
        process.join()

    return filtered_image

def custom_filter(imagepath,filename):
    input_image_path = imagepath
    output_image_path = "filtered_image_parallel.jpg"
    filter_matrix_file = filename

    max_processes = multiprocessing.cpu_count()
    num_processes = min(4, max_processes)

    filter_matrix = read_filter_matrix_from_file(filter_matrix_file)

    input_image = Image.open(input_image_path)
    filtered_image = apply_filter_parallel(input_image, filter_matrix, num_processes)
    filtered_image.save(output_image_path)

    print("Filter applied in parallel and saved as filtered_image_parallel.jpg")