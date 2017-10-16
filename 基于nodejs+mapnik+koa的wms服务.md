
---
title: 基于nodejs+mapnik+koa的wms服务
date: 2017-09-15 22:54:44
tags:
---
        ## mapnik介绍

[Node Mapnik文档](http://mapnik.org/documentation/node-mapnik/3.5/)

## 简介
mapnik是一个又快又好的制图库,它用c++ 语言编写,但是提供了c++ ,python,nodejs接口.本文使用它的nodejs接口.

## 安装
可以直接使用npm来安装mapnik和它的nodejs绑定.然后就可以直接使用mapnik了(安装需要g++>=5),具体请查看[node-mapnik](https://github.com/mapnik/node-mapnik)

## 使用

mapnik库结构清晰.基本的使用只需要了解几个类就可以了.

1. mapnik 是导入的模块,本身主要负责提供一些元信息,和插件加载
2. mapnik.Map 负责设置数据源和样式
3. mapnik.Image 图像对象,是Map的渲染结果


## proj.4

prjo.4是一个执行空间坐标系转换的工具.主要提供3个工具:

1. proj 投影转换
2. cs2cs 和1类似,但是还可以做跨大地基准面的转换
3. geod 大地测量


很多其它gis工具使用proj.4做为自己的空间坐标系转换基础库,所以proj.4的坐标系定义方式很通用.



