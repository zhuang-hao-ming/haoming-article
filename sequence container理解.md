
---
title: sequence container理解
date: 2017-09-15 22:54:44
tags:
---
        ## vector

`vector`是一个`sequence container`，它使用一片连续的内存，它是一个大小自动增长的数组。

`vector`的运行模式:
1. 向`vector`中插入元素时，如果`vector`对应的内存已满
    1. 重新分配一片大小为原来两倍的内存，如果是第一次插入分配1。
    2. 将插入位置前的元素复制到新内存位置（直接内存复制还是调用构造函数，二者的性能差异）。
    3. 插入新元素。
    4. 将插入位置后的元素复制到新内存位置。
    5. 析构并归还原来的内存。
2. `vector`的内部数据只有3个指针
    1. start指向首元素。
    2. finish指向最后一个元素的后一个位置。
    3. end_of_storage指向存储空间的最后一个位置的下一个位置。（这是因为vecotr每次分配内存的大小是原本内存大小的两倍）
3. 根据`vector`的性质,`vector::iterator`可以设计为一个`T*`,也可以提供一个`T*`的`adapter`来作为`vector::iterator`。

## array

`array`是一个`sequence container`，它使用一片连续的内存，它的行为和语言内部的数组相比并无二致。它是数组的一个容器包装，提供容器接口。

## deque

`deque`是一个`sequence container`, 它在逻辑上是连续的，它的设计如下

1. `deque`使用多段小内存(`buffer`)，`buffer`的长度固定，`buffer`的首地址被保存在一个vector中(称为`map`)
2. `buffer`大小的确定方法:`sizeof(node) < 512 : 512 / sizeof(node) : 1`
3. `deque`的`iterator`的数据结构由4个指针组成
    1. cur: 指向当前元素
    2. first： 指向元素所在`buffer`的头部
    3. last: 指向元素所在`buffer`的尾部
    4. node: 指向元素所在`buffer`的指针所在的`map`元素
4. 插入元素
    1. 在头部插入元素
        1. 由`start iterator`的`node`，确定要插入的`buffer`,然后在`start iterator`的`cur`前放入元素，更改`start iterator`
        2. 如果该`buffer`已满， 分配一个新`buffer`， 将`buffer`的地址保存到`map`的头部， 在新`buffer`的尾部放入元素。
    2. 在尾部插入元素
        1. 由`finish iterator`的`node`，确定要插入的`buffer`,然后在`finish iterator`的`cur`处放入元素,更改`finish iterator`
        2. 如果`finish iterator`的`cur`无效， 分配一个新的`buffer`，将`buffer`地址保存到`map`尾部，在新`buffer`头部放入元素。
    3. 在其它位置插入元素
        1. 确定插入位置到`deque`头部或者尾部的距离
        2. 如果到`deque`的头部近，在`deque`头部插入一个位置，然后将`front`到插入位置整体向前搬移,在空出来的位置放入元素
        3. 如果到`deque`的尾部近，在`deque`尾部插入一个元素，然后将插入位置到`back`整体向后搬移，在空出来的位置放入元素

模拟连续空间

`deque`在内存布局上是不连续的，但是在逻辑使用上，对于用户来说，它是连续的。它重载`iterator`的操作，使得它的行为表现的和连续内存容器相同。

模拟连续的做法：

1. `operator-`： 连续内存容器可以计算两个`iterator`之间的地址差(中间的元素个数)，为了模拟这个行为，在`deque`中两个`iterator`的距离可以根据`iterator`跨越的`buffer`个数，和开始`iterator`的`cur`到`last`的距离，再加上结束`iterator`的`first`到`cur`的距离。
2. `operator++`, `operator--`: 连续内存容器的`iteraotr`可以通过`++`或者`--`得到相邻的`iterator`， 在`deque`中为了模拟这个行为，需要考虑`++`和`--`跨越`buffer`的情况。(注意` prefix ++(--) `和`postfix ++(--)`的区别)。
3. `operator+=`, `operator+`, `operator-=`, `operator-`, 这4个操作符的行为类似，只要设计一个`operator+=`，其它的操作可以调用`operator+=`来完成。`operatpr+=`返回一个指向新位置的`operator`，需要考虑跨越多个buffer的情况，为了便于考虑，可以先假想cur在buffer头部。（注意，`operator+=`是操作后复制，所以可以直接返回自身，而`operaotr+`应该返回新元素）。

## stack queue

`stack`和`queue`是`deque`的适配器。

由于`stack`和`queue`有操作规定*先进后出*或者*先进先出*，所以这两种容器都没有iterator。

根据`stack`和`queue`的接口行为也可以使用`list`作为底层容器。

`stack`还可以选择`queue`作为底层容器。



