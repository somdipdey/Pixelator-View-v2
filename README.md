# Pixelator v2 - Perceptual Image Comparison

Pixelator v2 is an advanced image comparison tool that integrates pixel-wise RGB analysis, perceptual relevance via the CIE-LAB colour space, and structural integrity detection using Sobel filters. It outperforms traditional methods like MSE, SSIM, and LPIPS by offering a robust and computationally efficient method to detect both subtle pixel-level changes and perceptually significant modifications.

## Features
- Combines RGB pixel-level analysis with perceptual analysis using the CIE-LAB colour space.
- Incorporates Sobel edge detection for enhanced structural comparison.
- Optimized for various applications, including image security and tamper detection.
  
## Requirements
Before running Pixelator v2, make sure the following dependencies are installed on your system:

### Dependencies
- **Python 3.x** (Make sure you have Python 3.7+)
- **NumPy** - For numerical operations
- **OpenCV** - For image manipulation
- **scikit-image** - For advanced image processing techniques
- **Matplotlib** - For visualizing the output (optional, for plotting)

You can install the required dependencies by running:

```bash
pip install numpy opencv-python scikit-image matplotlib
```

## Installation
Clone the repository to your local machine:

```bash
git clone https://github.com/somdipdey/Pixelator-View-v2.git
cd Pixelator-View-v2
```

## Running Pixelator v2

To run the Pixelator v2 code, follow the steps below:

Navigate to the cloned repository directory.
Run the Python script:

```bash
python pixelatorv2.py [Image 1] [Image 2]
```

## Example Usage

To compare two images, simply call the pixelatorv2.py script with the paths to the images as arguments. Example:

```bash
python pixelatorv2.py /path/to/image1.jpg /path/to/image2.jpg
```
