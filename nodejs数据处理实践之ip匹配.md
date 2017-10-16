
---
title: nodejs数据处理实践之ip匹配
date: 2017-09-15 22:54:44
tags:
---
        ## 问题描述

对于一份ip数据，我们希望使用开放API来获得ip地址对应的地理地址。

## ip查询API选择

互联网上开放的ip查询API有很多，但是，它们各有优缺点。笔者在短暂的实践中了解了一下两个API。

1. [淘宝IP地址库](http://ip.taobao.com/)
2. [百度普通IP定位API](http://lbsyun.baidu.com/index.php?title=webapi/ip-api) 

这两个API都是免费开放。淘宝的API的访问限制是10qps，百度API的访问限制是6000/min。百度对于未认证用户一天的访问限制次数是10万次（认证后可以提高配额）。

通过少量数据的比对，淘宝的api可以返回县地址，而百度的api基本没有返回县地址。但是百度的api访问速度，并发量都比淘宝要大的多。考虑到淘宝api的统计数据中，县数据的覆盖率也只有6.72%。所以我们选择百度的api。

读者可以查看上述的两个链接，进一步了解判断，根据自己的情况做出决定。

## API接口了解

```
http://api.map.baidu.com/location/ip?ak=yourak&ip=targetIp

```

百度的api存在两种认证模式，一种是ip白名单，一种是sn校验算。不过笔者在nodejs下发起请求时，一直没有办法算对sn值，在网络上也没有找到相应的资料，最后转而使用ip白名单模式，其实对于数据处理的应用，使用ip白名单模式就可以了。

设置ip白名单后就可以直接发起API请求了。

> 	只有IP白名单内的服务器才能成功发起调用
> 格式: 202.198.16.3,202.198.0.0/16 填写IP地址或IP前缀网段，英文半角逗号分隔
> 如果不想对IP做任何限制，请设置为0.0.0.0/0

请求的格式如上，详细请直接查看链接。

## 代码

代码的细节就不多讨论，读者可以直接阅读源代码来了解。这里提及一下使用到的npm包以及使用该包的原因和相应的技术文档，

1. 数据处理在nodejs下必然包含很多*异步操作*比如*文件读写*，*网络请求*等。所以我们使用了流程控制库`co`
如果你不了解co请参看这个链接
[Generator 函数的异步应用](http://es6.ruanyifeng.com/#docs/generator-async)
你也可以使用其它流程控制库。
2. `co-parallel`和`async`。`co`只能让异步的流程同步化。但是一些细节的控制还是要依赖其它一些库。笔者在这里没有过多调研。简单查阅资料后，使用`co-parallel`来做*并发控制*,使用`async.retry`在请求失败的时候重试。
3. `superagent` http请求库

下面是源代码。

```


const bluebird = require('bluebird')
const fs = bluebird.promisifyAll(require('fs'))
const co = require('co')
const os = require('os')
const superagent = require('superagent')
const parallel = require('co-parallel')
const async = require('async')
// 计数连接失败的个数
let failCount = 0

//百度IP地址库
const urltaoip = 'http://api.map.baidu.com/location/ip?ak=yourak&ip='
// 输入文件名字
let inputFileName = process.argv[2] || 'xxx.csv'
// 输出文件名
let outputFileName = process.argv[3] || 'result.csv'
// 输出文件流
const writer = fs.createWriteStream(outputFileName)

// 把supsuperagent 包装为promise 供co使用
// 使用async.retry 在发生错误的情况下重试5次
function getUrlPromise(url) {
    return new Promise((resolve, reject) => {
        async.retry(5, (cb) => {
            superagent.get(url)
                .end((err, res) => {
                    if (err) {
                        cb(err)
                    } else {
                        cb(null, res)
                    }
                })
        }, (err, res) => {
            if (err) {
                resolve('{}') // 重连5次后，仍然错误， 也不要抛出错误，避免程序终止
            } else {
                resolve(res.text)
            }
        })
    })
}




co(function* () {
    // 读取文件
    let content = yield fs.readFileAsync(inputFileName, 'utf-8')
    // 分割得到行
    let lineArr = content.split(os.EOL)
    // 从行中得到ip
    let ipArr = []
    for(line of lineArr) {
        let itemArr = line.split(',') // 确保ip在最后一列
        let ip = itemArr.pop()
        ipArr.push(ip)
    }

    // 构造请求列表
    let reqs = ipArr.map(function* (ip) {
        
        let url = `${urltaoip}${ip}`
        console.log(url)
        return yield getUrlPromise(url)
    })
    // 并发不超过100 来请求， 百度限制 一分钟 6000个并发请求
    let res = yield parallel(reqs, 100)



    // 输出结果
    for(let i = 0; i < res.length; i++) {
        let ipObjStr = res[i]
        let ipObj = JSON.parse(ipObjStr)
        let address =ipObj && ipObj.content && ipObj.content.address_detail
        
        if (!address) {
            failCount++;
            address = {
                province: '获取失败',
                city: '获取失败',
                district: '获取失败'
            }
        }
        console.log(address.province)
        console.log(address.city)
        console.log(address.district)
        
        writer.write(lineArr[i])
        writer.write(`,${address.province || '无数据'},${address.city || '无数据'},${address.district || '无数据'}${os.EOL}`)
    }
    
    

    

})
.catch(err => {
    console.log(err)
}) 
.then(() => {
    console.log('失败个数' + failCount)
})




```

## 参考文献：
1. [淘宝IP地址库](http://ip.taobao.com/)
2. [百度普通IP定位API](http://lbsyun.baidu.com/index.php?title=webapi/ip-api) 
3. [NodeJS实现批量查询地理位置经纬度接口](http://www.jianshu.com/p/7c17300b2c0f)
4. [Generator 函数的异步应用](http://es6.ruanyifeng.com/#docs/generator-async)
5. [async.retry](http://caolan.github.io/async/docs.html#retry)
