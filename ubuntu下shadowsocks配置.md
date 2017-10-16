
---
title: ubuntu下shadowsocks配置
date: 2017-09-15 22:54:44
tags:
---
        久久以前就把旧的电脑装成了Ubuntu系统，想着，会有很多工作在Linux下处理，不过啊，人的惰性是很强的。一直也没有从windows切换过来。主要是用来翻越gfw的shadowsock一直懒得配置。今天花了一点时间把它弄好了。下文记录一下步骤，作为备忘

## 安装shadowsocks-qt5

从`shadowsocks-qt5`的项目主页上查看下载方式。
在ubuntu上的过程是：
```
sudo add-apt-repository ppa:hzwhuang/ss-qt5
sudo apt-get update
sudo apt-get install shadowsocks-qt5

```

### 配置

通过搜索找到安装好的软件。按照和windows类似的方法填写好服务端信息。

## pac文件生成

安装pip,然后通pip安装genpac，然后通过genpac生成pac文件。之后，打开系统设置中的网络，选择网络代理，设置代理为自动代理，配置url为生成的pac文件。

## 参考文献

[安装指南](https://github.com/shadowsocks/shadowsocks-qt5/wiki/%E5%AE%89%E8%A3%85%E6%8C%87%E5%8D%97)

[使用手册](https://github.com/shadowsocks/shadowsocks-qt5/wiki/%E4%BD%BF%E7%94%A8%E6%89%8B%E5%86%8C)

[genpac生成](http://www.pulller.com/2015/06/02/shadowsocks%E5%9C%A8ubuntu%E4%B8%8B%E7%9A%84%E8%87%AA%E5%8A%A8%E4%BB%A3%E7%90%86%EF%BC%88pac%E6%A8%A1%E5%BC%8F%EF%BC%89/)
