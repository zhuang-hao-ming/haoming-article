
---
title: svm笔记
date: 2017-09-15 22:54:44
tags:
---
        对于一个二分类任务来说，它的模型可以定义如下：

```math
        g(x):
        \lbrace
        
        f(x) > 0 : output = +1 


        f(x) < 0 : output = -1
        
        \rbrace
```

它的理想损失函数可以定义如下：

```math

L(f) = \sum_n\delta(g(x^n)\neq y^n)

```
代表g在训练集上错误的个数。（δ是一个示性函数，如果表达式为真返回1否则返回0）

这个损失函数的缺陷在于，它不是一个连续函数，很难用梯度下降的方法来优化。


想象一下：
1. 一个理想的损失函数，应该在训练数据正确的点处取到较小的值（理想的损失函数值取0）。

2. 在训练数据点上正确意味着， 当`$y^n = +1$`时`$f(x) > 0 $`, `$y^nf(x) > 0$`，当`$y^n =  -1$`时， `$f(x) < 0$`,
`$y^nf(x) > 0$`。

根据这两点，可以知道，如果以`$y^nf(x)$`为自变量，损失函数应该是一个单调下降的函数。


## 平方损失的误差函数
如果我们这样设计误差函数，规定，如果`$y^n = +1$`那么f(x)接近+1，如果`$y^n = -1$`那么f(x)接近-1，那么它的损失函数可以定义如下：

```math
l(f(x^n), y^n) = (y^nf(x^n) - 1)^2
```

很明显，我们可以观察到，当`$y^nf(x^n)$`很大的时候，损失函数的值也会很大，但这并不合理。因为这个情况下，模型的判断应该时正确的。

## sigmoid损失函数

如果我们这样设计损失函数，规定如果`$y^n = +1$`那么，`$\sigma(f(x^n)) = 1$`,如果`$y^n = -1$`那么，`$\sigma(f(x^n)) = 0$`

那么损失函数的定义如下：

```math
l(f(x^n), y^n) = (\sigma(y^nf(x^n)) - 1)^2

```

这个损失函数，和平方损失相比，当`$y^nf(x^n)$`很大的时候，会取到较小的值，它的函数图像是S形。

## cross entropy 损失函数

```math

l(f(x^n), y^n) = \ln(1+exp(-y^nf(x^n)))
```

## hinge loss

```math

l(f(x^n), y^n) = max(0, 1-y^nf(x^n))
```


## linear svm(support vector machine)

如果一个模型，它的候选函数集是：

```math
f(x) = \sum_iw_ix_i + b

```

它的损失函数是hinge损失函数

那么这个模型就是SVM模型

hinge函数是一个凸函数，即使加上一个归一化项，多个凸函数相加还是一个凸函数，所以可以用梯度下降来优化。

### 梯度下降优化svm

svm的损失函数定义为
```math
L(f) = \sum_nl(f(x^n), y^n)

l(f(x^n), y^n) = max(0, 1-y^nf(x^n))



```

求：
```math
\frac{\partial l}{\partial \omega_i}
= \frac{\partial l}{\partial f}\frac{\partial f}{\partial \omega_i}
= \frac{\partial l}{\partial f}x_{i}^n

if 

y^nf(x^n) < 1 : \frac{\partial l}{\partial f} = -y^n

else 

\frac{\partial l}{\partial f} = 0

\frac{\partial L}{\partial \omega_i}
=\sum_n-\delta(y^nf(x^n) < 1)y^nx_{i}^n

let

-\delta(y^nf(x^n) < 1)y^ = c^n(w)

\omega_i = \omega_i - \eta \sum_nc^n(w)x_{i}^n

```

## 优化得到的权重是训练数据的线性组合



```math
w^* = \sum_n\alpha^*x^n

```

### 证明

根据前面梯度下降的公式：

```math
\omega_1 = \omega_1 - \eta \sum_nc^n(w)x_{1}^n

\omega_2 = \omega_2 - \eta \sum_nc^n(w)x_{2}^n

\omega_i = \omega_i - \eta \sum_nc^n(w)x_{i}^n

...

\omega_k = \omega_k - \eta \sum_nc^n(w)x_{k}^n


\omega = \omega - \eta \sum_nc^n(w)x^n

```

如果ω初始化为0，那么`$\omega^*$`就是`$x^n$`的线性组合。

根据前面的定义:
```math
-\delta(y^nf(x^n) < 1)y^ = c^n(w)

```
如果`$y^nf(x^n) > 1$`那么对应的α值是0，我们将对应的α非零的向量称为，支持向量。

## kernel trick

```math
\omega = \sum_n \alpha_nx^n = X\alpha

X = (x^1, x^2, ...,x^n)

\alpha = (\alpha_1,\alpha_2,...,\alpha_n)^t

f(x) = \omega^tx

= \alpha^tX^tx

= \sum_n\alpha_n(x^n.x)

let : x^n.x = K(x^n,x)

so: f(x) = \sum_n \alpha K(x^n,x)
```

观察上面的式子，如果我们知道`$K(x^n,x)$`和`$y^n$`其实就可以优化上面的问题。

我们常常会把，x做转换，转换到别的高维空间，然后再使用线性分类器。特征转换为Φ。

那么可以计算
```math
K(x^n, x) = \phi(x^n).\phi(x)

=K'(x^n,x)
```

也就是说，为了求，K(x^n,x)我们可以，先做特征转换，然后再求点乘，也可以先算到新的K函数来算。

这个特征称为kernel trick

## RBL (radial basis function)
其实我们可以直接定义
```math
K(x,z) = exp(-\frac{1}{2}||x-z||_2)
```

这个K可以认为是，把x,z投影到无穷多维，然后再做inner product


也就是说，我们可以直接定义K函数，跳过inner product。

只要K函数说明了某种相似性。






















