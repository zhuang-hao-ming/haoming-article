
---
title: postgresql 连接 总结
date: 2017-09-15 22:54:44
tags:
---
        ## inner join
```
SELECT
 A.pka,
 A.c1,
 B.pkb,
 B.c2,
 C.c3
FROM
 A
INNER JOIN B ON A .pka = B.fka
INNER JOIN C ON B.pka = c.fka;
```

对于主表A中的每一行，pg扫描表B检查是否有行满足连接条件，继续扫描表C，检查是否有行满足连接条件。如果找到一个匹配，将匹配加到结果集中。然后按照多重循环的顺序继续判断。对于多表同理。

## left join (left outer join)

```
SELECT
 A.pka,
 A.c1,
 B.pkb,
 B.c2
FROM
 A
LEFT JOIN B ON A .pka = B.fka;
```

和inner join类似。但是对于a中最终找不到匹配的行，仍然会保留到结果集中，并将其它字段的值设置为null。


## full outer join
```
SELECT * FROM A
FULL [OUTER] JOIN B on A.id = B.id;
```

和left join类似， 但是对于右边最终未被匹配的结果，也会被加入到结果集合中，并将其它字段值设置为null


## cross join
```
SELECT * 
FROM T1
CROSS JOIN T2;

SELECT * 
FROM T1, T2; 
```
交叉连接，产生两个或多个表的笛卡儿积。交叉连接有两个类似的语法。


## natural join

```
SELECT *
FROM T1
NATURAL [INNER, LEFT, RIGHT] JOIN T2;
```


自然连接使用两个表的同名字段，基于同名字段值相同的条件来进行连接。
可以指定多种连接类型，如果没有指定，默认使用inner join。

使用自然连接时候要注意，如果两个表之间有多个字段相同，那么可能出现问题。


# 注意
1. cross join 和 inner join.使用corss join + where得到的结果和使用inner join相同。根据
[https://stackoverflow.com/questions/670980/performance-of-inner-join-compared-to-cross-join](https://stackoverflow.com/questions/670980/performance-of-inner-join-compared-to-cross-join)
cross join 和 inner join没有性能差别，使用何种方法只是喜好的问题。

使用explain sql语句观察cross join和inner join的查询计划,查询计划相同：

```
cross join + where:

Nested Loop (cost=0.71..17.01 rows=1 width=148)
    -> Index Scan using gps log valid idx on gps log valid gps (cost0.43..8.45 rows = 1 width=46)
        Index Cond: (id=23421853)
    -> Index Scan using shenzhen line1 gidx on shenzhen line1 r (cost0.28..8.55 rows=1 width=102)
        Index Cond: (geom && expand(gps.geom, '50':double precision))
        Filter: ((geom && expand(gps.geom, '50':double precision) AND
        st dwithin(gps.geom, geom, '50'::double precision))


```