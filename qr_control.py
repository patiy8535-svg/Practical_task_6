import cv2
from bear import Bear


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

    if bbox is not None:
        for i in range(len(bbox[0])):
            pt1 = tuple(bbox[0][i].astype(int))
            pt2 = tuple(bbox[0][(i + 1) % len(bbox[0])].astype(int))
            cv2.line(img, pt1, pt2, (255, 0, 0), 3)
        cv2.imshow("QR Code Detection", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return data.strip().lower()


def run_flight(bear, command, target_h=10, steps=100, dt=0.1):
    if command == "start":
        print(f"Starting flight for {bear.name}, target height: {target_h}m")
        bear.pid.setpoint = target_h
    elif command == "stop":
        print(f"Stopping flight for {bear.name}")
        bear.pid.setpoint = 0
    else:
        print(f"Unknown command: '{command}'. Use 'start' or 'stop'.")
        return

    h = bear.h
    speed = bear.speed
    for i in range(steps):
        h, speed = bear.calcPosition(h, speed, dt)
        if i % 10 == 0:
            print(f"  t={i * dt:.1f}s  h={h:.2f}m  speed={speed:.2f}m/s")

    bear.h = h
    bear.speed = speed
    print(f"Flight ended. Final height: {h:.2f}m")


if __name__ == "__main__":
    pooh = Bear("Pooh")
    command = read_qr_command("qr1.jpg")
    if command:
        run_flight(pooh, command)
