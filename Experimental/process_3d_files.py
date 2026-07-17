import os
import open3d as o3d
import numpy as np
from sklearn.cluster import DBSCAN


# ==========================
# SETTINGS
# ==========================
DBSCAN_EPS = 0.005
DBSCAN_MIN_SAMPLES = 20
RADIUS = 0.04

# ==========================
# Alignment Function
# ==========================

def align(file_path1, file_path2):
    """Load two point clouds, remove floors, align using Point-to-Point ICP, and visualise."""
    try:
        # Load point clouds
        pcd1 = o3d.io.read_point_cloud(file_path1)
        pcd2 = o3d.io.read_point_cloud(file_path2)

        if len(pcd1.points) == 0 or len(pcd2.points) == 0:
            print(f"Error: One of the alignment files is empty. PCD1: {len(pcd1.points)}, PCD2: {len(pcd2.points)}")
            return None

        # Inner helper to remove floor
        def remove_floor(pcd):
            plane_model, inliers = pcd.segment_plane(
                distance_threshold=0.002, 
                ransac_n=3,
                num_iterations=5000
            )
            return pcd.select_by_index(inliers, invert=True)

        # Clean floor elements
        obj1 = remove_floor(pcd1)
        obj2 = remove_floor(pcd2)

        # Base downsample settings
        voxel_size = 0.005

        # Multi-stage gates: Fix coarse angle tweaks, then clamp down tight.
        stages = [
            {"voxel": voxel_size * 2, "thresh": 0.040},  # Loose search gate
            {"voxel": voxel_size * 1, "thresh": 0.015},  # Medium search gate
            {"voxel": voxel_size * 0.5, "thresh": 0.004} # Tight sub-millimetre lock
        ]

        # Natural close start position means initial guess is an Identity Matrix
        current_transformation = np.identity(4)

        print(f"\nRunning ICP alignment between:\n  1: {file_path1}\n  2: {file_path2}")
        for i, stage in enumerate(stages):
            s_obj1 = obj1.voxel_down_sample(stage["voxel"])
            s_obj2 = obj2.voxel_down_sample(stage["voxel"])
            
            # PointToPoint avoids plane-sliding or rotation drift on flatter geometries
            result = o3d.pipelines.registration.registration_icp(
                source=s_obj2,
                target=s_obj1,
                max_correspondence_distance=stage["thresh"],
                init=current_transformation,
                estimation_method=o3d.pipelines.registration.TransformationEstimationPointToPoint(False)
            )
            current_transformation = result.transformation

        print("Alignment Complete.")
        
        # Apply alignment matrix to original full-resolution source cloud (obj2)
        obj2.transform(current_transformation)

        # Colorize for explicit visual confirmation
        obj1.paint_uniform_color([1, 0, 0])  # Red (Target reference)
        obj2.paint_uniform_color([0, 1, 0])  # Green (Aligned source)

        # Visualise
        print("Opening 3D viewer window...")
        #o3d.visualization.draw_geometries([obj1, obj2])
        
        return obj1,obj2

    except Exception as e:
        print(f"Alignment execution failed: {e}")
        return None


def calc(obj1, obj2):
    """
    Calculates the average distance and standard deviation between 
    the nearest points of two point clouds.
    
    Parameters:
    obj1 (open3d.geometry.PointCloud): The reference point cloud (Target)
    obj2 (open3d.geometry.PointCloud): The aligned point cloud (Source)
    
    Returns:
    tuple: (average_distance, standard_deviation)
    """
    if len(obj1.points) == 0 or len(obj2.points) == 0:
        print("Warning: One of the input point clouds is empty.")
        return 0.0, 0.0

    # Compute distances from every point in obj1 to its nearest neighbor in obj2
    distances = obj1.compute_point_cloud_distance(obj2)
    
    # Convert the Open3D DoubleVector to a standard NumPy array
    dist_array = np.asarray(distances)
    
    # Calculate metrics
    avg_distance = np.mean(dist_array)
    std_dev = np.std(dist_array)
    
    return avg_distance, std_dev

def process_ply(input_file, output_file):
    """Load, clean, centre and save a point cloud."""

    try:
        pcd = o3d.io.read_point_cloud(input_file)

        points = np.asarray(pcd.points)

        if len(points) == 0:
            print(f"Skipping empty cloud: {input_file}")
            return

        colours = np.asarray(pcd.colors)

        # ----------------------
        # DBSCAN clustering
        # ----------------------

        clustering = DBSCAN(
            eps=DBSCAN_EPS,
            min_samples=DBSCAN_MIN_SAMPLES
        ).fit(points)

        labels = clustering.labels_

        valid = labels != -1

        if not np.any(valid):
            print(f"No valid cluster found: {input_file}")
            return

        clusters = labels[valid]

        largest_cluster = np.argmax(np.bincount(clusters))

        mask = labels == largest_cluster

        object_points = points[mask]

        if len(colours):
            object_colours = colours[mask]
        else:
            object_colours = None

        # ----------------------
        # Centre
        # ----------------------

        centre = np.median(object_points, axis=0)

        centred_points = object_points - centre

        # ----------------------
        # Radius crop
        # ----------------------

        distances = np.linalg.norm(centred_points, axis=1)

        radius_mask = distances <= RADIUS

        centred_points = centred_points[radius_mask]

        if object_colours is not None:
            object_colours = object_colours[radius_mask]

        # ----------------------
        # Save
        # ----------------------

        output_pcd = o3d.geometry.PointCloud()
        output_pcd.points = o3d.utility.Vector3dVector(centred_points)

        if object_colours is not None:
            output_pcd.colors = o3d.utility.Vector3dVector(object_colours)

        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        o3d.io.write_point_cloud(output_file, output_pcd)

        print(f"Processed: {input_file}")

    except Exception as e:
        print(f"Failed: {input_file}")
        print(e)
if __name__=="__main__":
    texture=np.random.randint(1,5)
    obj1,obj2=align("C:/Users/dexte/Documents/data/processed_models/RESIN/R"+str(texture)+"T1.ply",
                    "C:/Users/dexte/Documents/data/processed_models/RESIN/R"+str(texture)+"T2.ply")
    av,std=calc(obj1,obj2)
    print("Average:",av,"STD:",std)