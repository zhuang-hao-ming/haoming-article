
---
title: associative container理解
date: 2017-09-15 22:54:44
tags:
---
        关联容器的主要目的是查找。有两大类关联容器：
1. rb_tree类
2. hashtable类

## hashtable

关联容器的目的是*快速查找元素*。为了实现这个目的就要在元素的存储上做特别的设计。hashtable就是符合要求的一个存储数据结构。

数据结构hashtable

对于一类元素，它有N种不同的实例，我们可以为每种实例映射一个不同的整数。假设我们有一个长度为N的连续存储空间(vector),对于第n种实例我们可以存储在位置n。查找元素时，只要确定了元素的种类，如元素
是第n种就可以直接在位置n以O(1)的时间复杂度取回元素。

上述的描述忽略了两个问题

1. 一类元素可能有无限多种不同的实例，无法分配一个如此长的连续存储空间。
2. 同一种实例可能出现多次，如何存储。

问题解法

1. 我们可以分配一个有限的长度为N的连续内存。然后对于实例映射的整数n做`n = n % N`确定存取位置。（此时可能出现多个元素保存到同一个位置的情况，即问题2）。
2. 同一个位置无法存储多个元素，对于这个问题一般有两个想法：
    1. 设计第二规则，例如当元素在位置n重复时在(n+1,n-1,n+2,n-2,n+3,n-3...)或(n-1,n+1,n-4,n+4,n-9,n+9,...)处寻找空位置。有1次2次或多次的规则。或其它合适的规则。
    2. 将多个相同的元素串成链表，将表头保留在连续内存上。（标准库的做法）

特殊设计

链表的查找时间复杂度是O(n)，为了保证查找速度，标准库设计了*rehashing*的策略来保证链表不过长。

当hashtbale中的元素大于hashtable中的bucket时执行`rehashing`的操作，分配大小为原来两倍的bucket，然后将元素重新插入hashtable。

标准库将bucket的数目设计为素数，并且将相邻大小差约为2倍的一个素数数组hardcode在代码中。


```
#include <unordered_map>
#include <string>
using std::unordered_map;
using std::string;
using std::pair;
void testMap()
{
	unordered_map<string, double> name_rate_map;
	name_rate_map.insert(pair<string, double>("haoming", 100));		
	name_rate_map["xiaoming"] = 50;
	auto it = name_rate_map.find("xiaoming");
	if (it != name_rate_map.end())
	{
		cout << it->second << endl;
	}		
}
```


