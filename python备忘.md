
---
title: python备忘
date: 2017-09-15 22:54:44
tags:
---
        ## 迭代器

在python中迭代器对象，是一个有__iter__方法和next方法的对象。__iter__方法返回迭代器本身，next方法返回迭代的下一个项。
任何一个对象，如果有__iter__方法，并且__iter__方法返回的是迭代器对象，那么这个对象可以被for in遍历。

一个便捷的实现__iter__方法的方式是，令__iter__方法是一个generator function，调用generator function后将返回generator对象，
generator对象是一个迭代器对象，它每一项的返回值是yield后面的值。

# 包
```
# 使用import pkgname1.pkgnam2.item来导入模块的时候，规定最后一项可以是模块或包，前面的项只能是包
# import sound.formats.a

# 使用 from xxx1.xxx2 import item 来导入时，规定最后一项首先在xxx2的命名空间中搜索，如果搜索不到，那么在xxx2中的模块或包中搜索
# from sound.formats import a
# print a
# 直接import一个变量名
# from sound.formats.a import name
# print name

# 使用 from pkgname import * 时分为以下几种情况
# 如果pkg的__init__.py文件中定义了__all__ = ['modulename1', 'modulename2']
# 那么只有modulename1,modulename2被引入当前的命名空间
# from sound.formats import *
# print dir()

# 如果pkg的__init__.py文件中没有定义 __all__ = []
# 那么__init__.py被作为一个模块导入
# from sound.formats import *
# print dir()

# 如果在from xx.xx import *前使用了
# import xx.xx.a
# import xx.xx.b
# 那么__init__.py会被导入
# a,b也会被导入
# import sound.formats.a
# import sound.formats.b
# from sound.formats import *
# print dir()
```
# 模块

模块的搜索路径为`sys.path`，它由脚本所在的路径，PYTHONPATH环境变量，和系统特化的安装路径组成，用户也可以直接修改`sys.path`来指定模块搜索路径。


可以使用`dir(moduleObject)`来列出，模块下的所有变量名。如果参数省略，`dir()`将列出当前模块下的所有变量名。`dir()`会忽略内置的变量名，如果想查看所有的内置变量名可以使用`import __builtint__ dir(__builtin__)`

`from module import *`将把模块中的所有变量名（除了用_开头的）0导入当前的环境。


## 浅复制和深复制

```
import copy
lst1 = ['a', 'b', ['c', 'd']]
lst2 = copy.deepcopy(lst1)
lst2[0] = 'h'
lst2[2][0] = 'm'

print lst2
print lst1
```
使用copy.deepcopy方法来实现深复制


```
lst1 = [1, 2, 3, 4, 5]
lst2 = lst1[:]
lst2[0] = 0
print lst1
print lst2

```
使用切片的方法来实现浅复制




## 数据类型

python和其他语言在数据类型上最大的不同,在于

```
x = 2
y = x

id(x) = id(y)

```
如这个例子所展示的,即使是基本数据类型,也是引用类型.



如果要判断两个string是否内容一致,应该使用==操作符,而不是is,因为使用is在字符串有特殊字符的情况下,结果是不确定的.

