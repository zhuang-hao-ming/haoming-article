
---
title: pgRouting使用
date: 2017-09-15 22:54:44
tags:
---
        








pgRouting跟随postgis扩展一起被安装。

```
-- 使用这个语句来使能pgrouting
CREATE EXTENSION pgrouting;
```


准备数据：

1. 导入路网数据
2. 对路网数据建立拓扑信息

```
-- Add "source" and "target" column
ALTER TABLE planet_osm_roads ADD COLUMN "source" integer;
ALTER TABLE planet_osm_roads ADD COLUMN "target" integer;

-- Run topology function
SELECT pgr_createTopology('planet_osm_roads', 0.00001, 'way', 'osm_id');
```

查询：

```
SELECT * FROM pgr_dijkstra('
    SELECT gid AS id,
         source,
         target,
         length AS cost
        FROM ways',
    13224, 6549, directed := false);
```

## 备注

1. 直接建立一个连通的路网表，也可以进行routing，不需要使用`create topology`