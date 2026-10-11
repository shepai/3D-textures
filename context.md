## 📝 Current Work & Goals
**Overall Goal:** To develop a robust pipeline that compares 3D scans (PLY/Point Clouds) against CAD templates (STL) to quantify physical manufacturing deviations.

**Current Priority:** 
Automated Batch Processing & Metadata Aggregation. We have moved from individual file analysis to a global loop that processes all folders within the project structure. The focus is now on ensuring accurate metadata extraction (Printer type, "Standards" status, Texture Index, Test Number) and aggregating results into a structured Pandas DataFrame for high-level analysis.

## 🧠 Knowledge Base & Conventions
*   **Branch Context:** We are working in a dedicated branch for the Scan-to-CAD comparison engine.
*   **Color Coding:** 
    *   **Red:** Reference Model (Target/STL)
    *   **Green:** Captured Scan (Source/PLY)
*   **Coordinate Systems:** Scan point clouds are in mm. STL point clouds are in metres.
*   **Optimization Strategy:** We use a **"Coarse-to-Fine"** ICP approach.
    *   *Loose Gate:* Broad search to "grab" the object.
    *   *Medium Gate:* Refines the general position.
    *   *Tight Gate:* Sub-millimeter lock-in for high-precision surface matching.
*   **Data Handling:** We prioritize "Surface vs. Surface" comparison. We ignore the "solid" thickness of the STL to focus on the printed surface geometry.
*   **Naming Conventions & Metadata:**
    *   **Files:** Named as `[Printer][Texture]T[TestNo].ply` (e.g., `B1T2.ply` $\rightarrow$ Texture 1, Test 2).
    *   **Folder Structure:** `processed_models/[Printer]` or `processed_models/[Printer] STANDARDS`.
    *   **Extraction Logic:** The system dynamically maps `z_data` from the generator using the texture index from the filename and automatically flags "Standards" folders as boolean values.
*   **File Locations:**
    *   **Analysis:** `Experimental/scan_comparison/scan_comp_analysis.ipynb`
    *   **Comparison Engine:** `Experimental/scan_comparison/stl_to_scan_comp.ipynb`
    *   **Master Results:** `Experimental/scan_comparison/scan_comp_master_results.csv`
    *   **Final Filtered Results:** `Experimental/scan_comparison/final_comp_result_under1.5.csv`

## 📅 Progress Log

**[Current Phase] Batch Processing & Automated Evaluation**
*   Implemented a global iteration script to process all subfolders in `SCANS_LOC`.
*   Developed a dynamic mapping system using `getattr` to fetch the correct `z_data` for STL generation based on filename characters.
*   Implemented automated Quality Control (QC): Results are automatically flagged as `aligned` if the average deviation is below a defined threshold (currently 1.2mm).
*   **Refined Analysis Pipeline:** 
    *   Implemented a filter to exclude results with `avg_dist > 1.5mm` to remove outliers from high-level stats.
    *   Grouped results by `printer`, `stl_texture`, and `standards` flag to enable "Standard vs. Non-Standard" comparison.
    *   Calculated Mean and Standard Error (SE) rounded to 3 decimal places.
    *   Exporting to `final_comp_result_under1.5.csv`.

**[Previous Phase] Scaling & Registration Engine**
*   Implemented `scale_pcd_to_reference`: Added logic to calculate a dynamic scale factor by comparing bounding box dimensions (Width, Height, Depth).
*   Implemented Median Ratio Scaling: Used the median of the dimension ratios to prevent 1D axis collapse from skewing the scale factor.
*   Implemented Multi-Stage ICP: Transitioned from single-pass ICP to a 3-stage pipeline (Loose, Medium, Tight) to handle the "Identity Trap."

**[Previous Phase] Data Preprocessing & Architecture**
*   Architecture Fix: Implemented `importlib` pattern to handle modules inside folders with spaces (e.g., `3d scan`).
*   Preprocessing Pipeline: Integrated RANSAC plane segmentation (`remove_floor`) to isolate objects from the table surface.
*   Clustering: Implemented DBSCAN to isolate the primary object from noise/background.
*   Normalization: Added automatic centering and radius cropping for consistent "comparison boxes."

**[Previous Phase] Logic & Strategy Definition**
*   The "Surface vs. Surface" Pivot: Corrected the logic to ensure we aren't comparing a solid block STL to a surface scan, which would produce false-positive thickness errors.
*   Identified 50x scale discrepancy between RealSense point clouds and CAD models.
