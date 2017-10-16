
---
title: tiff图像的空间参照信息
date: 2017-09-15 22:54:44
tags:
---
        ## 设置tiff的spatial reference

*GeoTIFF*格式的图像是携带*spatial reference*的。通过*geotransform*和*projection*来体现。

*geotransform*声明了如何从屏幕坐标转换为地理坐标，它是一个`double[6]`的数组，分别给定了图像左上角的地理
坐标，像元在投影坐标系下的长宽，像元的旋转角度。

*projection*给定了图像的空间参照信息。


这里给出了一个，为新图像添加一个已有tiff的空间参照信息的例子。
获取：
```
OSGeo.GDAL.Dataset dataset = OSGeo.GDAL.Gdal.Open(fileName, OSGeo.GDAL.Access.GA_ReadOnly);
width = dataset.RasterXSize;
height = dataset.RasterYSize;
this.geoTransform = new double[6];
dataset.GetGeoTransform(geoTransform);            
this.projStr = dataset.GetProjection();
double[] imageBuffer = new double[width * height];
OSGeo.GDAL.Band b = dataset.GetRasterBand(1);
b.ReadRaster(0, 0, width, height, imageBuffer, width, height, 0, 0);
double noDataVal;
int hasVal;
b.GetNoDataValue(out noDataVal, out hasVal);
```
设置：
```
datasetSave.SetProjection(ca.projStr);
datasetSave.SetGeoTransform(ca.geoTransform);
datasetSave.GetRasterBand(1).SetNoDataValue(ca.noDataVal);
```

