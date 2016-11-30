from nose.tools import assert_in, eq_
from rushhour.solver import Solver, ZeroHeuristic, BlockingCarsHeuristic
from rushhour.board import Board


def test_basic_case():
    board = Board.readFromfile('tests/files/redcar.txt')
    solver = Solver(board, ZeroHeuristic())

    moves = solver.solve()
    eq_(len(moves), 4)
    for move in moves:
        eq_(move[1], "right")


def test_blocking_car_case():
    board = Board.readFromfile('tests/files/blocking.txt')
    solver = Solver(board, ZeroHeuristic())

    moves = solver.solve()
    for move in moves:
        if(move[0] == 'r'):
            eq_(move[1], "right")
        if(move[0] == 'C'):
            eq_(move[1], "down")


def test_assignment_case():
    board = Board.readFromfile('input.txt')
    solver = Solver(board, ZeroHeuristic())

    moves = solver.solve()
    eq_(len(moves), 29)

# http://cs.ulb.ac.be/~fservais/rushhour/
# Hardest configuration
def test_hard_case():
    board = Board.readFromfile('hard.txt')
    solver = Solver(board, ZeroHeuristic())

    moves = solver.solve()
    eq_(len(moves), 93)
