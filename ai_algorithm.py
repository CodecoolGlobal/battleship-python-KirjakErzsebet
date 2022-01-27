import random
import time
from battleship import generate_neighbors, is_won

def place_ships(table):
    row = random.randint(0, len(table) - 1)
    col = random.randint(0, len(table) - 1)
    orientation = random.randint(1, 2)
    return row, col, orientation


def select_ai_ship(table, ship_type, board):
    row, col, orientation = place_ships(table)
    ship = []
    for i in range(int(ship_type)):
        if orientation == 1:
            new_position = (row, col + i)
            ship.append(new_position)
        else:
            new_position = (row + i, col)
            ship.append(new_position)
    return ship
    

def get_right_coords(table, board):
    row, col ,orientation = place_ships(table)
    empty_neighbours = generate_neighbors(row, col, board)
    for point in empty_neighbours:
        point1, point2 = point[0], point[1]
        if board[point1][point2] != "O":
            continue
        elif board[point1][point2] == "\033[32mS\033[0m":
            break
        elif board[point1][point2] == "O" and board[row][col] == "O":
            return row, col
        else:
            break
    return get_right_coords(table, board)


def get_ai_shooting_coords(table, board):
    for index, list in enumerate(board):
        for index2, item in enumerate(list):
            if item == "\033[33mH\033[0m":
                neigh = generate_neighbors(index, index2, board)
                for coord in neigh:
                    row, col = coord[0], coord[1]
                    if board[row][col] == "O":
                        return row, col

    return get_right_coords(table, board)
