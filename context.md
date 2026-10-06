## 📝 Current Work & Goals
**Overall Goal:** To develop a robust pipeline that compares 3D scans (PLY/Point Clouds) against CAD templates (STL) to quantify physical manufacturing deviations.

**Current Priority:** 
Achieving high-fidelity alignment between the "Source" (the scan) and the "Target" (the STL). We are currently tuning the multi-stage ICP parameters to ensure that the scan "snaps" perfectly onto the reference model, ensuring that the resulting `avg` and `std` metrics accurately reflect surface texture/printing errors rather than orientation or scale offsets.

## 🧠 Knowledge Base & Conventions
*   **Branch Context:** We are working in a dedicated branch for the Scan-to-CAD comparison engine.
*   **Color Coding:** 
    *   **Red:** Reference Model (Target/STL)
    *   **Green:** Captured Scan (Source/PLY)
*   **Coordinate Systems:** Open3D defaults to meters; STL files are often in millimeters. The pipeline must account for these unit discrepancies.
*   **Optimization Strategy:** We use a **"Coarse-to-Fine"** ICP approach.
    *   *Loose Gate:* Broad search to "grab" the object.
    *   *Medium Gate:* Refines the general position.
    *   *Tight Gate:* Sub-millimeter lock-in for high-precision surface matching.
*   **Data Handling:** We prioritize "Surface vs. Surface" comparison. We ignore the "solid" thickness of the STL to focus on the printed surface geometry.

## 📅 Progress Log

**[Current Phase] Alignment Calibration & Debugging**
*   Identified that the multi-stage ICP "gates" need fine-tuning; currently investigating if the "Loose" search threshold is wide enough to overcome large rotation/translation offsets from the camera.

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

## 🚀 Next Steps

**1. ICP Parameter Tuning**
*   Experiment with wider `thresh` values for the "Loose" gate (e.g., 0.080 or 0.100) to determine if the camera's physical distance from the object is preventing the initial "grab."
*   Iteratively shrink the "Tight" gate to see the point of failure for sub-millimeter precision.

**2. Global Registration Research**
*   If the camera angle remains too varied, investigate **Global Registration** (like FPFH features) to find a better "Initial Guess" than `np.identity(4)`.

**3. Validation of Metrics**
*   Once visual alignment is achieved, cross-reference the `avg` and `std` values with the known 3D printer layer height (e.g., 0.2mm) to ensure the math is interpreting the "ripples" correctly.

**4. Unit Consistency Check**
*   Verify if a 1000x difference exists between the STL units and RealSense output, and standardize the pipeline to a single unit (mm) at the start of the process.

**5. Rework align function**
*   Test difference approaches for aligning.
