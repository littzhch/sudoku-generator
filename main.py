# main.py
# project:sudoku
# littzhch
# 20200723
# 20200729


import tkinter as tk
import tkinter.ttk as ttk
from tkinter.filedialog import asksaveasfilename
from tkinter.messagebox import showerror
from copy import deepcopy
import time

from square_filling import generate_filled_square
from square_removing import remove
from output import create_docx, create_json
from sudoku import SudokuSquare
from square_solving import solve_square


IMG_PATH = "./image"
VERSION = "0.3"


class Window:
    def __init__(self, width, height, title, mainwindow=False):
        if mainwindow:
            self.win = tk.Tk()
        else:
            self.win = tk.Toplevel()
        self.win.iconbitmap(IMG_PATH + "/icon.ico")
        self.win.geometry(str(width) + 'x' + str(height))
        self.win.title(title)
        self.win.wm_resizable(0, 0)

    def show_window(self):
        self.win.mainloop()

    def close(self):
        self.win.destroy()


class MainWindow(Window):
    def __init__(self):
        Window.__init__(self, 800, 500, "数独生成器", mainwindow=True)

        c = tk.Canvas(self.win, width=800, height=400)
        self.i_file = tk.PhotoImage(file=IMG_PATH + "/welcome.png")
        c.create_image(-20, 0, anchor="nw", image=self.i_file)
        c.pack()

        frm = tk.Frame(self.win)
        frm.pack()

        b1 = ttk.Button(frm, text="\n解数独\n", command=self.solve)
        b2 = ttk.Button(frm, text="\n生成数独\n", command=self.generate)
        b1.grid(row=0, column=0, padx=100)
        b2.grid(row=0, column=1, padx=100)

        l = tk.Label(self.win, text="version:" + VERSION)
        l.place(x=0, y=500, anchor="sw")

    def generate(self):
        gw = GeneratingWindow()
        gw.show_window()

    def solve(self):
        sw = SolvingWindow()
        sw.show_window()


class GeneratingWindow(Window):
    def __init__(self):
        Window.__init__(self, 400, 400, "生成数独")
        self.sdks = []
        self.ans = []
        self.amount = 0
        self.generated = 0

        self.l1 = tk.Label(self.win, text="\n已生成数独：0")
        self.l2 = tk.Label(self.win, text="状态：空闲\n")
        self.l1.pack()
        self.l2.pack()

        frm1 = tk.Frame(self.win)
        frm1.pack()

        l3 = tk.Label(frm1, text="生成数量：")
        self.e = tk.Entry(frm1, width=4)
        l3.grid(row=0, column=0)
        self.e.grid(row=0, column=1)

        scale = tk.Scale(self.win, from_=0, to=60, orient=tk.HORIZONTAL, resolution=1, label="设空数量", tickinterval=10,
                         command=self.set_amount, length=360, showvalue=1)
        scale.pack()

        frm2 = tk.Frame(self.win)
        frm2.pack(pady=20)

        self.b1 = ttk.Button(frm2, text="生成", command=self.generate)
        self.b2 = ttk.Button(frm2, text="导出docx", command=self.output_docx)
        self.b3 = ttk.Button(frm2, text="清空", command=self.clean)
        self.b4 = ttk.Button(frm2, text="导出json", command=self.output_json)
        self.b1.grid(row=0, column=0, padx=30)
        self.b3.grid(row=0, column=1, padx=30)
        self.b2.grid(row=1, column=0, padx=30, pady=20)
        self.b4.grid(row=1, column=1, padx=30, pady=20)

    def set_amount(self, amount):
        self.amount = int(amount)

    def generate(self):
        num = 0
        try:
            num = int(self.e.get())
        except:
            pass
        if num <= 0:
            showerror("错误", "无效的生成数量")
            self.win.lift()
            return

        self.b1["state"] = tk.DISABLED
        self.b2["state"] = tk.DISABLED
        self.b3["state"] = tk.DISABLED
        self.b4["state"] = tk.DISABLED
        amount = self.amount
        for i in range(1, num + 1):
            self.l2.config(text="状态：生成中（" + str(i) + '/' + str(num) + ")...\n")
            self.win.update()
            answer = generate_filled_square()
            self.ans.append(deepcopy(answer))
            if amount != 0:
                remove(answer, amount, amount)
            self.sdks.append(answer)

            self.generated += 1
            self.l1.config(text="\n已生成数独：" + str(self.generated))

        self.win.lift()
        self.l2.config(text="状态：完成\n")
        self.b1["state"] = tk.NORMAL
        self.b2["state"] = tk.NORMAL
        self.b3["state"] = tk.NORMAL
        self.b4["state"] = tk.NORMAL

        self.win.update()
        time.sleep(.5)
        self.l2.config(text="状态：空闲\n")

    def output_docx(self):
        self.l2.config(text="状态：询问导出文件名\n")
        path = str(asksaveasfilename(title=u"导出docx格式文件", filetypes=[("DOCX", "docx")]))
        if not path:
            self.l2.config(text="状态：空闲\n")
            self.win.lift()
            return
        self.win.lift()
        self.l2.config(text="状态：保存中...\n")
        self.win.update()
        create_docx(path, self.sdks, self.ans)
        self.l2.config(text="状态：已保存\n")
        self.win.update()
        time.sleep(.5)
        self.l2.config(text="状态：空闲\n")

    def output_json(self):
        self.l2.config(text="状态：询问导出文件名\n")
        path = str(asksaveasfilename(title=u"导出json格式文件", filetypes=[("json", "json")]))
        if not path:
            self.l2.config(text="状态：空闲\n")
            self.win.lift()
            return
        self.win.lift()
        self.l2.config(text="状态：保存中...\n")
        self.win.update()
        create_json(path, self.sdks, self.ans)
        self.l2.config(text="状态：已保存\n")
        self.win.update()
        time.sleep(.5)
        self.l2.config(text="状态：空闲\n")

    def clean(self):
        self.l1.config(text="\n已生成数独：0")
        self.generated = 0
        self.sdks = []
        self.ans = []


