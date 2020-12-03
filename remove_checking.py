# remove_checking.py
# project:sudoku
# littzhch
# 20200716
# 20200718
# 20200801


def _core(zero_idxs, current_idx, size, sdk, success):
    zero_idx = zero_idxs[current_idx]
    nums = sdk.get_possible_nums(zero_idx)
    if not nums:
        return success
    else:
        if current_idx == size:
            if len(nums) >= 2:
                return 2
            else:
                return success + 1
        else:
            for num in nums:
                sdk.num_update(zero_idx, num)
                success = _core(zero_idxs, current_idx + 1, size, sdk, success)
                if success >= 2:
                    return 2
            sdk.num_update(zero_idx, 0)
            return success


def remove_check(sdk):
    sdk.idx_update()
    zero_idxs = sdk.zero_idx
    size = len(zero_idxs) - 1
    success = _core(zero_idxs, 0, size, sdk, 0)
    if success >= 2:
        return False
    return True
