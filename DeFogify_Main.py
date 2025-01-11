import cv2
import numpy as np
import gradio as gr
import tempfile
import os


# Core Image Processing Functions
def dark_channel(img, size=15):  # Dark Channel Estimation Function          
    r, g, b = cv2.split(img)
    min_img = cv2.min(r, cv2.min(g, b))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (size, size))
    dc_img = cv2.erode(min_img, kernel)
    return dc_img


def get_atmo(img, percent=0.001):
    flat_img = img.reshape(-1, img.shape[-1])
    indices = np.argsort(np.mean(flat_img, axis=1))
    top_indices = indices[-int(len(indices) * percent):]
    return np.mean(flat_img[top_indices], axis=0)


def get_trans(img, atom, w=0.95):
    normalized_img = img / atom
    t = 1 - w * dark_channel(normalized_img, 15)
    return t  # Transmission Map


def guided_filter(p, i, r, e):  # Guided Filter Function      
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
    return q  # Guided Filter Output


def dehaze(image):
    img = image.astype('float64') / 255
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype('float64') / 255

    atom = get_atmo(img)
    trans = get_trans(img, atom)
    trans_guided = guided_filter(trans, img_gray, 20, 0.0001)
    trans_guided = np.maximum(trans_guided, 0.25)

    result = np.empty_like(img)
    for i in range(3):
        result[:, :, i] = (img[:, :, i] - atom[i]) / trans_guided + atom[i]

    result = np.clip(result, 0, 1)
    return (result * 255).astype(np.uint8)  # Dehazed Image Output


# Define the correct folder path for the "Sample Images for Testing"
image_folder = "Sample Images for Testing"  # Adjust if needed
example_images = [
    os.path.join(image_folder, "ai-generated-9025430_1280.jpg"),
    os.path.join(image_folder, "meadow-5648849_1280.jpg"),
    os.path.join(image_folder, "mountains-7662717_1280.jpg"),
    os.path.join(image_folder, "mountains-8292685_1280.jpg"),
    os.path.join(image_folder, "nature-6722031_1280.jpg")
]

# Save Example Images for Gradio
example_paths = []  # List to store the paths of the example images for Gradio
for i, img_path in enumerate(example_images):
    if os.path.exists(img_path):  # Check if the image exists
        img = cv2.imread(img_path)
        save_path = os.path.abspath(f"example_image_{i+1}.png")  # Save with absolute path
        cv2.imwrite(save_path, img)
        example_paths.append([save_path])  # Add the path for Gradio examples
    else:
        print(f"Error: Image not found at {img_path}")  # Log error if file doesn't exist


# Gradio Interface for Single Image Dehazing
PixelDehazer = gr.Interface(
    fn=dehaze,
    inputs=gr.Image(type="numpy"),
    outputs="image",
    examples=example_paths,  # Attach the examples
    cache_examples=False,
    description="Upload a single image to remove haze."
)


# Batch Processing Function for Multiple Images
def process_images(files):
    temp_dir = tempfile.mkdtemp()
    output_files = []

    for file in files:  # Iterate over the uploaded files
        img = cv2.imread(file.name)
        if img is not None:
            dehazed_img = dehaze(img)
            output_path = os.path.join(temp_dir, os.path.basename(file.name))
            cv2.imwrite(output_path, dehazed_img)
            output_files.append(output_path)

    return output_files  # Return the paths of the processed images


# Gradio Interface for Batch Dehazing
BatchDehazer = gr.Interface(
    fn=process_images,
    inputs=gr.Files(label="Upload Multiple Images", file_types=["image"]),
    outputs=gr.Files(label="Download Dehazed Images"),
    description="Upload multiple images to remove haze. Download the processed dehazed images."
)


# Combined Gradio App
app = gr.TabbedInterface(
    [PixelDehazer, BatchDehazer],
    ["Single Image Dehazing", "Batch Image Dehazing"],
    title="DeFogify App"
)

# Main Execution
if __name__ == "__main__":
    app.launch()
