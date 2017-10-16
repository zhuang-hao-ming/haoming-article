
---
title: postgis空间数据表建立
date: 2017-09-15 22:54:44
tags:
---
        有两种建立带几何字段数据表的方法。

## 直接建立

```
CREATE TABLE points (name varchar, point geometry);

INSERT INTO points VALUES ('Origin', 'POINT(0 0)'),
  ('North', 'POINT(0 1)'),
  ('East', 'POINT(1 0)'),
  ('West', 'POINT(-1 0)'),
  ('South', 'POINT(0 -1)');

SELECT name, ST_AsGeoJSON(point) FROM points;
SELECT name, ST_AsText(point) FROM points;
SELECT name, ST_AsKML(point) FROM points;
SELECT name, ST_AsSVG(point) FROM points;
SELECT name, ST_AsGML(point) FROM points;

```

## 使用AddGeometryColumn函数

```
CREATE TABLE lines (name varchar);

SELECT AddGeometryColumn('lines', 'line', -1, 'LINESTRING', 2);

INSERT INTO lines VALUES ('North West', 'LINESTRING(0 0,-1 1)'),
  ('North East', 'LINESTRING(0 0, 1 1)'),
  ('South West', 'LINESTRING(0 0,-1 -1)'),
  ('South East', 'LINESTRING(0 0,1 -1)');

SELECT name, ST_AsText(line) FROM lines;
```

## 区别

1. 使用AddGeometryColumn函数添加几何字段，会为表增加约束， 限定了表支持的几何类型， 几何类型的维数，表的空间参照系。保证表的一致性。(只存在geometry这种几何类型，不存在LINESTRING，POLYGON这些具体的几何类型，存在POINT类型，但是它是postgresql内的一个类型，不是几何类型)
2. 使用AddGeometryColumn函数会更新数据库的几何元数据表。


----------------

postgis提供了两个元数据表来报告数据库支持的空间参照系，和数据库提供的要素（几何数据+属性数据， 一个表如果有一个几何字段代表一个要素，有多个几何字段，则代表多个不同的要素）

```
SELECT * FROM geometry_columns; # 要素表记录了要素所在的数据表的名称，对应的几何字段的名字，维数，空间参照系

SELECT * FROM spatial_ref_sys; # 空间参照系表记录了空间参照系的EPSG号，proj4字符串，WKT字符串 

```


