import cv2
import pytesseract
from PIL import ImageGrab
import re
import pyautogui
import time

def extract_coordinates(text):
    coordinate_pattern = r'\d+,\d+'
    coordinates = re.findall(coordinate_pattern, text)

    return coordinates

def capture_and_analyze_screen(region):
    try:
        
        screenshot = ImageGrab.grab(bbox=region)
        print("Dimensions de l'image capturée : ", screenshot.size)


        gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

        _, thresholded = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        text = pytesseract.image_to_string(thresholded)

        coordinates = extract_coordinates(text)

        if coordinates:
           return coordinates
        else:
           return "Coordonnées non trouvées"
    except Exception as e:
        print(f"Erreur : {str(e)}")
        return "Erreur"


medems = pyautogui.getWindowsWithTitle(title="Hirodees")[0]
medems.minimize()
medems.maximize()
time.sleep(0.5)
region_a_capturer = (0, 0, 300, 300)
resultat = capture_and_analyze_screen(region_a_capturer)
print("Coordonnées extraites : ", resultat)
