import kagglehub
import subprocess 
import os 
import pandas as pd
import numpy as np
import cv2 
PATH="/home/dexter/Documents/GitHub/3D-textures/Experimental/data/gel"
"""
pathA = kagglehub.dataset_download("dextershepherd/repeatable-3d-dataset-resin")
pathB = kagglehub.dataset_download("dextershepherd/3d-texture-gel-tactip")

result = subprocess.run(["mv", pathA, PATH], capture_output=True, text=True)
result = subprocess.run(["mv", pathB, PATH], capture_output=True, text=True)"""
datapath=PATH
import os 
files=os.listdir(datapath)
dataset= pd.DataFrame({
    'Index':[],
    'Filament':[],
    'Pattern':[],
    'Printer':[],
    "Pressure":[]
})
X=[]
idx=0
percentage=0.4
for i,file in enumerate(files):
    data=np.load(datapath+"/"+file)
    info=file.replace(".npy","").split("_")
    data=data.reshape((1*2*5*5,480,640,3))
    print(file,data.shape)
    d=[]
    for image in data: #conversion
        gray = np.dot(image[..., :3], [0.2989, 0.5870, 0.1140])
        h=int(image.shape[0]*percentage)
        w=int(image.shape[1]*percentage)
        gray = cv2.resize(gray,(w,h),interpolation=cv2.INTER_AREA)
        d.append(gray)
    new_row = pd.DataFrame([{
    'Index': int(idx),
    'Filament': info[0],
    'Pattern': info[1],
    'Printer': info[3],
    'Pressure': info[2]
}])
    dataset = pd.concat([dataset, new_row], ignore_index=True)
    idx+=1
    X.append(np.array(d).reshape((1,2,5*5,h,w)))

dataset.head()
X=np.array(X).reshape(len(X),2,25,h,w)
np.save("/home/dexter/Documents/GitHub/3D-textures/Experimental/data/X",X)
dataset.to_csv("/home/dexter/Documents/GitHub/3D-textures/Experimental/datameta.csv")
print(X.shape,len(dataset))