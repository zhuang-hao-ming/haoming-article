
---
title: libuv初探索
date: 2017-09-15 22:54:44
tags:
---
        
## 下载安装




```

1. 从官网下载libuv的压缩包

2. 解压：tar -zxvf xxx.tar.gz

3. 安装缺少的工具

sudo apt-get install automake
sudo apt-get install libtool

4. 安装

$ sh autogen.sh
$ ./configure
$ make
$ make check
$ make install

5. 如果失败了，可能是权限问题，加上sudo重试。
```


## 编译

设置环境变量：

将库的安装目录`/usr/local/lib`设置为环境变量`LD_LIBRARY_PATH`的值。

方法：
```
$ cd ~
$ code .bashrc
进入文本编辑界面添加新一行：
export LD_LIBRARY_PATH="/usr/local/lib"


```

编译：

```

$ gcc -o main main.c -luv

```

或者编写Makefile

```
main:
    gcc -o main main.c -luv
clean:
    rm main

```
在控制台中:
```
$ make main 编译链接

$ make clean 删除目标文件

```

**值得注意的是，Makefile文件要求使用`tab`来缩进，很多编辑器例如`visual code`可能会配置使用空格来替换tab，所以如果Makefile文件报错，请确认你是否使用了
tab来缩进，而不是空格。**

可以用下面这个命令:

`cat -e -t -v Makefile`

来查看，在这个模式下`tab`会被显示为`^I`，换行会被显示为$，你可以确认你是否使用了不正确的控制字符。

## 线程

libuv库封装了不同平台的线程实现，提供统一接口，由于不同平台的线程实现差异较大，libuv提供的接口功能较少。接口和`pthreads`类似。

下文分几个例子用代码展示libuv的线程接口：

创建线程

```
#include <stdio.h>
#include <uv.h>
#include <unistd.h>

void hare(void* arg) {
	int tracklen = *((int*)arg);
	while (tracklen) {
		tracklen--;
		sleep(1);
		printf("hare ran another step  %d\n", tracklen);
	}
	printf("hare done running\n");

}



void tortoise(void* arg) {
	int tracelen = *((int*)arg);
	while (tracelen) {
		tracelen--;
		sleep(3);
		printf("tortoise ran another step %d\n ", tracelen);
	}
	printf("tortoise done running\n");
}

int main() {
	int tracklen = 10;
	/*
		uv_thread_t 这个类型可以认为是线程的标记
	*/
	uv_thread_t hare_id; /* 声明线程 */
	uv_thread_t tortoise_id; /* 声明线程 */
	/*
		开启一个线程，
		参数：
		uv_thread_t* 线程标记指针
		void (*uv_thread_cb)(void* arg) 线程执行的函数
		void* 传给线程执行函数的用户数据
		这个函数，开启一个新线程，用用户指定的数据运行函数.	
	*/
	uv_thread_create(&hare_id, hare, &tracklen);
	uv_thread_create(&tortoise_id, tortoise, &tracklen);	

	/*
		uv_thread_join调用
		阻塞主线程,
		等到hare_id和tortoise_id都退出以后
		主线程才继续执行
	*/
	uv_thread_join(&hare_id);
	uv_thread_join(&tortoise_id);

	// 疑问， 为什么两个线程同时操作同一个变量，不会互相影响。

	return 0;

}

```

libuv支持读写锁和barrier锁


```
#include <stdio.h>
#include <uv.h>
/*
	声明barrier
*/
uv_barrier_t blocker;
/*
	声明读写锁
*/
uv_rwlock_t numlock;
int shared_num;

void reader(void *n)
{
    int num = *(int *)n;
    int i;
    for (i = 0; i < 20; i++) {
        uv_rwlock_rdlock(&numlock); // 对numlock加读取锁
        printf("Reader %d: acquired lock\n", num); // - 在这期间，其他的写操作被禁止，读操作允许
        printf("Reader %d: shared num = %d\n", num, shared_num);// -
        uv_rwlock_rdunlock(&numlock); // 解开读取锁
        printf("Reader %d: released lock\n", num);
    }
    i = uv_barrier_wait(&blocker); // 栅栏等待
	printf("%d barrier %d\n", num, i);

}

void writer(void *n)
{
    int num = *(int *)n;
    int i;
    for (i = 0; i < 20; i++) {
        uv_rwlock_wrlock(&numlock); // 加numlock写锁
        printf("Writer %d: acquired lock\n", num); // - 在这期间， 其他所有的读写操作都被禁止
        shared_num++;
        printf("Writer %d: incremented shared num = %d\n", num, shared_num);
        uv_rwlock_wrunlock(&numlock); // 解写锁
        printf("Writer %d: released lock\n", num);
    }
    i = uv_barrier_wait(&blocker);
	printf("%d barrier %d\n", num, i);
}

int main()
{	
	/*
		初始化barrier锁
		要求5个线程(包括主线程)都在uv_barrier_wait等待其它线程,
		直到所有的线程都到达等待点,所有的线程才恢复执行.
	*/
    uv_barrier_init(&blocker, 5);
	
    shared_num = 0;
	/*
		初始化读写锁
	*/
    uv_rwlock_init(&numlock);

    uv_thread_t threads[4];

    int thread_nums[] = {1, 2, 1, 2};
    uv_thread_create(&threads[0], reader, &thread_nums[0]);
    uv_thread_create(&threads[1], reader, &thread_nums[1]);

    uv_thread_create(&threads[2], writer, &thread_nums[2]);
	uv_thread_create(&threads[3], writer, &thread_nums[3]);
	/*
		阻塞
		等待其它线程
		函数返回0代表等待,
		函数返回1代表恢复执行
	*/
    int i = uv_barrier_wait(&blocker);
	printf("main barrier %d\n", i);
	/*
		销毁barrier锁
	*/
    uv_barrier_destroy(&blocker);
	/*
		销毁读写锁
	*/
    uv_rwlock_destroy(&numlock);
    return 0;
}
```

