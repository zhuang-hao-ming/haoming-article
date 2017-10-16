
---
title: malloc和free原理
date: 2017-09-15 22:54:44
tags:
---
        本文整理自侯捷老师的cpp内存管理课。讨论malloc的实现。

1. cpp程序启动后首先会调用`_heap_init`函数。
    1. `_heap_init`调用`HeapCreate`函数建立一个堆`_crtheap`。
    2. `_heap_init`调用`_sbh_heap_init`,`_sbh_heap_init`调用`HeapAlloc`从`_crtheap`中申请16个`HEADER`


调用`malloc(size)`申请内存时，如果size>threshold,将调用`HeapAlloc`从`_crtheap`中申请内存，如果size<=threshold，将使用`sbh(small block heap)`策略。

讨论在debug模式下malloc的调用行为。

1. 调用函数`_malloc_crt(size)`
2. 由于`_malloc_crt`是一个宏，在debug模式下，实际调用的函数是`_malloc_dbg`
3. `_malloc_dbg`将调用`_heap_alloc_dbg`
    1. 调整size，增加sizeof(_CrtMemBlockHeader)和nNoMansLandSize
    2. _CrtMemBlockHeader是debug头
    ```
    typdef struct _CrtMemBlockHeader
    {
        struct _CrtMemBlockHeader* pBlockHeaderNext; //将所有申请的内存块连接为一个双链表
        struct _CrtMemBlockHeader* pBlockHeaderPrev;
        char* szFileName; // 申请内存的文件名
        int nLine; // 申请内存的代码行号
        size_t nDataSize; // 申请的内存大小
        int nBlockUse; // 申请的内存类型
        long lRequest;
        unsigned char gap[nNoMansLandSize] // 哨兵，确保debug头没有被滥用，尾部也会有。
    } _CrtMemBlockHeader;
    
    ```
    3. 调用`_heap_alloc_base`申请内存
    4. 完成双链表的链接，调试信息填充，哨兵设置，数据区清理，返回指针。
4. `_heap_alloc_base`是真正进行内存分配的位置
    1. 如果size>threshold调用`HeapAlloc`从`_crtheap`中申请内存。
    2. 如果size<=threshold调用`__sbh_alloc_block`申请内存。
5. `__sbh_alloc_block`函数对于小于`1k`的内存进行管理。
    1. 调整size，增加8bytes，并将size向上调整到16的倍数。
    2. 从`_crtheap`中申请的16个`HEADER`是内存管理的入口。每个`HEADER`上有两个指针，一个指向1m的待分配内存，一个指向`tagRegion`.
    ```
    typedef unsigned int BITVEC;
    typdef struct tagRegion
    {
        int indGroupUse; // 当前正在使用的group的索引
        char cntRegionSize[64];
        BITVEC bitvGroupHi[32]; // Hi和Lo共同组成32个长度为64bit的vec，每个vec代表对应group，vec中的每个bit代表对应group的对应链表是否有内存。
        BITVEC bitvGroupLo[32];
        struct tagGroup[32]; // group
    }REGION, *PREGION;
    ```
    3. 
    ```
    typedef struct tagGroup
    {
        int cntEntries; // group被使用的内存个数
        struct tagListHead listHead[64]; // 双链表，按照16，32,48,64,...,1024bytes(>=1024)分别处理64种大小（最后一个较特殊）。
    } GROUP, *PGROUP;
    
    typedef struct tagListHead //表头
    {
        struct tagEntry* pEntryPrev;
        struct tagEntry* pEntryNext;
    } LISTHEAD, *PLISTHEAD;
    
    typedef struct tagEntry // 链表节点
    {
        int sizeFront;
        struct tagEntry* pEntryPrev;
        struct tagEntry* pEntryNext;
        
    } ENTRY, *PENTRY;
    
    ```
    4. 函数首先使用`VirtualAlloc(0,1m,MEM_RESERVE)`从操作系统中申请1m的虚拟地址空间。然后将这1m的地址空间分成32个`paragraph`,每个大小为32kb。每个`paragraph`由一个`group`负责管理。
    5. 第一次申请内存，或者已经没有可用的`group`时，函数调用`VirtualAlloc(0, 32k,MEM_COMMIT)`从操作系统申请32k内存。
    6. 32k的内存将会分成8块，每块4k，称为一个`page`。这8块将被链接到group的#63号链表。每一个`page`的大小为4096bytes，使用了8bytes作为哨兵，为了保证大小为16的倍数，保留8bytes不使用，最后剩余大小为4080bytes。数据区的头部被借用为tagEntry。
    7. 当申请内存时，首先将内存大小调整到16的倍数，然后到对应的链表中去获取内存，如果对应的链表中没有内存，则由近及远的在后方的链表中查找是否有内存。
    8. 7的处理在非匹配链表上的行为。
        1. 根据第一个节点中tagEntry中sizeFront的值，节点的地址和申请的内存块的大小，确定返回地址。2. 修改tagEntry中的sizeFront
        3. 修改返回cookie，返回地址。
        4. 如果剩余的内存小于当前链表处理的大小，将内存移动到其它合适链表上。
    9. 7的处理在匹配链表上直接修改cookie然后返回对应的内存地址。
    10. free释放内存是，根据内存的大小，将内存插入到合适的链表中。
    11. 不断的分配，导致内存块越来越小，由于大内存块易于管理和使用，所以在free时，我们希望合并小内存块。合并的策略如下:
        1. 对于free的一块内存，根据内存的布局，向上移动4bytes就可以读取到内存块的cookie获知内存块的大小，然后将指针下移内存块的大小，就可以读取到，下一块内存的cookie，如果下一块内存是释放的内存，那么将下一块内存合并进来。
        2. 根据内存布局，将指针向上移动8bytes就可以读到上一块内存的cookie，如果上一块内存是已经释放的（cookie最后的bit为1），那么将它合并进来。
    12. free(p)时，根据p的地址，测试它究竟落在那个HEADER中，那一个GROUP中，那一个链表中，然后将内存还到指定位置。
    13. 根据tagGroup中的cntEntry我们可以确定group的内存被完全会收了。对于完全回收的group，malloc的处理如下：
        1. 使用一个全局指针保存完全回收的group所在的HEADER，使用一个全局索引保存完全回收的group的索引。
        2. 当只有一个完全回收group时，不会将它直接还给操作系统，此时group的状态和初始状态相同（合并）。如果有新的内存申请使用group，a的指针和索引将被清空。
        3. 当有另一个完全回收group出现时，此时前一个group被还给操作系统，全局指针和索引的值也更新到新出现的完全回收group上。
    

malloc之所以设计一个如此多层的内存分配系统，是因为32k的内存块比较容易完全回收。

在新版本的vc中，malloc的内存管理被下移到操作系统中。
