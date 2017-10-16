
---
title: nodejs数据处理实践
date: 2017-09-15 22:54:44
tags:
---
        任务描述：

有一个csv文件， 但是其中某些行的字段的值是一个json数组，数组的值又是json对象，内部有很多`','`。

这导致，在其它的数据分析工具中，无法进行处理。

现在我们希望，把这个json数组拆分开来，取出内部的值，然后对于字段值不是json的则补空位，形成一个比较规整的表格。遍历于后面分析。


> 最好的语言，是熟悉的语言。

所以我用了js，当然因为是处理文件，所以肯定是nodejs.

不过熟悉是相对的，真正开始还是要靠google。


## 思路

大概的思路就是，使用`readline`模块，逐行读取文件，然后对于每一行，首先使用`split(,)`切分开来，然后对数组的长度进行判断，数组长度超过规定值的，就是内部包含json数组的，因为json数组的位置，总是在第3个到导数第2个之间，使用`slice()`函数，提取出来。然后把这个不规整的数组，用`join()`拼成`json`字符串，再解析出数组，提取出值，写回去，对于正常的行，则使用一个固定的模式填补。


## 代码

```

const readline = require('readline');
const fs = require('fs');
const os = require('os')

let inputName = process.argv[2] || 'honglingbo_12844_result.csv' // 输入文件
let outputName = process.argv[3] || 'parse3 .csv' // 输出文件

const reader = fs.createReadStream(inputName);
const writer = fs.createWriteStream(outputName);
const rl = readline.createInterface({
    input: reader,
    output: writer
});


let lineNum = 0;
let 没用的数 = 0;
let padArray = ['null', 0, 'null', 0, 'null', 0]


rl.on('line', (line) => {
    if (lineNum == 0) {
        lineNum++;
        return; // 跳过行头
    }

   
    let arr = line.split(',');
   
    if (arr.length > 5) {
        // 特殊情况，含有json数组
        let midArrRaw = arr.splice(3, arr.length - 4); // 取出json数组部分
        
        let json = midArrRaw.join(','); // 拼成json字符串

        let midArr = JSON.parse(json); // 解析json
        let newMidArr = []
        for (let i = 0; i < midArr.length; i++) {
            let obj = midArr[i]
          
            for(let key in obj) {
                newMidArr.push(obj[key]) // 遍历，解析出对象中的值， 这里不保险，因为 for in 不保证顺序，不过在这里没有问题
            }
        }
        if (newMidArr.length !== 6) {
            console.log(newMidArr)
            throw new Error('error ' + lineNum + midArr) // 异常终止， 解析出来的数组长度应为6
        }
        
        arr.splice(3, 0, ...newMidArr); // 把数组插入到第3个位置。 ...是es6语法，把数组扩展开
        
    } else {
        arr.splice(3, 1, ...padArray); // 正常情况， 把补位数组插入
    }

    writer.write(arr.join(',') + os.EOL) // 输出， 这里用','分割，如果','不行也可以换别的，csv文件不一定要用','分割
    
    没用的数++;
    if (没用的数 == 10000) {
        console.log(lineNum) // 输出一下进度
        没用的数=0
    }
    

    lineNum++;

});

// close事件监听
rl.on("close", function () {
    // 结束程序    
    console.log(lineNum)
});


```

## 总结
使用
```
require('os').EOL
```
来得到操作系统范化的换行符。

*令我疑问的是，不知道为什么不可以直接利用readline模块输出。*

参考文献：


1. [【node.js】'readline' 逐行读取、写入文件内容](http://sodino.com/2016/04/28/nodejs-readline/)

2. [nodejs readline](https://nodejs.org/api/readline.html#readline_rl_write_data_key)

3. [nodejs中如何按行读取文件？](https://cnodejs.org/topic/4f152db38b3242105b00405d) 
