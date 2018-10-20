Serial Tool
================================================================

master分支使用Python2.7

用python(2.7)、Tkinter、pyserial(3.3)模块开发的串口调试工具

串口工具和USB整合在一起地址：
* [SlaveDebugTool](https://git.oschina.net/jakey.chen/SlaveDebugTool)

python3版本分支地址：
* [Serial Tool - python3](https://gitee.com/jakey.chen/Serial-Tool/tree/py3/)

安装使用
================================================================

需要安装的模块：

# 在Windows下:

默认是有安装Tkinter的，因此只需要安装pyserial

可以通过pip来安装：
>pip install pyserial

* [点此下载源码或者whl(以pyserial-3.4-py2.py3-none-any.whl举例)安装](https://pypi.python.org/pypi/pyserial)
        
>python setup.py install

>pip install wheel

>pip install pyserial-3.4-py2.py3-none-any.whl

* [或者pythonlibs下载对应版本的whl安装](http://www.lfd.uci.edu/~gohlke/pythonlibs)

# 在Ubuntu下：

默认是没有安装Tkinter的，需要先进行必要模块的安装

使用apt-get安装tk

>sudo apt-get install python-tk

pyserial可以通过pip来安装:

>sudo apt-get install python-pip

>pip install pyserial

* [点此下载源码或者whl(以pyserial-3.4-py2.py3-none-any.whl举例)安装](https://pypi.python.org/pypi/pyserial)
        
>python setup.py install

>pip install wheel

>pip install pyserial-3.4-py2.py3-none-any.whl

* [或者pythonlibs下载对应版本的whl安装](http://www.lfd.uci.edu/~gohlke/pythonlibs)

执行python main.py即可开始使用(ubuntu下需要使用root权限 sudo python main.py)

>python main.py

>sudo python main.py

![](http://git.oschina.net/jakey.chen/Serial-Tool/raw/master/Images/serial_tool.png)

确认通讯是否正常
================================================================

将连接串口RX TX短接，如果是常见的USB转串口线，将2和3短接（上排5下排4，上排第2和3）。这样串口会原样返回发送的命令。


使用技巧
================================================================

在左侧列表框，可以显示出当前连接的串口设备。

可以通过双击打开设备（或者点击下面的Open打开设备）

状态栏会有相应的提示信息

点击Clear可以清除计数和接收的数据

New Line默认添加 "\r\n"，判断结束标记也为 "\r\n"，默认阈值为 1，请按自己需求更改

其他待定，暂使用良好，暂未发现Bug和需要改进的地方，若需新功能请自行按需添加修改。
