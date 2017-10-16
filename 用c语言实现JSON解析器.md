
---
title: 用c语言实现JSON解析器
date: 2017-09-15 22:54:44
tags:
---
        用c语言实现json解析器本质上就是实现一个简单的编译器.

编译器的两大组成部分,词法解析器,语法分析器.在json解析中都要出现.只不过json的语法足够的简单.所以可以不需要词法解析器,根据字母即可区分不同的token.使用一个*递归下降解析器*就可以完成语法解析构建语法树.





## JSON字符串解析:

### JSON的字符串标准是:

```

string = quotation-mark *char quotation-mark
char = unescaped /
   escape (
       %x22 /          ; "    quotation mark  U+0022
       %x5C /          ; \    reverse solidus U+005C
       %x2F /          ; /    solidus         U+002F
       %x62 /          ; b    backspace       U+0008
       %x66 /          ; f    form feed       U+000C
       %x6E /          ; n    line feed       U+000A
       %x72 /          ; r    carriage return U+000D
       %x74 /          ; t    tab             U+0009
       %x75 4HEXDIG )  ; uXXXX                U+XXXX
escape = %x5C          ; \
quotation-mark = %x22  ; "
unescaped = %x20-21 / %x23-5B / %x5D-10FFFF

```

这个标准以BNF的形式给出.

概略来说,字符串由一对双引号括起来,中间是零个或者多个字符.字符可以是转义字符或者是非转义字符.

值得注意的是:
合法的转义字符区间是:

0x20-21 / 0x23-5B / 0x5D-0010FFFF

空缺的部分,0x22是双引号.0x5C是反斜杠,< 0x20的部分为控制字符等.它们都要用转义字符表示.


### 解析方法:

简单来说,通过把解析出来的字符放置在栈中,解析结束后,将栈中的数据倒出保存到数据结构 即可.

如果不在JSON字符串中包含\0,那么可以用\0来标志字符串的结尾.对字符串从头遍历,对于一般的非转义字符直接入栈,如果读到了'\'字符,说明转义字符序列开始了,需要往栈中推入一个转义字符'\f'等.不过'/'在c中不需要转义了.如果读到了非法的字符,比如转义字符没有出现在'\'后面,那么报错.

当读到结尾的单独的`"`说明,读取结束.



cmake使用

```
cmake -DCMAKE_BUILD_TYPE=Debug ..

```