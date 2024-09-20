# https://abeljoshua-cruzada.medium.com/image-segmentation-part-1-thresholding-otsu-and-hsv-color-space-method-dca7cfabbb7b

import numpy as np
from skimage.color import rgb2hsv
import cv2
import matplotlib.pyplot as plt

def isolate_color(image, graph=False):
    image_hsv = rgb2hsv(image)

    lower_mask = image_hsv[:,:,0] > 0.25
    upper_mask = image_hsv[:,:,0] < 0.5
    mask = upper_mask*lower_mask

    red = image[:,:,0]*mask
    green = image[:,:,1]*mask
    blue = image[:,:,2]*mask
    img = np.dstack((red,green,blue)) #img cosa?

    #return img

    # Converti l'immagine nello spazio colore HSV
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Estrai il canale Value
    value_channel = hsv_image[:, :, 2]

    # Calcola l'istogramma per il canale Value
    hist = cv2.calcHist([value_channel], [0], None, [256], [1, 256])

    # Calcola la distribuzione cumulativa
    cdf = hist.cumsum()
    #cdf_normalized = cdf * hist.max() / cdf.max()

    # Definisci i percentili per il passa banda
    low_percentile = 15
    high_percentile = 80

    # Trova i valori di intensità corrispondenti ai percentili
    cdf_min = np.min(cdf)
    low_cutoff = np.searchsorted(cdf, cdf_min + (low_percentile / 100.0) * cdf[-1])
    high_cutoff = np.searchsorted(cdf, cdf_min + (high_percentile / 100.0) * cdf[-1])

    # Crea una maschera per il filtro passa banda
    # passa basso manuale
    # passa alto da statistiche
    mask = cv2.inRange(value_channel, int(low_cutoff), 180)

    if graph:
        print("cdf thresh", low_cutoff, high_cutoff)
        plt.plot(hist, label='Histogram')
        plt.plot(cdf, label='Cumulative Distribution')
        plt.legend()
        plt.title('Histogram and CDF of Value Channel')
        plt.show()

    # Applica la maschera all'immagine originale
    return cv2.bitwise_and(image, image, mask=mask)
