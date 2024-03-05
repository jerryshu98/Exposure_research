from pathlib import Path
import pydicom
import matplotlib.pyplot as plt
import pandas as pd
import pickle
import cv2
import numpy as np


def find_directories(directory):
    root_dir = Path(directory)
    directories = [str(d) for d in root_dir.iterdir() if d.is_dir()]
    
    return directories

def find_dcm_files(directory):
    root_dir = Path(directory)
    dcm_files = root_dir.rglob('*.dcm')
    dcm_file_paths = [str(file) for file in dcm_files]
    
    return dcm_file_paths

def display_dicom_image(filepath):
    dcm = pydicom.dcmread(filepath)
    image_data = dcm.pixel_array
    resized_image = cv2.resize(image_data, (256,256)) 
    normalized_image = resized_image / 255.0
    return np.array(normalized_image)

def draw_CR(image_data):
    
    plt.imshow(image_data, cmap='gray') 
    plt.axis('off')
    plt.show()

root_path = "./downloads/"
id_list = find_directories(root_path)
total_folder_list = []
for path in id_list:
    total_folder_list+=find_directories(path)
all_floder_list = []
for path in total_folder_list:
    all_floder_list+=find_directories(path)
    

id_list = all_floder_list

file_path = './MIDRC_Cases_table33.csv' 
data_df = pd.read_csv(file_path)
data_df = data_df.set_index('submitter_id')
#US, Not Reported

zip_list = []
image_list = []
fail = 0
count = 0
now = -1
for id_path in id_list:
    count+=1
    #print(count, len(zip_list), now)
    #print(count)
    if(count % 100 == 0):
        print(count, len(zip_list), now)
    id = id_path.split('/')[-1]
    zip_now = data_df.loc[id]['zip']
    if (zip_now == "US" or zip_now == "Not Reported"):
        continue
    pic_path_now = find_dcm_files(id_path)
    for image_path in pic_path_now:
        try:
            image_now = display_dicom_image(image_path)
            zip_list.append(zip_now)
            image_list.append(image_now)
        except:
            print("fail on "+id)
        
'''
with open('zip_lists_9968.pkl', 'wb') as f:
    pickle.dump((zip_list), f)
    
print("store zip_list")
with open('image_lists_9968.pkl', 'wb') as f:
    pickle.dump((image_list), f)
print("store image_list")
'''
