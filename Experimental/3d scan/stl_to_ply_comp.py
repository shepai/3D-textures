""" This is a script to compare the source STL shapes that we used to make the 3D printed objects to the scanned point clouds from the Intel Real Sense cameras.
"""
#%%  imports and path configuration
import sys
import os
import open3d as o3d
import numpy as np

# Add the 'Experimental' directory to the system path so we can import from '3d scan'
# Note: Since '3d scan' has a space, we use a slightly different approach to import it
sys.path.append(os.path.abspath("Experimental"))

# We use importlib to handle the folder name with a space
import importlib.util
module_name = "three_d_scan" # We treat it as a module
file_path = os.path.join( "process_3d_files.py")
#file_path = os.path.join("3d scan", "process_3d_files.py")

# Load the module manually to bypass the space in the folder name
spec = importlib.util.spec_from_file_location(module_name, file_path)
p3f = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p3f)

#%% process the ply file

# ==========================
# Processing
# ==========================

# Fixed the path string (removed the trailing ""3d scan" typo)
ply_path1 = r"D:\Projects\3D-textures\processed_models\BAMBU\B1T2.ply"

# Call the function
# This will return the PointCloud object as a variable
ply_obj1 = p3f.process_ply(ply_path1, rm_floor=True)

if ply_obj1 is not None:
    print("Successfully loaded and processed point cloud.")
    
    # ==========================
    # Visualization
    # ==========================
    # This will open a separate interactive window showing the 3D point cloud
    o3d.visualization.draw_geometries([ply_obj1], window_name="3D Scan Result")
else:
    print("Failed to process the point cloud. Check if the path is correct.")