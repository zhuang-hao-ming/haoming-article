---
title: iterator_category理解
date: 2017-09-15 22:54:44
tags:
---

algorithm只接收iterator而看不见container，它所需要的信息都只能从iterator获得，根据前文的介绍，iterator要回答算法5个问题

1. iterator_category
2. value_type
3. difference_type
4. referenct_type
5. pointer_type

其中iterator_category对于算法的效率有重大影响，算法需要根据iterator _category来确定不同的处理策略。

标准库将iterator_category设计为class而不是enum或者const。主要是为了利用重载和继承的(is-a)特性来简化编码。

```
struct input_iterator_tag {};
struct output_iterator_tag {};
struct forward_iterator_tag: public input_iterator_tag {};
struct bidirectional_iterator_tag: public forward_iterator_tag {};
struct random_access_iterator_tag: public bidictional_iterator_tag{};
```


```
iterator_category的继承关系

input_iterator_tag <-
forward_iterator_tag <-
bidirectional_iterator_tag <-
random_access_iterator_tag

output_iterator_tag
```


iterator_category影响算法性能

1. 算法接口调用算法实现函数，并传入询问到的iterator_category对象。
2. 对应的重载版本实现被调用（特化的，高效的）。

以distance为例
```cpp
1.
template<class RandomAccessIterator>
inline iterator_traits<RandomAccessIterator>::differenct_type
__distance(RandomAccessIterator first, RandomAccessIterator last, random_access_iterator_tag)
{
    return last - first;
}


2.
template<class InputIterator>
inline iterator_traits<InputIterator>::differenct_type
__distance(InputIterator first, InputIterator last, input_iterator_tag)
{
    iterator_traits<InputIterator>::differenct_type n = 0;
    while(first != last)
    {
        ++first;
        ++n;
    }
    return n;
}

3.
template <class InputIterator>
inline iterator_traits<InputIterator>::difference_type
distance(InputIterator first, InputIterator last)
{
    typedef typename iterator_traits<InputIterator>::iterator_category category;
    
    return __distance(first, last, category());
}

```

在这个例子中，利用了重载和继承的特性，使得random_access_iterator_tag类型的迭代器可以在O(1)完成算法,而其它input_iterator_tag类型的迭代器可以在O(n)完成算法。


