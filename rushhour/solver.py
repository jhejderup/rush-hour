# -*- coding: utf-8 -*-
"""
This module defines the Solver for solving the rushhour game

The Solver uses the A* algorithm to solve a board:
http://web.mit.edu/eranki/www/tutorials/search/

Provided are two Heuristics

H0: Zero Heuristics (Essentially a BFS)
H1: Blocking Heuristic,
    an admissible heuristic that counts the number of blocking cars
    in front of the red_car

"""
import heapq
from copy import deepcopy
from board import Board, Orientation


class PriorityQueue:
    """A simple version of a Priority Queue, that allows to give a priority value to an element"""

    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def empty(self):
        return len(self._queue) == 0

    def pop(self):
        return heapq.heappop(self._queue)[-1]

class NotSolvable(Exception):
    pass

class ZeroHeuristic:
    """Zero Heuristcs, same as a BFS search"""

    def calculate(self, board):
        return 0

    def __repr__(self):
        return 'ZeroHeuristic'


class BlockingCarsHeuristic:
    """Calculate number of cars blocking the way"""

    def calculate(self, board):
        red_car = [
            car for car in board.cars if car.is_red_car][0]
        if red_car.coord['x'] == 4:
            return 0
        blockingcars = 1
        for car in board.cars:
            if car.orientation == Orientation.VERTICAL and car.coord['x'] >= (red_car.coord['x'] + red_car.length) and (car.coord['y'] <= red_car.coord['y'] and car.coord['y'] + car.length > red_car.coord['y']):
                blockingcars += 1
        return blockingcars

    def __repr__(self):
        return 'BlockingCarsHeuristic'


class Solver(object):
    """The Solver class takes as input the board to be solved

        Attributes:
        board: the initial config of the puzzle
        hfn: heuristic_function
    """

    def __init__(self, board, hfn):
        self.board = board
        self.hfn = hfn

    def solve(self):
        frontier = PriorityQueue()
        board = self.board
        closed_set = set()
        frontier.push([[], board], 0)
        # g(u)
        g = {}
        g[hash(str(board))] = 0
        while not frontier.empty():
            moves, board = frontier.pop()

            if board.is_solved():
                return moves

            for new_moves, new_boards in board.explore_moves():
                new_g = new_boards.depth + 1
                # f = g(u) + h(u)
                priority = new_g + self.hfn.calculate(new_boards)
                if hash(str(new_boards)) not in closed_set:
                    frontier.push([moves + new_moves, new_boards], priority)
                    closed_set.add(hash(str(new_boards)))
                else:
                    if new_g < g[hash(str(new_boards))]:
                        frontier.push(
                            [moves + new_moves, new_boards], priority)
                    else:
                        continue
                g[hash(str(new_boards))] = new_g

        raise NotSolvable('Not able to solve!')

    def solution(self, board, moves):
        """Format the steps and provide a step-by-step guide to solve the puzzle"""
        output = ''
        output += "; ".join(["{} {}".format(move[0], move[1]) for move in moves])
        cars = deepcopy(board.cars)
        for move in moves:
            car = [x for x in cars if x.name == move[0]][0]
            output += '\nMOVE {} {}\n'.format(move[0], move[1])
            car.move(move[1], 1)
            output += self.board.prettify(cars)
        return output
