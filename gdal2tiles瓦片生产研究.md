
---
title: gdal2tiles瓦片生产研究
date: 2017-09-15 22:54:44
tags:
---
        ## gdal2tiles.py研究

这个python脚本用于将一个高分辨率的栅格地图转换为瓦片地图目录。
用法：

```
gdal2tiles.py [-p profile] [-r resampling] [-s srs] [-z zoom]
              [-e] [-a nodata] [-v] [-q] [-h] [-k] [-n] [-u url]
              [-w webviewer] [-t title] [-c copyright]
              [-g googlekey] [-b bingkey] input_file [output_dir]
```

1. -p 指定生成瓦片的方式，可取的值是mercator，geodetic，raster中的一个，默认值是mercator。mercator指示生产球面墨卡托投影下的瓦片，geodetic指示产生wgs84地理坐标系下的瓦片，raster指示不做任何处理，直接生成瓦片。
使用mercator和geodetic产生的瓦片可以和其他相应的瓦片兼容，进行叠加和拼接。mercator是一个等角投影，它保证了投影前后形状不变。geodetic是一个简单投影，它直接将经纬度作为投影坐标，可以认为它没有进行投影，它既不等角又不等长，它的优点是，像元坐标和瓦片的对应关系非常清晰。

2. -r 指定重采样算法， 脚本使用4个n级比例尺的瓦片来产生一个相关的n-1级比例尺的瓦片，4个n级瓦片拼接成一个256 * 4 * 256 * 4的图像，然后使用指定的重采样算法重采样到256 * 256
3. -s 输入地图的空间参照系
4. -z 指定需要产生的瓦片级别, 格式2-10或者10，前者指定了最低和最高级，后者只生成一个级别。
如果没有指定级别，那么首先脚本会得到原始图像的分辨率(一个像元代表的实际距离)，然后将它从小到大和每个比例尺级别的分辨率(initialResolution(地球赤道周长) / 2 ** zoom)进行比较，找到不小于原始分辨率的最大级别，作为瓦片的最大级别（最大为32），0作为最小级别。
5. -e 只生产需要的瓦片，已经存在的瓦片不再重新生产
6. -a 0,0,0 指定透明值
7. -v 冗余输出
8. -q 静默输出
9. -h 输出帮助信息
10. --version 输出版本信息
11. -k 强制产生kml
12. -n 禁止产生kml
13. -u 瓦片的url地址
14. -w none 配置生成的网页地图浏览器，none指示不产生地图浏览器，all指示产生所有类型的地图浏览器
