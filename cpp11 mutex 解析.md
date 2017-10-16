---
title: cpp11 mutex 解析
date: 2017-10-16
tags: cpp11 
---

## mutex

互斥通过'排它资源访问'来控制'并发资源访问'.
为了排它访问资源,线程先锁住一个互斥然后访问资源然后再解锁互斥.
别的尝试访问相同资源的线程也会先锁住相同的互斥,但是由于互斥已经被前面的线程锁住,它会阻塞直到前一个线程解锁互斥.


```c++

1.

#include <iostream>
#include <mutex>
#include <thread>
#include <future>
#include <chrono>
#include <vector>
using namespace std;
namespace haoming01
{
	/*
		互斥使用排它资源访问来控制并发资源访问.为了排它访问资源,线程先锁住一个互斥然后访问资源然后再解锁互斥.
		别的尝试访问相同资源的线程也会先锁住相同互斥,但是由于互斥已经被前面的线程锁住,它会阻塞直到前一个线程解锁互斥.
	*/

	int cnt = 0;
	mutex i_mutex;
	void add_cnt()
	{
		
		for(int i = 0; i < 1000; i++)
		{
			cout << "add" << endl;
			{
				lock_guard<mutex> lg(i_mutex);
				cnt = cnt + 1;
			}
			// i_mutex.lock();			
			// cnt = cnt + 1;
			// i_mutex.unlock();

			this_thread::sleep_for(chrono::milliseconds(1));
		}
		
		
	}
	void del_cnt()
	{	
		
		
		for(int i = 0; i < 1000; i++)
		{
			cout << "del" << endl;

			{
				lock_guard<mutex> lg(i_mutex);
				cnt = cnt - 1;
			}


			// i_mutex.lock();
			// cnt = cnt - 1;
			// i_mutex.unlock();			
			this_thread::sleep_for(chrono::milliseconds(1));
			
		}
		
	}
	void test_mutex()
	{
		vector<future<void>> v{};
		cout << "test mutex" << endl;
		for(int i = 0; i < 4; i++)
		{
			if (i % 2 == 0) {				
				auto f1 = async(launch::async, add_cnt);					
				v.push_back(move(f1));
			} else {
				auto f2 = async(launch::async, del_cnt);
				v.push_back(move(f2));
			}
		}
		
		for(auto& f: v)
		{
			f.get();
		}
		
		cout << "cnt: " << cnt << endl;

	}
}
```

## lock_guard

代码1存在问题
1. 如果在关键区内发生异常,互斥如果没有解锁,将会导致死锁
2. 如果同时并发访问多个资源,不同线程的加锁顺序不同,将会导致两个线程互相等待不同的互斥解锁,导致死锁

我们可以使用RAII(resourece acquisition is initialization)策略.让构造函数来锁互斥,析构函数来解锁互斥,这样即使异常发生
只要管理对象死亡,互斥还是会正常解锁.

```
{
		lock_guard<mutex> lg(i_mutex);
		cnt = cnt - 1;
}
```

用上面的方法定义一个互斥管理lock_guard<mutex>对象,会自动的将互斥加锁.如果无法加锁将阻塞等待.
当对象生命结束时,会自动解锁互斥.


## recursive_mutex

有时候我们需要可以在同一个线程中锁多次的互斥
标准库提供了recursive_mutex
这个互斥允许我们在同一个线程中加锁和解锁多次.
代码2展示了一个例子.

```c++
2.

class DataBaseAccess
	{
	private:
		//mutex db_mutex;
		recursive_mutex db_mutex;
	public:
		void create_table()
		{
			//lock_guard<mutex> lg(db_mutex);
			lock_guard<recursive_mutex> lg(db_mutex);
			cout << "create table" << endl;
		}
		void insert_table()
		{
			//lock_guard<mutex> lg(db_mutex);
			lock_guard<recursive_mutex> lg(db_mutex);
			cout << "insert data" << endl;
		}
		void create_and_inert_table()
		{
			
			//lock_guard<mutex> lg(db_mutex);
			lock_guard<recursive_mutex> lg(db_mutex);
			create_table();
			insert_table();
			
			
		}
	};


	void test_recursive_mutex()
	{
		DataBaseAccess da{};
		da.create_and_inert_table();
	}

```

## mutex try_lock


当mutex.lock()无法加锁的时候,线程会阻塞.如果不想线程阻塞,可以使用mutex.try_lock(),这个函数在无法加锁时
会返回false.

为了使用管理类lock_guard<mutex>,需要传入第二个参数adopt_lock,这个构造函数不会给mutex加锁,我们需要自己加锁.

try_lock可能会返回虚假结果

```c++

3.

	mutex try_lock_mutex;

	void lock_10s_1()
	{
		while (!try_lock_mutex.try_lock()) 
		{
			cout << "lock_10s_1 : wait for mutex" << endl;
			this_thread::yield();
		}
		lock_guard<mutex> lg(try_lock_mutex, adopt_lock);
		this_thread::sleep_for(chrono::seconds(2));
		cout << "finish lock_10s_1" << endl;
	}

	void lock_10s_2()
	{
		while (!try_lock_mutex.try_lock()) 
		{
			cout << "lock_10s_1 : wait for mutex" << endl;
			this_thread::yield();
		}
		lock_guard<mutex> lg(try_lock_mutex, adopt_lock);
		this_thread::sleep_for(chrono::seconds(2));
		cout << "finish lock_10s_2" << endl;
	}



	void test_try_lock()
	{
		auto f1 = async(launch::async, lock_10s_1);
		auto f2 = async(launch::async, lock_10s_2);
		f1.get();
		f2.get();
		
	}
```

