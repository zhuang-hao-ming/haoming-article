
---
title: c语言认真认识const
date: 2017-09-15 22:54:44
tags:
---
        [C语言的那些小秘密之const修饰符](http://blog.csdn.net/bigloomy/article/details/6595197/)

这篇文章介绍了c语言的const修饰符.其中最值得注意的点是:

**const指针值** 

还是 

**const指针指向的内存值**

```
int k = 0;
int* const i = &k; /***const指针值** */

const int* j = &k; /***const指针指向的内存值** */

int const* j = &k; /***const指针指向的内存值** */

```

作者提到的口诀:

**const出现在`*`之后意味着地址被const不能改变**

**const出现在`*`之前意味着地址指向的内存被const不能改变**


```

#include "stdio.h"
int main() {
	int k = 0;
	int m = 5;
	int* const i = &k;
	printf("%d\n", *i);// 0
	*i = 2;
	printf("%d\n", *i); // 2
	printf("%d\n", k); // 2
	//i++; // 报错

	int const* j = &m;
	//const int* j = &m;
	
	printf("%d\n", *j); // 5
	j = &k;
	printf("%d\n", *j); // 2
	//*j = 3; // 报错


}


```

