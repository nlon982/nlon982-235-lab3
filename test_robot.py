import pytest

from robot import Robot, Direction, IllegalMoveException


@pytest.fixture
def robot():
    return Robot()


def test_constructor(robot):
    state = robot.state()

    assert state['direction'] == Direction.NORTH
    assert state['row'] == 10
    assert state['col'] == 1


# turning tests

def test_east_turn(robot):
    robot.turn()

    state = robot.state()
    assert state['direction'] == Direction.EAST

def test_south_turn(robot):
    # recall 'robot' starts facing North
    robot.turn() # facing east
    robot.turn() # facing south
    state = robot.state()
    assert state['direction'] == Direction.SOUTH

def test_west_turn(robot):
    # recall 'robot' starts facing North
    robot.turn() # facing east
    robot.turn() # facing south
    robot.turn() # facing west
    state = robot.state()
    assert state['direction'] == Direction.WEST

def test_north_turn(robot):
    # recall 'robot' starts facing North
    robot.turn() # facing east
    robot.turn() # facing south
    robot.turn() # facing west
    robot.turn() # facing north
    state = robot.state()
    assert state['direction'] == Direction.NORTH


# (legal) move tests

def test_move_north(robot):
    robot.move()
    state = robot.state()
    assert state['row'] == 9
    assert state['col'] == 1

def test_move_east(robot):
    robot.turn() # facing east
    robot.move()
    state = robot.state()
    assert state['row'] == 10
    assert state['col'] == 2

def test_move_south(robot):
    robot._state = Robot.State(Direction.SOUTH, 5, 5)  # around the middle
    robot.move()
    state = robot.state()
    assert state['row'] == 6
    assert state['col'] == 5


def test_move_west(robot):
    robot._state = Robot.State(Direction.WEST, 5, 5)  # around the middle
    robot.move()
    state = robot.state()
    assert state['row'] == 5
    assert state['col'] == 4

# illegal move tests

def test_invalid_move_north(robot):
    robot._state = Robot.State(Direction.NORTH, 1, 1) # top left

    with pytest.raises(IllegalMoveException):
        robot.move()

def test_invalid_move_east(robot):
    robot._state = Robot.State(Direction.EAST, 1, 10) # top right

    with pytest.raises(IllegalMoveException):
        robot.move()

def test_illegal_move_south(robot):
    robot.turn() # facing east
    robot.turn() # facing south

    with pytest.raises(IllegalMoveException):
        robot.move()

def test_invalid_move_west(robot):
    robot.turn() # facing east
    robot.turn() # facing south
    robot.turn() # facing west

    with pytest.raises(IllegalMoveException):
        robot.move()

#  backtrack / history tests

def test_back_track_without_history(robot):
    robot.back_track()
    state = robot.state()
    assert state['direction'] == Direction.NORTH
    assert state['row'] == 10
    assert state['col'] == 1

def test_back_track_after_move(robot):
    robot.move()
    robot.back_track()
    state = robot.state()
    assert state['direction'] == Direction.NORTH
    assert state['row'] == 10
    assert state['col'] == 1

def test_back_track_after_turn(robot):
    robot.turn()
    robot.back_track()
    state = robot.state()
    assert state['direction'] == Direction.EAST
    assert state['row'] == 10
    assert state['col'] == 1

def test_back_track_once_after_multiple_moves(robot):
    number_of_moves = 3 # more future proof

    for i in range(number_of_moves): # i.e. iterate number_of_moves times
        robot.move()
    robot.back_track() # backtrack once

    state = robot.state()
    assert state['direction'] == Direction.NORTH
    assert state['row'] == 8
    assert state['col'] == 1

def test_back_track_all_after_multiple_moves(robot):
    number_of_moves = 3 # more future proof

    for i in range(number_of_moves): # i.e. iterate number_of_moves times
        robot.move()
    for i in range(number_of_moves): # i.e. iterate number_of_moves times
        robot.back_track() # backtrack once

    state = robot.state()
    assert state['direction'] == Direction.NORTH
    assert state['row'] == 10
    assert state['col'] == 1