class SolvingWindow(Window):
    def __init__(self):
        Window.__init__(self, 350, 350, "解数独")
        self.es = []
        frm = tk.Frame(self.win)
        frm.pack()
        frm1 = tk.Frame(frm)
        frm2 = tk.Frame(frm)
        frm3 = tk.Frame(frm)
        frm4 = tk.Frame(frm)
        frm5 = tk.Frame(frm)
        frm6 = tk.Frame(frm)
        frm7 = tk.Frame(frm)
        frm8 = tk.Frame(frm)
        frm9 = tk.Frame(frm)
        frm1.grid(row=0, column=0, padx=15, pady=5)
        frm2.grid(row=0, column=1, padx=15, pady=5)
        frm3.grid(row=0, column=2, padx=15, pady=5)
        frm4.grid(row=1, column=0, padx=15, pady=5)
        frm5.grid(row=1, column=1, padx=15, pady=5)
        frm6.grid(row=1, column=2, padx=15, pady=5)
        frm7.grid(row=2, column=0, padx=15, pady=5)
        frm8.grid(row=2, column=1, padx=15, pady=5)
        frm9.grid(row=2, column=2, padx=15, pady=5)

        e0 = tk.Entry(frm1, width=1)
        self.es.append(e0)
        e1 = tk.Entry(frm1, width=1)
        self.es.append(e1)
        e2 = tk.Entry(frm1, width=1)
        self.es.append(e2)
        e3 = tk.Entry(frm2, width=1)
        self.es.append(e3)
        e4 = tk.Entry(frm2, width=1)
        self.es.append(e4)
        e5 = tk.Entry(frm2, width=1)
        self.es.append(e5)
        e6 = tk.Entry(frm3, width=1)
        self.es.append(e6)
        e7 = tk.Entry(frm3, width=1)
        self.es.append(e7)
        e8 = tk.Entry(frm3, width=1)
        self.es.append(e8)
        e9 = tk.Entry(frm1, width=1)
        self.es.append(e9)
        e10 = tk.Entry(frm1, width=1)
        self.es.append(e10)
        e11 = tk.Entry(frm1, width=1)
        self.es.append(e11)
        e12 = tk.Entry(frm2, width=1)
        self.es.append(e12)
        e13 = tk.Entry(frm2, width=1)
        self.es.append(e13)
        e14 = tk.Entry(frm2, width=1)
        self.es.append(e14)
        e15 = tk.Entry(frm3, width=1)
        self.es.append(e15)
        e16 = tk.Entry(frm3, width=1)
        self.es.append(e16)
        e17 = tk.Entry(frm3, width=1)
        self.es.append(e17)
        e18 = tk.Entry(frm1, width=1)
        self.es.append(e18)
        e19 = tk.Entry(frm1, width=1)
        self.es.append(e19)
        e20 = tk.Entry(frm1, width=1)
        self.es.append(e20)
        e21 = tk.Entry(frm2, width=1)
        self.es.append(e21)
        e22 = tk.Entry(frm2, width=1)
        self.es.append(e22)
        e23 = tk.Entry(frm2, width=1)
        self.es.append(e23)
        e24 = tk.Entry(frm3, width=1)
        self.es.append(e24)
        e25 = tk.Entry(frm3, width=1)
        self.es.append(e25)
        e26 = tk.Entry(frm3, width=1)
        self.es.append(e26)
        e27 = tk.Entry(frm4, width=1)
        self.es.append(e27)
        e28 = tk.Entry(frm4, width=1)
        self.es.append(e28)
        e29 = tk.Entry(frm4, width=1)
        self.es.append(e29)
        e30 = tk.Entry(frm5, width=1)
        self.es.append(e30)
        e31 = tk.Entry(frm5, width=1)
        self.es.append(e31)
        e32 = tk.Entry(frm5, width=1)
        self.es.append(e32)
        e33 = tk.Entry(frm6, width=1)
        self.es.append(e33)
        e34 = tk.Entry(frm6, width=1)
        self.es.append(e34)
        e35 = tk.Entry(frm6, width=1)
        self.es.append(e35)
        e36 = tk.Entry(frm4, width=1)
        self.es.append(e36)
        e37 = tk.Entry(frm4, width=1)
        self.es.append(e37)
        e38 = tk.Entry(frm4, width=1)
        self.es.append(e38)
        e39 = tk.Entry(frm5, width=1)
        self.es.append(e39)
        e40 = tk.Entry(frm5, width=1)
        self.es.append(e40)
        e41 = tk.Entry(frm5, width=1)
        self.es.append(e41)
        e42 = tk.Entry(frm6, width=1)
        self.es.append(e42)
        e43 = tk.Entry(frm6, width=1)
        self.es.append(e43)
        e44 = tk.Entry(frm6, width=1)
        self.es.append(e44)
        e45 = tk.Entry(frm4, width=1)
        self.es.append(e45)
        e46 = tk.Entry(frm4, width=1)
        self.es.append(e46)
        e47 = tk.Entry(frm4, width=1)
        self.es.append(e47)
        e48 = tk.Entry(frm5, width=1)
        self.es.append(e48)
        e49 = tk.Entry(frm5, width=1)
        self.es.append(e49)
        e50 = tk.Entry(frm5, width=1)
        self.es.append(e50)
        e51 = tk.Entry(frm6, width=1)
        self.es.append(e51)
        e52 = tk.Entry(frm6, width=1)
        self.es.append(e52)
        e53 = tk.Entry(frm6, width=1)
        self.es.append(e53)
        e54 = tk.Entry(frm7, width=1)
        self.es.append(e54)
        e55 = tk.Entry(frm7, width=1)
        self.es.append(e55)
        e56 = tk.Entry(frm7, width=1)
        self.es.append(e56)
        e57 = tk.Entry(frm8, width=1)
        self.es.append(e57)
        e58 = tk.Entry(frm8, width=1)
        self.es.append(e58)
        e59 = tk.Entry(frm8, width=1)
        self.es.append(e59)
        e60 = tk.Entry(frm9, width=1)
        self.es.append(e60)
        e61 = tk.Entry(frm9, width=1)
        self.es.append(e61)
        e62 = tk.Entry(frm9, width=1)
        self.es.append(e62)
        e63 = tk.Entry(frm7, width=1)
        self.es.append(e63)
        e64 = tk.Entry(frm7, width=1)
        self.es.append(e64)
        e65 = tk.Entry(frm7, width=1)
        self.es.append(e65)
        e66 = tk.Entry(frm8, width=1)
        self.es.append(e66)
        e67 = tk.Entry(frm8, width=1)
        self.es.append(e67)
        e68 = tk.Entry(frm8, width=1)
        self.es.append(e68)
        e69 = tk.Entry(frm9, width=1)
        self.es.append(e69)
        e70 = tk.Entry(frm9, width=1)
        self.es.append(e70)
        e71 = tk.Entry(frm9, width=1)
        self.es.append(e71)
        e72 = tk.Entry(frm7, width=1)
        self.es.append(e72)
        e73 = tk.Entry(frm7, width=1)
        self.es.append(e73)
        e74 = tk.Entry(frm7, width=1)
        self.es.append(e74)
        e75 = tk.Entry(frm8, width=1)
        self.es.append(e75)
        e76 = tk.Entry(frm8, width=1)
        self.es.append(e76)
        e77 = tk.Entry(frm8, width=1)
        self.es.append(e77)
        e78 = tk.Entry(frm9, width=1)
        self.es.append(e78)
        e79 = tk.Entry(frm9, width=1)
        self.es.append(e79)
        e80 = tk.Entry(frm9, width=1)
        self.es.append(e80)
        e0.grid(row=0, column=0, padx=8, pady=2)
        e1.grid(row=0, column=1, padx=8, pady=2)
        e2.grid(row=0, column=2, padx=8, pady=2)
        e9.grid(row=1, column=0, padx=8, pady=2)
        e10.grid(row=1, column=1, padx=8, pady=2)
        e11.grid(row=1, column=2, padx=8, pady=2)
        e18.grid(row=2, column=0, padx=8, pady=2)
        e19.grid(row=2, column=1, padx=8, pady=2)
        e20.grid(row=2, column=2, padx=8, pady=2)
        e3.grid(row=0, column=0, padx=8, pady=2)
        e4.grid(row=0, column=1, padx=8, pady=2)
        e5.grid(row=0, column=2, padx=8, pady=2)
        e12.grid(row=1, column=0, padx=8, pady=2)
        e13.grid(row=1, column=1, padx=8, pady=2)
        e14.grid(row=1, column=2, padx=8, pady=2)
        e21.grid(row=2, column=0, padx=8, pady=2)
        e22.grid(row=2, column=1, padx=8, pady=2)
        e23.grid(row=2, column=2, padx=8, pady=2)
        e6.grid(row=0, column=0, padx=8, pady=2)
        e7.grid(row=0, column=1, padx=8, pady=2)
        e8.grid(row=0, column=2, padx=8, pady=2)
        e15.grid(row=1, column=0, padx=8, pady=2)
        e16.grid(row=1, column=1, padx=8, pady=2)
        e17.grid(row=1, column=2, padx=8, pady=2)
        e24.grid(row=2, column=0, padx=8, pady=2)
        e25.grid(row=2, column=1, padx=8, pady=2)
        e26.grid(row=2, column=2, padx=8, pady=2)
        e27.grid(row=0, column=0, padx=8, pady=2)
        e28.grid(row=0, column=1, padx=8, pady=2)
        e29.grid(row=0, column=2, padx=8, pady=2)
        e36.grid(row=1, column=0, padx=8, pady=2)
        e37.grid(row=1, column=1, padx=8, pady=2)
        e38.grid(row=1, column=2, padx=8, pady=2)
        e45.grid(row=2, column=0, padx=8, pady=2)
        e46.grid(row=2, column=1, padx=8, pady=2)
        e47.grid(row=2, column=2, padx=8, pady=2)
        e30.grid(row=0, column=0, padx=8, pady=2)
        e31.grid(row=0, column=1, padx=8, pady=2)
        e32.grid(row=0, column=2, padx=8, pady=2)
        e39.grid(row=1, column=0, padx=8, pady=2)
        e40.grid(row=1, column=1, padx=8, pady=2)
        e41.grid(row=1, column=2, padx=8, pady=2)
        e48.grid(row=2, column=0, padx=8, pady=2)
        e49.grid(row=2, column=1, padx=8, pady=2)
        e50.grid(row=2, column=2, padx=8, pady=2)
        e33.grid(row=0, column=0, padx=8, pady=2)
        e34.grid(row=0, column=1, padx=8, pady=2)
        e35.grid(row=0, column=2, padx=8, pady=2)
        e42.grid(row=1, column=0, padx=8, pady=2)
        e43.grid(row=1, column=1, padx=8, pady=2)
        e44.grid(row=1, column=2, padx=8, pady=2)
        e51.grid(row=2, column=0, padx=8, pady=2)
        e52.grid(row=2, column=1, padx=8, pady=2)
        e53.grid(row=2, column=2, padx=8, pady=2)
        e54.grid(row=0, column=0, padx=8, pady=2)
        e55.grid(row=0, column=1, padx=8, pady=2)
        e56.grid(row=0, column=2, padx=8, pady=2)
        e63.grid(row=1, column=0, padx=8, pady=2)
        e64.grid(row=1, column=1, padx=8, pady=2)
        e65.grid(row=1, column=2, padx=8, pady=2)
        e72.grid(row=2, column=0, padx=8, pady=2)
        e73.grid(row=2, column=1, padx=8, pady=2)
        e74.grid(row=2, column=2, padx=8, pady=2)
        e57.grid(row=0, column=0, padx=8, pady=2)
        e58.grid(row=0, column=1, padx=8, pady=2)
        e59.grid(row=0, column=2, padx=8, pady=2)
        e66.grid(row=1, column=0, padx=8, pady=2)
        e67.grid(row=1, column=1, padx=8, pady=2)
        e68.grid(row=1, column=2, padx=8, pady=2)
        e75.grid(row=2, column=0, padx=8, pady=2)
        e76.grid(row=2, column=1, padx=8, pady=2)
        e77.grid(row=2, column=2, padx=8, pady=2)
        e60.grid(row=0, column=0, padx=8, pady=2)
        e61.grid(row=0, column=1, padx=8, pady=2)
        e62.grid(row=0, column=2, padx=8, pady=2)
        e69.grid(row=1, column=0, padx=8, pady=2)
        e70.grid(row=1, column=1, padx=8, pady=2)
        e71.grid(row=1, column=2, padx=8, pady=2)
        e78.grid(row=2, column=0, padx=8, pady=2)
        e79.grid(row=2, column=1, padx=8, pady=2)
        e80.grid(row=2, column=2, padx=8, pady=2)

        b1 = ttk.Button(self.win, text="确定", command=self.start_solving)
        b1.pack(pady=14)

    def start_solving(self):
        num_list = []
        for e in self.es:
            rst = e.get()
            try:
                num = int(rst)
            except ValueError:
                num = 0
            num_list.append(num)
        sdk = SudokuSquare(num_list)
        rst_list = solve_square(sdk)

        self.win.lift()
        rw = ResultWindow(rst_list)
        rw.show_window()


