import cv2
import numpy as np
import gradio as gr

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

    # Ensure the result is in the range [0, 1]
    result = np.clip(result, 0, 1)
    return (result * 255).astype(np.uint8)

# Save example images for testing
example_images = [
    "Sample Images for Testing/ai-generated-9025430_1280.jpg",
    "Sample Images for Testing/meadow-5648849_1280.jpg",
    "Sample Images for Testing/mountains-7662717_1280.jpg",
    "Sample Images for Testing/mountains-8292685_1280.jpg",
    "Sample Images for Testing/nature-6722031_1280.jpg"
]

example_paths = []
for i, img_path in enumerate(example_images):
    img = cv2.imread(img_path)
    save_path = f"example_image_{i+1}.png"
    cv2.imwrite(save_path, img)
    example_paths.append([save_path])

# Create Gradio interface
PixelDehazer = gr.Interface(
    fn=dehaze,
    inputs=gr.Image(type="numpy"),
    outputs="image",
    title="Dehaze Images with PixelDehazer",
    description="Upload an image or use one of the provided samples to remove haze from images.",
    examples=example_paths,
    cache_examples=False
)

PixelDehazer.launch()
