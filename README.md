# sudoku-generator
生成数独和解数独

## 功能
- 生成唯一解数独，可导出为docx格式和一种类似于Json的纯文本
- 解数独，显示所有的解法（对于多解数独）

## 注意
- docx格式在最新的MS office上不兼容且有排版问题，用WPS效果更好
- 设空数量在55个以上时，生成时间会很长，可能根本无法生成
- 数独的解过多时，解数独时间会很长
- 解数独的结果只对正确的数独（包括多解数独）负责

## 运行
- 需要python3
- 需要docx库（pip3 install python-docx)
- main.py为程序入口
- 可以用pyinstaller打包（pip3 install pyinstaller)
