# NotARobot
Automated reCAPTCHA solving using Tensorflow

This project leverages the Tensorflow Object Detection API to automatically solve Google reCAPTCHAs.

The procedure is as follows:

1. Locate and click the reCAPTCHA checkbox.
2. Locate the reCAPTCHA text and image(s).
3. Read the text using OCR.
4. Load the appropriate model based on the text.
5. Denoise the image using Nvidia's Noise2Noise implementation.
6. Detect objects within the captcha.
7. Click the appropriate boxes and verify.
8. Profit?

## Getting Started

### Python dependencies

This project was run on Ubuntu 19.04 running Python3.7. Dependencies include pyautogui, pillow, numpy, matplotlib, and tensorflow.
These can be installed by running the following:

```
pip3 install -r requirements.txt
```
