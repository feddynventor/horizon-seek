import cv2
import numpy as np

# Imposta un'area minima per le componenti da mantenere
min_area = 100000 # Cambia questo valore in base alle dimensioni del tuo foreground

def filter( image ):

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Passo 3: (Opzionale) Applicare operazioni morfologiche per rimuovere il rumore
    # Usiamo una piccola operazione di apertura (erosione seguita da dilatazione)
    kernel = np.ones((9,9), np.uint8)  # Kernel 3x3 per l'operazione morfologica
    cleaned = cv2.morphologyEx(gray_image, cv2.MORPH_OPEN, kernel)
    ##cleaned = gray_image

    # Analisi delle componenti connesse
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(cleaned, connectivity=8)

    # Crea una maschera vuota per il foreground pulito
    filtered_foreground = np.ones_like(cleaned)
    # Filtra e mantieni solo le componenti che hanno un'area maggiore o uguale a `min_area`
    for i in range(1, num_labels):  # Salta il background con etichetta 0
        if stats[i, cv2.CC_STAT_AREA] >= min_area:
            filtered_foreground[labels == i] = 255
        else:
            filtered_foreground[labels == i] = 0

    return filtered_foreground

    # Converte l'immagine in RGB per poter disegnare i punti colorati
    dots_image = cv2.cvtColor(filtered_foreground, cv2.COLOR_GRAY2BGR)
    # Disegna i centroidi (punti rossi) sull'immagine
    for i in range(1, num_labels):  # Salta lo sfondo (etichetta 0)
        centroid = centroids[i]
        # Arrotonda le coordinate del centroide
        cX, cY = int(centroid[0]), int(centroid[1])
        # Disegna un cerchio rosso sui centroidi
        cv2.circle(dots_image, (cX, cY), 5, (0, 0, 255), -1)  # (0, 0, 255) è il colore rosso in BGR
        cv2.putText(dots_image, str(stats[i, cv2.CC_STAT_AREA]), (cX, cY+40), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3, cv2.LINE_AA)

    ## return filtered_foreground, dots_image

    # Estrai lo sfondo (tutti i pixel con valore 0)
    #background = cv2.bitwise_and(image, image, mask=cv2.bitwise_not(thresholded))

    # Estrai il foreground (tutti i pixel con valore 255)
    #foreground = cv2.bitwise_and(image, image, mask=thresholded)
