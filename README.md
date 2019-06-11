# NotARobot - Automating reCAPTCHAs with Tensorflow
##### Emil Tu

This project leverages the Tensorflow Object Detection API to automatically solve Google reCAPTCHAs.

The procedure is as follows:

1. Locate and click the reCAPTCHA checkbox.
2. Locate the reCAPTCHA text and image(s).
3. Read the text using OCR.
4. Load the appropriate model based on the text.
5. Denoise the image using Nvidia's Noise2Noise implementation.
6. Classify the reCaptcha based on type (3x3 grid, 4x4 grid, 2x4 grid).
7. Detect objects within the captcha.
8. Click the appropriate boxes and verify.
9. Profit?

## Details

The detection of objects within the reCAPTCHA is accomplished using Google's Faster-RCNN NASNet architecture. Images were gathered from the Open Images V4 Dataset, and trained on a Titan RTX using a batch size of 1. Currently, 5 of the most common types have been trained, these being cars, buses, bicycles, fire hydrants, and traffic lights. Depending on availability from Open Images, each class included between 400 and 17000 images of training and validation data.

The detection of checkboxes and the reCAPTCHA itself uses the SSD Mobilenet architecture, as this lighweight model is better suited for the task. These models were trained using approximately 100 screenshots that I created.

The classification of reCaptchas is done with a simple Tensorflow classification model. This was trained on about 300 screenshots, and is relatively proficient at separating 3x3, 4x4, and 2x4 captchas. This is important as they determine what coordinates should be used for each square of the captcha.

The denoising algorithm uses Nvidia's noise2noise library. It is trained using Gaussian noise on a dataset of 15,000 reCaptcha images that I collected. This library is interesting in that data does not have to be labelled, allowing for easy use of large datasets. Denoising is beneficial in reCaptcha solving, as Google has begun implementing adversarial noise in a portion of images.



## Getting Started

### Hardware

A GPU capable of inference on the NASNet architecture is required (approximately 8GB of VRAM or more).

### Python dependencies

This project was run on Ubuntu 19.04 running Python3.7. Dependencies include pyautogui, pillow, numpy, matplotlib, and tensorflow. By default, it opens the Chrome browser, but this is easy to change according to preference.
These can be installed by running the following:

```
pip3 install -r requirements.txt
```
Note: I recommend either compiling Tensorflow yourself, or installing the tensorflow-gpu package for best results.

### Models

Each model used is approximately 1.2 GB, and thus cannot be included in Github repositories.
They are hosted in Google Drive at the following links (will be available when uploading finishes):

| Class  | URL |
| ------------- | ------------- |
| Bus  | Content Cell  |
| Bicycle | Content Cell  |
| Captcha image(s) | Content Cell|
| Car | Content Cell|
| Captcha checkbox | Content Cell|
| Fire Hydrant | Content Cell|
| Traffic Light | Content Cell|

Each model is compressed into a tar.gz, and should be extracted into the object_detection directory.
