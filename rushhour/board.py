# -*- coding: utf-8 -*-
"""
This module defines the Board and Car classes for the rush-hour game

The Car class serve more to store car data and logic involving possible
moves of car in the board is defined in the Board class

TODO: Add an Enum for all possible directions
"""
from copy import deepcopy
from collections import defaultdict


class Orientation(object):
    """ Direction of the car"""
    HORIZONTAL = 0
    VERTICAL = 1


class Car(object):
    """Car Class for the Rushhour game

    Attributes:
        name: character
        coord: Coordinate of the car in the board
        length: length of the car (e.g space occupiying the board)
        orientation: horizontal or vertical alighment
        is_red_car: the car to be freed

    """

    def __init__(self, name, coord, length, orientation, is_red_car=None):
        self.name = name
        self.coord = coord
        self.length = length - 1 
        self.orientation = orientation
        self.is_red_car = is_red_car

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return str(self.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__repr__())

    def __repr__(self):
        if self.orientation == Orientation.HORIZONTAL:
            other_coord = {'x': self.coord['x'] + self.length,
                           'y': self.coord['y']}
            return "{} [{},{}]".format(self.name, self.coord, other_coord)
        else:
            other_coord = {'x': self.coord[
                'x'], 'y': self.coord['y'] + self.length}
            return "{} [{},{}]".format(self.name, self.coord, other_coord)
    

    def move(self, direction, distance):
        """Given the direction and distance, move the car according to it
        TODO: good to have validation with Orientation,
              e.g if the car is horizontal shouldnt be able to move up/down
        """
        if direction == 'up':
            self.coord['y'] -= distance

        if direction == 'down':
            self.coord['y'] += distance

        if direction == 'left':
            self.coord['x'] -= distance

        if direction == 'right':
            self.coord['x'] += distance

    @staticmethod
    def createFromBoardInfo(name, coords):
        def plane(coords):
            if coords[0]['x'] != coords[1]['x'] and coords[0]['y'] == coords[1]['y']:
                return Orientation.HORIZONTAL
            else:
                return Orientation.VERTICAL
        return Car(name, coords[0], len(coords), plane(coords), is_red_car=(name == 'r'))


class Board(object):
    """Board Class for setting up the playing board

    Attributes:
        cars: list of cars on the play board
        size: size of the board
    """

    def __init__(self, cars, width=6, height=6):
        self.size = {'x': height, 'y': width}
        self.cars = cars
        self.depth = 0
        self.hval = 0

    def __eq__(self, other):
        return self.cars == other.other

    def __str__(self):
        return str(self.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__repr__())

    @staticmethod
    def readFromfile(filename):
        """Reads a puzzle from a file and creates a new board instance, identifies the red car and board dimensions """
        def get_coord(row_idx):
            def result((col_idx, value)):
                return (value, {'y': row_idx, 'x': col_idx})
            return result

        def flatten(l):
            return [item for sublist in l for item in sublist]

        puzzle_file = open(filename, 'r')
        raw_board = [list(line.strip()) for line in puzzle_file]
        coords_board = [map(get_coord(row_idx), enumerate(row))
                        for row_idx, row in enumerate(raw_board)]
        cars_board = flatten([filter(lambda (c, v): c.isalpha(), list(row))
                              for row in list(coords_board)])
        raw_cars = defaultdict(list)
        for (k, v) in cars_board:
            raw_cars[k].append(v)
        cars = []
        for i in raw_cars:
            cars.append(Car.createFromBoardInfo(i, raw_cars[i]))
        return Board(cars, len(raw_board), len(raw_board[0]))

    def explore_moves(self):
        """Explore the state space of possible moves for a single car, this also checks whether we bump into a car or a wall"""
        board = self.game_board(self.cars)
        for car in self.cars:
            if car.orientation == Orientation.VERTICAL:
                # UP
                if car.coord['y'] - 1 >= 0 and board[car.coord['y'] - 1][car.coord['x']] == '.':
                    new_cars = deepcopy(self.cars)
                    new_car = [x for x in new_cars if x.name == car.name][0]
                    new_car.coord['y'] -= 1
                    yield [[[car.name, 'up']], Board(new_cars)]
                # DOWN
                if car.coord['y'] + car.length + 1 <= (self.size['x'] - 1) and board[car.coord['y'] + car.length + 1][car.coord['x']] == '.':
                    new_cars = deepcopy(self.cars)
                    new_car = [x for x in new_cars if x.name == car.name][0]
                    new_car.coord['y'] += 1
                    yield [[[car.name, 'down']], Board(new_cars)]
            else:
                # LEFT
                if car.coord['x'] - 1 >= 0 and board[car.coord['y']][car.coord['x'] - 1] == '.':
                    new_cars = deepcopy(self.cars)
                    new_car = [x for x in new_cars if x.name == car.name][0]
                    new_car.coord['x'] -= 1
                    yield [[[car.name, 'left']], Board(new_cars)]
                # RIGHT
                if car.coord['x'] + car.length + 1 <= (self.size['y'] - 1) and board[car.coord['y']][car.coord['x'] + car.length + 1] == '.':
                    new_cars = deepcopy(self.cars)
                    new_car = [x for x in new_cars if x.name == car.name][0]
                    new_car.coord['x'] += 1
                    yield [[[car.name, 'right']], Board(new_cars)]

    def game_board(self, cars):
        """Given a set of cars, create a 2D array of the puzzle"""
        board = [['.' for col in range(self.size['x'])]
                 for row in range(self.size['y'])]
        for car in cars:
            if car.orientation == Orientation.HORIZONTAL:
                x_start = car.coord['x']
                x_stop = car.coord['x'] + car.length
                for x in range(x_start, x_stop + 1):
                    board[car.coord['y']][x] = car.name
            else:
                y_start = car.coord['y']
                y_stop = car.coord['y'] + car.length
                for y in range(y_start, y_stop + 1):
                    board[y][car.coord['x']] = car.name
        return board

    def prettify(self, cars):
        """Printable version that represents the 2D array of the puzzle"""
        board = self.game_board(cars)
        output = ''
        for line in board:
            output += " ".join(line) + '\n'
        return output

    def is_solved(self):
        """Check if the red_car is free"""
        red_car = [car for car in self.cars if car.is_red_car][0]
        return red_car.coord['x'] + red_car.length == self.size['x'] - 1
