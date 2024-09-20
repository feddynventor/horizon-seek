import cv2
import numpy as np


def apply_otsu( image ):

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Applica la soglia di Otsu
    _, thresholded = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Passo 3: (Opzionale) Applicare operazioni morfologiche per rimuovere il rumore
    # Usiamo una piccola operazione di apertura (erosione seguita da dilatazione)
    kernel = np.ones((5,5), np.uint8)  # Kernel 3x3 per l'operazione morfologica
    otsu_cleaned = cv2.morphologyEx(thresholded, cv2.MORPH_OPEN, kernel)

    # Analisi delle componenti connesse
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(otsu_cleaned, connectivity=8)

    # Imposta un'area minima per le componenti da mantenere
    min_area = 100000 # Cambia questo valore in base alle dimensioni del tuo foreground
    # Crea una maschera vuota per il foreground pulito
    filtered_foreground = np.ones_like(otsu_cleaned)
    #filtered_foreground = np.ones_like(thresholded)
    # Filtra e mantieni solo le componenti che hanno un'area maggiore o uguale a `min_area`
    for i in range(1, num_labels):  # Salta il background con etichetta 0
        if stats[i, cv2.CC_STAT_AREA] >= min_area:
            filtered_foreground[labels == i] = 255

    return filtered_foreground

    # Converte l'immagine in RGB per poter disegnare i punti colorati
    image_color = cv2.cvtColor(filtered_foreground, cv2.COLOR_GRAY2BGR)
    # Disegna i centroidi (punti rossi) sull'immagine
    for i in range(1, num_labels):  # Salta lo sfondo (etichetta 0)
        centroid = centroids[i]
        # Arrotonda le coordinate del centroide
        cX, cY = int(centroid[0]), int(centroid[1])
        # Disegna un cerchio rosso sui centroidi
        cv2.circle(image_color, (cX, cY), 5, (0, 0, 255), -1)  # (0, 0, 255) è il colore rosso in BGR
        cv2.putText(image_color, str(stats[i, cv2.CC_STAT_AREA]), (cX, cY+40), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3, cv2.LINE_AA)

    return image_color

    # Estrai lo sfondo (tutti i pixel con valore 0)
    #background = cv2.bitwise_and(image, image, mask=cv2.bitwise_not(thresholded))

    # Estrai il foreground (tutti i pixel con valore 255)
    #foreground = cv2.bitwise_and(image, image, mask=thresholded)
