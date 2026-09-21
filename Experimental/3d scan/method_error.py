import os
import re
import open3d as o3d
import numpy as np
import pandas as pd
from process_3d_files import * # Adjust this import to your actual file/function name

# ==========================
# SETTINGS
# ==========================
SOURCE_FOLDER = r"/home/dexter/Documents/data/processed_models"

# Regex to parse: A1B2.ply
FILE_PATTERN = re.compile(r"^([A-Za-z])(\d+)([A-Za-z])(\d+)\.ply$", re.IGNORECASE)

# Storage dictionaries
experimental_data = {}
standards_data = {}

# ==============================================================================
# STEP 1: SCAN, PARSE, AND SEPARATE STANDARDS FROM EXPERIMENTS
# ==============================================================================
print("Scanning directories and classifying files...")

for root, dirs, files in os.walk(SOURCE_FOLDER):
    # Detect if this folder belongs to a standard run
    is_standard = "STANDARDS" in root.upper()
    
    for file in files:
        if file.lower().endswith(".ply"):
            match = FILE_PATTERN.match(file)
            if match:
                printer, texture, test_type, test_num = match.groups()
                group_key = (printer.upper(), texture)
                test_key = test_type.upper()
                full_path = os.path.join(root, file)
                
                # Pick target dictionary based on folder location
                target_dict = standards_data if is_standard else experimental_data
                
                if group_key not in target_dict:
                    target_dict[group_key] = {}
                if test_key not in target_dict[group_key]:
                    target_dict[group_key][test_key] = []

                target_dict[group_key][test_key].append((int(test_num), full_path))
# ==============================================================================
# STEP 2: CALCULATE SYSTEM METRIC ERRORS (STANDARDS)
# ==============================================================================
print("\n--- Calculating Baseline Method Errors (From Standards Folders) ---")
# { texture: [list of distances found on identical blocks] }

# ==============================================================================
# STEP 3: RUN EXPERIMENTAL ALIGNMENT & SUBTRACT METHOD ERROR
# ==============================================================================
print("\n--- Processing Experimental Trials ---")
results_list = []

for (printer, texture), tests in standards_data.items():
    # Fetch the custom method error calculated for this specific texture profile
    # Defaults to 0.0 if no standards files existed for this texture pattern
    for test_key, file_list in tests.items():
        file_list.sort(key=lambda x: x[0])
        if len(file_list) < 2:
            print(f"Skipping {printer}{texture}{test_key}: Under 2 files available.")
            continue
            
        for i in range(len(file_list) ):
            num1, path1 = file_list[i]
            for j in range(len(file_list)):
                if i!=j:
                    num2, path2 = file_list[j]
                    try:
                        name1 = os.path.basename(path1)
                        name2 = os.path.basename(path2)
                        
                        target_pcd, aligned_src_pcd = align(path1, path2)
                        avg_dist, std_dev = calc(target_pcd, aligned_src_pcd)

                        
                        results_list.append({
                            "Printer": printer,
                            "Texture": texture,
                            "Test_Type": test_key,
                            "Comparison": f"{num1} vs {num2}",
                            "Raw_Avg_Distance": avg_dist,
                            "Std_Deviation": std_dev,
                        })
                        
                    except Exception as e:
                        print(f"Failed to process experimental pair {name1} and {name2}: {e}")

# ==============================================================================
# STEP 4: BUILD PANDAS DATAFRAME
# ==============================================================================

df = pd.DataFrame(results_list)

print("\n--- Complete Processing Complete! Data Summary Table ---")
if not df.empty:
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    print(df.to_string(index=False))
    numeric_cols = df.select_dtypes(include="number").columns

    for col in numeric_cols:
        df[col] = df[col].map(lambda x: f"{x:.8f}")
    # Save output to disk
    df.to_csv("/home/dexter/Documents/GitHub/3D-textures/assets/experimental_method_results.csv", index=False)
    print("\nSaved output table successfully to 'experimental_corrected_results.csv'")
else:
    print("No matching experimental pairs were compiled.")
