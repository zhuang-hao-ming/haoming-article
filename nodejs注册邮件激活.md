
---
title: nodejs注册邮件激活
date: 2017-09-15 22:54:44
tags:
---
        ## 
在网站开发时常常有这样的需求：用户注册后需要给用户发送一个激活邮件，用户点击邮件中的链接来激活账号。目的大概时确保用户使用了一个正确可用的邮箱，毕竟一个通过了正则表达式的邮箱不一定就是一个合格的邮箱。

## 实现方法

1. 注册逻辑结束后，通过代码给用户邮箱发送一个内容是`html`的邮件。
2. 用户点击`html`中的链接后，跳转到网站，网站进行确认。

## 发送邮件的方法

在nodejs中可以使用一个`nodemailer`模块来发送邮件。用法：

```
npm i nodemailer -S // 下载模块

const nodemailer = require('nodemailer')

const transporter = nodemailer.createTransport({
    host: 'smtp.126.com',
    port: 25,
    auth: {
        user: '',
        pass: ''
    },
    ignoreTLS: true
}) // 创建输送者



transporter.sendMail({
        from: 'xx@email.com',
        to: 'xx@email.com',
        subject: '标题',
        html: '内容'
}, err => {
    console.log(err)
})



```

这个模块使用SMTP协议来发送邮件。

开启126邮箱的SMTP支持的时候，用单独设置一个密码，SMTP客户端使用这个密码，而不是原先的密码。

## 验证的方法

在html中包含这样的链接

```
let token = utility.md5(data.email + config.secret + data.password)

<a href="${SITE_ROOT_URL}/active_acount?key=${token}&name=${name}">链接</a>

    
```

在该路由对应的处理程序中进行验证

```
    let key = validator.trim(this.query.key)
    let name = validator.trim(this.query.name)


    let flash = {}

    let data = yield $user.getUserByName(name)

    if (!data) {
        flash.error = `不存在用户${name} 激活失败`
    }
    else if (data.active) {
        flash.error = '账号已经激活'
    }
    else if (utility.md5(data.email + config.secret + data.password) !== key) {    
        flash.error = '信息有误，激活失败'
    }


    if (!flash.error) {
        data.active = true
        yield data.save()
        flash.success = '激活成功'
    }
    this.flash = flash
    return this.redirect('/')

```

