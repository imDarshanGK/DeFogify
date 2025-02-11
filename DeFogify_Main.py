import cv2
import numpy as np
import gradio as gr
import tempfile
import os
from tqdm import tqdm

# Original Functions
def dark_channel(img, size=15):
    r, g, b = cv2.split(img)
    min_img = cv2.min(r, cv2.min(g, b))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (size, size))
    dc_img = cv2.erode(min_img, kernel)
    return dc_img

def get_atmo(img, percent=0.001):
    mean_perpix = np.mean(img, axis=2).reshape(-1)
    mean_topper = mean_perpix[:int(img.shape[0] * img.shape[1] * percent)]
    return np.mean(mean_topper)

def get_trans(img, atom, w=0.95):
    x = img / atom
    t = 1 - w * dark_channel(x, 15)
    return t

def guided_filter(p, i, r, e):
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
    img = image.astype('float64') / 255
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype('float64') / 255
    atom = get_atmo(img)
    trans = get_trans(img, atom)
    trans_guided = guided_filter(trans, img_gray, 20, 0.0001)
    trans_guided = np.maximum(trans_guided, 0.25)  # Ensure trans_guided is not below 0.25
    result = np.empty_like(img)
    for i in range(3):
        result[:, :, i] = (img[:, :, i] - atom) / trans_guided + atom
    result = np.clip(result, 0, 1)
    return (result * 255).astype(np.uint8)

# Single Image Processing
def process_single_image(image):
    dehazed_img = dehaze(image)
    return dehazed_img

# Batch Processing Function for Multiple Images with Progress Bar
def process_images(files):
    temp_dir = tempfile.mkdtemp()
    output_files = []
    
    for file in tqdm(files, desc="Processing Images"):
        img = cv2.imread(file.name)
        if img is not None:
            dehazed_img = dehaze(img)
            output_path = os.path.join(temp_dir, os.path.basename(file.name))
            cv2.imwrite(output_path, dehazed_img)
            output_files.append(output_path)
    
    return output_files

# Video Dehazing Function with Gradio Progress Bar and Error Handling
def dehaze_video(input_video_path, output_video_path, progress=None):
    try:
        cap = cv2.VideoCapture(input_video_path)
        if not cap.isOpened():
            raise ValueError("Error: Could not open video.")

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if total_frames <= 0:  # Assume a constant count for webcam scenarios
            total_frames = 1000

        out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))
        frame_count = 0

        if progress is not None:
            progress(0, desc="Processing Video", unit="frame")

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            dehazed_frame = dehaze(frame)
            out.write(dehazed_frame)
            frame_count += 1

            if progress is not None:
                progress(frame_count / total_frames)  # Ensure progress is within 0-1 range

        cap.release()
        out.release()
        print(f"\nDehazed video saved to: {output_video_path}")
    except Exception as e:
        print(f"An error occurred during video processing: {e}")

# Gradio Video Processing Wrapper
def process_video(file):
    input_video_path = file  # File is a string representing the path
    output_video_path = os.path.join(tempfile.mkdtemp(), "dehazed_video.mp4")
    progress = gr.Progress()
    dehaze_video(input_video_path, output_video_path, progress)
    return output_video_path

# Real-Time Webcam Processing with Gradio Progress Bar
def dehaze_webcam(progress=gr.Progress()):
    try:
        cap = cv2.VideoCapture(0)  # Capture from the first webcam
        if not cap.isOpened():
            raise ValueError("Unable to open webcam")

        frame_count = 0
        total_frames = 100  # Arbitrary number for progress bar
        progress(0, desc="Processing Webcam Feed", unit="frame")

        while frame_count < total_frames:
            ret, frame = cap.read()
            if not ret:
                break
            dehazed_frame = dehaze(frame)
            frame_count += 1
            progress(frame_count / total_frames)  # Ensure progress is within 0-1 range

            cv2.imshow('Dehazed Webcam Feed', dehazed_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        progress(1)  # Ensure progress bar reaches 100%
    except Exception as e:
        print(f"An error occurred during webcam processing: {e}")

# Gradio Webcam Processing Wrapper
def process_webcam():
    progress = gr.Progress()
    dehaze_webcam(progress)
    return "Webcam processing completed."

# Example Images for Testing
example_images = [
    "Sample Images for Testing/ai-generated-9025430_1280.jpg",
    "Sample Images for Testing/meadow-5648849_1280.jpg",
    "Sample Images for Testing/mountains-7662717_1280.jpg",
    "Sample Images for Testing/nature-6722031_1280.jpg"
]

example_paths = []
for i, img_path in enumerate(example_images):
    img = cv2.imread(img_path)
    save_path = f"example_image_{i+1}.png"
    cv2.imwrite(save_path, img)
    example_paths.append([save_path])

# Gradio Interfaces
PixelDehazer = gr.Interface(
    fn=process_single_image,
    inputs=gr.Image(type="numpy"),
    outputs="image",
    examples=example_paths,
    cache_examples=False,
    description="Upload a single image to remove haze."
)

BatchDehazer = gr.Interface(
    fn=process_images,
    inputs=gr.Files(label="Upload Multiple Images", file_types=["image"]),
    outputs=gr.Files(label="Download Dehazed Images"),
    description="Upload multiple images to remove haze. Download the processed dehazed images."
)

VideoDehazer = gr.Interface(
    fn=process_video,
    inputs=gr.Video(label="Upload a Video"),
    outputs=gr.File(label="Download Dehazed Video"),
    description="Upload a video to remove haze. Download the processed dehazed video."
)

# Combined Gradio App
app = gr.TabbedInterface(
    [PixelDehazer, BatchDehazer, VideoDehazer],
    ["Single Image Dehazing", "Batch Image Dehazing", "Video Dehazing"],
    title="DeFogify App"
)

# Launch the Gradio App
if __name__ == "__main__":
    app.launch()
