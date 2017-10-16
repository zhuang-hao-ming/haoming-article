
---
title: merge多个栅格图像的方法
date: 2017-09-15 22:54:44
tags:
---
        
镶嵌栅格图像是一个费时的操作(为什么?)

实现图像镶嵌可以使用方法有：
1. arcgis的Mosaic To New Raster工具
2. gdal的gdalwarp
3. gdal的gdal_merge.py


gdalwarp是一个多功能的工具，它可以投影raster,利用地面控制点扭曲raster,镶嵌raster
mosaic to new raster和gdal_merge.py是一个单纯的mosaic工具

gdal_merge.py把所有的raster读入内存中，然后又在内存中分配了mosaic后图像的内存，所以它的运行速度很快，但只适合小图像和镶嵌。
gdalwarp则只会利用一个固定大小的内存块来进行操作，所以即使是很大的图像也可以进行镶嵌，但是速度会较慢，可以通过-wm选项来增加这个内存块的大小。
因为gdalwarp需要进行频繁的磁盘IO，我们可以设置--config GDAL_CACHEMAX xxx来设置底层IO的缓存大小。
使用32位的gdalwarp时受制于进程的可用内存和内存碎片问题，可能很难在堆中分配一个大块内存，这时候使用64位gdalwarp是一个比较好的选择。


## 参考
1. [The gdalwarp utility](https://trac.osgeo.org/gdal/wiki/UserDocs/GdalWarp)
2. [gdal_merge.py](http://www.gdal.org/gdal_merge.html)
3. [Mosaic To New Raster](http://desktop.arcgis.com/en/arcmap/10.3/tools/data-management-toolbox/mosaic-to-new-raster.htm)