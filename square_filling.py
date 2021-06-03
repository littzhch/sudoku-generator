# square_filling.py
# project:sudoku
# littzhch
# 20200715
# 20200716
# 20200718
# 20210603


import random
from sudoku import SudokuSquare


def _fill_cell(sdk: SudokuSquare, idx: int) -> int:
    if idx == 81:
        return 1
    nums = sdk.get_possible_nums(idx)
    if not nums:
        return 0
    random.shuffle(nums)
    for num in nums:
        sdk.num_update(idx, num)
        if _fill_cell(sdk, idx + 1):
            return 1
    sdk.num_update(idx, 0)
    return 0


def generate_filled_square():
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

    _fill_cell(sdk, 9)
    return sdk

