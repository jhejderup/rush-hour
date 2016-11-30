from nose.tools import assert_in, eq_

from rushhour.board import Orientation, Car, Board


def test_empty_board():
    board = Board.readFromfile('tests/files/empty.txt')
    eq_(len(board.cars), 0)


def test_red_car():
    board = Board.readFromfile('tests/files/redcar.txt')
    eq_(len(board.cars), 1)
    assert_in(Car('r', {'x': 0, 'y': 2}, 2,
                  Orientation.HORIZONTAL, True), board.cars)


def test_gameboard():
    board = Board.readFromfile('input.txt')
    eq_(len(board.cars), 10)
    assert_in(Car('r', {'x': 0, 'y': 2}, 2,
                  Orientation.HORIZONTAL, True), board.cars)
    assert_in(Car('A', {'x': 4, 'y': 0}, 2,
                  Orientation.HORIZONTAL, False), board.cars)
    assert_in(Car('B', {'x': 2, 'y': 1}, 2,
                  Orientation.HORIZONTAL, False), board.cars)
    assert_in(Car('C', {'x': 4, 'y': 1}, 2,
                  Orientation.HORIZONTAL, False), board.cars)
    assert_in(Car('E', {'x': 4, 'y': 2}, 3,
                  Orientation.VERTICAL, False), board.cars)
    assert_in(Car('F', {'x': 5, 'y': 2}, 3,
                  Orientation.VERTICAL, False), board.cars)
    assert_in(Car('G', {'x': 0, 'y': 3}, 2,
                  Orientation.HORIZONTAL, False), board.cars)
    assert_in(Car('H', {'x': 2, 'y': 3}, 2,
                  Orientation.HORIZONTAL, False), board.cars)
    assert_in(Car('I', {'x': 3, 'y': 4}, 2,
                  Orientation.VERTICAL, False), board.cars)
    assert_in(Car('J', {'x': 4, 'y': 5}, 2,
                  Orientation.HORIZONTAL, False), board.cars)


def test_moves_vertical():
    board = Board.readFromfile('tests/files/vertical.txt')
    eq_(len(board.cars), 1)

    moved_cars = [Car('r', {'x': 1, 'y': 3}, 2,
                      Orientation.VERTICAL, True), Car('r', {'x': 1, 'y': 1}, 2,
                                                       Orientation.VERTICAL, True)]

    for new_b in board.explore_moves():
        assert_in(new_b[1].cars[0], moved_cars)


def test_moves_horizontal():
    board = Board.readFromfile('tests/files/horizontal.txt')
    eq_(len(board.cars), 1)

    moved_cars = [Car('r', {'x': 2, 'y': 2}, 2,
                      Orientation.HORIZONTAL, True), Car('r', {'x': 0, 'y': 2}, 2,
                                                         Orientation.HORIZONTAL, True)]
    for new_b in board.explore_moves():
        assert_in(new_b[1].cars[0], moved_cars)


def test_wall_horizontal():
    board = Board.readFromfile('tests/files/redcar.txt')
    eq_(len(board.cars), 1)

    moved_cars = [Car('r', {'x': 1, 'y': 2}, 2, Orientation.HORIZONTAL, True)]
    for new_b in board.explore_moves():
        assert_in(new_b[1].cars[0], moved_cars)


def test_red_car_exit():
    board = Board.readFromfile('tests/files/exit.txt')
    eq_(board.is_solved(), True)
