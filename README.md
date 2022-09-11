# Delhaize_dates

This repository contains code and models to detect expiry dates on products from an image.
This was created as a 2-week challenge for a BeCode project.

#### Two versions with user interface were created:
- Detect dates in realtime by holding the date in a rectangle (like a barcode scanner)
- Detect dates fields in an image and extract them


#### 2 pytorch models from ocr.pytorch were retrained on the given dataset:
- CTPN model to detect the date location
- CRNN model to perform OCR

#### Kivy is used as UI.
