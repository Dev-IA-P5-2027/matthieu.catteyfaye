import cv2

img = cv2.imread("data/bird.jpg", 1) # image en couleur
print(img.shape)

cv2.imshow("Image Test", img) # Affiche l'image
"""cv2.waitKey(2000) # L'image va s'afficher pendant 2000ms (2 secondes)"""
k = cv2.waitKey(0) # Affiche l'image jusqu'à ce qu'on appuie sur une touche

if k == ord("s"):
    cv2.imwrite("data/bird_as_png.png", img)
    print("L'image a été sauvgardée")
else:
    cv2.destroyAllWindows()
    print("Les fenêtres ont été détruites")