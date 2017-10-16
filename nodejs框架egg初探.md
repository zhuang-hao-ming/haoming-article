
---
title: nodejs框架egg初探
date: 2017-09-15 22:54:44
tags:
---
        ##

阿里最近开源了一个新的nodejs框架egg，昨晚和今天花了一些时间探索了一下。框架还很不稳定，在我实验的时候，`模板渲染`的规范刚刚在更改。导致在应用模板引擎的时候一直出错。令人不爽。`orm`规范也还没有出来。

##

egg框架是一个强调**约定强于配置**的框架。所以除非用户自己去更改加载器，否则就要按照**约定**来组织目录结构，文件名，代码结构。这使得多人开发时，代码的一致性得到了很好的保证。对于个人来说，也得到了一个可以遵守的规范。

egg强调自己是一个轻量的框架，但毋庸置疑，这个框架相比于koa这种超基础框架来说还是要重了很多。

##

下文开始对egg框架的开发做一些介绍。

##

在开发环境中，egg使用`egg-bin`来辅助。在`package.json`中配置命令。

```
  "dependencies": {
    "egg": "^1.0.0-rc.1"
  },
  "devDependencies": {
    "egg-bin": "^2.2.1"
  }

    
    "scripts": {
        "dev": "egg-bin dev --port 7002"
     }
```

然后在终端中输入`npm run dev`就可以启动项目，这个工具的优点就是，更改了文件后，项目会自动重启，不需要用户去反复启动。从这里可以看到，node项目的入口是被隐藏到底层去的。


##
egg项目的目录规范。（）

```
/
    app/
        controller/
        service/
        public/
        views/
        extend/
        router.js
    config/
        config.defualt.js
        plugin.js


```
## router.js

egg把所有的路由规则都集中到router.js文件中。它的思路是，确保不会有路由冲突。而且路由挂载的操作其实和配置文件一样，不需要很复杂的目录结构来管理。语法如下：

```

module.exports = app => {
    app.redirect('/', '/news')
    app.get('/news', 'news.list')
    app.get('/news/item/:id', 'news.detail')
    app.get('/news/user/:id', 'news.user')
}

```

**约定**:文件导出一个函数
`app => {}`路由挂载在`app`上。


## controller

`controller`顾名思义是控制层，系统给`controller`赋予的能力是，处理对应的路由请求。具体来说就是:
1. 请求参数校验
2. 调用service服务得到响应结果
3. 对响应结果进行调整，并返回

`egg`在`controller`的语法比较灵活，但我认为，使用者应该只使用一种语法，并且保持一致。

```

// app/controller/news.js

module.exports = app => {
    class NewsController extends app.Controller {
        * list() {            
            const ctx = this.ctx
            const pageSize = ctx.app.config.news.pageSize
            const page = ~~ctx.query.page || 1
            const idList = yield ctx.service.hackerNews.getTopStories(page, pageSize)
            const newsList = yield idList.map(id => ctx.service.hackerNews.getItem(id))
            ctx.body = newsList

        }
        * detail() {
            const ctx = this.ctx
            const id = ctx.params.id
            const newsInfo = yield ctx.service.hackerNews.getItem(id)
            const commentList = yield (newsInfo.kids || []).map(id => ctx.service.hackerNews.getItem(id))
            ctx.body = {
                newsInfo,
                commentList
            }
        }
        * user() {
            const ctx = this.ctx
            const id = ctx.params.id
            const userInfo = yield ctx.service.hackerNews.getUser(id)
            ctx.body = userInfo
        }

    }
    return NewsController
}

```

总结如下：

 * 导出一个函数
 * 函数的参数是 app
 * 函数的返回值是一个继承**app.Controller**的类
 * 类中的方法可以作为controller（不一定是controller也可以是辅助方法）
 * controller要求是generator函数
 * controller 接受一个参数ctx代表请求上下文
 * 在类中的controller访问this.ctx和参数ctx效果一样，都是请求上下文
 
**在类中this代表Controller类实例，this.ctx代表koa上下文对象,其他的Service也类似，只要通过this.ctx获得上下文对象，进而就可以获得挂载在上下文上的service，helper，app， app.config，其他出于便利的代理属性可以不用**


 ## Service
 
 ```
 // app/service/hackerNews.js
 
 /**
 * 导出一个函数
 * 函数返回一个继承app.Service的类
 * 类中的方法通过this.ctx访问上下文
 * 通过上下文来获取框架和插件提供的功能
 *  
 */
module.exports = app => {
    class HackerNews extends app.Service {
        constructor(ctx) {
            super(ctx)
            this.serverUrl = this.ctx.app.config.news.serverUrl
            this.pageSize = this.ctx.app.config.news.pageSize
        }
        /**
         * @param {String} api 
         * @param {Object} opts 
         * @return {Promise} 
         */
        * request(api, opts) {
            const options = Object.assign({
                dataType: 'json', // 返回值类型
                timeout: ['30s', '30s'], // 连接超时时间， 响应返回超时时间
            }, opts)

            const result = yield this.ctx.curl(`${this.serverUrl}/${api}`, options)
            return result.data
        }
        /**
         * @param {int} page
         * @param {int} pageSize
         * @returns {Promise} 
         */
        * getTopStories(page, pageSize) {
            page = page || 1
            pageSize = pageSize || this.pageSize
            const result = yield this.request('topstories.json', {
                                    data: {
                                        orderBy: '"$key"',
                                        startAt: `"${pageSize * (page - 1)}"`,
                                        endAt: `"${pageSize * page - 1}"`,
                                    }
                                })
            return Object.keys(result).map(key => result[key])
        }

        * getItem(id) {
            return yield this.request(`item/${id}.json`)
        }

        * getUser(id) {
            return yield this.request(`user/${id}.json`)
        }





    }
    return HackerNews
}
 ```

`service`的职责是负责给`controller`提供数据。

整体语法上，`service`和`controller`类似。


## views

### 模板渲染，等到egg更稳定了再研究


## ORM

数据库层的规范也还没确定

## config

在config文件夹下可以有多个配置文件。

```
config.defualt.js
config.test.js
config.unittest.js
config.prod.js

```
在所有环境下都会加载`default`其它的在特定环境下加载。后面加载的文件会覆盖前面加载的文件，环境特化的文件会覆盖默认文件。整体的加载顺序是插件，框架，应用

## 插件

插件在config/plugin.js中启用。注意插件的配置不在这里，还是在配置文件。

