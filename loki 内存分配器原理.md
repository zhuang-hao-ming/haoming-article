
---
title: loki 内存分配器原理
date: 2017-09-15 22:54:44
tags:
---
        本文整理自侯捷老师的内存管理课程。

loki是一个先进的cpp库，它的作者是cpp标准委员会的成员。loki的内存管理策略，和gnu c的alloc相比有更可取之处。

loki使用一个3层的内存分配系统。

第3层：

```
class Chunk
{
    unsigned char* pData_; // 内存指针
    unsigned char firstAvailabelBlock_; // 可用块的索引
    unsigned char blocksAvailabel; // 剩余可用块的数目
}
```

`Chunk`使用*以array替代list，以index替代pointer*的策略。

它的行为模式如下：

1. 上层类会调用`Init`使用`malloc`申请内存，然后将内存地址保存到`pData_`上。`Init`还会调用`Reset`完成初始化。
2. `Reset`根据`blockSize(块大小)`,`blocks(块数目)`将`pData_`的内存划分为`blocks`块，每块的第一个字节被借用，记录1,2,3...blocks的索引(*注意由1开始*)。然后将`firstAvailabelBlock`设为0，blocksAvailabel设为`blocks`。
3. 每当申请内存是，`Allocate`函数会被调用，它根据`firstAvailabelBlock`，`blockSize`和`pData_`计算返回的内存地址。同时，将读取到的第一个字节的值保存到`firstAvailabelBlock`作为下一个候选内存块的索引。
4. 每当内存释放时，`Deallocate`函数会被调用，首先将`firstAvailabelBlock`保存到内存的第一个字节，然后根据内存的地址，`pData_`，`blockSize`计算内存块的索引，将索引保存到`firstAvailabelBlock`中。并让`blocksAvailabel`加1。



第2层：

```
class FixedAllocator
{
    vector<Chunk> chunks_;
    Chunk* allocChunk;
    Chunk* deallocChunk_;
}
```

它的行为模式：

1. 每当申请内存时，首先检查`allocChunk`所指的`Chunk`有没有可用的内存，如果有，由对应的`Chunk`完成内存分配。
2. 在1中，如果`allockChunk`所指的`Chunk`没有可用的内存，或者`allocChunk`是空指针。那么，遍历`chunks`将找到的第一个可用的`chunk`作为`allocChunk`的目标，然后重复1。如果所有的`chunk`都没有可用的内存了，那么在`chunks`的尾部插入一个新的`chunk`，由于在vector中插入元素可能导致整个vector移动，所以还要重设`allocChunk`和`deallocChunk`指针。
3. 每当释放内存时。
    1. 查找内存所处的`chunk`。loki使用一个`vicinity(邻近)`的想法，从`deallocChunk`的前后交替寻找指针所处的`chunk`。
    2. 将内存交由对应的chunk释放。对于完全收回的chunk，延迟归还给操作系统。这个策略和`malloc`类似，只有当第二个完全收回的chunk出现时，第一个才会被还给操作系统。（它将完全回收的chunk保存到vector的尾部，当完全回收的chunk出现时，只要检查尾部的chunk，如果尾部的chunk是完全回收chunk则将其还给操作系统，新的完全回收chunk会被保存在vector的尾部）

第一层:

SmallObjAllocator根据申请的内存块大小，将任务转交给对应的FixedAllocator。