## timed_mutex, try_lock_for()

在一个关注时延的应用中,在加锁一个mutex的时候,我们希望控制最大的阻塞时间.
标准库提供了timed_mutex
`tm.try_lock_for(chrono::seconds(2)))`这个调用指示如果2s内无法加锁成功将返回false,应用应该采取其它措施.
和mutex.try_lock()不同.

```C++

4.

	timed_mutex tm;

	void lock_10s_1()
	{
		
		if (tm.try_lock_for(chrono::seconds(2))) 
		{
			lock_guard<timed_mutex> lg(tm, adopt_lock);
			cout << "lock_10s_1 get lock" << endl;
			this_thread::sleep_for(chrono::seconds(1));
		} 
		else
		{
			cout << "lock_10s_1 cannot get lock" << endl;
		}
	}

	void lock_10s_2()
	{
		
		if (tm.try_lock_for(chrono::seconds(2))) 
		{
			lock_guard<timed_mutex> lg(tm, adopt_lock);
			cout << "lock_10s_2 get lock" << endl;
			this_thread::sleep_for(chrono::seconds(1));
		} 
		else
		{
			cout << "lock_10s_2 cannot get lock" << endl;
		}
	}


	void test_time_mutex()
	{
		auto f1 = async(launch::async, lock_10s_1);
		auto f2 = async(launch::async, lock_10s_2);
		f1.get();
		f2.get();
	}
```

## lock(), try_lock()

通常一个线程一次只会锁一个互斥,但是有时也需要锁多个互斥.
比如从一个银行账号转账到另一个银行账号.
如果多个互斥加锁的顺序不一致的话,同时锁多个互斥很容易导致死锁.
为了解决这个问题,标准库提供了`lock()`和`try_lock()`

`lock()`尝试加锁所有mutex,如果有一个mutex无法加锁成功,那么解开所有mutex,阻塞.lock()不按照顺序加锁mutex


`try_lock()`按顺序尝试加锁所有mutex,如果有一个mutex无法成功,返回它的index(0 base),如果全部加锁成功返回-1,不阻塞.


```C++

5.

	class Account
	{
	public:
		double balance;
		mutex mt;
		Account(double amount): balance(amount){}
	};

	Account a1(100);
	Account a2(100);

	void transfer_from_a1_to_a2(double amount)
	{
	
		// lock(a1.mt, a2.mt);
		// cout << "lock ok: " << amount << endl;
	
		// lock_guard<mutex> lg1(a1.mt, adopt_lock);
		// lock_guard<mutex> lg2(a2.mt, adopt_lock);
		// a1.balance -= amount;
		// a2.balance += amount;
		
		
		int idx = try_lock(a1.mt, a2.mt);
		if( idx < 0)
		{
			lock_guard<mutex> lg1(a1.mt, adopt_lock);
			lock_guard<mutex> lg2(a2.mt, adopt_lock);
			a1.balance -= amount;
			a2.balance += amount;
		}
		else
		{
			cout << "cannot lock "<< idx << endl;
		}
		
		
	}

	void test_lock()
	{
		auto f1 = async(launch::async, transfer_from_a1_to_a2, 20);
		auto f2 = async(launch::async, transfer_from_a1_to_a2, 30);
		f1.get();
		f2.get();
		cout << "a1: " << a1.balance << endl;
		cout << "a2: " << a2.balance << endl;
	}
```

## unique_lock

lock_guard<mutex>在初始化以后直到生命结束,它都拥有一个mutex,生命结束的时候解锁这个mutex.
而unique_lock<mutex>则不是.它在生命期内,可以拥有也可以不拥有一个mutex,生命结束的时候,如果有一个mutex则
解锁它,否则不做操作.



1. unique_lock<mutex> ul(mutex); // 锁mutex, 阻塞
2. unique_lock<mutex> ul(mutex, try_to_lock); //尝试锁mutex,如果失败返回false, 不阻塞
3. unique_lock<mutex> ul(mutex, defer_lock);  // 不锁mutex, 不阻塞
4. unique_lock<mutex> ul(mutex, chrono::seconds(10)); // 

生命期内可以调用`ul.lock()`来锁互斥,`ul.unlock()`来解锁互斥.
`ul.owns_lock()`或者bool(ul)检查是否有锁住互斥.

```c++


6.

	bool ready_flag = false;
	mutex ml;

	void thread_1()
	{
		lock_guard<mutex> lg(ml);
		ready_flag = true;
	}

	void thread_2()
	{
		unique_lock<mutex> ul(ml);
		cout << bool(ul) << endl;
		cout << ul.owns_lock() << endl;
		while (!ready_flag)
		{
			ul.unlock();
			this_thread::yield();
			this_thread::sleep_for(chrono::seconds(1));
			ul.lock();
		}
		cout << ready_flag << endl;
	}


	void test_unique_lock()
	{
		auto f1 = async(launch::async, thread_1);
		auto f2 = async(launch::async, thread_2);
		f1.get();
		f2.get();

	}


```