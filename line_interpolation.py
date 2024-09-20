import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import RANSACRegressor

def interpolate(img):

    # Assicurati che l'immagine sia binaria
    _, img_binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    altezza, larghezza = img_binary.shape

    punti = []

    # Scansiona ogni 20 pixel in larghezza
    for x in range(0, larghezza, 20):
        colonna = img_binary[:, x]
        # Trova gli indici dove avviene il cambiamento tra bianco e nero
        edge_indices = np.where(np.diff(colonna) != 0)[0]
        if len(edge_indices) > 0:
            # Prendi il primo punto di bordo trovato
            y = edge_indices[0]
            punti.append((x, y))

    punti = np.array(punti)

    # Verifica che ci siano abbastanza punti per l'interpolazione
    line_y_ransac = []
    if len(punti) >= 2:
        X = punti[:, 0].reshape(-1, 1)
        y = punti[:, 1]
        
        # Utilizza RANSAC per filtrare i falsi positivi e interpolare la retta
        ransac = RANSACRegressor()
        ransac.fit(X, y)
        line_X = np.array([0, larghezza]).reshape(-1, 1)
        line_y_ransac = ransac.predict(line_X)
        
        # Visualizza i risultati
        #plt.imshow(img_binary, cmap='gray')
        #plt.scatter(punti[:, 0], punti[:, 1], color='yellow', label='Punti di Bordo')
        #plt.plot(line_X, line_y_ransac, color='red', linewidth=2, label='Retta Interpolata')
        #plt.legend()
        #plt.show()
    else:
        print("Non ci sono abbastanza punti per interpolare una retta.")

    return line_y_ransac
