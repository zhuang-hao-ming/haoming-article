
---
title: 文献综述_用半自动分割改进NDBI城市提取
date: 2017-09-15 22:54:44
tags:
---
        Improving the normalized difference built-up index to map urban built-up areas using a semiautomatic segmentation approach

http://dx.doi.org/10.1080/2150704X.2013.763297



------------

这篇文章，首先介绍了先前的一种用NDBI来自动提取建成区地图的方法。
这种先前的方法，假设NDBI的正值都是建成区，假设NDVI的正值都是植物。
然后令BU = NDBI - NDVI
让BU为正值的代表城市，BU为负值的代表非城市。
然后，

它将上述的所有NDBI和NDVI保持连续，然后得到了一个连续BU，通过一个double-window flexible pace(DFPS)的方法来搜索一个最优阈值，分割出非城市和城市。

这个搜索的方法，大概描述如下：

首先对`$BU_c$`找出它的最大值b和最小值a，然后确定一个m代表搜索次数，这样搜索的步长`$p = (b - a)/m$`,
搜索的阈值依次是`$a + p, a+2p, a+ 3p, ..., b$`,
对于每一个阈值，在训练样本上得到一个正确率。
其中最大的正确率是`$L_{max}$`最小的是`$L_{min}$`，
如果`$L_{max} - L_{min} < \delta$`那么就选出`$L_{max}$`对应的阈值作为最优阈值。

否则，将b,a设置为`$L_{max}$` `$L_{min}$`对应的阈值，然后重新搜索。

直到找到最优阈值。

这里的假设是，训练样本上的阈值，也是总体的阈值。