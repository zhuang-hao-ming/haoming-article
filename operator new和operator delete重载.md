
---
title: operator new和operator delete重载
date: 2017-09-15 22:54:44
tags:
---
        我们可以重新定义`operator new`函数和`operator delete`函数。


```
1.
void* operator new(size_t size);
void operator delete(void* p, size_t size);

```
我们还可以重载`operator new`和`operator delete`函数，但是要求重载的版本，`operator new`的第一个参数是`size_t`,`operator delete`函数的前两个参数分别是`void*, size_t `。

```
2.

void* operator new(size_t size, size_t extra);
void operator delete(void* p ,size_t size, size_t extra);

void* operator new(size_t size, char c);
void operator delete(void*p ,size_t size, char c);

```

对于`operator new`的重载版本的调用方法如下
```
1. 原始版本

new Foo()

2. 重载版本

new(10)Foo()
new('a')Foo()


```

`operator delete`的重载版本只在对应的`operator new`重载版本抛出异常时被调用，一般是在构造函数抛出异常后，释放已经分配好的内存。

----------------------

```
3.
void* q = malloc(sizeof(Foo))
Foo* p = new(q)Foo(0)

```
从前面的叙述中可以知道，`placement new`不过是`operator new`的一个重载版本。