# square_removing.py
# project:sudoku
# littzhch
# 20200716
# 20200717
# 20200718


import random
from copy import copy, deepcopy
from remove_checking import remove_check


def _remove_core(sdk, remain: list, remain_goal: int):
    """
    解决删除问题的递归函数
    :param sdk:sudoku.SudokuSquare对象
    :param remain: 还未删除的数字的索引列表
    :param remain_goal: 目标保留数量
    :return: bool
    """
    for idx in remain:
        current_num = sdk.raw_info[idx]
        sdk.num_update(idx, 0)
        if remove_check(deepcopy(sdk)):
            if len(remain) - 1 == remain_goal:
                return True
            n_remain = copy(remain)
            n_remain.remove(idx)
            if _remove_core(sdk, n_remain, remain_goal):
                return True
        sdk.num_update(idx, current_num)
    return False


def remove(sdk, a, b):
    """
    删除一定数量的数字，完成数独题目构建
    :param sdk: sudoku.SudokuSquare对象，填充完整的数独
    :param a: 删除数字的数量限制（可包含）
    :param b: 删除数字的数量限制（可包含）
    :return: 无
    """
    num = random.randint(a, b)
    remain_goal = 81 - num
    remain = [0,  1,  2,  3,  4,  5,  6,  7,  8,
              9, 10, 11, 12, 13, 14, 15, 16, 17,
             18, 19, 20, 21, 22, 23, 24, 25, 26,
             27, 28, 29, 30, 31, 32, 33, 34, 35,
             36, 37, 38, 39, 40, 41, 42, 43, 44,
             45, 46, 47, 48, 49, 50, 51, 52, 53,
             54, 55, 56, 57, 58, 59, 60, 61, 62,
             63, 64, 65, 66, 67, 68, 69, 70, 71,
             72, 73, 74, 75, 76, 77, 78, 79, 80]
    random.shuffle(remain)
    _remove_core(sdk, remain, remain_goal)
