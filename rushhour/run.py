from board import Board
from solver import Solver, ZeroHeuristic, BlockingCarsHeuristic



if __name__ == "__main__":
  b = Board.readFromfile('input.txt')
  print 'Configuraton'
  print b.prettify(b.cars)
  print 'Working on solving it!'
  s = Solver(b, BlockingCarsHeuristic())
  moves = s.solve()
  print s.solution(b, moves)
