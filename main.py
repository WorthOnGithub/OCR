import pytesseract
import cv2
from pytesseract import Output

# Constants and Parameters
IMAGE_PATH = 'IMAGE_NAME'
CONFIDENCE_THRESHOLD = 60
PYTESSERACT_CONFIG = r'--psm 11 --oem 3'


def main():
    img = load_image(IMAGE_PATH)
    data = extract_text_data(img, PYTESSERACT_CONFIG)
    draw_text_boxes(img, data, CONFIDENCE_THRESHOLD)
    lines = extract_text_lines(data)
    result = '\n\n'.join(lines)
    print(result)
    display_image_with_boxes(img)


def load_image(image_path):
    return cv2.imread(image_path)


def extract_text_data(img, config):
    return pytesseract.image_to_data(img, config=config, output_type=Output.DICT)


def draw_text_boxes(img, data, confidence_threshold):
    for i in range(len(data['text'])):
        conf = int(data['conf'][i])

        if conf > confidence_threshold:
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, data['text'][i], (x, y + h + 20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)


def extract_text_lines(data):
    lines = []
    prev_top = None

    for i in range(len(data['text'])):
        conf = int(data['conf'][i])

        if conf > 0:  # Filter out low-confidence results
            left, top, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            text = data['text'][i]

            if text.strip():  # Skip empty text
                if prev_top is None or top - prev_top >= h:  # New line
                    lines.append(text)
                else:
                    lines[-1] += ' ' + text  # Append to the last line

                prev_top = top

    return lines


def display_image_with_boxes(img):
    cv2.imshow('img', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
