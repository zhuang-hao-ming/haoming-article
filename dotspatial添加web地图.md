
---
title: dotspatial添加web地图
date: 2017-09-15 22:54:44
tags:
---
        
有这样一个需求，要在dotspatial程序中添加web地图，作为底图。

由于，我们的dotspatial程序，并不单单使用dotspatial这样一个库，所以很难说使用dotspatial的
webmap插件。因为dotspatial的插件机制，是有比较强的约定的， 它要求宿主实现IDockManager，IHeaderControl，IStatusControl这些接口。并且依赖于.net的MEF（manage extension framework）插件机制。

而我们的程序使用的是sharpdeveloper的插件机制。这是一种依赖于配置文件与反射的插件机制。并且对于界面也有要求。

所以我们无法使用webmap插件。

> [MEF](https://www.codeproject.com/articles/376033/from-zero-to-proficient-with-mef)
> 这篇文章比较详细地介绍了，MEF的机制。


一个比较好的想法是，将DotSpatial.Plugins.WebMap这样一个dotspatial的插件，改装成适合我们插件机制的插件。


整个过程的想法并不困难，虽然在实现的时候，饶了很多弯路。


-----------

## 第一步

任何时候，想要从一个开源项目中，提取一点功能，总是需要获得它的源代码，并且运行起来，才有了后面操作的可能。


dotspatial的代码已经迁移到了github上。直接

```
git clone https://github.com/DotSpatial/DotSpatial.git

```

下载代码即可。

下载以后就是编译生成了。*build*这样一个过程只有在windows上才会如此困难。我想这也是大家，纷纷投奔linux的原因。

值得一提的是，nutget存在两种自动构建的机制，在旧版本中需要.nuget文件夹，在新版本的vs中，则不再需要这个文件夹了，只需要在工程下面有package.config文件。而且在新版本中使用旧版本的解决方案是会报错的。

网络上给出的解法是，删除掉.nuget文件夹，并且把所有.sln文件.csproj文件中对.nuget的依赖都删除掉。

*注意哦，笔者一直一zhi没有能成功切换*


不过在dotspatial这个项目中，提供了两个解决方案文件。可能是开发团队考虑到了这个问题。我使用vs2015社区版，打开.sln后缀（没有vs2010标记）的解决方案顺利构建成功。


## 第二步

从插件中，抽离出最本质的代码。这一步，就是一b的步一布删除掉我们不需要的和原本插件机制相关的代码，以及一些其它的界面控制代码。

没有什么技巧可言。

附录抽取出来的代码加注释。


## 总结

看了dotspatial的一些代码，又受到了很多震惊。

任何稍微庞大一点的项目，或者专业一点的项目，都充满了很多高级技术。比如代码中大量的使用了，c#的较新的语法，比如匿名列表，对象，匿名函数，linq，var，还有比较特别的后台线程机制设计。

如果认真阅读，我想应该可以学习到很多东西吧。














