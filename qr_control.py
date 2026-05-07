import sys
import cv2
from bear import Bear


def run_with_camera(bear, target_h=10, dt=0.1, camera_index=0):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Could not open camera {camera_index}")
        return

    detector = cv2.QRCodeDetector()
    print("Show QR with 'start' to begin flight, 'stop' to quit. (q = force quit)")

    flying = False
    h = bear.h
    speed = bear.speed
    last_command = None
    status = "Waiting for QR..."

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        data, bbox, _ = detector.detectAndDecode(frame)

        if bbox is not None:
            pts = bbox.astype(int)
            for i in range(len(pts[0])):
                pt1 = tuple(pts[0][i])
                pt2 = tuple(pts[0][(i + 1) % len(pts[0])])
                cv2.line(frame, pt1, pt2, (0, 255, 0), 3)

        if data:
            command = data.strip().lower()
            if command != last_command:
                print(f"QR command received: {command}")
                last_command = command
                if command == "start":
                    bear.pid.setpoint = target_h
                    flying = True
                    status = f"FLYING (target {target_h}m)"
                elif command == "stop":
                    status = "STOP — exiting..."
                    cv2.putText(frame, status, (20, 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.imshow("QR Flight Control", frame)
                    cv2.waitKey(1500)
                    break

        if flying:
            h, speed = bear.calcPosition(h, speed, dt)
            bear.h = h
            bear.speed = speed

        cv2.putText(frame, f"Status: {status}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(frame, f"Height: {h:.2f} m", (20, 75),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        cv2.putText(frame, f"Speed:  {speed:.2f} m/s", (20, 105),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
        cv2.putText(frame, f"Bear: {bear.name}", (20, 135),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)

        cv2.imshow("QR Flight Control", frame)

        if cv2.waitKey(int(dt * 1000)) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def read_qr_command(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Could not load image: {image_path}")
        return None

    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(img)

    if not data:
        print("QR Code not detected or could not be decoded.")
        return None

    print(f"QR command received: {data}")
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

    if len(sys.argv) > 1:
        command = read_qr_command(sys.argv[1])
        if command:
            run_flight(pooh, command)
    else:
        run_with_camera(pooh)