class ResultWindow(Window):
    def __init__(self, rst_list):
        Window.__init__(self, 400, 450, "")

        self.rst_list = rst_list
        self.current_idx = 0
        self.labels = []
        self.length = len(rst_list)
        self.win.title("解法1/" + str(self.length))

        frm = tk.Frame(self.win)
        frm.pack()
        frm1 = tk.Frame(frm)
        frm2 = tk.Frame(frm)
        frm3 = tk.Frame(frm)
        frm4 = tk.Frame(frm)
        frm5 = tk.Frame(frm)
        frm6 = tk.Frame(frm)
        frm7 = tk.Frame(frm)
        frm8 = tk.Frame(frm)
        frm9 = tk.Frame(frm)
        frm1.grid(row=0, column=0, padx=15, pady=5)
        frm2.grid(row=0, column=1, padx=15, pady=5)
        frm3.grid(row=0, column=2, padx=15, pady=5)
        frm4.grid(row=1, column=0, padx=15, pady=5)
        frm5.grid(row=1, column=1, padx=15, pady=5)
        frm6.grid(row=1, column=2, padx=15, pady=5)
        frm7.grid(row=2, column=0, padx=15, pady=5)
        frm8.grid(row=2, column=1, padx=15, pady=5)
        frm9.grid(row=2, column=2, padx=15, pady=5)

        l0 = tk.Label(frm1, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[0]))
        l1 = tk.Label(frm1, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[1]))
        l2 = tk.Label(frm1, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[2]))
        l3 = tk.Label(frm2, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[3]))
        l4 = tk.Label(frm2, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[4]))
        l5 = tk.Label(frm2, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[5]))
        l6 = tk.Label(frm3, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[6]))
        l7 = tk.Label(frm3, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[7]))
        l8 = tk.Label(frm3, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[8]))
        l9 = tk.Label(frm1, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[9]))
        l10 = tk.Label(frm1, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[10]))
        l11 = tk.Label(frm1, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[11]))
        l12 = tk.Label(frm2, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[12]))
        l13 = tk.Label(frm2, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[13]))
        l14 = tk.Label(frm2, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[14]))
        l15 = tk.Label(frm3, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[15]))
        l16 = tk.Label(frm3, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[16]))
        l17 = tk.Label(frm3, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[17]))
        l18 = tk.Label(frm1, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[18]))
        l19 = tk.Label(frm1, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[19]))
        l20 = tk.Label(frm1, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[20]))
        l21 = tk.Label(frm2, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[21]))
        l22 = tk.Label(frm2, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[22]))
        l23 = tk.Label(frm2, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[23]))
        l24 = tk.Label(frm3, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[24]))
        l25 = tk.Label(frm3, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[25]))
        l26 = tk.Label(frm3, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[26]))
        l27 = tk.Label(frm4, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[27]))
        l28 = tk.Label(frm4, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[28]))
        l29 = tk.Label(frm4, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[29]))
        l30 = tk.Label(frm5, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[30]))
        l31 = tk.Label(frm5, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[31]))
        l32 = tk.Label(frm5, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[32]))
        l33 = tk.Label(frm6, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[33]))
        l34 = tk.Label(frm6, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[34]))
        l35 = tk.Label(frm6, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[35]))
        l36 = tk.Label(frm4, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[36]))
        l37 = tk.Label(frm4, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[37]))
        l38 = tk.Label(frm4, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[38]))
        l39 = tk.Label(frm5, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[39]))
        l40 = tk.Label(frm5, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[40]))
        l41 = tk.Label(frm5, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[41]))
        l42 = tk.Label(frm6, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[42]))
        l43 = tk.Label(frm6, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[43]))
        l44 = tk.Label(frm6, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[44]))
        l45 = tk.Label(frm4, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[45]))
        l46 = tk.Label(frm4, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[46]))
        l47 = tk.Label(frm4, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[47]))
        l48 = tk.Label(frm5, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[48]))
        l49 = tk.Label(frm5, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[49]))
        l50 = tk.Label(frm5, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[50]))
        l51 = tk.Label(frm6, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[51]))
        l52 = tk.Label(frm6, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[52]))
        l53 = tk.Label(frm6, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[53]))
        l54 = tk.Label(frm7, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[54]))
        l55 = tk.Label(frm7, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[55]))
        l56 = tk.Label(frm7, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[56]))
        l57 = tk.Label(frm8, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[57]))
        l58 = tk.Label(frm8, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[58]))
        l59 = tk.Label(frm8, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[59]))
        l60 = tk.Label(frm9, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[60]))
        l61 = tk.Label(frm9, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[61]))
        l62 = tk.Label(frm9, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[62]))
        l63 = tk.Label(frm7, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[63]))
        l64 = tk.Label(frm7, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[64]))
        l65 = tk.Label(frm7, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[65]))
        l66 = tk.Label(frm8, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[66]))
        l67 = tk.Label(frm8, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[67]))
        l68 = tk.Label(frm8, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[68]))
        l69 = tk.Label(frm9, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[69]))
        l70 = tk.Label(frm9, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[70]))
        l71 = tk.Label(frm9, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[71]))
        l72 = tk.Label(frm7, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[72]))
        l73 = tk.Label(frm7, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[73]))
        l74 = tk.Label(frm7, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[74]))
        l75 = tk.Label(frm8, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[75]))
        l76 = tk.Label(frm8, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[76]))
        l77 = tk.Label(frm8, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[77]))
        l78 = tk.Label(frm9, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[78]))
        l79 = tk.Label(frm9, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[79]))
        l80 = tk.Label(frm9, font=("Comic Sans MS",), text=str(self.rst_list[0].raw_info[80]))
        l0.grid(row=0, column=0, padx=8, pady=2)
        l1.grid(row=0, column=1, padx=8, pady=2)
        l2.grid(row=0, column=2, padx=8, pady=2)
        l9.grid(row=1, column=0, padx=8, pady=2)
        l10.grid(row=1, column=1, padx=8, pady=2)
        l11.grid(row=1, column=2, padx=8, pady=2)
        l18.grid(row=2, column=0, padx=8, pady=2)
        l19.grid(row=2, column=1, padx=8, pady=2)
        l20.grid(row=2, column=2, padx=8, pady=2)
        l3.grid(row=0, column=0, padx=8, pady=2)
        l4.grid(row=0, column=1, padx=8, pady=2)
        l5.grid(row=0, column=2, padx=8, pady=2)
        l12.grid(row=1, column=0, padx=8, pady=2)
        l13.grid(row=1, column=1, padx=8, pady=2)
        l14.grid(row=1, column=2, padx=8, pady=2)
        l21.grid(row=2, column=0, padx=8, pady=2)
        l22.grid(row=2, column=1, padx=8, pady=2)
        l23.grid(row=2, column=2, padx=8, pady=2)
        l6.grid(row=0, column=0, padx=8, pady=2)
        l7.grid(row=0, column=1, padx=8, pady=2)
        l8.grid(row=0, column=2, padx=8, pady=2)
        l15.grid(row=1, column=0, padx=8, pady=2)
        l16.grid(row=1, column=1, padx=8, pady=2)
        l17.grid(row=1, column=2, padx=8, pady=2)
        l24.grid(row=2, column=0, padx=8, pady=2)
        l25.grid(row=2, column=1, padx=8, pady=2)
        l26.grid(row=2, column=2, padx=8, pady=2)
        l27.grid(row=0, column=0, padx=8, pady=2)
        l28.grid(row=0, column=1, padx=8, pady=2)
        l29.grid(row=0, column=2, padx=8, pady=2)
        l36.grid(row=1, column=0, padx=8, pady=2)
        l37.grid(row=1, column=1, padx=8, pady=2)
        l38.grid(row=1, column=2, padx=8, pady=2)
        l45.grid(row=2, column=0, padx=8, pady=2)
        l46.grid(row=2, column=1, padx=8, pady=2)
        l47.grid(row=2, column=2, padx=8, pady=2)
        l30.grid(row=0, column=0, padx=8, pady=2)
        l31.grid(row=0, column=1, padx=8, pady=2)
        l32.grid(row=0, column=2, padx=8, pady=2)
        l39.grid(row=1, column=0, padx=8, pady=2)
        l40.grid(row=1, column=1, padx=8, pady=2)
        l41.grid(row=1, column=2, padx=8, pady=2)
        l48.grid(row=2, column=0, padx=8, pady=2)
        l49.grid(row=2, column=1, padx=8, pady=2)
        l50.grid(row=2, column=2, padx=8, pady=2)
        l33.grid(row=0, column=0, padx=8, pady=2)
        l34.grid(row=0, column=1, padx=8, pady=2)
        l35.grid(row=0, column=2, padx=8, pady=2)
        l42.grid(row=1, column=0, padx=8, pady=2)
        l43.grid(row=1, column=1, padx=8, pady=2)
        l44.grid(row=1, column=2, padx=8, pady=2)
        l51.grid(row=2, column=0, padx=8, pady=2)
        l52.grid(row=2, column=1, padx=8, pady=2)
        l53.grid(row=2, column=2, padx=8, pady=2)
        l54.grid(row=0, column=0, padx=8, pady=2)
        l55.grid(row=0, column=1, padx=8, pady=2)
        l56.grid(row=0, column=2, padx=8, pady=2)
        l63.grid(row=1, column=0, padx=8, pady=2)
        l64.grid(row=1, column=1, padx=8, pady=2)
        l65.grid(row=1, column=2, padx=8, pady=2)
        l72.grid(row=2, column=0, padx=8, pady=2)
        l73.grid(row=2, column=1, padx=8, pady=2)
        l74.grid(row=2, column=2, padx=8, pady=2)
        l57.grid(row=0, column=0, padx=8, pady=2)
        l58.grid(row=0, column=1, padx=8, pady=2)
        l59.grid(row=0, column=2, padx=8, pady=2)
        l66.grid(row=1, column=0, padx=8, pady=2)
        l67.grid(row=1, column=1, padx=8, pady=2)
        l68.grid(row=1, column=2, padx=8, pady=2)
        l75.grid(row=2, column=0, padx=8, pady=2)
        l76.grid(row=2, column=1, padx=8, pady=2)
        l77.grid(row=2, column=2, padx=8, pady=2)
        l60.grid(row=0, column=0, padx=8, pady=2)
        l61.grid(row=0, column=1, padx=8, pady=2)
        l62.grid(row=0, column=2, padx=8, pady=2)
        l69.grid(row=1, column=0, padx=8, pady=2)
        l70.grid(row=1, column=1, padx=8, pady=2)
        l71.grid(row=1, column=2, padx=8, pady=2)
        l78.grid(row=2, column=0, padx=8, pady=2)
        l79.grid(row=2, column=1, padx=8, pady=2)
        l80.grid(row=2, column=2, padx=8, pady=2)
        self.labels.append(l0)
        self.labels.append(l1)
        self.labels.append(l2)
        self.labels.append(l3)
        self.labels.append(l4)
        self.labels.append(l5)
        self.labels.append(l6)
        self.labels.append(l7)
        self.labels.append(l8)
        self.labels.append(l9)
        self.labels.append(l10)
        self.labels.append(l11)
        self.labels.append(l12)
        self.labels.append(l13)
        self.labels.append(l14)
        self.labels.append(l15)
        self.labels.append(l16)
        self.labels.append(l17)
        self.labels.append(l18)
        self.labels.append(l19)
        self.labels.append(l20)
        self.labels.append(l21)
        self.labels.append(l22)
        self.labels.append(l23)
        self.labels.append(l24)
        self.labels.append(l25)
        self.labels.append(l26)
        self.labels.append(l27)
        self.labels.append(l28)
        self.labels.append(l29)
        self.labels.append(l30)
        self.labels.append(l31)
        self.labels.append(l32)
        self.labels.append(l33)
        self.labels.append(l34)
        self.labels.append(l35)
        self.labels.append(l36)
        self.labels.append(l37)
        self.labels.append(l38)
        self.labels.append(l39)
        self.labels.append(l40)
        self.labels.append(l41)
        self.labels.append(l42)
        self.labels.append(l43)
        self.labels.append(l44)
        self.labels.append(l45)
        self.labels.append(l46)
        self.labels.append(l47)
        self.labels.append(l48)
        self.labels.append(l49)
        self.labels.append(l50)
        self.labels.append(l51)
        self.labels.append(l52)
        self.labels.append(l53)
        self.labels.append(l54)
        self.labels.append(l55)
        self.labels.append(l56)
        self.labels.append(l57)
        self.labels.append(l58)
        self.labels.append(l59)
        self.labels.append(l60)
        self.labels.append(l61)
        self.labels.append(l62)
        self.labels.append(l63)
        self.labels.append(l64)
        self.labels.append(l65)
        self.labels.append(l66)
        self.labels.append(l67)
        self.labels.append(l68)
        self.labels.append(l69)
        self.labels.append(l70)
        self.labels.append(l71)
        self.labels.append(l72)
        self.labels.append(l73)
        self.labels.append(l74)
        self.labels.append(l75)
        self.labels.append(l76)
        self.labels.append(l77)
        self.labels.append(l78)
        self.labels.append(l79)
        self.labels.append(l80)

        frm10 = tk.Frame(self.win)
        frm10.pack(pady=12)

        self.b1 = ttk.Button(frm10, text="<", state=tk.DISABLED, command=self.left_update)
        if self.length == 1:
            self.b2 = ttk.Button(frm10, text=">", state=tk.DISABLED, command=self.right_update)
        else:
            self.b2 = ttk.Button(frm10, text=">", command=self.right_update)
        self.b1.grid(row=0, column=0, padx=20)
        self.b2.grid(row=0, column=1, padx=20)

    def left_update(self):
        self.current_idx -= 1
        rst = self.rst_list[self.current_idx].raw_info

        self.win.title("解法" + str(self.current_idx + 1) + '/' + str(self.length))

        num_idx = 0
        for lab in self.labels:
            lab.config(text=str(rst[num_idx]))
            num_idx += 1

        if self.current_idx == 0:
            self.b1.config(state=tk.DISABLED)
        if self.current_idx == self.length - 2:
            self.b2.config(state=tk.NORMAL)

    def right_update(self):
        self.current_idx += 1
        rst = self.rst_list[self.current_idx].raw_info

        self.win.title("解法" + str(self.current_idx + 1) + '/' + str(self.length))

        num_idx = 0
        for lab in self.labels:
            lab.config(text=str(rst[num_idx]))
            num_idx += 1

        if self.current_idx == 1:
            self.b1.config(state=tk.NORMAL)
        if self.current_idx == self.length - 1:
            self.b2.config(state=tk.DISABLED)


a = MainWindow()
a.show_window()
