
---
title: postgresql在windows服务器上的安装问题记录
date: 2017-09-15 22:54:44
tags:
---
        

尝试在windows server 2008 r2上安装postgresql5-x64。

遇到了如下错误：
```
an error occurred executing the microsoft vc++ runtime installer

```
按照[Can't install PostgreSQL: An error occurred executing the Microsoft VC++ runtime installer on Windows XP](https://stackoverflow.com/questions/4288303/cant-install-postgresql-an-error-occurred-executing-the-microsoft-vc-runtime)
使用命令`postgresql.exe --install_runtimes 0`跳过vc++runtime检查。

遇到如下错误：
```

C:\Users\Administrator\AppData\Local\Temp\postgresql_installer_b424dec66a\getlocales.exe
: child killed: unknown signal
```



仔细查阅谷歌后的资料后，没有得到较为清晰的答案。

因为要安装软件的服务器是被物理隔离的，所以要仔细查找问题的难度太大。考虑到出错的的原因都来自于TEMP中的程序执行。认为使用zip版本的二进制包跳过安装步骤可以避免错误。











[Installing PostgreSQL 9.1 to Windows 7 from the Binary Zip Distribution](https://www.petrikainulainen.net/programming/tips-and-tricks/installing-postgresql-9-1-to-windows-7-from-the-binary-zip-distribution/)
给出了zip版二进制免安装程序包的具体使用指南。使用这个包以后成功安装。

## 教训

1. 仔细，慢慢，认真阅读安装文档。安装文档列出了所有常见的错误的解决方法，错误日志的位置，以及一些指导。
2. 仔细，慢慢，认真阅读邮件列表和StackOverflow，虽然很多时候，都是扫一眼看看有没有信息，但是如果卡在了一个问题上的时候，应该放慢下来仔细阅读一下别人遇到的问题，或许有一些启示。
3. 编译版和免安装版，往往有更好的兼容性。