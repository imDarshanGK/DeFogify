## Overview

This project implements a single-image haze removal technique using the Dark Channel Prior, as described in the research paper: [Single Image Haze Removal Using Dark Channel Prior](https://ieeexplore.ieee.org/document/5567108). The dehazing algorithm is designed to enhance the quality of images affected by haze, making it ideal for various applications in image processing where haze reduction is required.

## Features

- **Single Image Processing:** Effective haze removal for individual images.
- **Dark Channel Prior Algorithm:** Implements a robust algorithm for haze reduction.
- **High-Quality Results:** Outputs visually appealing dehazed images.
- **Efficient Processing:** Suitable for real-time and batch processing with optimization.

## Demo

### Before and After Examples

| Original Image | Dehazed Image |
|----------------|---------------|
| <img src="https://github.com/user-attachments/assets/efe6e3c9-2d50-43d8-9218-beb2dbd9fd83" height="300"> | <img src="https://github.com/user-attachments/assets/657268d3-7c28-4c13-ad85-c97fdf1fa2e0" height="300"> |
| <img src="https://github.com/user-attachments/assets/e16e378c-7ebd-4dff-8d6b-d9aef5ab644f" height="300"> | <img src="https://github.com/user-attachments/assets/ac08593d-2579-4496-bb64-a9b48ed7b4d4" height="300"> |
| <img src="https://github.com/user-attachments/assets/870fcd06-28ac-4c15-b5c2-03e05f515321" height="300"> | <img src="https://github.com/user-attachments/assets/e898ee3f-662a-441a-b38f-2362291931df" height="300"> |

## Live Demo

Try the dehazing app live on Hugging Face:

[Visit DeFogify in 🤗 space](https://huggingface.co/spaces/MLap/deFogify)

## Installation

Ensure you have the required Python packages installed. Dependencies are listed in the `requirements.txt` file.

To install the required packages, use:

```bash
pip install -r requirements.txt
```

## Usage Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo-url
   cd your-repo-folder
   ```
2. Place the input image(s) in the specified input directory.
3. Run the script to dehaze images:
   ```bash
   python dehaze.py --input_dir ./input --output_dir ./output
   ```
4. The dehazed images will be saved in the output directory.

## Algorithm Overview

The Dark Channel Prior algorithm is based on the observation that in most non-sky patches of a haze-free image, at least one color channel has some pixels with very low intensity. Using this prior, the algorithm estimates the haze transmission map and reconstructs the image by removing the estimated haze effect.

### Steps:
1. Estimate the dark channel of the image.
2. Compute the atmospheric light using the brightest pixels.
3. Calculate the transmission map.
4. Refine the transmission map using guided filtering.
5. Recover the scene radiance using the transmission map and atmospheric light.

## Known Issues

- The algorithm may struggle with extreme haze conditions.
- Artifacts might appear in areas with very low contrast or uniform color.

## Future Work

- **Video Dehazing:** Extend support for video processing.
- **Parameter Tuning:** Add more configurable parameters for user customization.
- **Performance Optimization:** Improve speed for real-time applications.
- **Integration:** Combine with other image enhancement techniques for better results.

## Example Dataset

Test the algorithm using these benchmark datasets:

- [RESIDE Dataset](https://sites.google.com/view/reside-dehaze-datasets)
- [Middlebury Stereo Dataset](http://vision.middlebury.edu/stereo/)


## Credits

- Algorithm inspired by the research paper: [Single Image Haze Removal Using Dark Channel Prior](https://ieeexplore.ieee.org/document/5567108).
- Special thanks to contributors and collaborators for their support.



