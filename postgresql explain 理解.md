
---
title: postgresql explain 理解
date: 2017-09-15 22:54:44
tags:
---
        ## 
postgreSQL数据库会为每一个查询设计查询计划。一个符合查询特点和数据特点的查询计划对于性能的影响是重大的。所以postgreSQL有一个规划器来为查询选择一个好的查询计划。

**我们可以使用EXPLAIN命令来查看，规划器究竟为一个查询选定了什么样的查询计划**

## 查询计划的结构

查询计划是一颗查询节点树。树的最底层节点是扫描节点，它负责获取数据行。根据访问表的方法有*sequential scans*,*index scans*,*bitmap index scans*,也有其它从非表源获取数据行的扫描节点。在扫描节点上是负责排序，聚集，连接等特定操作的查询节点。在输出中，查询节点由一个总结行和可选的附加属性行(相对总结行缩进)组成。总结行包含节点的类型，执行该节点的估计成本信息。节点树的第一行，也就是最顶部的查询节点的总结行，带有整个查询计划的估计时间，规划器的目的就是最小化这个估计时间。


```
explain select * from gps_log limit 1;

"Limit  (cost=0.00..0.02 rows=1 width=64)"
"  ->  Seq Scan on gps_log  (cost=0.00..231633.24 rows=10354424 width=64)"

```

如上代码所示，查询节点总结行中括号中数字的含义如下（从左至右）:

1. 启动成本（估计），这个值代表从开始查询到开始输出经过的时间，例如，对于一个排序节点，排序花费的时间就是它的启动成本。
2. 总成本（估计）， 这个值代表，假设整个查询节点运行完毕的成本。由于父查询节点可能会在当前查询节点运行完毕之前就终止它，所以实际的运行时间可能会比总成本小。（如上代码的limit节点）
3. 输出数据行（估计），这个值代表，假设整个查询节点运行完毕输出的数据行数目(不是处理的数据行)。
4. 输出行的大小（估计），单位为byte

成本是无单位的，它使用配置中成本变量的值来计算。通常我们将*seq_page_cost*设置为1，然后其它成本变量依此按照比列关系设置值。这样，我们可以认为成本的单位是*seq_page_cost*,当然也可以使其它成本变量作为单位。

上层查询节点的总成本是它所有子查询节点总成本的和（运行完毕的情况下）。成本不包括将数据传输客户端的时间（虽然在真实环境下这很重要，但是查询规划器并没有能力改变这个时间（任何正确的查询计划都应该返回相同的结果），所以它不考虑它）。

## 规划器如何计算总成本

```
ANALYZE gps_log; -- 更新表的统计信息，也就是relpages, reltuples


-- 获得表的统计信息
select relpages, reltuples from pg_class where relname = 'gps_log';

输出：
relpages;reltuples
128089;1.03589e+007

relpages代表表所占用的磁盘页, reltuples代表表的总行数。

explain select * from gps_log where car_id = '13632984831';

输出：

"Seq Scan on gps_log  (cost=0.00..257574.66 rows=2650 width=64)"
"  Filter: (car_id = '13632984831'::text)"


```

总成本计算公式：
```
(disk pages read * seq_page_cost) + (rows scanned * (cpu_tuple_cost + cpu_operator_cost))

默认情况下：
seq_page_cost = 1
cpu_tuple_cost = 0.01
cpu_operator_cost = 0.0025


查询
select * from gps_log where car_id = '13632984831';
的成本为：

128089 + 0.0125 * 1.03589e+007 = 257575.25

```

## 参考
1. [Chapter 14. Performance Tips](https://www.postgresql.org/docs/9.6/static/using-explain.html#USING-EXPLAIN-BASICS)