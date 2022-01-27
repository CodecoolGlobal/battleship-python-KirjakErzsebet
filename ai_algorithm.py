import random
import time
from battleship import print_table, generate_neighbors, is_won

def place_ships(table):
    row = random.randint(0,len(table)-1)
    col = random.randint(0, len(table)-1)
    orientation = random.randint(1,2)
    return row, col, orientation

def select_ai_ship(table, ship_type):
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

def validate_ai_ship(table, ship_type):
    ship = select_ai_ship(table, ship_type)
    while ship[-1][0] >= len(table) or ship[-1][1] >= len(table):
        ship = select_ai_ship(table, ship_type)
    is_valid = True
    for element in ship:
        row = element[0]
        col = element[1]
        if table[row][col] == "O" :
            neigh = generate_neighbors(row, col, table)
            for el in neigh:
                if table[el[0]][el[1]] == "O":
                    is_valid = is_valid and True
                else:
                    is_valid = False
        else:
            is_valid = False
    return is_valid, ship

def put_ai_ship(table, ship_type):
    is_valid, ship = validate_ai_ship(table, ship_type)
    if is_valid:
        for element in ship:
            row = element[0]
            col = element[1]
            table[row][col] = "X"
        return table, is_valid, ship
    else:
        return table, is_valid, ship

def put_all_ai_ships(table, size):
    print("\nNow AI is setting the coordinates for its ships!\n")
    time.sleep(1)
    count_ships = 0
    ships_list = []
    ship_type = 2
    while count_ships != size // 2:
        table, is_valid, ship = put_ai_ship(table, ship_type)
        ships_list.append(ship)
        if is_valid:
        
            count_ships += 1
            if ship_type == 2:
                ship_type = 3
            else:
                ship_type = 2
    return table, ships_list

def get_right_coords(table,board):
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
            return get_right_coords(table,board)
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


def ai_shooting_phase(table, board, ships_list):
    row, col = get_ai_shooting_coords(table, board)
    if table[row][col] == "O":
        board[row][col] = "\033[31mM\033[0m"
        # print("\n\033[31mYou've missed! Refilling...\033[0m\n")
    elif table[row][col] == "X":
        board[row][col] = "\033[33mH\033[0m"
        # print("\n\033[33mEnemy's shield is down!\033[0m\n")
    for ship in ships_list:
        is_ship_shink = 0
        for place in ship:
            if board[place[0]][place[1]] == "\033[33mH\033[0m":
                is_ship_shink += 1
        if is_ship_shink == len(ship):
            for place in ship:
                board[place[0]][place[1]] = "\033[32mS\033[0m"
            # print("\n\033[32mYou've destroyed one of the enemy's spaceships!\033[0m\n")
            return board
        else:
            continue
    return board

def ai_shooting_turn(player, table_player, board_player, ships_list):
    print(f"\nPlayer {player}'s turn:")
    board_player = ai_shooting_phase(table_player, board_player, ships_list)
    winner = is_won(board_player, table_player, player)
    return board_player, winner