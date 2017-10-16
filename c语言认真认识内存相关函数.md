
---
title: c语言认真认识内存相关函数
date: 2017-09-15 22:54:44
tags:
---
        [realloc 用法](http://blog.csdn.net/snlying/article/details/4005238)

[ C/C++ 动态存储分配 malloc calloc realloc函数的用法与区别](http://blog.csdn.net/zhangxiao93/article/details/43966425)

[cppreference.com](http://zh.cppreference.com/w/c/memory/realloc)




```
stdlib.h

void* realloc(void* ptr, size_t new_size);
void* malloc(size_t size);
void* calloc(size_t n_ele, size_t ele_size);

```

realloc函数用于扩展内存.扩展意味着,内存的内容没有改变.当然具体的行为根据堆内存的情况有差异.

注意:

*new_size不能为0, 会导致不确定行为*

*ptr可以为NULL,那么函数的行为和malloc一致*

*返回的地址可能和ptr一样也可能不同,这由堆的内存情况决定,如果在ptr后面有足够的内存空间那么,地址相同,否则会重新开辟一片内存,原本的内存会被释放*

*新分配的内存是未定义(初始化)的*

##

malloc分配size大小的内存

注意:

*分配的内存是未初始化的*


##

calloc分配 n_ele * ele_size 大小的内存

注意:

*分配的内存是初始化为0的*


## 内存泄露检测工具

```
$ sudo apt-get install valgrind

$ valgrind --leak-check=full ./leptjson_test 
```

