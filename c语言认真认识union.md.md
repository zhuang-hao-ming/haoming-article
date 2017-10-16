
---
title: c语言认真认识union.md
date: 2017-09-15 22:54:44
tags:
---
        [浅谈C语言中的联合体](http://www.cnblogs.com/dolphin0520/archive/2011/10/03/2198493.html)

union存在的场景是,多个数据选一的时候.

作者在这篇文章中,指出了union的特点.

1. union中所有成员现对于union变量的地址偏移为
2. union所占的内存大小,要足够大来容纳最大的成员
3. union的内存对齐要配合内部成员和自身




```

#include <stdio.h>

typedef union {
	char s[9];
	int i;
	double u;
} U1;

typedef union {
	char s[8];
	int i;
	double u;
} U2;

int main() {
	U1 u1;
	U2 u2;
	printf("%ld\n", sizeof(u1)); // 16
	printf("%ld\n", sizeof(u2)); // 8
}

```

关于*内存对齐*还需要继续探讨.