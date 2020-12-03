# sudoku.py
# project:sudoku
# littzhch
# 20200715
# 20200716
# 20200718


class SudokuSquare:
    def __init__(self, raw_info):
        self.raw_info = raw_info
        self.zero_idx = []
        for idx, val in list(enumerate(self.raw_info)):
            if val == 0:
                self.zero_idx.append(idx)

    def num_update(self, location, num):
        self.raw_info[location] = num

    def idx_update(self):
        self.zero_idx = []
        for idx, val in list(enumerate(self.raw_info)):
            if val == 0:
                self.zero_idx.append(idx)

    def get_possible_nums(self, idx):
        idxs = []
        divd = idx // 9
        rema = idx % 9
        start = idx - rema
        for num in range(start, 9 + start):
            idxs.append(num)
        start = - divd
        for coeff in range(start, start + 9):
            idxs.append(idx + coeff * 9)
        a = rema // 3
        b = divd // 3
        center_idx = a * 3 + 27 * b + 10
        for idx in [center_idx, center_idx + 9, center_idx - 9]:
            idxs.append(idx)
            idxs.append(idx - 1)
            idxs.append(idx + 1)
        idxs = set(idxs)
        total_nums = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        imposb_nums = set()
        for idx in idxs:
            imposb_nums.add(self.raw_info[idx])
        return list(total_nums.difference(imposb_nums))
