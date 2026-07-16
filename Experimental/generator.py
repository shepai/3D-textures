import os
import open3d as o3d
import numpy as np
from sklearn.cluster import DBSCAN


# ==========================
# SETTINGS
# ==========================

SOURCE_FOLDER = r"C:/Users/dexte/Documents/data/textures"
DESTINATION_FOLDER = r"C:/Users/dexte/Documents/data/processed_models"

DBSCAN_EPS = 0.005
DBSCAN_MIN_SAMPLES = 20
RADIUS = 0.04


# ==========================
# Processing Function
# ==========================

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


# ==========================
# Walk through folders
# ==========================

for root, dirs, files in os.walk(SOURCE_FOLDER):

    # Relative path from source
    relative = os.path.relpath(root, SOURCE_FOLDER)

    # Matching destination folder
    output_root = os.path.join(DESTINATION_FOLDER, relative)

    os.makedirs(output_root, exist_ok=True)

    for file in files:

        if file.lower().endswith(".ply"):

            input_file = os.path.join(root, file)
            output_file = os.path.join(output_root, file)

            process_ply(input_file, output_file)

print("/nFinished!")