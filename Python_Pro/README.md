# Simple Image Processing Tool

A web-based tool for basic image processing tasks with an easy-to-use interface.

## Tasks Implemented

1. **Reduce Intensity Levels**: Convert images from 256 levels to fewer levels (2, 4, 8, etc.)
2. **Spatial Averaging**: Blur images using different size filters (3×3, 10×10, 20×20)
3. **Image Rotation**: Rotate images by 45° and 90°
4. **Block Averaging**: Reduce spatial resolution by averaging pixel blocks (3×3, 5×5, 7×7)

## How to Run

### Quick Start

1. Install requirements:

   ```
   pip install -r requirements.txt
   ```

2. Start the app:

   ```
   python app.py
   ```

3. Open in browser:
   ```
   http://127.0.0.1:5000
   ```

### Using the Web Interface

1. Upload an image
2. Select one of the four operations
3. For intensity reduction, choose the number of levels
4. Click "Process Image"
5. View and compare the results

## Running Individual Scripts

Each task has its own script that can be run directly:# Computer Vision and Image Processing - Assignment 1

This repository contains the implementation of various image processing techniques as part of the EC7212 Computer Vision and Image Processing course assignment.

## Overview

The assignment demonstrates the application of fundamental image processing operations:

1. **Intensity Level Reduction**: Reducing the number of intensity levels in grayscale images from 256 to lower powers of 2
2. **Spatial Averaging**: Applying average filtering with different kernel sizes (3×3, 10×10, and 20×20)
3. **Image Rotation**: Rotating images by 45° and 90°
4. **Resolution Reduction**: Replacing non-overlapping blocks with their average values for varying block sizes

## Contents

- `assignment1.ipynb`: Jupyter notebook containing all implementations
- Image files:
  - `chipmunk.png`
  - `flycatcher.jpg`
  - `giraffe.png`
  - `lone-tree.png`
  - `parrot.png`
  - `tiger.png`

## How to Use

1. Open the `assignment1.ipynb` notebook in Jupyter or VS Code
2. Update the image path in the notebook to point to one of the provided images
3. Run the cells to see the effects of various image processing operations
4. Use the interactive widgets to experiment with different parameters

## Requirements

- Python 3.x
- OpenCV (cv2)
- NumPy
- Matplotlib
- ipywidgets (for interactive elements)

## Results

The notebook generates visual comparisons between original images and their processed versions, allowing for easy analysis of each technique's effects on image quality and appearance.

```
python intensity_reducer.py image.jpg 8    # Reduce to 8 intensity levels
python spatial_averager.py image.jpg 3     # Apply 3×3 spatial average
python image_rotator.py image.jpg 45       # Rotate by 45 degrees
python block_averager.py image.jpg 3       # 3×3 block average
```

```
python intensity_reducer.py input.jpg 8
python spatial_averager.py input.jpg 3
python image_rotator.py input.jpg 45
python block_averager.py input.jpg 3
```
