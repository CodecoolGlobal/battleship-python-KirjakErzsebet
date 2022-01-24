import string
import math
from locale import ABDAY_3
# table class

# size_of_table = 5 
# num_of_ships = math.floor(5/2)

def size_table(size):
    table = []
    for _ in range(size):
        table.append(["O" for _ in range(size)])
    return table

def print_table(table):
    abc = list(string.ascii_uppercase) 
    print(f"\n  {' '.join([str(num + 1) for num in range(len(table))])}")
    for index, row in enumerate(table):
        print(f"{abc[index]} {' '.join(row)}")

def ask_input():
    coordinates = input("Please give me a coordinate!")
    return coordinates.upper()


def is_valid_input(abc, table, coordinates):
    coordinates = list(coordinates)
    num_list = [str(num) for num in range(len(table)+1)]
    if len(coordinates) == 2 and coordinates[0] in abc[0:len(table)] and coordinates[1] in num_list:
        return True
    return False

""""Vertical A1 Cruiser looks like : [(0,0),(0,1),(0,2)]"""
def select_ship(table):
    ship_type = input("Please select a ship type: 1 - Cruiser (size:3), 2 - Destroyer (size:2)")
    orientation = input("Choose orientation: 1 - Horizontal, 2 - Vertical ")
    position = ask_input()

    return ship_type, orientation, position

def is_ship_on_table(table, ship_type, orientation, row, col):
    ship=[]
    
    if orientation == '1':
        if ship_type == '1': 
            if is_valid_input(abc,table,position):

                return True, [(row,col),(row,col+1),(row,col+2)]
            return False
        elif ship_type == '2':
            if is_valid_input(abc,table,position):
                return True
            return False
    if orientation == '2':
        if ship_type == '1': 
            pass
            
    
def put_ship(table, ship): 
    pass

# def guess():

def update_board(guess, board, ship, guesses):
    pass

def main():
    table = size_table(5)
    abc = list(string.ascii_uppercase)
    print_table(table)
    coordinates = ask_input()
    while not is_valid_input(abc, table, coordinates):
        coordinates = ask_input()
    row = abc.index(coordinates[0])
    col = int(coordinates[1])-1


if __name__ == '__main__':
    main()





