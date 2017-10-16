
---
title: c语言认真认识之宏
date: 2017-09-15 22:54:44
tags:
---
        [C语言条件编译及编译预处理阶段](http://www.cnblogs.com/rusty/archive/2011/03/27/1996806.html)

这篇文章比较清晰地介绍了c语言的*预处理指令*和*宏*.

不过上面这一句话可能不太准确.因为*宏*是*预处理指令* `#define xx xx`的产物.


## #define:

1. `char* s = "hello" "haoming";` 这样的写法是合法的,所以在宏里面可以写这样的语句
```
"%s:%d: expect: " format "actual: " format "\n"
```

2. 宏内换行要用`\`来分割,而且`\`和`\n`之间不可以跟任何字符,*注释*也不可以

3. 宏函数的参数尽量用括号括起来,保证参数优先级正确

4. 包含多条语句的宏,应该包括在`do {...} while(0)`中,以防止文本替换产生的bug

5. 可以使用#来把参数字符串化,同1.如果要使用1的用法,如果参数不是字符串的化,要使用#来字符串化.
```
	#define num(idx) #idx
	int i9 = 9;
	int i10 = 10;
	printf("%s\n", num(i9)); // i9
	printf("%s\n", num(10)); // 10

```

6. 可以使用##来连接值构造token


```

	#define num(idx) i##idx // 不能有括号
	int i9 = 9;
	int i10 = 10;
	printf("%d\n", num(9)); // 9
	printf("%d\n", num(10)); // 10
	
```
 

c语言的其它预处理指令有:

```

#if
#if [defined]
#else
#endif
#ifdef
#ifndef
#elif [defined]
#inlcude


```
其中`#if.*`类型的预处理指令都要以`#endif`来终结.这些指令的语义和c语言内部的`if`语义一样,不过它的功能是指示预处理器,跳过不符合条件的语句.

用途主要有:

1. 条件编译
2. include guard, 避免重复包含头文件

# 其它预处理指令

```

#paragma 未定义,由实现来决定功能
#line  num 指定下一行的行号为num
#error 使编译器在这一行编译出错

```

# 内部宏

预处理器内部包含一些宏,来提供一些元信息.

```

__FILE__ 程序文件名字符串

__LINE__ 当前代码的行号

__TIME__ 当前时间的字符串

__DATE__ 当前日期的字符串

__STDC__ 是否符合c标准的整数值(非0符合)

```









