
---
title: boost_progam_options用法
date: 2017-09-15 22:54:44
tags:
---
        ## cmake build

要使用boost库必须在编译链接时指定头文件的路径和库文件的路径以及需要链接的库的名字.一般我们通过一个构建工具来辅助,这里使用camke.

使用cmake来构建一个链接boost库的程序的步骤如下:

1. 编写CMakeLists.txt文件
```
cmake_minimum_required(VERSION 3.5)
project(main)

set(CMAKE_CXX_FLAGS "--std=gnu++11 ${CMAKE_CXX_FLAGS}")

find_package(Boost 1.54 REQUIRED COMPONENTS program_options)
include_directories(${Boost_INCLUDE_DIRS})


add_executable(main main.cpp)
target_link_libraries(main ${Boost_LIBRARIES})

add_executable(main1 main1.cpp)

```

2. cmake构建流程
```
mkdir -p build
cd build
cmake ..
make
```

*注意,只需要运行一次cmake即可,以后运行make时,如果CMakeLists.txt文件修改了的话,make会自动运行cmake调整构建*


## Boost.ProgramOptions

这个库负责命令行参数的设置和解析.

```

#include <iostream>
#include <boost/program_options.hpp>
using namespace std;
using namespace boost::program_options;


void on_age(int age)
{
	std::cout << "On age: " << age << '\n';
}

int main(int argc, char** argv)
{
	try
	{
		options_description desc{"Options"}; // 命令行选项的描述对象,可以被写到标准输出中作为帮助信息, 参数是帮助信息的标题
		// add_options() 返回一个代理对象,代理options_description
		// 代理对象重载了operator(), 可以调用代理对象来定义命令行选项
		// 这个调用返回相同的代理对象的引用,所以可以多次重复调用
		// 第一个参数是可选参数的名字, 可以传入两个名字,一个长名字和一个短名字用逗号分隔
		// 传入一个value_semantic对象的指针定义了一个名值对选项
		// 可以使用辅助函数value()来创建一个value_semantic对象,并返回它的地址
		// value是一个模板函数
		// 我们使用命令行选项的值的类型作为模板参数
		// value_semantic对象有一些有用的成员函数
		// 比如default_value()提供默认值
		// notifier链接一个回调函数,它将以选项的值被调用
		// 使用parse_command_line函数来解析命令行它返回一个parsed_options对象
		// 你一般不会直接使用parsed_options对象,而是将它和variables_map对象传给store函数,variables_map是一个map<string, variable_value>字典,选项会被存在这个字典中
		desc.add_options()("help,h", "Help screen")("pi", value<float>()->default_value(3.14f), "Pi")("age", value<int>()->notifier(on_age), "Age");

		variables_map vm{};
		store(parse_command_line(argc, argv, desc), vm);
		notify(vm); // 调用notify函数来激发那些通过notifier链接的函数

		if (vm.count("help")) // 调用字典的count函数来确定,指定的选项是否存在
			std::cout << desc << '\n';
		else if (vm.count("age"))
			std::cout << "Age: " << vm["age"].as<int>() << '\n'; // 使用variable_value的as模板函数来将值转换为选项指定的值
		else if (vm.count("pi"))
			std::cout << "Pi: " << vm["pi"].as<float>() << '\n';
	}
	catch (const error &ex)
	{
		std::cerr << ex.what() << '\n';
	}
	return 0;
}
```



```

#include <boost/program_options.hpp>
#include <string>
#include <vector>
#include <algorithm>
#include <iterator>
#include <iostream>

using namespace boost::program_options;

void to_cout(const std::vector<std::string> &v)
{
  std::copy(v.begin(), v.end(), std::ostream_iterator<std::string>{
    std::cout, "\n"});
}

int main(int argc, const char *argv[])
{
  try
  {
    int age;

    options_description desc{"Options"};
    desc.add_options()
      ("help,h", "Help screen")
      ("pi", value<float>()->implicit_value(3.14f), "Pi") // implicit_value不同于default_value, 如果不指定--pi选项,那么它是不会有默认值的, 但是允许制定--pi而不指定值,这样它会使用隐含值3.14
      ("age", value<int>(&age), "Age") // 传一个指针给value函数, 讲保存选项的值在指定的地址,同时, 选项仍然在variables_map中, 必须要调用notify后才会保存到变量中
      ("phone", value<std::vector<std::string>>()->multitoken()->
        zero_tokens()->composing(), "Phone") // sematic_value的multitoken方法指示选项可以接受多个值,zero_tokens方法指示,选项可以不接受值,composing方法指示选项可以出现多次,然后它的值将被收集在一起
      ("unreg", "Unrecognized options");

    command_line_parser parser{argc, argv}; // 命令行解析器对象
    parser.options(desc).allow_unregistered().style( // 允许未在options_description中声明的选项, 运行使用slash形式的段参数
      command_line_style::default_style |
      command_line_style::allow_slash_for_short); // 配置解析器
    parsed_options parsed_options = parser.run(); // 运行解析器

    variables_map vm;
    store(parsed_options, vm); // 保存选项的值到字典中
    notify(vm); // 使得前面的age可以设置值, 一般都要调用这个函数

    if (vm.count("help"))
      std::cout << desc << '\n';
    else if (vm.count("age"))
      std::cout << "Age: " << age << '\n';
    else if (vm.count("phone"))
      to_cout(vm["phone"].as<std::vector<std::string>>());
    else if (vm.count("unreg"))
      to_cout(collect_unrecognized(parsed_options.options,
        exclude_positional)); // collect_unrecognized函数收集没有被声明的选项,返回一个vector<string>
    else if (vm.count("pi"))
      std::cout << "Pi: " << vm["pi"].as<float>() << '\n';
  }
  catch (const error &ex)
  {
    std::cerr << ex.what() << '\n';
  }
}

```

```

#include <boost/program_options.hpp>
#include <string>
#include <vector>
#include <algorithm>
#include <iterator>
#include <iostream>

using namespace boost::program_options;

void to_cout(const std::vector<std::string> &v)
{
  std::copy(v.begin(), v.end(),
    std::ostream_iterator<std::string>{std::cout, "\n"});
}

int main(int argc, const char *argv[])
{
  try
  {
    options_description desc{"Options"};
    desc.add_options()
      ("help,h", "Help screen")
      ("phone", value<std::vector<std::string>>()->
        multitoken()->zero_tokens()->composing(), "Phone");

    positional_options_description pos_desc; // 位置选项描述对象
    pos_desc.add("phone", -1); // 讲所有位置的值给phone, phone一定要在desc中声明过, -1指定命令中所有位置的值都赋值给phone,其他值代表一个给定位置

    command_line_parser parser{argc, argv}; // 解析器对象
    parser.options(desc).positional(pos_desc).allow_unregistered(); // 配置解析器
    parsed_options parsed_options = parser.run(); // 运行解析

    variables_map vm;
    store(parsed_options, vm);
    notify(vm);

    if (vm.count("help"))
      std::cout << desc << '\n';
    else if (vm.count("phone"))
      to_cout(vm["phone"].as<std::vector<std::string>>());
  }
  catch (const error &ex)
  {
    std::cerr << ex.what() << '\n';
  }
}
```



## 参考:

1. [Boost.ProgramOptions](https://theboostcpplibraries.com/boost.program_options)
