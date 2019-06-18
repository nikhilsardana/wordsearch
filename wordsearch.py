import numpy as np
import math
import cv2
import sys
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


d = {}
with open("english.txt") as f:
    for line in f:
       key = line.split()
       d[key[0].rstrip()] = 1 # all words set to value of 1

with open("addendum.txt") as f:
	for line in f:
		key = line.split()
		d[key[0].rstrip()] = 1



 
if __name__ == '__main__':
 
  if len(sys.argv) < 2:
    print('Usage: python wordsearch.py image.jpg')
    sys.exit(1)
   
  # Read image path from command line
  imPath = sys.argv[1]
  
 
  # Define config parameters.
  # '-l eng'  for using the English language
  # '--oem 1' for using LSTM OCR Engine
  config = ('-l eng --oem 0 --psm 3')
 
  # Read image from disk
  im = cv2.imread(imPath, cv2.IMREAD_COLOR)
 
  # Run tesseract OCR on image
  text = pytesseract.image_to_string(im, config=config)
 
  # Print recognized text
  print(text)