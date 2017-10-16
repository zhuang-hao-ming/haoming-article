
---
title: postgis函数
date: 2017-09-15 22:54:44
tags:
---
        ## accessor 函数

```
SELECT * FROM shenzhen_road LIMIT 1;

SELECT ST_NumGeometries(geom) FROM shenzhen_road LIMIT 1; # 返回multi-geometry或者geometry collection中几何体的数目。
SELECT ST_AsText(ST_GeometryN(geom, 1)) FROM shenzhen_road LIMIT 1; # 返回multi-geometry或者geometry collection中index位置的geometry， 索引计数从1开始

SELECT ST_NumInteriorRings(ST_GeometryN(geom, 1)) FROM road_buffer LIMIT 1; # 返回一个POLYGON的内环的数目
SELECT ST_NRings(ST_GeometryN(geom, 1)) FROM road_buffer LIMIT 1; # 返回一个POLYGON环的数目
SELECT ST_ExteriorRing(ST_GeometryN(geom,1)) FROM road_buffer LIMIT 1; # 返回POLYGON的外环LINESTRING
SELECT ST_InteriorRingN(ST_GeometryN(geom,1), 1) FROM road_buffer LIMIT 1; # 返回POLYGON的内环LINESTRING, 多个内环索引从1开始， 如果没有内环放回NULL


SELECT ST_NumPoints(ST_GeometryN(geom,1)) FROM shenzhen_road LIMIT 1; # 返回线串中点的数目
SELECT ST_NPoints(geom) FROM shenzhen_road LIMIT 1; # 和NumPoints功能一样，但是不限制几何类型
SELECT ST_PointN(ST_GeometryN(geom,1), 1) FROM shenzhen_road LIMIT 1; # 返回线串的第index个点几何体， index从1开始

SELECT ST_StartPoint(ST_GeometryN(geom,1)) FROM shenzhen_road LIMIT 1; # 返回线串的起点
SELECT ST_EndPoint(ST_GeometryN(geom,1)) FROM shenzhen_road LIMIT 1;  # 返回线串的终点

SELECT ST_X(ST_PointN(ST_GeometryN(geom,1), 1)) FROM shenzhen_road LIMIT 1; # 返回点的X坐标
SELECT ST_Y(ST_PointN(ST_GeometryN(geom,1), 1)) FROM shenzhen_road LIMIT 1; # 返回点的Y坐标
SELECT ST_Z(ST_PointN(ST_GeometryN(geom,1), 1)) FROM shenzhen_road LIMIT 1; # 返回点的Z坐标
SELECT ST_M(ST_PointN(ST_GeometryN(geom,1), 1)) FROM shenzhen_road LIMIT 1; # 返回点的M坐标
```

## measurement 函数

```

# 获得二维线的长度， 使用笛卡尔坐标系
# 默认认为提供的坐标是投影坐标系
# 如果坐标是经纬度，由于经度和维度方向上的距离随着位置和方向而改变，所以无法直接计算

SELECT ST_Length(ST_GeomFromText('LINESTRING(0 2 1,5 1 3,5 10 4)')); 



SELECT
  ST_Length(geography(g)),
  ST_Length(g, false)
FROM (
  VALUES (
    ST_GeomFromEWKT('LINESTRING(151.1205 -33.7145 0,151.1218 -33.7087 54)')
  ) ) AS query(g); 
# 656.73 658.26
# 如果指定了第二个参数，那么坐标会被认为是经纬度， 默认使用spheriod来计算长度， 也可以指定false来使用sphere来加快运算速度
# 有多种方式来指示一个几何体是地理坐标
# 1. 显式使用参数2， 如果输入几何体没有指定空间参照系，或者指定的空间参照系是地理坐标系，那么几何体使用地理坐标，默认是4326
# 2. 显式的调用geography(geom)函数， 指示几何体使用的是地理坐标， 前提和1一样，几何体没有指定空间参照系，或者指定的空间参照系是地理坐标系
# 3. 使用GeographyFromText('SRID=4326;LINESTRING(151.1205 -33.7145 0,151.1218 -33.7087 54)'), 显式的创造一个使用地理坐标的几何体			

# 656.73 658.26
SELECT ST_Length(the_geog) AS length_spheriod, ST_Length(the_geog, false) AS length_sphere FROM
(
SELECT ST_GeographyFromText('SRID=4326;LINESTRING(151.1205 -33.7145 0,151.1218 -33.7087 54)') AS the_geog
) AS foo

# 789.548549287286 789.548549287286
# 这里将地理坐标投影为投影坐标以后，使用笛卡尔坐标系计算
SELECT ST_Length(geom) AS length_spheriod, ST_Length(geom) AS length_sphere FROM
(
SELECT ST_Transform(ST_GeomFromEWKT('SRID=4326;LINESTRING(151.1205 -33.7145 0,151.1218 -33.7087 54)'), 3857) AS geom
) AS foo






# 计算周长
SELECT ST_Perimeter(ST_GeomFromEWKT(g))
  FROM (
    VALUES
      ('POLYGON((-2 -2 0,2 -2 1,2 2 2,-2 2 1,-2 -2 0))'),
      ('POLYGON((-2 -2,2 -2,2 2,-2 2,-2 -2),(1 1,-1 1,-1 -1,1 -1,1 1))')
   ) AS query(g);

# 计算面积
SELECT ST_Area(ST_GeomFromEWKT(g))
  FROM (
    VALUES
      ('POLYGON((-2 -2 0,2 -2 1,2 2 2,-2 2 1,-2 -2 0))'),
      ('POLYGON((-2 -2,2 -2,2 2,-2 2,-2 -2),(1 1,-1 1,-1 -1,1 -1,1 1))')
     ) AS query(g);

# 计算距离
SELECT ST_Distance(ST_GeomFromEWKT('POINT(0 5)'),
  ST_GeomFromEWKT('LINESTRING(-2 2,2 2)'));




# 计算地理距离
SELECT
  ST_Distance_Sphere(a, b),
  ST_Distance_Spheroid(a, b, 'SPHEROID["GRS 1980",6378137,298.257222101]')
FROM (
  VALUES (
    ST_GeomFromText('POINT(151.1205 -33.7145)'),
    ST_GeomFromText('POINT(151.1218 -33.7087)')
    ) ) AS query (a, b);
```

