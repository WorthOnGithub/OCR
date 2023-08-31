import pytesseract
import cv2
from pytesseract import Output

# Configuration
myconfig = r'--psm 11 --oem 3'

# Load and process the image
img = cv2.imread('logos.png')
height, width, _ = img.shape

data = pytesseract.image_to_data(img, config=myconfig, output_type=Output.DICT)
amount_boxes = len(data['text'])

# Draw boxes around text
for i in range(amount_boxes):
    if int(data['conf'][i]) > 60:
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        img = cv2.putText(img, data['text'][i], (x, y + h + 20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

# Extract text lines
lines = []
prev_top = None

for i in range(len(data['text'])):
    if int(data['conf'][i]) > 0:  # Filter out low-confidence results
        left, top, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
        text = data['text'][i]

        if text.strip():  # Skip empty text
            if prev_top is None or top - prev_top >= h:  # New line
                lines.append(text)
            else:
                lines[-1] += ' ' + text  # Append to the last line

            prev_top = top

result = '\n'.join(lines)
print(result)

# Display the image with highlighted text boxes
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