libuv支持线程池,并且可以通过线程池,把cpu密集的或者其他阻塞操作,加入到事件循环中.这一个特性是nodejs所依赖的.

```
#include <stdio.h>
#include <uv.h>
#include <stdlib.h>
#include <unistd.h>

uv_loop_t* loop; /* 声明事件循环 */
uv_async_t async; /* 声明异步handle（观察者） */

void print_progress(uv_async_t* handle) {
	double p = *(double*)handle->data;
	printf("%f %% \n", p);
}
/**	
	参数req是线程请求对象
	在线程池中执行的操作
*/
void fake_download(uv_work_t* req) {
	int size = *(int*)req->data; /* 获得用户数据 */
	int downloaded = 0;	
	double percentage = 0.0;
	while (downloaded < size) {
		percentage = downloaded * 100.0  / size;
		async.data = (void*)&percentage;  /* 把消息设置在观察者的用户数据域中 */
		/*
		 向观察者发出事件 
		 并不是每次事件发生后，回调函数一定会调用
		 libuv只保证， 事件发生后回调函数一定会调用一次
		 所以，可能出现，发生多次事件，只调用一次回调函数的情况
		 不过，在回调函数调用后，如果再发生事件，肯定还会再调用一次回调函数
		 */ 
		uv_async_send(&async); 
		downloaded += (200 + random()) % 1000;
		sleep(1);
	} 
}
/*
	参数 req 参数req是线程请求对象
	主线程执行的回调函数
*/
void after(uv_work_t* req, int s) {
	printf("download complete");
	uv_close((uv_handle_t*)&async, NULL); /* 关闭观察者 */
}

int main() {
	loop = uv_default_loop(); /* 获得默认事件循环 */

	/* 初始化异步handle（观察者）, 同时立刻开始监听'异步通知事件'，所以还要提供回调函数， 这个观察者只监听这个事件 */
	uv_async_init(loop, &async, print_progress); 

	uv_work_t req; /* 声明线程池请求对象 */
	int size = 10240;
	req.data = (void*)&size; /* 设置请求对象中的用户数据字段 */

	uv_queue_work(loop, &req, fake_download, after); /* 向线程池发起请求 */


	return uv_run(loop, UV_RUN_DEFAULT); /* 开启事件循环 */

}


```

libuv支持互斥锁,它相比于pthreads中的互斥锁略有简化.

```
#include <queue>
#include <uv.h>
using namespace std;
/**
	定义队列
*/
queue<int> product;
/**
	声明互斥锁
*/
uv_mutex_t mutex;

/*
	线程运行的函数
*/
void consume(void* ptr) {
	int i = 0;
	for (i = 0; i < 10; ) {
		/*  
			锁互斥锁,
			如果失败,则阻塞线程,等待锁成功
		*/
		uv_mutex_lock(&mutex); 
		if (product.empty()) {
			/*
				解互斥锁
				允许其他线程,锁互斥锁
			*/
			uv_mutex_unlock(&mutex);
			continue;
		}
		i++;
		printf("consume: %d \n", product.front());
		product.pop();
		/*
			解互斥锁
			允许其他线程,锁互斥锁
		*/
		uv_mutex_unlock(&mutex);		
	}		
}
/*
	线程运行的函数
*/
void produce(void* ptr) {
	int i = 0;
	for(i = 0; i < 10; i++) {
		/*
			锁互斥锁
			如果锁失败,代表互斥锁被使用了,此时阻塞该线程,等待锁成功
		*/
		uv_mutex_lock(&mutex);
		product.push(i);
		/*
			解互斥锁
			允许其他线程,锁互斥锁
		*/
		uv_mutex_unlock(&mutex);
	}
}


int main() {
	/*
		初始化互斥锁
	*/
	uv_mutex_init(&mutex);
	/*
		声明线程
	*/
	uv_thread_t pro;
	uv_thread_t con;
	/*
		创建线程
	*/
	uv_thread_create(&pro, produce, NULL);
	uv_thread_create(&con, consume, NULL);
	/*
		阻塞主线程,等待其他线程返回.
	*/

	uv_thread_join(&pro);
	uv_thread_join(&con);
	/*
		摧毁互斥锁
	*/
	uv_mutex_destroy(&mutex);
	return 0;
}


```

总结:

libuv支持的线程同步方式有:

1. mutex互斥锁
2. condition条件锁
3. semaphore信号量
4. barrier栅栏锁
5. read-write读写锁

这些同步方式的功能和用法和libuv的类似,但是在功能上略有减少,使用上也更加简单.

