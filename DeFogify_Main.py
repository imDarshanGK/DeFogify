import cv2
import numpy as np
import gradio as gr

def dark_channel(img, size = 15):
    """ Compute the dark channel prior for an image. 
    Parameters: img (numpy.ndarray): Input image. size (int): Kernel size for the morphological operation. 
    Returns: numpy.ndarray: Dark channel image. """
    try:
        r, g, b = cv2.split(img)
        min_img = cv2.min(r, cv2.min(g, b))
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (size, size))
        dc_img = cv2.erode(min_img, kernel)
        return dc_img
    except Exception as e:
        print("Error in dark_channel: ", e)
        return np.zeros_like(img)

def get_atmo(img, percent = 0.001):
    """ Estimate the atmospheric light in the image. 
    Parameters: img (numpy.ndarray): Input image. percent (float): Percentage of the brightest pixels to consider for atmospheric light. 
    Returns: float: Estimated atmospheric light. """
    try:
        mean_perpix = np.mean(img, axis = 2).reshape(-1)
        mean_topper = mean_perpix[:int(img.shape[0] * img.shape[1] * percent)]
        return np.mean(mean_topper)
    except Exception as e:
        print("Error in get_atmo: ", e)
        return 0.0

def get_trans(img, atom, w = 0.95):
    """ Compute the transmission map of the image. 
    Parameters: img (numpy.ndarray): Input image. atom (float): Estimated atmospheric light. w (float): Weighting factor for the dark channel. 
    Returns: numpy.ndarray: Transmission map of the image. """
    try:
        x = img / atom
        t = 1 - w * dark_channel(x, 15)
        return t
    except Exception as e:
        print("Error in get_trans: ", e)
        return np.zeros_like(img)

def guided_filter(p, i, r, e):
    """ Apply a guided filter to the transmission map. 
    Parameters: p (numpy.ndarray): Input transmission map. i (numpy.ndarray): Guidance image (grayscale version of the input image). r (int): Radius of the local window. e (float): Regularization parameter. 
    Returns: numpy.ndarray: Refined transmission map. """
    try:
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
    except Exception as e:
        print("Error in guided_filter: ", e)
        return np.zeros_like(p)

def dehaze(image):
    """ Perform image dehazing using the dark channel prior. 
    Parameters: image (numpy.ndarray): Input image. 
    Returns: numpy.ndarray: Dehazed image. """
    try:
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
    except Exception as e:
        print("Error in dehaze: ", e)
        return image 

# Create Gradio interface
PixelDehazer = gr.Interface(fn=dehaze, inputs=gr.Image(type="numpy"), outputs="image")
PixelDehazer.launch()
