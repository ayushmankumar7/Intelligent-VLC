import cv2
import glob
import argparse
import numpy as np
from scipy.linalg import fractional_matrix_power


def image_agcwd(img, a=0.25, truncated_cdf=False):
    h, w = img.shape[:2]
    hist, bins = np.histogram(img.flatten(), 256, [0, 256])
    cdf = hist.cumsum()
    cdf_normalized = cdf / cdf.max()
    prob_normalized = hist / hist.sum()

    unique_intensity = np.unique(img)
    intensity_max = unique_intensity.max()
    intensity_min = unique_intensity.min()
    prob_min = prob_normalized.min()
    prob_max = prob_normalized.max()

    pn_temp = (prob_normalized - prob_min) / (prob_max - prob_min)
    pn_temp[pn_temp > 0] = prob_max * (pn_temp[pn_temp > 0]**a)
    pn_temp[pn_temp < 0] = prob_max * (-((-pn_temp[pn_temp < 0])**a))
    prob_normalized_wd = pn_temp / pn_temp.sum()  # normalize to [0,1]
    cdf_prob_normalized_wd = prob_normalized_wd.cumsum()

    if truncated_cdf:
        inverse_cdf = np.maximum(0.5, 1 - cdf_prob_normalized_wd)
    else:
        inverse_cdf = 1 - cdf_prob_normalized_wd

    img_new = img.copy()
    for i in unique_intensity:
        img_new[img == i] = np.round(255 * (i / 255)**inverse_cdf[i])

    return img_new


def process_bright(img):
    img_negative = 255 - img
    agcwd = image_agcwd(img_negative, a=0.25, truncated_cdf=False)
    reversed = 255 - agcwd
    return reversed


def process_dimmed(img):
    agcwd = image_agcwd(img, a=0.75, truncated_cdf=True)
    return agcwd


def auto_gamma(img, threshold=.28, exp_in=115):

    # Extract intensity component of the image
    YCrCb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    Y = YCrCb[:, :, 0]
    # Determine whether image is bright or dimmed
    threshold = 0.19  # 0.3
    exp_in = 95  # Expected global average intensity 112
    M, N = img.shape[:2]
    mean_in = np.sum(Y/(M*N))
    t = (mean_in - exp_in) / exp_in

    # Process image for gamma correction
    img_output = None
    if t < -threshold:  # Dimmed Image
        result = process_dimmed(Y)
        YCrCb[:, :, 0] = result
        img_output = cv2.cvtColor(YCrCb, cv2.COLOR_YCrCb2BGR)
    elif t > threshold:
        result = process_bright(Y)
        YCrCb[:, :, 0] = result
        img_output = cv2.cvtColor(YCrCb, cv2.COLOR_YCrCb2BGR)
    else:
        img_output = img

    return(img_output)



def automatic_brightness_and_contrast(image, clip_hist_percent=25):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate grayscale histogram
    hist = cv2.calcHist([gray],[0],None,[256],[0,256])
    hist_size = len(hist)

    # Calculate cumulative distribution from the histogram
    accumulator = []
    accumulator.append(float(hist[0]))
    for index in range(1, hist_size):
        accumulator.append(accumulator[index -1] + float(hist[index]))

    # Locate points to clip
    maximum = accumulator[-1]
    clip_hist_percent *= (maximum/100.0)
    clip_hist_percent /= 2.0

    # Locate left cut
    minimum_gray = 0
    while accumulator[minimum_gray] < clip_hist_percent:
        minimum_gray += 1

    # Locate right cut
    maximum_gray = hist_size -1
    while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
        maximum_gray -= 1

    # Calculate alpha and beta values
    alpha = 255 / (maximum_gray - minimum_gray)
    beta = -minimum_gray * alpha

    '''
    # Calculate new histogram with desired range and show histogram 
    new_hist = cv2.calcHist([gray],[0],None,[256],[minimum_gray,maximum_gray])
    plt.plot(hist)
    plt.plot(new_hist)
    plt.xlim([0,256])
    plt.show()
    '''

    auto_result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return (auto_result)


# cap = cv2.VideoCapture(0)
# threshold = .28
# exp_in = 115
# while(1):
#     ret, frame = cap.read()
#     cv2.imshow('original', frame)
#     frame2 = auto_gamma(frame, threshold, exp_in)
#     cv2.imshow('adjusted', frame2)
#     keypress = cv2.waitKey(1) & 0xFF 
#     if keypress == 27:
#         break
#     if keypress == ord('t'):
#         threshold += .05
#         print(threshold, exp_in)
#     if keypress == ord('y'):
#         threshold -= .05
#         print(threshold, exp_in)
#     if keypress == ord('c'):
#         exp_in += 10
#         print(threshold, exp_in)
#     if keypress == ord('v'):
#         exp_in -= 10
#         print(threshold, exp_in)


# cap.release()
# cv2.destroyAllWindows()
