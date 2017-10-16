
---
title: iterator_traits理解
date: 2017-09-15 22:54:44
tags:
---
        `stl`中的`algorithm`需要使用`iterator`来访问`container`完成算法的操作。


为了使用`iterator`，`stl`规定，`algorithm`需要知道
1. `iterator`的类别（例如*RandomAccessIterator*或*BidirectionalIterator*等）。
2. 两个`iterator`差的类别(例如*unsigned int*)
3. 容器的元素类型
4. 容器元素的指针类型
5. 容器元素的引用类型

其中4，5一般不使用。

对于一般的`class`的`iterator`如代码1所示，我们可以在`class`内部声明关联类型(`associative type`)。

```
1.
template <typename _Tp>
struct _List_iterator
{
    typedef std::bidirectional_iterator_tag iterator_category;
    typedef _Tp value_type;
    typedef _Tp* pointer;
    typedef _Tp& reference;
    typedef ptrdiff_t difference_type;
}
```

algorithm使用如代码2.所示的方法就可以获得想要的信息。

```
2.
void algorithm(iterator first)
{
    first::value_type
}
```

但是有一些`iterator`是指针,我们无法声明`associative type`。


**iterator_traits**是一个中间层，它使得算法可以从`iterator`处获得自己想要的信息，而不需要考虑`iterator`究竟是一个指针还是一个类。


**iterator_traits**使用模板偏特化技术来实现。

```
3. 

template <class I> // class iterator
struct iterator_traits 
{
    typedef typename I::value_type value_type;
}

template <class I> // pointer iterator
struct iterator_traits<I*>
{
    typedef I value_type;
}

template <class I> // const iterator
struct iterator_traits<const I*>
{
    typedef I value_type; // 特别不加const
}

template <class I>
void algorithm(I first)
{
    typename iterator_traits<I>::value_type v1; // 使用
}

```


如代码3.所示。当`algorithm`需要从`iterator`处获得信息时，它从`iterator_traits`处请求，`iterator_traits`根据`iterator`的类型，使用不同的模板实现。如果是一般的`class`型`iterator`那么`iterator_traits`直接获得`iterator`的信息，如果是`pointer`型的`iterator`那么`iterator_traits`根据`pointer`的类型确定。