## relation function

```
Below are short descriptions of a number of relational operators. Each of these functions will return true or false. Later sections will make greater use of these functions. For a more complete description of each please refer to the PostGIS documentation [1].
ST_Contains(A, B)
Returns true if no points in B lie outside of A, and the interiors of A and B share at least one point, otherwise false.
ST_ContainsProperly(A, B)
Returns true if B intersects the interior of A but not the boundary, otherwise false.
ST_Covers(A, B)
Returns true if no point in B is outside of A, otherwise false.
ST_CoveredBy(A, B)
Returns true if no point in A is outside of B, otherwise false.
ST_Crosses(A, B)
Returns true if A and B share some but not all points in common, otherwise false.
ST_Disjoint(A, B)
Returns true if there are no points in common between A and B, otherwise false.
ST_Intersects(A, B)
Returns true if there are any points in common between A and B, otherwise false.
ST_Overlaps(A, B)
Returns true if the geometries intersect, but are not contained and are of the same dimension (i.e. both lines, both points or both polygons), otherwise false.
ST_Touches(A, B)
Returns true if A and B have at least one point in common but their interiors don’t overlap, otherwise false.
ST_Within(A, B)
Returns true if A is completely inside B, otherwise false.
```

## projection
```
SELECT ST_AsText(geom) FROM road_buffer LIMIT 1;
# 查看几何体的srid
SELECT ST_SRID(geom) FROM road_buffer LIMIT 1;
# 查看表的空间参照
SELECT * FROM geometry_columns WHERE f_table_name='road_buffer';
# 投影数据
SELECT ST_AsText(ST_Transform(geom, 4326)) FROM road_buffer LIMIT 1;
# 设置几何体的srid，注意它不会投影数据
SELECT ST_Distance(ST_SetSRID(ST_Point(-118.143, 33.812), 32649), geom) FROM road_buffer LIMIT 1;
# 接收表名， 几何列名， srid， 更改表的srid并且创造新的约束，注意它不会重投影数据
SELECT UpdateGeometrySRID('road_buffer', 'geom', 32649); 
```

一般要保证几何体和表的srid一致。通过AddGeometryColumn或者UpdateGeometrSRID来确保，应用了约束，并在元数据表geometry_columns中记录要素信息。

只有ST_Transform函数是做了投影操作，其它的函数，只是单纯的指示数据是来自于哪个空间参照系。

## 有效性和相等

```
SELECT count(*), ST_IsValid(geom)
  FROM shenzhen_road
  GROUP BY ST_IsValid;
```
使用ST_IsValid来判断一个几何体是否是拓扑有效的。

可以使用缓存半径为0的缓冲区来解决拓扑问题.
```
UPDATE jacksonco_taxlots
  SET the_geom = ST_Multi(ST_Buffer(the_geom, 0));
```

### 相等

在postgis中存在3种不同的相等：
1. 完全相等， 组成几何体的顶点依照顺序一一相等，使用~=来判断
2. 空间相等， 不同的几何体覆盖相同的点，使用ST_Equals来判断
3. 范围相等， 不同的几何体外包矩形相同，使用=来判断。