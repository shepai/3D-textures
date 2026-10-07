""" This is a script to compare the source STL shapes that we used to make the 3D printed objects to the scanned point clouds from the Intel Real Sense cameras.
"""
#%% imports and path configuration
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
file_path = os.path.join("3d scan", "process_3d_files.py")

# Load the module manually to bypass the space in the folder name
spec = importlib.util.spec_from_file_location(module_name, file_path)
p3f = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p3f)

# import script used to generate the actual
gen_file_path = os.path.abspath(r"D:\Projects\3D-textures\Generator\Generator.py")

# We use importlib to handle the import, same as we did for the 3d scan folder
spec = importlib.util.spec_from_file_location("Generator", gen_file_path)
gen_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen_module)

#%% ==========================
# Processing
# ==========================

# path to a point cloud
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
    #o3d.visualization.draw_geometries([ply_obj1], window_name="3D Scan Result")
else:
    print("Failed to process the point cloud. Check if the path is correct.")


#%% ==========================
# Generate and Visualize z1 Surface
# ==========================

# Grab the math variables directly from the imported Generator module
# These were defined and calculated when the module was loaded
x_data = gen_module.x
y_data = gen_module.y
z1_data = gen_module.z1

# Use the modified surface_to_stl function to get a PointCloud object
# We pass filename=None so it returns the object instead of saving to disk
pcd_z1 = gen_module.surface_to_stl(x_data, y_data, z1_data, filename=None)

if pcd_z1 is not None:
    print(f"Generated PointCloud for z1. Number of points: {len(pcd_z1.points)}")
    
    # Visualize the result
    # This will open the Open3D window
    #o3d.visualization.draw_geometries([pcd_z1], window_name="Generator Texture: z1")
else:
    print("Failed to generate PointCloud for z1.")

#%% 1. Load the reference (STL)
# This returns an object directly
ref_obj = gen_module.surface_to_stl(gen_module.x, gen_module.y, gen_module.z1, filename=None)

# 2. Load and process the scan (PLY)
# path to a point cloud
ply_path1 = r"D:\Projects\3D-textures\processed_models\BAMBU\B1T2.ply"
# This returns an object directly
scan_obj = p3f.process_ply(ply_path1, rm_floor=True)

if ref_obj is not None and scan_obj is not None:
    # 3. Align the two objects directly
    # We set rm_floor=False here because process_ply already handled it
    aligned_ref, aligned_scan = p3f.align_ply_objects(ref_obj, scan_obj, rm_floor=False, scale=True)
    
    if aligned_ref is not None:
        # 4. Visualize
        o3d.visualization.draw_geometries([aligned_ref, aligned_scan], window_name="Surface Overlay")
        
        # 5. Calculate
        avg, std = p3f.calc(aligned_ref, aligned_scan)
        print(f"Average: {avg}, STD: {std}")

#%% load ref
ref_obj = gen_module.surface_to_stl(gen_module.x, gen_module.y, gen_module.z1, filename=None)
# load scan
ply_path1 = r"D:\Projects\3D-textures\processed_models\BAMBU\B1T2.ply"
scan_obj = p3f.process_ply(ply_path1, rm_floor=True)

# --- Visualisation 1: Raw comparison ---
# Paint them different colors so you can see the overlap/offset clearly
ref_obj.paint_uniform_color([1, 0, 0])  # Red
scan_obj.paint_uniform_color([0, 1, 0])  # Green
print("Showing Raw Comparison (Red: STL, Green: Scan)...")
o3d.visualization.draw_geometries([ref_obj, scan_obj])

# --- Next scale the scan according to the ref ---
# We use your helper function to fix the size difference
scaled_scan_obj = p3f.scale_pcd_to_reference(ref_obj, scan_obj)

# --- Visualisation 2: After scaling ---
# The green cloud should now be roughly the same size as the red cloud
scaled_scan_obj.paint_uniform_color([0, 1, 0]) 
print("Showing Scaled Comparison...")
o3d.visualization.draw_geometries([ref_obj, scaled_scan_obj])

# --- Next perform alignment ---
# We set rm_floor=False and scale=False because those steps are already complete
# align_ply_objects returns (ref_obj, aligned_scan)
ref_obj, aligned_scan = p3f.align_ply_objects(ref_obj, scaled_scan_obj, rm_floor=False, scale=False)

# --- Visualisation 3: Final Alignment ---
# The green cloud should now be "snapped" onto the red cloud
aligned_scan.paint_uniform_color([0, 1, 0])
print("Showing Final Alignment...")
o3d.visualization.draw_geometries([ref_obj, aligned_scan])

# Final step: Calculate metrics
avg, std = p3f.calc(ref_obj, aligned_scan)
print(f"Final Metrics -> Average Deviation: {avg:.4f}, STD: {std:.4f}")