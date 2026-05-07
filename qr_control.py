import cv2


def read_qr_command(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Could not load image: {image_path}")
        return None

    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)

    if not data:
        print("QR Code not detected or could not be decoded.")
        return None

    print(f"QR command received: {data}")
    return data.strip().lower()


if __name__ == "__main__":
    command = read_qr_command("qr1.jpg")
    print(f"Command: {command}")
