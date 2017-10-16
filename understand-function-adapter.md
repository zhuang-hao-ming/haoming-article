---
title: 理解仿函数
date: 2017-09-15 22:34:26
tags:
---



## 仿函数

```c++
template<class _Ty = void>
	struct plus
	{	// functor for operator+
	typedef _Ty first_argument_type;
	typedef _Ty second_argument_type;
	typedef _Ty result_type;

	constexpr _Ty operator()(const _Ty& _Left, const _Ty& _Right) const
		{	// apply operator+ to operands
		return (_Left + _Right);
		}
	};

		// TEMPLATE STRUCT minus
template<class _Ty = void>
	struct minus
	{	// functor for operator-
	typedef _Ty first_argument_type;
	typedef _Ty second_argument_type;
	typedef _Ty result_type;

	constexpr _Ty operator()(const _Ty& _Left, const _Ty& _Right) const
		{	// apply operator- to operands
		return (_Left - _Right);
		}
	};
```

仿函数是重载了`operator()`的类，是callable的对象。标准库的仿函数为了可以被函数适配器使用需要在内部使用typedef

```c++
	typedef _Ty first_argument_type; // 第一形参的类型
	typedef _Ty second_argument_type; // 第二形参的类型
	typedef _Ty result_type; // 返回值类型
```


```cpp
		// TEMPLATE STRUCT unary_function
template<class _Arg,
	class _Result>
	struct unary_function
	{	// base class for unary functions
	typedef _Arg argument_type;
	typedef _Result result_type;
	};

		// TEMPLATE STRUCT binary_function
template<class _Arg1,
	class _Arg2,
	class _Result>
	struct binary_function
	{	// base class for binary functions
	typedef _Arg1 first_argument_type;
	typedef _Arg2 second_argument_type;
	typedef _Result result_type;
	};

template<typename T>
class less<T>: public binary_function<T, T, bool>
{
     bool operator()(const T& _Left, const T& _Right) const
    {	// apply operator< to operands
        return (_Left < _Right);
    }
}

```

也可以将`typedef`设计在一个父类中，然后令所有仿函数都继承父类。




## 函数适配器
正如容器适配器类是容器类，容器适配器对象是容器对象一样。仿函数适配器类是一个仿函数类，仿函数适配器实例是一个仿函数。

```c++

1. vs_2015中的仿函数类binder2nd
// TEMPLATE CLASS binder2nd
template<class _Fn2>
	class binder2nd
		: public unary_function<typename _Fn2::first_argument_type,
			typename _Fn2::result_type>
	{	// functor adapter _Func(left, stored)
public:
    // 这3个typedef和unary_function有点重复
	typedef unary_function<typename _Fn2::first_argument_type, 
		typename _Fn2::result_type> _Base;
	typedef typename _Base::argument_type argument_type;
	typedef typename _Base::result_type result_type;

	binder2nd(const _Fn2& _Func,
		const typename _Fn2::second_argument_type& _Right)
		: op(_Func), value(_Right)
		{	// construct from functor and right operand
		}

	result_type operator()(const argument_type& _Left) const
		{	// apply functor to operands
		return (op(_Left, value));
		}

	result_type operator()(argument_type& _Left) const
		{	// apply functor to operands
		return (op(_Left, value));
		}

protected:
	_Fn2 op;	// the functor to apply
	typename _Fn2::second_argument_type value;	// the right operand
	};

```

以binder2nd来讨论标准库仿函数适配器类的设计思路

1. 构造函数接受一个仿函数对象和一个第二实参值并记录在对象中， 值的类型从仿函数对象的模板实参中获得
2. 从仿函数对象的模板实参中获得，仿函数的第一参数类型`first_argument_type`和返回值类型`return_type`
2. 重载`return_type operator(first_argument_type)`函数， 使用记录的第二实参值调用仿函数对象
3. 仿函数适配器要继承`unary_function`,获得`unary_function`中的`typedef`，保证它是一个可以被继续适配的一般仿函数对象。

```c++
2. 简化函数调用的接口

		// TEMPLATE FUNCTION bind2nd
template<class _Fn2,
	class _Ty> inline
	binder2nd<_Fn2> bind2nd(const _Fn2& _Func, const _Ty& _Right)
	{	// return a binder2nd functor adapter
	typename _Fn2::second_argument_type _Val(_Right);
	return (binder2nd<_Fn2>(_Func, _Val));
	}
```

为了使用binder2nd，我们需要知道仿函数对象的类型，标准库使用函数模板的自动推导功能，来简化仿函数适配器的调用。