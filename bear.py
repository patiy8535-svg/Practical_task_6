from simple_pid import PID


class Bear:
    # This is the 'constructor'
    def __init__(self, name):
        self.name = name  # Attribute
        self.h = 0
        self.speed = 0
        self.m = 10
        self.pid = PID(20, 5, 2, setpoint=0)
        self.pid.output_limits = (0, 200)

    def singsong(self):
        return "Up, Down, Touch the Ground"

    def calcPosition(self, curentH, curentSpeed, t):
        g = 9.81
        # Engine power from PID controller
        power = self.pid(curentH)
        # Acceleration: engine force / mass - gravity
        acceleration = power / self.m - g
        # New speed and height using kinematics
        newSpeed = curentSpeed + acceleration * t
        newH = curentH + curentSpeed * t + 0.5 * acceleration * t ** 2
        # Don't go below ground
        if newH < 0:
            newH = 0
            newSpeed = 0
        return newH, newSpeed


if __name__ == "__main__":
    pooh = Bear("Pooh")
    print(pooh.singsong())

    # Set target height
    target_h = 10
    pooh.pid.setpoint = target_h

    h = 0
    speed = 0
    dt = 0.1

    for i in range(100):
        h, speed = pooh.calcPosition(h, speed, dt)
        if i % 10 == 0:
            print(f"t={i * dt:.1f}s  h={h:.2f}m  speed={speed:.2f}m/s")
