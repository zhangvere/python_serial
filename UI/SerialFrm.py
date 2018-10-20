#! /usr/bin/env python
# -*- coding: utf-8 -*-

# import Tkinter as tk
# import ttk
# import tkFont
import tkinter.ttk as ttk
import tkinter.font as tkFont
import tkinter as tk
import PyTkinter as pytk

g_font = ('Monaco', 12)

class SerialFrame(object):
    '''
    Serial窗体
    '''

    def __init__(self, master=None):
        '''
        初始化
        '''
        self.root = master
        self.create_frame()

    def create_frame(self):
        '''
        创建窗体，分为上下2个部分，下半部分为状态栏
        '''
        self.frm = pytk.PyFrame(self.root)

        self.frm_top = pytk.PyLabelFrame(self.frm)
        self.frm_status = pytk.PyLabelFrame(self.frm)

        self.frm_top.pack(fill="both", expand=1)
        self.frm_status.pack(fill="both", expand=0)

        self.create_frm_top()
        self.create_frm_status()

    def create_frm_top(self):
        '''
        上半部分窗口分为左右2个部分
        '''
        self.frm_left = pytk.PyLabelFrame(self.frm_top)
        self.frm_right = pytk.PyLabelFrame(self.frm_top)

        self.frm_left.pack(fill="both", expand=0, padx=2, pady=5, side=tk.LEFT)
        self.frm_right.pack(fill="both", expand=1, padx=2, pady=5, side=tk.RIGHT)

        self.create_frm_left()
        self.create_frm_right()

    def create_frm_left(self):
        '''
        上半部分左边窗口：
        Listbox显示连接的USB设备
        Button按钮点击连接设备
        '''
        self.frm_left_label = pytk.PyLabel(self.frm_left,
                                           text="Serial Ports",
                                           font=g_font,
                                           anchor="w")
        self.frm_left_listbox = pytk.PyListbox(self.frm_left,
                                               font=g_font)
        self.frm_left_serial_set = pytk.PyLabelFrame(self.frm_left)
        self.frm_left_btn = pytk.PyButton(self.frm_left,
                                          text="Open",
                                          font=g_font,
                                          command=self.Toggle)

        self.frm_left_label.pack(fill="both", expand=0, padx=5, pady=5)
        self.frm_left_listbox.pack(fill="both", expand=1, padx=5, pady=5)
        self.frm_left_serial_set.pack(fill="both", expand=0, padx=5, pady=5)
        self.frm_left_btn.pack(fill="both", expand=0, padx=5, pady=5)

        self.frm_left_listbox.bind("<Double-Button-1>", self.Open)
        self.create_frm_left_serial_set()

    def create_frm_left_serial_set(self):
        '''
        串口配置，比如波特率，奇偶校验等
        '''
        setting_label_list = ["BaudRate :", "Parity :", "DataBit :", "StopBit :"]
        baudrate_list = ["1200", "2400", "4800", "9600", "14400", "19200", "38400",
                         "43000", "57600", "76800", "115200"]
        # PARITY_NONE, PARITY_EVEN, PARITY_ODD PARITY_MARK, PARITY_SPACE
        parity_list = ["N", "E", "O", "M", "S"]
        bytesize_list = ["5", "6", "7", "8"]
        stopbits_list = ["1", "1.5", "2"]

        self.frm_left_left = pytk.PyFrame(self.frm_left_serial_set)
        self.frm_left_right = pytk.PyFrame(self.frm_left_serial_set)
        self.frm_left_left.pack(fill="both", expand=1, side=tk.LEFT)
        self.frm_left_right.pack(fill="both", expand=1, side=tk.RIGHT)

        for item in setting_label_list:
            frm_left_label_temp = pytk.PyLabel(self.frm_left_left, 
                                               text=item,
                                               font=g_font)
            frm_left_label_temp.pack(fill="both", expand=1, padx=5, pady=5)

        self.frm_left_combobox_baudrate = ttk.Combobox(self.frm_left_right,
                                                       width=15,
                                                       font=g_font,
                                                       values=baudrate_list)
        self.frm_left_combobox_parity = ttk.Combobox(self.frm_left_right,
                                                       width=15,
                                                       font=g_font,
                                                       values=parity_list)
        self.frm_left_combobox_databit = ttk.Combobox(self.frm_left_right,
                                                       width=15,
                                                       font=g_font,
                                                       values=bytesize_list)
        self.frm_left_combobox_stopbit = ttk.Combobox(self.frm_left_right,
                                                       width=15,
                                                       font=g_font,
                                                       values=stopbits_list)
        self.frm_left_combobox_baudrate.pack(fill="both", expand=1, padx=5, pady=5)
        self.frm_left_combobox_parity.pack(fill="both", expand=1, padx=5, pady=5)
        self.frm_left_combobox_databit.pack(fill="both", expand=1, padx=5, pady=5)
        self.frm_left_combobox_stopbit.pack(fill="both", expand=1, padx=5, pady=5)

        self.frm_left_combobox_baudrate.current(3)
        self.frm_left_combobox_parity.current(0)
        self.frm_left_combobox_databit.current(3)
        self.frm_left_combobox_stopbit.current(0)

    def create_frm_right(self):
        '''
        上半部分右边窗口：
        分为4个部分：
        1、Label显示和重置按钮和发送按钮
        2、Text显示（发送的数据）
        3、Label显示和十进制选择显示和清除接收信息按钮
        4、Text显示接收到的信息
        '''
        self.frm_right_reset = pytk.PyLabelFrame(self.frm_right)
        self.frm_right_send = pytk.PyText(self.frm_right,
                                          font=g_font,
                                          width=60,
                                          height=5)
        self.frm_right_clear = pytk.PyLabelFrame(self.frm_right)
        self.frm_right_receive = pytk.PyText(self.frm_right,
                                             font=g_font,
                                             width=60,
                                             height=15)

        self.frm_right_reset.pack(fill="both", expand=0, padx=1)
        self.frm_right_send.pack(fill="both", expand=1, padx=1)
        self.frm_right_clear.pack(fill="both", expand=0, padx=1)
        self.frm_right_receive.pack(fill="both", expand=1, padx=1)

        self.frm_right_receive.tag_config("green", foreground="#228B22")

        self.create_frm_right_reset()
        self.create_frm_right_clear()

    def create_frm_right_reset(self):
        '''
        1、Label显示和重置按钮和发送按钮
        '''
        self.frm_right_reset_label = pytk.PyLabel(self.frm_right_reset,
                                                  text="Hex Bytes",
                                                  font=g_font,
                                                  anchor="w")
        self.frm_right_reset_btn = pytk.PyButton(self.frm_right_reset,
                                                 text="Reset",
                                                 width=10,
                                                 font=g_font,
                                                 command=self.Reset)
        self.frm_right_send_btn = pytk.PyButton(self.frm_right_reset,
                                                text="Send",
                                                width=10,
                                                font=g_font,
                                                command=self.Send)

        self.new_line_cbtn_var = tk.IntVar()
        self.send_hex_cbtn_var = tk.IntVar()
        self.frm_right_reset_newLine_checkbtn = pytk.PyCheckbutton(self.frm_right_reset,
                                                                   text="New Line",
                                                                   variable=self.new_line_cbtn_var,
                                                                   font=g_font)
        self.frm_right_reset_hex_checkbtn = pytk.PyCheckbutton(self.frm_right_reset,
                                                               text="Hex",
                                                               variable=self.send_hex_cbtn_var,
                                                               font=g_font)

        self.frm_right_reset_label.pack(fill="both", expand=1, padx=5, pady=5, side=tk.LEFT)
        self.frm_right_reset_newLine_checkbtn.pack(fill="both", expand=0, padx=5, pady=5, side=tk.LEFT)
        self.frm_right_reset_hex_checkbtn.pack(fill="both", expand=0, padx=5, pady=5, side=tk.LEFT)
        self.frm_right_reset_btn.pack(fill="both", expand=0, padx=5, pady=5, side=tk.LEFT)
        self.frm_right_send_btn.pack(fill="both", expand=0, padx=5, pady=5, side=tk.RIGHT)

    def create_frm_right_clear(self):
        '''
        3、Label显示和清除接收信息按钮
        '''
        self.checkValue = tk.IntVar()
        self.frm_right_clear_label = pytk.PyLabel(self.frm_right_clear,
                                                  text="Data Received",
                                                  anchor="w",
                                                  font=g_font)
        self.frm_right_threshold_label = pytk.PyLabel(self.frm_right_clear,
                                                      text="Threshold:",
                                                      font=g_font)

        self.threshold_str = tk.StringVar()
        self.frm_right_threshold_entry = pytk.PyEntry(self.frm_right_clear,
                                                      textvariable=self.threshold_str,
                                                      width=6,
                                                      font=g_font)

        self.receive_hex_cbtn_var = tk.IntVar()
        self.frm_right_hex_checkbtn = pytk.PyCheckbutton(self.frm_right_clear,
                                                         text="Hex",
                                                         variable=self.receive_hex_cbtn_var,
                                                         relief="flat",
                                                         font=g_font)

        self.frm_right_clear_btn = pytk.PyButton(self.frm_right_clear,
                                                 text="Clear",
                                                 width=10,
                                                 font=g_font)

        self.frm_right_clear_label.pack(fill="both", expand=1, padx=5, pady=5, side=tk.LEFT)
        self.frm_right_threshold_label.pack(fill="both", expand=0, padx=5, pady=5, side=tk.LEFT)
        self.frm_right_threshold_entry.pack(fill="both", expand=0, padx=5, pady=5, side=tk.LEFT)
        self.frm_right_hex_checkbtn.pack(fill="both", expand=0, padx=5, pady=5, side=tk.LEFT)
        self.frm_right_clear_btn.pack(fill="both", expand=0, padx=5, pady=5, side=tk.RIGHT) 

    def create_frm_status(self):
        '''
        下半部分状态栏窗口
        '''
        self.frm_status_label = pytk.PyLabel(self.frm_status,
                                             text="Ready",
                                             font=g_font)
        self.frm_status_label.grid(row=0, column=0, padx=5, pady=5, sticky="wesn")

    def Toggle(self):
        pass

    def Open(self, event):
        pass

    def Reset(self):
        self.frm_right_send.delete("0.0", "end")

    def Send(self):
        pass

if __name__ == '__main__':
    '''
    main loop
    '''
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.geometry()

    monacofont = tkFont.Font(family="Monaco", size=16)
    root.option_add("*TCombobox*Listbox*background", "#292929")
    root.option_add("*TCombobox*Listbox*foreground", "#FFFFFF")
    root.option_add("*TCombobox*Listbox*font", monacofont)

    root.configure(bg="#292929")
    combostyle = ttk.Style()
    combostyle.theme_use('default')
    combostyle.configure("TCombobox",
                         selectbackground="#292929",
                         fieldbackground="#292929",
                         background="#292929",
                         foreground="#FFFFFF")

    app = SerialFrame(root)
    app.frm.pack(fill="both", expand=1)
    root.mainloop()
