# 3D-textures

[![GitHub Stars](https://shields.io)](https://github.com)
[![Dataset](https://shields.io)](https://www.kaggle.com/datasets/dextershepherd/3d-printed-tactile-dataset-tactip-readings)
[![Data DOI](https://shields.io)](https://doi.org/10.25377/sussex.30256453)

A research repository containing 3D-printable and highly replicable texture blocks designed specifically for benchmarking artificial tactile sensors. 

This project explores how varying 3D printing parameters (such as filament types and printer models) impact the quality of physical textures, and evaluates how these deviations ultimately affect a machine learning tactile classifier. Physical validation is performed using a **TacTip** optical tactile sensor.

---

## Table of Contents
- [Project Overview](#-project-overview)
- [Repository Structure](#-repository-structure)
- [Texture Generation](#%EF%B8%8F-texture-generation)
- [Data & Experiments](#-data--experiments)
- [Friction Testing Rig](#-friction-testing-rig)
- [Citation & Funding](#-citation--funding)

---

## Project Overview

Benchmarking tactile sensors requires standardized, reproducible surface patterns. This framework parameters a 2D surface using 5 core mathematical parameters:
* Amplitudes along two directional axes
* Frequencies along two directional axes
* Phase shift between the directions

By compounding sine functions, we can programmatically generate complex repetitive shapes (e.g., squares, pyramids, waves, or protruded features). This simplifies sensor benchmarking by helping researchers pinpoint the exact minimum sine pattern threshold a specific tactile sensor can successfully resolve.

---

## Repository Structure

The repository is organized into the following primary directories:

```text
├── Generator/          # Source code to mathematically generate custom 3D texture blocks
├── objects/            # Pre-generated texture models in STL format
├── Experimental/       # Jupyter Notebooks and scripts for sensor validation and classification
├── Friction/           # Code for control and data collection via a physical friction testing rig
├── assets/             # Media and documentation images
├── .gitignore
├── README.md
└── movement_log.csv    # Baseline telemetry log for testing data
```

---

## Texture Generation

Under the `/Generator` folder, you will find scripts to create texture blocks from scratch. 
* All models are exported as standard **STL files** wrapped inside a solid base block.
* Models are strictly constrained to the **same uniform height** to ensure reliable physical experiments (i.e., allowing the tactile sensor to be lowered to an identical, repeatable relative depth for every single sample).

If you prefer not to generate them yourself, you can use the pre-compiled models provided directly in the `/objects` folder.

---

## Data & Experiments

We evaluate the interplay between physical manufacturing quality and algorithmic classification. 

### 1. Tactile Sensor Validation
We collect data using a **TacTip** tactile sensor to investigate how different hardware setups (filaments, nozzle profiles, printer brands) introduce surface artifacts and how those variations alter the classifier's performance.

### 2. Open Datasets
The datasets associated with this research are openly hosted across the following platforms:
* **Tactile Readings Dataset:** Access the sensor log matrices directly on [Kaggle](https://www.kaggle.com/datasets/dextershepherd/3d-printed-tactile-dataset-tactip-readings).
* **3D Printable Models Archive:** The exact generated benchmark STL shapes can be alternative-sourced or cited via [Sussex Figshare](https://doi.org/10.25377/sussex.30256453).

---

## Friction Testing Rig

To augment the geometric and visual data, the `/Friction` directory contains automation and logging code designed for a custom testing rig. This hardware configuration gathers the physical **coefficient of friction** for each 3D-printed texture block, providing cross-validation ground truth alongside the optical/tactile sensor profiles.

---

## Citation & Funding

If you use these texture generators, datasets, or experimental methodologies in your research, please cite the corresponding work:

```bibtex
@misc{shepherd2025tactile,
  author    = {Shepherd, Dexter and Herzig, Nicolas and Philippides, Andy and Husbands, Phil and Johnson, Chris},
  title     = {3D Printable Tactile Dataset},
  month     = {October},
  year      = {2025},
  publisher = {University of Sussex},
  doi       = {10.25377/sussex.30256453},
  url       = {https://doi.org/10.25377/sussex.30256453}
}
```

### Acknowledgments
This research was supported by the **be.AI scholarship** initiative.
