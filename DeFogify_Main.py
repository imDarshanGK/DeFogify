import cv2
import numpy as np
import gradio as gr
import tempfile
import os

# Original Functions (Unchanged)
def dark_channel(img, size=15):
    """
    Compute the dark channel prior for an image.
    """
    r, g, b = cv2.split(img)
    min_img = cv2.min(r, cv2.min(g, b))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (size, size))
    dc_img = cv2.erode(min_img, kernel)
    return dc_img

def get_atmo(img, percent=0.001):
    """
    Estimate the atmospheric light in the image.
    """
    mean_perpix = np.mean(img, axis=2).reshape(-1)
    mean_topper = mean_perpix[:int(img.shape[0] * img.shape[1] * percent)]
    return np.mean(mean_topper)

def get_trans(img, atom, w=0.95):
    """
    Compute the transmission map of the image.
    """
    x = img / atom
    t = 1 - w * dark_channel(x, 15)
    return t

def guided_filter(p, i, r, e):
    """
    Apply a guided filter to the transmission map.
    """
    mean_I = cv2.boxFilter(i, cv2.CV_64F, (r, r))
    mean_p = cv2.boxFilter(p, cv2.CV_64F, (r, r))
    corr_I = cv2.boxFilter(i * i, cv2.CV_64F, (r, r))
    corr_Ip = cv2.boxFilter(i * p, cv2.CV_64F, (r, r))
    var_I = corr_I - mean_I * mean_I
    cov_Ip = corr_Ip - mean_I * mean_p
    a = cov_Ip / (var_I + e)
    b = mean_p - a * mean_I
    mean_a = cv2.boxFilter(a, cv2.CV_64F, (r, r))
    mean_b = cv2.boxFilter(b, cv2.CV_64F, (r, r))
    q = mean_a * i + mean_b
    return q

def dehaze(image):
    """
    Perform image dehazing using the dark channel prior.
    """
    img = image.astype('float64') / 255
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype('float64') / 255

    atom = get_atmo(img)
    trans = get_trans(img, atom)
    trans_guided = guided_filter(trans, img_gray, 20, 0.0001)
    trans_guided = np.maximum(trans_guided, 0.25) # Ensure trans_guided is not below 0.25

    result = np.empty_like(img)
    for i in range(3):
        result[:, :, i] = (img[:, :, i] - atom) / trans_guided + atom

    result = np.clip(result, 0, 1)
    return (result * 255).astype(np.uint8)

# Batch Processing Function for Multiple Images
def process_images(files):
    """
    This function processes multiple images using the `dehaze` function
    and saves the dehazed images to a temporary folder.
    """
    temp_dir = tempfile.mkdtemp()  # Create temporary directory to store output images
    output_files = []  # List to store output file paths

    for file in files:  # Loop over each file
        img = cv2.imread(file.name)
        if img is not None:
            dehazed_img = dehaze(img)  # Apply dehazing
            output_path = os.path.join(temp_dir, os.path.basename(file.name))
            cv2.imwrite(output_path, dehazed_img)  # Save the dehazed image
            output_files.append(output_path)  # Add the output file path to the list

    return output_files  # Return the list of output file paths

# Example Images for Testing (No changes needed)
example_images = [
    "Sample Images for Testing/ai-generated-9025430_1280.jpg",
    "Sample Images for Testing/meadow-5648849_1280.jpg",
    "Sample Images for Testing/mountains-7662717_1280.jpg",
    "Sample Images for Testing/mountains-8292685_1280.jpg",
    "Sample Images for Testing/nature-6722031_1280.jpg"
]

# Save Example Images for Gradio (Ensuring paths are correct)
example_paths = []
for i, img_path in enumerate(example_images):
    img = cv2.imread(img_path)
    save_path = f"example_image_{i+1}.png"
    cv2.imwrite(save_path, img)
    example_paths.append([save_path])

# Gradio Interface for Single Image Dehazing
PixelDehazer = gr.Interface(
    fn=dehaze,
    inputs=gr.Image(type="numpy"),
    outputs="image",
    examples=example_paths,
    cache_examples=False,
    description="Upload a single image to remove haze."
)

# Gradio Interface for Batch Dehazing
BatchDehazer = gr.Interface(
    fn=process_images,
    inputs=gr.Files(label="Upload Multiple Images", file_types=["image"]),
    outputs=gr.Files(label="Download Dehazed Images"),
    description="Upload multiple images to remove haze. Download the processed dehazed images."
)

# Combined Gradio App with Tabs for Single and Batch Image Processing
app = gr.TabbedInterface(
    [PixelDehazer, BatchDehazer],
    ["Single Image Dehazing", "Batch Image Dehazing"],
    title="DeFogify App"
)

# Launch the Gradio App
if __name__ == "__main__":
    app.launch()
