
---
title: cpp std 认识
date: 2017-09-15 22:54:44
tags:
---
        cpp标准库`(std)`是cpp编译器附带的一组头文件。它的组成：

1. 标准模版库`stl(standard template library)`
2. c 标准库
3. 其它

这一组头文件具有以下特点:

1. 不含文件扩展名`.h` `#include <vector>`
2. 原本属于c标准库的那些头文件的命名为`c${oldFileNameWithoutExtensioName}` `#include <cstdlib>`
3. 原本属于c标准库的那些头文件的命名仍然可用`oldFileNameWithExtension` `#include <stdlib.h>`
4. 在windows下可以观察到，1,2的保存目录是编译器的包含目录`C:\app\vs_2015\VC\include`，3的保存目录是操作系统的包含目录`C:\Program Files (x86)\Windows Kits\10\Include\10.0.10150.0\ucrt`。
5. 推荐使用1,2。

## stl

`stl`是`std`最重要的组成部分，`stl`由6个部分组成。

1. 容器(`container`)
2. 分配器(`allocator`)
3. 算法(`algorithm`)
4. 迭代器(`iterator`)
5. 适配器(`adapter`)
6. 函数对象(`functor`)

这6个部分互相联系构成一个整体。
1. 容器是`模板类`,是数据结构，负责元素的保存。
2. 分配器为容器提供内存管理。
3. 算法是`模板函数`，算法为了访问容器中的元素，需要使用和指针功能类似的迭代器，还需要函数对象来指定具体的操作（排序中如何比较大小）。`less<int>()`
4. 适配器将容器变为另外一种满足特定要求的容器（`stack`和`queue`），将函数对象变为另外一种函数对象(`bind2nd(less<int>(), 40)`)。以上，`stack`和`queue`是容器适配器，`bind2nd(less<int>(), 40)`的返回值是函数对象适配器。可以认为容器适配器是一种容器，函数对象适配器是一种函数对象。

```
1.
#include <vector>
#include <iostream>
#include <algorithm>
#include <functional>
using std::vector; // vector
using std::allocator; // vector
using std::cout;// iostream
using std::endl;// iostream
using std::count_if; // algorithm
using std::less;// functional
using std::bind2nd;// functional
using std::not1;// functional
int main()
{
	int arr[7] = { 1, 2, 3, 41, 42, 43, 44 };
	vector<int, allocator<int>> vec{ arr, arr + 7 };
	cout << count_if(vec.begin(), vec.end(), not1(bind2nd(less<int>(), 40))) << endl;
}

```

代码1.展示了`stl`6种部件的使用。

## 容器

stl中的容器分为两大类`sequence container`和`associative container`。

`sequence container`的特点是，容器内部的元素是有序的，可以进行排序操作。

`associative container`的特点是，容器内部的元素是无序的（树结构，stl使用高度平衡的红黑树实现，查找效率高），主要用来进行查找操作。

1. `sequence container`
    1. `array`: `array`是对语言的array的封装，使它具有容器的接口。它使用一段**大小固定的连续内存**。
    2. `vector`: `vector`使用一段**连续内存**,当内存不足以容纳新元素时，容器会重新申请一段**大小为原来两倍的连续内存**，然后将元素整体复制过去。`vector`只能在尾部单向增长。
    3. `deque`： `deque`使用一段**逻辑连续的内存(deque实际上使用多段小的连续内存称为buffer，buffer的指针被保存在列表之中，由于列表是有序的而且buffer的内存是连续的，所以在逻辑上整个内存是连续的。)**`deque`可以在头尾双向增长。当内存不足时在头部或者尾部插入新的buffer。
    4. `list`：`list`是双向链表。使用*不连续的内存*。
    5. `forward_list`: `forward_list`是单向链表。使用*不连续内存*。由于`forward_list`是单向链表，只有`头指针`所以`back()`和`size()`的成本较高，容器也不提供这两个接口。由于`forward_list`中每个元素只有一个指针和`list`相比节约了很多内存。
2. `associative container`
    1. `set`: `set`是一个集合容器，它只有键没有值（或者说键值一体）。`set`中的键不可以重复，如果重复插入相同的键，程序会自动忽视后一个插入。`set`内部自行实现了`find`比`algorithm`中的`find`性能高。
    2. `multiset`: `multiset`和`set`类似，但是内部的元素可以相同。
    3. `map`： `map`是一个字典容器，使用`pair<long,string>(i,string(buf))`作为元素类型。调用`pair.first`访问元素的键，调用`pair.second`访问元素的值。`map`重载了`[]`可以使用`[]`像数组一样进行元素存取(`multimap`没有)。和`set`一样内部自行实现了`find`。
    4. `multimap`： `multimap`和`map`类似，但是`multimap`没有重载`[]`，内部键可以重复。
    5. `unordered_set`
    6. `unordered_map`
    7. `unordered_multiset`
    8. `unordered_multimap`
3. 5,6,7,8这4中容器和对应的版本类似，但是使用`hashtable`实现。

