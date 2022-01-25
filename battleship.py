import string
import sys

# table class

# size_of_table = 5
# num_of_ships = math.floor(5/2)


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
        coordinates = input("Please give me a coordinate!")
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
            print("\nInvalid coordinates!")
    return row, col


def select_ship(table, ship_type):
    ship_types = {3: "Cruiser", 2: "Destroyer"}
    orientation = 0
    while orientation not in [1, 2]:
        orientation = input(
            f"\nChoose orientation for your {ship_types[ship_type]}: 1 - Horizontal, 2 - Vertical \n"
        )
        try:
            orientation = int(orientation)

        except ValueError:
            print("\nInvalid orientation!")
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


"""Vertical A1 Cruiser should looks like : [(0,0),(0,1),(0,2)]
TABLE [["x","x","o","o","o"],
       ["o","o","o","o","o"],
       ["o","o","o","o","o"],
       ["o","o","o","o","o"],
       ["o","o","o","o","o"]
       """


def generate_neighbors(row, col, table):
    neighbors = [
        (row - 1, col),  # top neighbor
        (row, col + 1),  # right neighbor
        (row + 1, col),  # bottom neighbor
        (row, col - 1),
    ]  # left neighbor
    new_neighbors = []
    for pos in neighbors:
        print(all(pos))
        if all(i > len(table) for i in pos) and all(i >= 0 for i in pos):
            new_neighbors.append(pos)

    return new_neighbors


def validate_ship(table, ship, ship_type):
    while ship[-1][0] >= len(table) or ship[-1][1] >= len(table):
        print("\nShip is out of the table!")
        print_table(table)
        select_ship(table, ship_type)
    is_valid = True
    for element in ship:
        row = element[0]
        col = element[1]
        if table[row][col] == "O":
            neigh = generate_neighbors(row, col, table)
            for el in neigh:
                if table[el[0]][el[1]] == "O":
                    is_valid = is_valid and True
                else:
                    is_valid = False
        else:
            is_valid = False
        return is_valid


def put_ship(table, ship, ship_type):
    if validate_ship(table, ship, ship_type):
        for element in ship:
            row = element[0]
            col = element[1]
            table[row][col] = "X"
        return table
    else:
        print("Invalid ship!")
        return table


# def guess():


def update_board(guess, board, ship, guesses):
    pass


def main():
    table = init_table(5)
    size = len(table)
    count_ships = 0
    ship_type = 2
    while count_ships != size // 2:
        print_table(table)
        ship = select_ship(table, ship_type)
        table = put_ship(table, ship, ship_type)
        if validate_ship(table, ship, ship_type):
            count_ships += 1
            if ship_type == 2:
                ship_type = 3
            else:
                ship_type = 2
    print_table(table)


if __name__ == "__main__":
    main()
