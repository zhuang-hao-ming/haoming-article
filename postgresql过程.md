
---
title: postgresql过程
date: 2017-09-15 22:54:44
tags:
---
        ## postgresql存储过程概述

存储过程是扩展数据库功能的自定义函数。

postgresql支持两种类型的语言来编写存储过程。
1. 安全语言，任何用户都可以使用，比如SQL，PL/pgSQL
2. 沙箱语言，因为沙箱语言（比如c语言）可以饶过安全检查和访问外部资源，所以只有超级用户可以使用。

postgresql内置支持3种过程语言， SQL，PL/pgSQL,c。也可以通过扩展，来导入其它语言。

存储过程的优点：
1. 减少数据库和应用之间的交互次数。把相关的操作放在存储过程中，可以将多个sql查询减少为1个sql查询。
2. 提升应用性能， 因为存储过程是预编译保存在数据库中的。
3. 可以在多个应用中重用相同的存储过程。

缺点：

1. 需要学习一门存储过程语言
2. 存储过程无法在不同的数据库系统之间移植
3. 复杂的逻辑难以调试

## 存储过程的结构
语法：
```
[ <<label>> ]
[ DECLARE
    declarations ]
BEGIN
    statements;
 ...
END [ label ];
```
例子：
```
DO
$$
<<test_label>>
DECLARE
    counter INTEGER := 1;
BEGIN
    counter := counter + 1;
    RAISE NOTICE 'counter: %',counter;
END test_label;
$$

```

1. 存储过程包含一个可选的声明块和一个必须的体块，体块用分号结束。可以在存储过程中嵌套存储过程，子过程有自己的作用域，如果要在子过程中访问同名的父过程中的变量要用**label_name.variable_name**这种形式。
2. 存储过程可以有一个可选的label，如果指定了label，那么一定要用<<label_name>>指定头部label，而且两个label必须相同。尾部的label可以省略。
3. 所有将要使用的变量都要在声明块中声明，每个语句用分号结尾。


## 变量声明语法

```
variable_name data_type [:= expression]
variable_name table_name.column_name%TYPE;
variable_name variable%TYPE;
```

变量的初始化是在运行时决定，而不是在编译时决定。
允许使用其它变量的类型，或者是表中列的类型来指定变量的类型。

## 常量声明语法

```
constant_name CONSTANT data_type := expression;
```

常量的初始化是在运行时决定的。
常量不可以更改。