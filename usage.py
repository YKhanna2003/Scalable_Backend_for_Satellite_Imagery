from API import image_filter
from API import chunk_processing as chunk
from API import multi_band_download
import cv2

def filter_usage():
    Image_File_Path = "./example.png"
    arr=image_filter.array_image(Image_File_Path,-1)
    image_filter.salt_and_pepper(Image_File_Path,"output2.jpg")
    image_filter.array_image(Image_File_Path,1,True)
    image_filter.print_specific_image(image_filter.salt_and_pepper(Image_File_Path,"output2.jpg"))
    image_filter.custom_filter(Image_File_Path,"output4.png","sharpen.txt")
    image_filter.gaussian(Image_File_Path,"output5.png",5,0)
    image_filter.min(Image_File_Path,"output6.jpg",5)
    image_filter.low_pass(Image_File_Path,"output7.jpg",5)
    image_filter.motion_blur(Image_File_Path,"output8.jpg",20)

def chunk_processing_usage():
    img = chunk.ImageProcessor("example.png")
    print(img.divide_into_chunks(100))
    def custom_filter(image):
        # Apply a custom filter (e.g., grayscale)
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print(img.apply_function_on_specific_chunks("chunk_0_0",custom_filter))
    print(img.apply_function_on_multiple_chunks(["chunk_0_1","chunk_0_2","chunk_0_3"],custom_filter))
    print(img.return_map())
    print(img.combine_image())
    print(img.delete_chunks())

def multi_band_download_usage():
    username="ENTER USERNAME HERE"
    password="ENTER PASSWORD HERE"
    m=multi_band_download.Multi_Band(username,password)
    m.geographic_info(15.39104765,73.87800155288005,'2000-01-01','2000-10-01',10)
    print(m.return_info())
    m.search_scenes('landsat_tm_c2_l1')
    m.search_all_datasets()
    scene_array = m.return_all_scene_id()
    scene_dic = m.return_all_scene_info()
    for scene in scene_array:
        print("Scene ID:- {}, Start Time:- {}".format(scene_dic[scene]["landsat_scene_id"],scene_dic[scene]["start_time"]))
    m.image_registraton('Image_dir\data','Image_dir\images')
    m.sceneid()
    scene_id=m.select_scene()
    m.json_sceneinfo(scene_id,'data.json')
    m.download_scene(scene_id,"./data")

if __name__ == "__main__":
    chunk_processing_usage()