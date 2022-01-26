import string
import sys
import os
import time

from asciiart import welcome, start_journey


def choose_size():
    size = None
    while size not in range(5,11):
        size = input("Please choose the size of the table: 5 to 10 \n")
        if size == "quit":
            sys.exit()
        try:
            size= int(size)
            if size not in range(5,11):
                print("\nWrong size! Please choose from 5 to 10! \n")
                continue
        except ValueError:
            print("\nPlease choose from 5 to 10! \n")
        
    return size


def init_table(size):
    table = []
    for _ in range(size):
        table.append(["O" for _ in range(size)])
    return table


def print_table(table):
    abc = list(string.ascii_uppercase)
    print(f"\n  {' '.join([str(num + 1) for num in range(len(table))])}")
    for index, row in enumerate(table):
        print(f"{abc[index]} {' '.join(row)}")


def ask_valid_input(table):
    rows = list(string.ascii_uppercase)
    columns = [str(num) for num in range(len(table) + 1)]
    row, col = (-1, -1)
    while (row, col) == (-1, -1):
        coordinates = input("\nPlease give me a coordinate! \n")
        if coordinates == "quit":  # quit
            sys.exit()
        coordinates = list(coordinates)
        coordinates[0] = coordinates[0].upper()
        if (
            len(coordinates) == 2
            and coordinates[0].upper() in rows[: len(table)]
            and coordinates[1] in columns
        ):
            row = rows.index(coordinates[0])
            col = int(coordinates[1]) - 1
        else:
            print("\nInvalid coordinates!\n")
    return row, col


def select_ship(table, ship_type):
    ship_types = {3: "Cruiser", 2: "Destroyer"}
    ship_lenght = {v:k for k,v in ship_types.items()}
    orientation = 0
    while orientation not in [1, 2]:
        orientation = input(
            f"\nChoose orientation for your {ship_types[ship_type]} (lenght:{ship_lenght[ship_types[ship_type]]}): \n1 - Horizontal,     2 - Vertical \n"
        )
        try:
            orientation = int(orientation)

        except ValueError:
            print("\nInvalid orientation!\n")
            continue

    row, col = ask_valid_input(table)
    ship = []
    for i in range(int(ship_type)):
        if orientation == 1:
            new_position = (row, col + i)
            ship.append(new_position)
        else:
            new_position = (row + i, col)
            ship.append(new_position)

    return ship


def generate_neighbors(row, col, table):
    neighbors = [
        (row - 1, col),  # top neighbor
        (row, col + 1),  # right neighbor
        (row + 1, col),  # bottom neighbor
        (row, col - 1),  # left neighbor
    ]  
    new_neighbors = []
    for pos in neighbors:
        if (0 <=pos[0] < len(table)) and (0 <= pos[1] < len(table)):
            new_neighbors.append(pos)
    return new_neighbors


def validate_ship(table, ship_type):
    ship = select_ship(table, ship_type)
    while ship[-1][0] >= len(table) or ship[-1][1] >= len(table):
        print("\nShip is out of the table!")
        print_table(table)
        ship = select_ship(table, ship_type)
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


def put_ship(table, ship_type):
    is_valid, ship = validate_ship(table, ship_type)
    if is_valid:
        for element in ship:
            row = element[0]
            col = element[1]
            table[row][col] = "X"
        return table, is_valid, ship
    else:
        print("\nShips are too close!\n")
        return table, is_valid, ship

def wait_for_another_player(size):
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Next player's placement phase.")
    input("Press any button!")
    # while True:
    #     if keyboard.read_key() == "p":
    #         break
    #     elif keyboard.read_key() != "p":
    #         break
    # x = 0
    # while x == 0:
    #     x = sys.stdin.read(1)[0]

    new_table = init_table(size)
    return new_table

def put_all_ships(table, size):
    count_ships = 0
    ships_list = []
    ship_type = 2
    while count_ships != size // 2:
        print_table(table)
        table, is_valid, ship = put_ship(table, ship_type)
        ships_list.append(ship)
        if is_valid:
            count_ships += 1
            if ship_type == 2:
                ship_type = 3
            else:
                ship_type = 2
    print_table(table)
    return table, ships_list


def shooting_phase(table, board, ships_list):
    row, col = ask_valid_input(table)
    if table[row][col] == "O":
        board[row][col] = "\033[31mM\033[0m"
        print("\nYou've missed!\n")
    elif table[row][col] == "X":
        board[row][col] = "\033[33mH\033[0m"
        print("\nYou've hit a ship!\n")
    is_ship_shink = 0
    for ship in ships_list:
        for place in ship:
            if board[place[0]][place[1]] == "\033[33mH\033[0m":
                is_ship_shink += 1
        if is_ship_shink == len(ship):
            for place in ship:
                board[place[0]][place[1]] = "\033[32mS\033[0m"
            print("\nYou've sunk a ship!\n")
            return board
        else:
            continue

    return board


def display_boards(board_player1, board_player2):
    board1 = board_player1.copy()
    board2 = board_player2.copy()
    print("Player 1     Player 2")
    abc = list(string.ascii_uppercase)
    boards = (board1, board2)
    for board in boards:
        for index, row in enumerate(board):
            board[index] = str(abc[index]+ ' ' + ' '.join(row))

        first_line = str('  ' +' '.join([str(num + 1) for num in range(len(board))]))
        board.insert(0, first_line)
        
    for line1, line2 in zip(board1, board2):
        print(f"{line1}  {line2}")


def flatten_list(_2d_list):
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list:
            # If the element is of type list, iterate through the sublist
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list


def is_won(board, table, player):
    flat_board = flatten_list(board)
    flat_table = flatten_list(table)
    if flat_board.count('\033[32mS\033[0m') == flat_table.count('X'):
        return player
    return ''


def main():
    welcome()
    winner = ''
    size = choose_size()
    table1 = init_table(size)
    table_player1, ships_player1 = put_all_ships(table1, size)
    table2 = wait_for_another_player(size)
    table_player2, ships_player2 = put_all_ships(table2, size)
    time.sleep(1)
    os.system('cls' if os.name == 'nt' else 'clear')
    start_journey()
    board_player1 = init_table(size)
    board_player2 = init_table(size)
    display_boards(board_player1, board_player2)
    player = 1
    while True:
        if player == 1:
            print(f"\nPlayer {player}'s turn:")
            board_player2 = shooting_phase(table_player2, board_player2, ships_player2)
            display_boards(board_player1, board_player2)
            winner = is_won(board_player2, table_player2, player)
            if winner != "":
                break
            player = 2
        elif player == 2:
            print(f"Player {player}'s turn:")
            board_player1 = shooting_phase(table_player1, board_player1, ships_player1)
            display_boards(board_player1, board_player2)
            winner = is_won(board_player1, table_player1, player)
            if winner != "":
                break
            player = 1
        
    print(f"\nPlayer {winner} wins!\n")

    




if __name__ == "__main__":
    main()