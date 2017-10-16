
---
title: git又备忘
date: 2017-09-15 22:54:44
tags:
---
        记得从大二还是大三开始，受到很多文章的鼓动，我就很想要用git来管理自己的代码。每次记起来了，都会在网上找个入门教程，然后花个把小时，啪啪啪啪啪地抄命令抄代码。然后，也就不了了之了。相比之下，另一个版本管理系统SVN，因了实习和项目的原因，用了有几个月的时间，反而熟悉很多，或许是因为它的gui界面更加清晰吧。而git的一些概念我一直比较模糊，以至于没能真正地在实践中使用它。

-------

昨天在nodeschool上找了git-it这个workshop，做完之后竟然有一种茅舍顿开的错觉，使我认为我终于是理清了一些git的概念。说来，我是很喜欢workshop这种学习方式。下文我对此做一些备忘和写一些感悟。

------

## 下载git

首先要离清`git`和`github`不是同一个东西。`git`是一个版本控制软件，而`github`可以说是一个用git实现的服务，它提供的功能包括：作为远程服务器(remote)，讨论，交友的社交功能，协作的fork和pull request。

git在windows下的实现很优越，不仅包含了git本身还提供了很多linux命令，完全可以吧git shell当作日常使用的shell替代cmd。
不过我使用cmder，这个shell比git shell更好用一些。

## 配置git

```
git config --global user.name "<your name>"
git config --global user.email "<youemail@example.com>"
```

配置git的目的是，让git把你做出来的改变和你的个人信息联系起来。这样别人就可以知道这个改变是你做出来的，你的联系方式是什么。这个`user.name`最好是你在`github`上的用户名*不是登录账号*。

## repository

在`git`中一个`repository`就是一个`文件夹`就是一个`项目`。在文件夹的根部使用命令`git init`，使这个文件夹成为了一个`repository`。

## add 和 commit

在仓库中的文件（文件夹）有几种状态:

- ignore 被git忽视，git认为它不存在
- stage 通过`git add <filename>`添加
- unstage 通过`git rm --cache <filename>`删除文件或者`git reset HEAD <filename>`删除自上次提交以来的更改
- commit `git commit <filename> -m "<message>"`

*ignore*说明这个文件在git的眼中不存在。
*unstage*的文件git会提示说你要stage它。
*stage*的文件，git可以提交它，也可以reset到上一次提交的状态。
*commit*则是提交

## remote
`github`充当了远程服务器的作用。可以有多个远程服务器。

通过`git remote add <remotename> <url>`添加一个远程服务器并取名

通过`git remote set-url <remotename> <url>`更改一个远程服务器的url

通过`git push <remotename> <branch>`把branch分支推到远程服务器的branch分支

通过`git pull <remotename> <branch>`把远程服务器的branch分支拉到本地的branch分支上

通过`git remote -v`查看所有远程服务器的配置

## fork 和 clone

fork是`github`使你参与开源项目的机制，通过fork一个项目，`github`把项目完整复制到属于你的服务器空间，让这个项目被你拥有，你可以对它进行修改。在`git`看来这个fork的项目就是你的项目，虽然`github`知道这个是fork来的,并且有一些处理。

通过 `git clone <url>`可以在本地建立一个与远程服务器一样的仓库并自动设置好远程服务器origin。**注意，并不需要提前创建文件夹**

fork来的项目常常需要和fork源交流，来获得最新的内容。所以通常会把源叫做`upstream`加为远程服务器，不过我们没有向这个服务器提交的权限。

## branch

通过 `git branch <branchname>`新建一个分支

通过 `git checkout <branchname>`切换到一个分支

通过 `git push origin <branchname>`把本地的分支推到远程的分支

通过 `git branch`列出所有的分支

通过`git branch -m <new branch name>`重命名当前的分支

通过`git status`检查当前工作的分支

通过`git checkout -n <branchname>`创建然后切换到新的分支

## merge

通过`git merge <branchname>`把一个分支合并到当前分支

通过 `git branch -d <branchname>`删除一个本地分支

通过 `git push <remotename> --delete <branchname>` 删除一个远程分支


## collaborator 和 pull request

这两个是属于`github`的功能。通过添加一个collaborator赋予了一个人修改你的仓库的权力。

`pull request`也叫做`PR`是和`fork`配合使用的。
你在自己的项目(fork来的项目)中做了修改,你希望最初的项目使用你的修改，也就是说你希望原作者来拉这个项目。那么你需要向原作者提出一个`pull request`。希望原作者拉走那一条分支，合并到主分支理由是什么。如果作者同意了，那么他就会把分支拉回并合并到原项目中。

这个项目的其他用户，通过`git pull <remotename> <branchname>`也可以拿到你贡献的代码。