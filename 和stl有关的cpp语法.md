
---
title: 和stl有关的cpp语法
date: 2017-09-15 22:54:44
tags:
---
        ## 操作符重载

`++i` and `i++`


```
1.
#include <iostream>
using std::cout;
using std::endl;
namespace haoming01
{

	class Foo
	{
	private:
		int j;
	public:
		// prefix ++i
		Foo& operator++()
		{
			cout << "prefix" << endl;
			j = j + 1;
			return *this;
		}
		// postfix i++
		Foo operator++(int)
		{
			cout << "postfix" << endl;
			Foo a = *this;
			j = j + 1;
			return a;
		}
		void print()
		{
			cout << j << endl;
		}
	};
}


int main()
{
	haoming01::Foo b{};
	b.print();

	(b++)++;
	b.print();
}
```

1. 在代码1.中。`postfix ++`的函数签名中多了一个`int`以与`prefix ++`区分。
2. `prefix ++`的行为是，操作对象然后返回对象的引用。`postfix ++`的行为是，以复制构造的方式新建一个对象，然后操作原对象，返回新建对象的值。这样设计的原因是为了与int的设计一致。


**问题，`b++++`可以正常运行？**


`p->a`

> The overload of operator -> must either return a raw pointer or return an object (by reference or by value), for which operator -> is in turn overloaded.

`operator->`的重载函数应该返回指针或者返回重载了`operator->`的对象。然后继续调用`operator->`,直到调用原生的`operator->`。

## 模版

1. 类模板
    1. 特化: 如代码2.所示。我们可以为所有类型提供一个一般的实现，为特定类型提供一个特定的实现。实例化模板时，如果有特定类型的实现我们就使用特定类型的实现，如果没有就使用一般的实现。
    2. 偏特化
        1. 类型数目偏特化: 如代码3.所示。
        2. 类型范围偏特化: 如代码2.所示。
2. 函数模板
    1. 模板实参推导： 模板函数调用时，不需要显式地指定模板实参，编译器可以自动从函数的实参中推导模板实参的类型。
3. 成员模板


```c++
2.
namespace haoming02
{
	template <typename T>
	class Foo
	{
		T a;
	public:
		Foo(T a) : a(a) {}
		void print()
		{
			cout << "type: anonymous. size: " << sizeof(T) << ". value: " << a << endl;
		}
	};

	template<>
	class Foo<int>
	{
		int a;
	public:
		Foo(int a) : a(a) {}
		void print()
		{
			cout << "type: int. size: " << sizeof(int) << ". value: " << a << endl;
		}
	};
	
	template<typename T>
	class Foo<T*>
	{
	public:
		void print()
		{
			cout << "it is pointer" << endl;
			cout << "type: int. size: " << sizeof(T*) << ". value: " << "" << endl;
		}
	};
}




int main()
{

	haoming02::Foo<int> a{ 1 };
	a.print();

	haoming02::Foo<char> b{ '1' };
	b.print();
	
	haoming02::Foo<int*> c;
	c.print();
}
```


```
3.
namespace haoming03
{
	template <typename T1, typename T2>
	class Foo
	{
		T1 a;
		T2 b;
	public:
		Foo(T1 t1, T2 t2): a(t1), b(t2) {}
		void addA()
		{
			cout << "i cannot" << endl;
		}
	};

	template<typename T2>
	class Foo<int, T2>
	{
		int a;
		T2 b;
	public:
		Foo(int t1, T2 t2) : a(t1), b(t2) {}
		void addA()
		{
			cout << a+1 << endl;
		}
	};
}




int main()
{

	haoming03::Foo<int, int> a{ 1,1 };
	haoming03::Foo<double, int> b{ 1,1 };
	a.addA();
	b.addA();

}
```