
---
title: c++ 内存管理
date: 2017-09-15 22:54:44
tags:
---
        
# cpp内存管理基本构件

分配 | 释放  | 类型 | 可不可以自定义
---|--- | --- | ---
malloc | free | 函数 | 
::operator new | ::operator delete | 函数 | 可以
new | delete | 操作符 | 不可以
allocator<>().allocate | allocator<>().deallocate | 函数 | 

## 用法

```
void* p = malloc(512) // 分配512 bytes
free(p)

int* p = new int; // 分配 4 bytes
delete p;

void* p = ::operator new(512); // 分配512 bytes
::operator delete(p);

int* p = allocator<int>().allocate(4); // 分配 4*4 bytes
allocator<int>().deallocate(p, 4);

```


### new and delete

- *new*的真实行为(`Complex* p = new Complex(1,2)`)
    1. void* p = operator new(sizeof(Complex));
    2. Complex* p = static_cast<Complex*>(p);
    3. p->Complex(1,2);

- *delete*的真实行为(`delete p`)
    1. p->~Complex();
    2. operator delete(p);

#### 注意：
1. 一般我们把new和delete称为new expression和delete expression， 以与operator new和operator delete区别。
2. operator new内部调用malloc，operator delete内部调用free

### array new and array delete

- *array new*(`Complex* p = new Complex[3]`)
- *array delete*(`delete[] p`)

#### 注意：

1. *array new*和*array delete*要配套使用，否则，当类具有non trival的析构函数时(带指针的类),*malloc*分配的内存布局中含有*长度字段*,将导致*free*函数被调用时p指向长度字段，导致析构函数无法正确调用。即使析构函数被正确调用了(如何被正确调用？？)，也只会调用一次，而不会对每个对象都调用，导致其它对象在未正确析构之前就被回收，引起内存泄漏。这两个原因是，*array new* 和*array delete*要配套使用的主要原因。


### placement new

```
Complex* p = new Complex[3];
Complex* q = p;

new(q)Complex(1,2);

```
以上代码展示了*placement new*的写法。它的真实行为如下：

1. void* p = operator new(sizeof(Complex), q);
2. Complex* p = static_cast<Compex*>(p)
3. p->Complex(1,2)

#### 注意
1. 这里使用的*operator new*重载版本并没有分配内存
2. *placement new*的功能就是在已经分配好的内存上，构造对象。


## operator new, operator delete, operator new[], operator delete[]函数的自定义

```
// 全局版本，不可以被声明在namespace中
void* operator new(size_t size);
void* operator new[](size_t size);
void operator delete(void* p);
void operator delete[](void* p);


// 类静态函数版本，由于这些函数一定是静态函数，所以可以省略static
class Foo
{
    public:
        static void* operator new(size_t size);
        static void operator delete(void* p);
}
```

我们可以通过上述方法对这4个函数进行自定义，以改变*expression new*和*expression delete*的行为，完成内存分配管理。