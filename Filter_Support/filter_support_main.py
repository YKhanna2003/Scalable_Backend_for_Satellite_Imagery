import os
import tkinter as tk
import cv2
from tkinter import filedialog
import random
from custom_filt import custom_filter
from PIL import Image, ImageFilter
import multiprocessing
from motion_blur import motion_blur_main
from gaussian import gaussian_main

img = []
file_name_address = ""
file_paths = []
file_path_list = []
s_no_space = 5
address_space = 128
dic = {}
root = tk.Tk()

def print_menu():
    menu_file = open("filters_menu.txt","r")
    print(menu_file.read())
    menu_file.close()

def print_image_list():
    global dic
    i = 1
    for file in file_path_list:
        if i==1:
            j=0
            while j < s_no_space + address_space + 7:
                print("-",end="")
                j+=1
            print("\n| {:>5} | {:<128} |".format("S.No.","File Address"))
            j=0
            while j < s_no_space + address_space + 7:
                print("-",end="")
                j+=1
            print("")
        addresscovered = 0
        print("| {:>5} | {:<128} |".format(str(i),file[:128]))
        addresscovered += 128
        while addresscovered<len(file):
            print("| {:>5} | {:<128} |".format("",file[addresscovered:addresscovered+128],""))
            addresscovered+=128
        dic[i]=file
        i+=1
    j=0
    while j < s_no_space + address_space + 7:
        print("-",end="")
        j+=1

def return_image_address():
    global dic
    print_image_list()
    file_name_input = int(input("\nEnter file number to continue:- "))
    return dic[file_name_input]

def print_image():
    checker = [0,1,-1]
    while 1:
        mode = int(input("Enter the Mode you wish to work with (1 - Color, 0 - Grayscale, -1 - Unchanged (As-Is)):- "))
        if mode not in checker:
            print("Incorrect Entry, Choose from the following options only")
        else:
            break
    img = cv2.imread(file_name_address,mode)
    print(img)
    cv2.imshow('Image Output',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def print_specific_image(img):
    cv2.imshow('Image Output',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def choose_file_list():
    global file_path_list
    global root
    root.withdraw()
    file_path_list = filedialog.askopenfilenames(parent=root,title='Choose a file')
    if len(file_path_list) == 0:
        print("Warning: No File Entered")
    file_path_list = root.tk.splitlist(file_path_list)

def print_file_address():
    global file_name_address
    print("File Chosen is:- {}".format(file_name_address))

def select_an_image():
    global file_name_address
    file_name_address = return_image_address()
    print_file_address()

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

def salt_and_pepper():
    mode = 0
    img = cv2.imread(file_name_address,mode)
    print(img)
    cv2.imshow('Image Output',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    rows = len(img)
    columns = len(img[0])
    print("Rows are {rows} and columns are {columns}".format(rows=rows,columns=columns))
    salt_and_pepper_img = add_noise(img)
    print_specific_image(salt_and_pepper_img)

def apply_median_filter_chunk(chunk, chunk_index):
    try:
        filtered_chunk = chunk.filter(ImageFilter.MedianFilter())
        return chunk_index, filtered_chunk
    except Exception as e:
        print(f"Error processing chunk {chunk_index}: {e}")
        return chunk_index, None

def apply_max_filter_chunk(chunk, chunk_index):
    try:
        filtered_chunk = chunk.filter(ImageFilter.MaxFilter())
        return chunk_index, filtered_chunk
    except Exception as e:
        print(f"Error processing chunk {chunk_index}: {e}")
        return chunk_index, None

def apply_min_filter_chunk(chunk, chunk_index):
    try:
        filtered_chunk = chunk.filter(ImageFilter.MinFilter())
        return chunk_index, filtered_chunk
    except Exception as e:
        print(f"Error processing chunk {chunk_index}: {e}")
        return chunk_index, None

def filter_multiprocessing(func_name):
    input_image_path = file_name_address
    
    num_processes = multiprocessing.cpu_count()
    
    image = Image.open(input_image_path)
    width, height = image.size
    chunk_width = width // num_processes
    
    chunks = []
    for i in range(num_processes):
        left = i * chunk_width
        right = left + chunk_width
        chunk = image.crop((left, 0, right, height))
        chunks.append(chunk)
    
    pool = multiprocessing.Pool(processes=num_processes)
    
    results = []
    for chunk_index, chunk in enumerate(chunks):
        results.append(pool.apply_async(func_name, args=(chunk, chunk_index)))
    
    pool.close()
    pool.join()
    
    sorted_results = sorted(results, key=lambda x: x.get()[0])
    filtered_chunks = [result.get()[1] for result in sorted_results]
    
    output_image = Image.new("RGB", (width, height))
    x_offset = 0
    for chunk in filtered_chunks:
        output_image.paste(chunk, (x_offset, 0))
        x_offset += chunk_width
    
    output_image.show()
    output_image.save("output_image.jpg")
    print("Image processed and recombined!")

def apply_pass_filter(mode):
    image = cv2.imread(file_name_address)
    kernel_size = (5, 5)
    sigma = 2.0
    low_pass_image = cv2.GaussianBlur(image, kernel_size, sigma)
    high_pass_image = cv2.subtract(image, low_pass_image)
    if mode == 1:
        return high_pass_image
    return low_pass_image

def pass_main(mode,image_string):
    output_image=apply_pass_filter(mode)
    cv2.imshow(image_string,output_image)
    output_image_path = 'output_image.jpg'
    cv2.imwrite(output_image_path, output_image)

def main():
    global file_name_address
    while 1:
        os.system("cls")
        print_menu()
        menu_input = int(input("Enter your Choice:- "))
        os.system("cls")
        match menu_input:
            case 0 : break
            case 1: select_an_image()
            case 2: print_image()
            case 3: print_file_address()
            case 4:
                choose_file_list()
                select_an_image()
            case 5: 
                print_image_list()
                input("\nPress Enter to Continue")
                continue
            case 6: salt_and_pepper()
            case 7: custom_filter(file_name_address,"custom_filter.txt")
            case 8: custom_filter(file_name_address,"sharpen_image.txt")
            case 9: gaussian_main(file_name_address)
            case 10: filter_multiprocessing(apply_median_filter_chunk)
            case 11: filter_multiprocessing(apply_max_filter_chunk)
            case 12: filter_multiprocessing(apply_min_filter_chunk)
            case 13: custom_filter(file_name_address,"emboss_filter.txt")
            case 14: custom_filter(file_name_address,"prewitt_horizontal.txt")
            case 15: custom_filter(file_name_address,"prewitt_vertical.txt")
            case 16: custom_filter(file_name_address,"sobel_horizontal.txt")
            case 17: custom_filter(file_name_address,"sobel_vertical.txt")
            case 18: pass_main(1,"High Pass Output")
            case 19: pass_main(0,"Low Pass Output")
            case 20: custom_filter(file_name_address,"laplacian_filter.txt")
            case 21: motion_blur_main(file_name_address)
            case _: print("Invalid Choice, please re-enter the choice")
        input("\nPress Enter to Continue")
if __name__ == "__main__":
    choose_file_list()
    select_an_image()
    main()
