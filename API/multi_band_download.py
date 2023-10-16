from landsatxplore.api import API
import json
from datetime import datetime
from shapely.geometry import Polygon
from landsatxplore.earthexplorer import EarthExplorer

class Multi_Band:
    def __init__(self, username, password):
        self.__username=username
        self.__password=password
        self.__sceneid=[]
        self.__sceneinfo=[]
        self.__scenedic={}
        self.__datasetlist = ['landsat_tm_c2_l1','landsat_tm_c2_l2','landsat_etm_c2_l1','landsat_etm_c2_l2','landsat_ot_c2_l1','landsat_ot_c2_l2','landsat_ot_c2_l1','landsat_ot_c2_l2']

    def __json_serial(self,obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Polygon):
            return obj.__dict__
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    def geographic_info(self, latitude, longitude, start_date, end_date, max_cloud_cover):
        self.__latitude=latitude
        self.__longitude=longitude
        self.__start_date=start_date
        self.__end_date=end_date
        self.__max_cloud_cover=max_cloud_cover

    def search_scenes(self,dataset_name):
        if dataset_name not in self.__datasetlist:
            print("Incorrect Dataset Query")
            return
        api = API(self.__username, self.__password)
        self.__sceneinfo = api.search(dataset_name,self.__latitude,self.__longitude,self.__start_date,self.__end_date,self.__max_cloud_cover)
        for scene in self.__sceneinfo:
            if scene['landsat_scene_id'] not in self.__sceneid:  
                self.__sceneid.append(scene['landsat_scene_id'])
                self.__scenedic[scene['landsat_scene_id']]=scene

    def sceneid(self):
        if len(self.__sceneid)==0:
            print("No Scenes Available")
            return
        print("Available Scene IDs are")
        for scene_id in self.__sceneid:
            print(scene_id)

    def json_sceneinfo(self,scene_id,json_file_path):
        if scene_id not in self.__scenedic:
            print("Scene ID not available")
            return
        data=self.__scenedic[scene_id]
        json_file_path=scene_id+"_"+json_file_path
        if json_file_path.endswith(".json"):
            pass
        else:
            json_file_path=json_file_path+".json"

        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, default=self.__json_serial,indent=4)
        print(f'Data has been written to {json_file_path}')

    def return_info(self):
        return {
            "username":self.__username,
            "password":self.__password,
            "latitude":self.__latitude,
            "longitude":self.__longitude,
            "start_date":self.__start_date,
            "end_date":self.__end_date,
            "max_cloud_state":self.__max_cloud_cover
            }
    
    def search_all_datasets(self):
        for dataset in self.__datasetlist:
            self.search_scenes(dataset)
        
    def select_scene(self):
        menu_items=self.__sceneid
        if len(menu_items)==0:
            print("Empty List Passed")
            return 
        print("Scene ID Number")
        for i, item in enumerate(menu_items, 1):
            print(f"{i}.\t{item}")
        return self.__get_user_choice(menu_items)

    def __get_user_choice(self,menu_items):
        while True:
            try:
                choice = int(input("Enter your choice: "))
                if 1 <= choice <= len(menu_items):
                    return menu_items[choice - 1]
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def download_scene(self,scene_id,output_dir):
        ee = EarthExplorer(self.__username, self.__password)
        ee.download(scene_id, output_dir)
        ee.logout()

    def return_all_scene_info(self):
        return self.__scenedic

# Usage Example
# username="enter_username_here"
# password="enter_password_here"
# m=Multi_Band(username,password)
# m.geographic_info(15.39104765,73.87800155288005,'1995-01-01','1995-10-01',10)
# m.search_scenes('landsat_tm_c2_l1')
# m.search_all_datasets()
# m.sceneid()
# scene_id=m.select_scene()
# m.json_sceneinfo(scene_id,'data.json')
# m.download_scene(scene_id,"./data")