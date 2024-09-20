import cv2
import numpy as np

K = 3 # Numero di cluster

def apply_kmeans(image, K):
    Z = image.reshape((-1, 3))
    Z = np.float32(Z)

    # Criteri di stop del K-means
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    center = np.uint8(center)
    res = center[label.flatten()]
    segmented_image = res.reshape((image.shape))

    return segmented_image, label, center

def update_image(val):
    # Ottieni l'indice del cluster selezionato dallo slider
    green_cluster_idx = cv2.getTrackbarPos('Cluster', 'Mask')

    # Crea una maschera per il cluster selezionato
    mask = (label.reshape(hsv_image.shape[:2]) == green_cluster_idx).astype("uint8") * 255

    # Azzeramento della saturazione nel cluster selezionato
    ##modified_hsv = hsv_image.copy()
    ##modified_hsv[:, :, 1] = np.where(mask == 255, 0, hsv_image[:, :, 1])

    # Converti di nuovo in BGR
    ##result_image = cv2.cvtColor(modified_hsv, cv2.COLOR_HSV2BGR)

    # Visualizza l'immagine risultante
    ##cv2.imshow('Mask', result_image)
    cv2.imshow('Mask', mask)
    return mask

# Leggi l'immagine
import sys
image = cv2.imread(sys.argv[1])
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Applica K-means per segmentare l'immagine
segmented_image, label, center = apply_kmeans(hsv_image, K)

# Esamina i valori centrali per ogni cluster
print("Centers of the clusters (in HSV):")
for idx, clr in enumerate(center):
    print(f"Cluster {idx}: H={clr[0]}, S={clr[1]}, V={clr[2]}")

# Crea una finestra per la visualizzazione
cv2.namedWindow('Mask', cv2.WINDOW_NORMAL)

# Crea uno slider per selezionare il cluster
cv2.createTrackbar('Cluster', 'Mask', 0, K-1, update_image)

# Visualizza inizialmente con il cluster 0
update_image(0)

# Mostra la finestra finché non si preme un tasto
# cv2.imshow('Segmented Image', segmented_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
