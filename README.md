## Overview

This project implements a single-image haze removal technique using the Dark Channel Prior, as described in the research paper: ``Single Image Haze Removal Using Dark Channel Prior``
The dehazing algorithm is designed to enhance the quality of images affected by haze. This method is effective for various applications in image processing where haze reduction is required.

## [Research Paper](https://ieeexplore.ieee.org/document/5567108)

## Introduction

Haze removal is essential for enhancing image clarity and visibility in outdoor scenes, improving the performance of vision-based applications.

## Features

- **Single Image Dehazing**  
  Process one image at a time to remove haze and bring out hidden details using the Dark Channel Prior.
- **Bulk Image Dehazing**  
  Process multiple images simultaneously. This feature is perfect for efficiently dehazing an entire batch of images.
- **Video Dehazing**  
  Dehaze video files by processing each frame individually to ensure a clear and detailed output even for moving visual content.





### Before and After Examples

| Original Image | Dehazed Image |
|----------------|---------------|
| <img src="https://github.com/user-attachments/assets/efe6e3c9-2d50-43d8-9218-beb2dbd9fd83" height="300"> | <img src="https://github.com/user-attachments/assets/657268d3-7c28-4c13-ad85-c97fdf1fa2e0" height="300"> |
| <img src="https://github.com/user-attachments/assets/e16e378c-7ebd-4dff-8d6b-d9aef5ab644f" height="300"> | <img src="https://github.com/user-attachments/assets/ac08593d-2579-4496-bb64-a9b48ed7b4d4" height="300"> |
| <img src="https://github.com/user-attachments/assets/870fcd06-28ac-4c15-b5c2-03e05f515321" height="300"> | <img src="https://github.com/user-attachments/assets/e898ee3f-662a-441a-b38f-2362291931df" height="300"> |

## Live Demo

Try the dehazing app live at ``Hugging Face``:

[Visit DeFogify in 🤗 space](https://huggingface.co/spaces/MLap/deFogify)

## Installation

Ensure you have the required Python packages installed. Dependencies are listed in the `requirements.txt` file.

To install the required packages, use:

```bash
pip install -r requirements.txt
```

For Ubuntu/Debian-based systems, also install:

```bash
sudo apt-get update
sudo apt-get install libgl1-mesa-glx
```



