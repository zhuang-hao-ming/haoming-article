
---
title: gdb调试初探
date: 2017-09-15 22:54:44
tags:
---
        
[ 用GDB调试程序（一）](http://blog.csdn.net/haoel/article/details/2879)

陈皓在这篇文章中概略地介绍了gdb的使用方法,总的来说有如下几步

1. 使用gcc的`-g`参数编译文件,是目标文件中带有*调试信息(函数名,变量名等)*.
2. gdb的使用
    1. gdb main 启动调试
    2. l 列出源代码(list)
    3. break 16 在源代码的第16行打断点
    4. break func 在函数func的第一行代码打断点
    5. info break 查看断点信息
    6. r 开始运行程序到断点处(run) *第一次用r以后用c*
    7. c 继续运行程序到断点出(continue)
    8. p i 打印变量i的值(print)
    9. n 单步执行 (next)
    10. bt 查看函数堆栈
    11. finish 退出函数*如果当前是函数堆栈中的唯一一个函数,那么无法退出*
    12. q 退出gdb程序











[linux下生成core dump文件方法及设置](http://www.cppblog.com/kongque/archive/2011/03/07/141262.aspx)
这篇文章介绍了*core dump*文件的概念.


