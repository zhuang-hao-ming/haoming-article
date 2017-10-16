
---
title: c语言认真认识static
date: 2017-09-15 22:54:44
tags:
---
        ##

[static变量和static函数](http://www.cppblog.com/dbkong/archive/2006/12/09/16169.html)

依据这篇文章作者的看法,static的功能是*访问控制*

针对于c语言来说:


```
文件main.c

#include "stdio.h"

extern int b;
extern void hello();

int main() {
	hello();
	printf("num %d\n", b);
}


```

```
文件test.c

#include "stdio.h"

void hello() {
	printf("hello\n");
}

int b = 2;

```


```
使用gcc编译链接
gcc -o main.c test.c
执行
./main
输出:
hello
num 2


```

从上面的这个例子我们看到.c语言中一个文件可以引用链接到的另一个文件中定义的变量或函数.但是要求在文件头部加上:

```
extern int b;
extern void hello();
```

*实验发现即使不加extern也得到相同的结果.*


这个声明,指示,变量和函数的定义在其它文件中.

但是,如果其它文件中的变量和函数在定义的时候使用了static

```
static void hello() {
	printf("hello\n");
}

static int b = 2;
```

则编译失败:

```
main.c:(.text+0xa): undefined reference to `hello'
main.c:(.text+0x10): undefined reference to `b'

```

*注意,我们平常使用的头文件一般只有声明,使用#include包含头文件,相当于上文中的声明,指示了当前文件去其他文件中寻找定义,如果头文件中的声明是static,那么仍会编译失败(实现和声明一致也一定是static).不过如果头文件中直接包含定义,那么相当于在文件内部定义函数,编译可以成功*


##

在函数内部声明静态变量,扩展变量的生存周期,从第一次调用,到程序结束.但是作用域没有变.


[C 语言中static用法总结](http://www.swanlinux.net/2013/05/16/c_static/)这篇文章指出了静态函数的优点:

> C 语言中使用静态函数的好处:
> 
> 静态函数会被自动分配在一个一直使用的存储区，知道退出应用程序实例，避免了调用函数时压栈出栈，速度快很多.

> 关键字 “static” ，译成中文就是”静态的”， 所以内部函数又称静态函数，但此处”static” 的含义不是指存储方式，而是指对函数的作用域仅局限于本文件.
> 

