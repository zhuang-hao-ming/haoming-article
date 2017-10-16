
---
title: c++研究
date: 2017-09-15 22:54:44
tags:
---
        1. 泛型是一种编程思想，它在c++上的实现是模板。

2. trait

考虑一个这样的场景，一个泛型的求和函数，它有一个泛型参数T，能够返回一个T数组的和，一般的实现返回类型是T。但是，如果传入一个char数组，而求和又大于255，那么返回值就会被截断，导致bug。

一个想法就是指定一个和T相关的返回类型，我们把这个返回类型叫做trait。

trait可以实现为一个模板类，接受T作为模板参数。

然后再特化这个模板类，针对不同的T给出不同的实现。

```
template <typename T>
class Trait
{
    
};

template <>
class Trait<char>
{
  public:
    typedef int ReturnType;
};

template <>
class Trait<int>
{
    public:
        typedef long ReturnType;
}




template <typename T>
Trait<T>::ReturnType sigma(T* start, T* end)
{
    typedef Trait<T>::ReturnType ReturnType;
    ReturnType s{};
    while (start != end)
    {
        s += *start;
        start++;
    }
    
    return s;
}


```

3. 迭代器

迭代器是一个指向容器中对象的对象。

设计迭代器的原因是为了分离算法与容器。比如，一个查找元素的算法， 需要遍历容器，找到一个和指定值匹配的元素。为了不针对每个容器都重复实现一遍算法，可以把遍历容器的操作独立为一个迭代器。算法只需要和迭代器进行交流。算法不再考虑底部的容器是什么。

然后再针对每个容器实现迭代器。



## 容器

1. vector
2. deque
3. list
4. set and multiset
5. map and multimap
6. stack
7. queue


## vector
是一个可以存放任意类型数据的动态数组，它在内存中占据一片连续的空间。

```
#include <vector>

// definition 
std::vector<T> v{}; // 存放T类型的空vector
std::vector<T> v{n}; // 容量为n存放T类型的vector
std::vector<T> v{n, i}; //容量为n初始化为i存放T类型的vector

std::vector<T> v{v1}; // 拷贝一个已经存在的vector
int arr[] = {1, 2, 3};
std::vector<T> v(arr, arr+3) // 用数组来初始化一个vector


v.push_back(i) // 在vector的尾部插入元素

bool is_empty = v.empty(); // 判断vector是否为空
std::size v_size = v.size(); // 获得vector的大小

T a = v[5]; // 获取索引为5的元素，不进行越界检查
T b = v.at(5); // 获取索引为5的元素， 进行越界检查，如果越界排除异常

v.clear() // 清空vector
v.pop_back() // 弹出vector的尾部元素



std::vector<int>::const_iterator it = v.begin();
v.erase(it+1); // 删除迭代器指示的位置


// 函数类
class ContainsString: public std::unary_function<std::string, bool>
{
    std::string match;
    ContainsString(const std::string& match): match(match) {}
    
    bool operator()(const std::string&  str) const
    {
        return (str.find(match) != -1)
    }
}

v.erase(
std::remove_if(v.begin(), v.end(), ContainsString{"c++"}),
v.end()
)

// remove_if 接收一个函数对象，将那些判别为true的元素，移动到vector的末尾，然后返回，这些元素的起始迭代器
// erase 删除两个迭代器指示的范围


```


## deque

deque是一个双向队列，和vector类似，多了push_front和pop_front方法。deque和vector使用了不同的内存分配策略（大块分配内存？）。


## list

list是一个双向链表，在list中进行插入，删除，替换等需要重新排列的操作以及两个list之间的合并效率很高（指针移动， 不需要复制）。

但是list访问元素的时间和list的长度成线性比例，随机访问性能低，而且由于每个元素都要额外存储两个指针开销较大。



```
#include <list>


std::list l{}
// 和vector不同的方法

l.remove // 删除值 l.erase是删除位置
l.insert // 任意位置插入
l.splic // 粘贴

```

