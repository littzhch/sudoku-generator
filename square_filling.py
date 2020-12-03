# square_filling.py
# project:sudoku
# littzhch
# 20200715
# 20200716
# 20200718


import random
from sudoku import SudokuSquare


def generate_filled_square():
    while True:
        try:
            source_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            random.shuffle(source_list)
            sdk = SudokuSquare(source_list + [0, 0, 0, 0, 0, 0, 0, 0, 0,
                                              0, 0, 0, 0, 0, 0, 0, 0, 0,
                                              0, 0, 0, 0, 0, 0, 0, 0, 0,
                                              0, 0, 0, 0, 0, 0, 0, 0, 0,
                                              0, 0, 0, 0, 0, 0, 0, 0, 0,
                                              0, 0, 0, 0, 0, 0, 0, 0, 0,
                                              0, 0, 0, 0, 0, 0, 0, 0, 0,
                                              0, 0, 0, 0, 0, 0, 0, 0, 0])
            for idx in range(9, 81):
                nums = sdk.get_possible_nums(idx)
                num = random.choice(nums)
                sdk.num_update(idx, num)
        except IndexError:
            continue
        else:
            return sdk
