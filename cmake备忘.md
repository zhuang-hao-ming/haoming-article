
---
title: cmake备忘
date: 2017-09-15 22:54:44
tags:
---
        1. *cmake*生成的vs2015解决方案存在“字符编码”问题？
vs2015不支持*utf-8*?
2. 编译错误的问题？ 有一些库没有找到？

## cmake使用备忘

[Introduction to CMake by Example](http://derekmolloy.ie/hello-world-introductions-to-cmake/)

作者在这篇文章中介绍了cmake的最基本用法。


### cmake的安装

在ubuntu下使用如下命令完成安装。
```
$ sudo apt-get install cmake
$ cmake -version # 这个命令查看下载的cmake的版本

```

## CMakeLists.txt 文件

cmake的使用需要配置文件*CMakeLists.txt*

一个最简单的配置文件的内容如下

```
cmake_minimum_required(VERSION 3.5.1) # 指定了这个配置文件依赖的最低cmake版本号，一般填写当前的版本号。
project(hello) # 为将要构建的项目命名
add_executable(hello hello.cpp) # 编译链接hello.cpp文件生成可执行文件hello

```

在这个最简单的项目中。`hello.cpp`和`CMakeLists.txt`在同一个目录下， 这个目录是项目（project）的根目录

一个比较好的实践是，将构建的可执行文件和构建所需要的一些临时文件都输出到一个子目录build/中，使源代码保持整洁。

使用如下命令，完成项目的构建
```
$ mkdir build # 新建build目录 
$ cd build # 进入build目录下
$ cmake .. # cmake 参数是project目录，即CMakeLists.txt所在的文件夹， 在这个例子中是 ..
$ make # 执行生成的Makefile文件完成构建
$ ./hello # 执行生成的可执行程序

```


## 多目录项目的构建

常常遇到项目是多目录的情况。可执行文件是由多个源文件编译链接生成的，同时也有多个头文件。

CMakeLists.txt的编写如下:
```
cmake_minimum_required(VERSION 3.5.1) # 指定了这个配置文件依赖的最低cmake版本号，一般填写当前的版本号。
project(hello) # 为将要构建的项目命名

include_directories(./include) # 指示#include预处理指令的搜索位置

file(GLOB SOURCES "./src/*.cpp")
 # 把当前目录下的src目录下的所有.cpp后缀的文件拼接成一个变量 SOURCES 值为 src/hello.cpp src/main.cpp
 # GLOB指示了可以使用通配符语法
 # set(SOURCES src/hello.cpp src/main.cpp) 等价

add_executable(hello ${SOURCES}) # 编译链接SOURCES所指的文件生成可执行文件hello


```

## 生成共享库

一般的开发中除了生成可执行文件外，有时也可能生成库。包括静态库和动态库。

生成动态库的CMakeLists.txt文件的写法：

```
cmake_minimum_required(VERSION 3.5.1) # 指定了这个配置文件依赖的最低cmake版本号，一般填写当前的版本号。
project(hello) # 为将要构建的项目命名

set(CMAKE_BUILD_TYPE Release) # 库一般以Release的方式发布，不过也可以是Debug

include_directories(./include) # 指示#include预处理指令的搜索位置

file(GLOB SOURCES "./src/*.cpp")
 # 把当前目录下的src目录下的所有.cpp后缀的文件拼接成一个变量 SOURCES 值为 src/hello.cpp src/main.cpp
 # GLOB指示了可以使用通配符语法
 # set(SOURCES src/hello.cpp src/main.cpp) 等价

 add_library(myLibrary SHARED ${SOURCES}) # 编译链接生成共享库

 # 共享库需要保存在库的搜索路径中，才可以被其它程序使用，使用下面这个配置命令
 # 允许用户使用`sudo make install`命令，来将共享库保存到可以被搜索到的路径中去
 install(TARGETS myLibrary DESTINATION /usr/lib)

```

*可以使用`ldd`命令来显示一个可执行文件或者库依赖那些共享库，以及它们的信息。*
```
ldd myLibrary.so

```

## 生成静态库

生成静态库的CMakeLists.txt文件的写法，和生成共享库的并没有什么区别。唯一的区别命令是:

```

add_library(myLibrary STATIC ${SOURCES}) # 编译链接生成静态库

```
可以使用下面这个命令,来列出这个静态库由那些目标文件组成。
```
ar -t myLibrary.a 
// hello.o
// main.o
```

也可以使用下面的命令，列出静态库使用的符号。
```
nm -C myLibrary.a 

```

## 使用库文件

如果一个项目需要使用其它库文件，那么它的配置文件书写如下：

```
cmake_minimum_required(VERSION 3.5.1) # 指定了这个配置文件依赖的最低cmake版本号，一般填写当前的版本号。
project(hello) # 为将要构建的项目命名

# 库文件搜索目录
link_directories(myLibrary1/build)
link_directories(myLibrary2/build)
# 保存要链接的库的名字到变量中
set(PROJECT_LINK_LIBS myLibrary1.so myLibrary2.a)
# #include指令搜索目录
include_directories(myLibrary1/include)
include_directories(myLibrary2/include)
# 编译链接生成可执行文件
add_executable(main main.cpp)
# 链接库到可执行文件中
target_link_libraries(main ${PROJECT_LINK_LIBS})

```





