
---
title: bitmap allocator原理
date: 2017-09-15 22:54:44
tags:
---
        可以将内存分配器分成两大类，普通型和智能型。

普通型的内存分配器，使用`operator new`和`operator delete`或者`malloc`和`free`来进行内存的分配和释放。它的好处在于可以保证在不同的操作系统和硬件上都可用。

智能型的内存分配器，使用内存池减少了对`malloc`等的调用，去除内存块的cookie。有多种智能的内存分配器。

1. pool allocator:
2. bitmap allocator
3. debug allocator
4. array allocator







`bitmap allocator`是gnu c中的一个内存分配器。本文介绍它的运作原理。

1. 一个`bitmap allocator`负责一种`value type`的内存管理（例如，负责`double`或者`int`）,不同的`value type`即使大小相同也由不同的`bitmap allocator`管理。
2. `bitmap allocator`内部有`mini-vecotr`和`freelist`两个vector容器用于保存内存块的指针。
3. `bitmap allocator`第一次申请的内存块为64个`block`（每个`block`的大小为`sizeof(value type)`）,为了管理64个`block`的使用还需要64`bit`来标识`block`是否可用，所以还需要8个`bytes`(两个`unsigned int`)，为了方便内存的回收还需要一个`unsigned int`来记录使用的`block`的数目。以上的这些内存合称为`super block`，`super block`前面还有一个`unsigned int`记录整个`super block`的大小。
4. 每当一个`block`被分配出去以后，对应的`bit`也将被设置为0。*注意，bitmap的顺序从高地址到低地址，block的顺序从低地址到高地址*。
5. `mini-vector`中的元素有两个指针，一个指向第一个block一个指向最后一个block。
6. 如果第一个`super block`被使用完了，此时将分配一个`128`个block的`super block`，以此类推，每次新分配的block数目都是前一次的两倍。`mini-vecotr`中也将插入新的元素指向新分配的内存块。*用户每次申请内存都从mini-vecotr的最后一个元素获得，即使前面的元素，因为回收已经有可用block了，此举可能是为了加快全回收的进度*
7. 如果出现一个`super block`被全回收了，即`super block`的已用block计数变为0。此时这个`super block`将从`mini-vecotr`中移除被插入`freelist`中。`freelist`的长度为64，也就是说最多可以记录64个`super block`,而且每个`super block`以大小排序。当新的`super block`被全回收时，如果`freelist`中还有空位，那么直接保存，如果没有空位，将比较当前`super block`的大小，和`freelist`中`super block`的大小，将较大的`super block`还回给操作系统。每一次有`super block`加入`freelist`都将使得6中申请的block数目减半。
8. 6在申请新的`super block`前会检查`freelist`如果`freelist`中有`super block`那么将它移除并插入`mini-vecotr`中来使用，而不申请新内存。