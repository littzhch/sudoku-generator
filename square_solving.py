# square_solving.py
# project:sudoku
# littzhch
# 20200716
# 20200718


from copy import deepcopy


def _core(zero_idxs, current_idx, size, sdk, success):
    zero_idx = zero_idxs[current_idx]
    nums = sdk.get_possible_nums(zero_idx)
    if not nums:
        return success
    else:
        if current_idx != size:
            for num in nums:
                sdk.num_update(zero_idx, num)
                success = _core(zero_idxs, current_idx + 1, size, sdk, success)
            sdk.num_update(zero_idx, 0)
            return success
        else:
            for num in nums:
                sdk.num_update(zero_idx, num)
                success.append(deepcopy(sdk))
            sdk.num_update(zero_idx, 0)
            return success


def solve_square(sdk):
    sdk.idx_update()
    current_idx = 0
    zero_idxs = sdk.zero_idx
    size = len(zero_idxs) - 1
    return _core(zero_idxs, current_idx, size, sdk, [])
