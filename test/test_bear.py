import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from bear import Bear


def test_bear_creation():
    pooh = Bear("Pooh")
    assert pooh.name == "Pooh"
    assert pooh.h == 0
    assert pooh.speed == 0
    assert pooh.m == 10


def test_singsong():
    pooh = Bear("Pooh")
    assert pooh.singsong() == "Up, Down, Touch the Ground"


def test_calcPosition_returns_tuple():
    pooh = Bear("Pooh")
    pooh.pid.setpoint = 10
    result = pooh.calcPosition(0, 0, 0.1)
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_calcPosition_height_not_negative():
    pooh = Bear("Pooh")
    pooh.pid.setpoint = 10
    newH, newSpeed = pooh.calcPosition(0, 0, 0.1)
    assert newH >= 0


def test_calcPosition_moves_toward_setpoint():
    pooh = Bear("Pooh")
    pooh.pid.setpoint = 10
    h = 0
    speed = 0
    for _ in range(200):
        h, speed = pooh.calcPosition(h, speed, 0.1)
    # After enough steps, height should approach setpoint
    assert h > 0


def test_calcPosition_zero_time():
    pooh = Bear("Pooh")
    pooh.pid.setpoint = 10
    newH, newSpeed = pooh.calcPosition(5, 2, 0)
    # With zero time step, position should not change
    assert newH == 5


def test_different_bears():
    pooh = Bear("Pooh")
    piglet = Bear("Piglet")
    assert pooh.name != piglet.name
    assert pooh.singsong() == piglet.singsong()
