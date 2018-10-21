#! /usr/bin/env python
# -*- coding: utf-8 -*-

# import time
import tkinter.ttk as ttk
import tkinter.font as tkFont
import logging
import datetime
import binascii
import platform
# import threading
import tkinter as tk
# import SerialHelper
from MainFrm import MainFrame

# import tkFont
# import Tkinter as tk
# from UI.MainFrm import MainFrame
# from Utils.SerialHelper import SerialHelper

# 根据系统 引用不同的库
if platform.system() == "Windows":
    from serial.tools import list_ports
else:
    import glob
    import os
    import re

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

# 结束符（16进制）CR 13(\r - 0x0D); NL(LF) 10(\n - 0x0A)
END_HEX = "0D0A"


class MainSerialTool(MainFrame):
    '''
    main func class
    '''

    def __init__(self, master=None):
        super(MainSerialTool, self).__init__(master)
        self.root = master

        self.serial_receive_count = 0
        self.serial_recieve_data = ""
        self.serial_listbox = list()

        self.find_all_devices()

    def find_all_devices(self):
        '''
        线程检测连接设备的状态
        '''
        self.find_all_serial_devices()
        self.start_thread_timer(self.find_all_devices, 1)

    def find_all_serial_devices(self):
        '''
        检查串口设备
        '''
        try:
            if platform.system() == "Windows":
                self.temp_serial = list()
                for com in list(list_ports.comports()):
                    try:
                        strCom = com[0].encode(
                            "utf-8") + ": " + com[1][:-7].encode("utf-8")
                    except:
                        strCom = com[0] + ": " + \
                            com[1][:-7].decode("gbk").encode("utf-8")
                    self.temp_serial.append(strCom)
                for item in self.temp_serial:
                    if item not in self.serial_listbox:
                        self.serial_frm.frm_left_listbox.insert("end", item)
                for item in self.serial_listbox:
                    if item not in self.temp_serial:
                        size = self.serial_frm.frm_left_listbox.size()
                        index = list(self.serial_frm.frm_left_listbox.get(
                            0, size)).index(item)
                        self.serial_frm.frm_left_listbox.delete(index)

                self.serial_listbox = self.temp_serial

            elif platform.system() == "Linux":
                self.temp_serial = list()
                self.temp_serial = self.find_usb_tty()
                for item in self.temp_serial:
                    if item not in self.serial_listbox:
                        self.serial_frm.frm_left_listbox.insert("end", item)
                for item in self.serial_listbox:
                    if item not in self.temp_serial:
                        index = list(self.serial_frm.frm_left_listbox.get(
                            0, self.serial_frm.frm_left_listbox.size())).index(item)
                        self.serial_frm.frm_left_listbox.delete(index)
                self.serial_listbox = self.temp_serial
        except Exception as e:
            logging.error(e)

    def Toggle(self, event=None):
        '''
        打开/关闭 设备
        '''
        self.serial_toggle()

    def Send(self):
        '''
        发送数据
        '''
        self.serial_send()

    def SerialClear(self):
        '''
        clear serial receive text
        '''
        self.serial_receive_count = 0
        self.serial_frm.frm_right_receive.delete("0.0", "end")

    def serial_toggle(self):
        '''
        打开/关闭串口设备
        '''
        if self.serial_frm.frm_left_btn["text"] == "Open":
            try:
                serial_index = self.serial_frm.frm_left_listbox.curselection()
                if serial_index:
                    self.current_serial_str = self.serial_frm.frm_left_listbox.get(
                        serial_index).encode("utf-8")
                else:
                    self.current_serial_str = self.serial_frm.frm_left_listbox.get(
                        self.serial_frm.frm_left_listbox.size() - 1).encode("utf-8")

                if platform.system() == "Windows":
                    self.port = self.current_serial_str.split(":")[0]
                elif platform.system() == "Linux":
                    self.port = self.current_serial_str
                self.baudrate = self.serial_frm.frm_left_combobox_baudrate.get()
                self.parity = self.serial_frm.frm_left_combobox_parity.get()
                self.databit = self.serial_frm.frm_left_combobox_databit.get()
                self.stopbit = self.serial_frm.frm_left_combobox_stopbit.get()
                self.ser = SerialHelper(Port=self.port,
                                        BaudRate=self.baudrate,
                                        ByteSize=self.databit,
                                        Parity=self.parity,
                                        Stopbits=self.stopbit)
                self.ser.on_connected_changed(self.serial_on_connected_changed)
            except Exception as e:
                logging.error(e)
                try:
                    self.serial_frm.frm_status_label["text"] = "Open [{0}] Failed!".format(
                        self.current_serial_str)
                    self.serial_frm.frm_status_label["fg"] = "#DC143C"
                except Exception as ex:
                    logging.error(ex)

        elif self.serial_frm.frm_left_btn["text"] == "Close":
            self.ser.disconnect()
            self.serial_frm.frm_left_btn["text"] = "Open"
            self.serial_frm.frm_left_btn["bg"] = "#008B8B"
            self.serial_frm.frm_status_label["text"] = "Close Serial Successful!"
            self.serial_frm.frm_status_label["fg"] = "#8DEEEE"

    def get_threshold_value(self, *args):
        '''
        get threshold value
        '''
        try:
            self.ser.threshold_value = int(self.serial_frm.threshold_str.get())
        except:
            pass

    def serial_send(self):
        '''
        串口数据发送 CR 13; NL(LF) 10
        '''
        send_data = self.serial_frm.frm_right_send.get("0.0", "end").strip()
        if self.serial_frm.new_line_cbtn_var.get() == 1:  # 是否添加换行符
            send_data = send_data + "\r\n"

        logging.info(">>>" + str(send_data))
        if self.serial_frm.send_hex_cbtn_var.get() == 1:  # 是否使用16进制发送
            send_data = send_data.replace(" ", "").replace("\n", "0A").replace("\r", "0D")
            self.ser.write(send_data, True)
        else:
            self.ser.write(send_data)

    def serial_on_connected_changed(self, is_connected):
        '''
        串口连接状态改变回调
        '''
        if is_connected:
            self.ser.connect()
            if self.ser._is_connected:
                self.serial_frm.frm_status_label["text"] = "Open [{0}] Successful!".format(
                    self.current_serial_str)
                self.serial_frm.frm_status_label["fg"] = "#66CD00"
                self.serial_frm.frm_left_btn["text"] = "Close"
                self.serial_frm.frm_left_btn["bg"] = "#F08080"
                self.ser.on_data_received(self.serial_on_data_received)
            else:
                self.serial_frm.frm_status_label["text"] = "Open [{0}] Failed!".format(
                    self.current_serial_str)
                self.serial_frm.frm_status_label["fg"] = "#DC143C"
        else:
            self.ser.disconnect()
            self.serial_frm.frm_left_btn["text"] = "Open"
            self.serial_frm.frm_left_btn["bg"] = "#008B8B"
            self.serial_frm.frm_status_label["text"] = "Close Serial Successful!"
            self.serial_frm.frm_status_label["fg"] = "#8DEEEE"

    def serial_on_data_received(self, data):
        '''
        串口接收数据回调函数
        '''
        self.serial_recieve_data += data
        self.serial_recieve_data_hex = binascii.hexlify(
            self.serial_recieve_data).upper()

        # 当接收到的数据达到阈值或者以结束符结束时
        if self.ser.threshold_value <= len(self.serial_recieve_data) or self.serial_recieve_data_hex.endswith(END_HEX):
            if self.serial_frm.receive_hex_cbtn_var.get() == 1:
                self.serial_frm.frm_right_receive.insert("end", "[" + str(datetime.datetime.now()) + " - "
                                                         + str(self.serial_receive_count) + "]:\n", "green")
                data_str = " ".join([hex(ord(x))[2:].upper().rjust(
                    2, "0") for x in self.serial_recieve_data])
                logging.info("<<<" + str(data_str))
                self.serial_frm.frm_right_receive.insert(
                    "end", data_str + "\n")
                self.serial_frm.frm_right_receive.see("end")
            else:
                self.serial_frm.frm_right_receive.insert("end", "[" + str(datetime.datetime.now()) + " - "
                                                         + str(self.serial_receive_count) + "]:\n", "green")
                self.serial_frm.frm_right_receive.insert(
                    "end", self.serial_recieve_data + "\n")
                logging.info("<<<" + str(self.serial_recieve_data))
                self.serial_frm.frm_right_receive.see("end")
            self.serial_receive_count += 1
            self.serial_recieve_data = ""

    def find_usb_tty(self, vendor_id=None, product_id=None):
        '''
        查找Linux下的串口设备
        '''
        tty_devs = list()
        for dn in glob.glob('/sys/bus/usb/devices/*'):
            try:
                vid = int(open(os.path.join(dn, "idVendor")).read().strip(), 16)
                pid = int(open(os.path.join(dn, "idProduct")).read().strip(), 16)
                if ((vendor_id is None) or (vid == vendor_id)) and ((product_id is None) or (pid == product_id)):
                    dns = glob.glob(os.path.join(
                        dn, os.path.basename(dn) + "*"))
                    for sdn in dns:
                        for fn in glob.glob(os.path.join(sdn, "*")):
                            if re.search(r"\/ttyUSB[0-9]+$", fn):
                                tty_devs.append(os.path.join(
                                    "/dev", os.path.basename(fn)))
            except Exception as ex:
                pass
        return tty_devs


if __name__ == '__main__':
    '''
    main loop
    '''
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.geometry()
    root.title("Serial Tool")

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

    app = MainSerialTool(root)
    root.mainloop()
