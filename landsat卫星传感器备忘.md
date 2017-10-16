
---
title: landsat卫星传感器备忘
date: 2017-09-15 22:54:44
tags:
---
        Landsat系列卫星使用的传感器包括MSS(Multispectral Scanner), TM(Thematic Mapper), ETM+(Enhanced Thematic Mapper Plus), OLI and TIRS(Operational Land Imager and Thermal Infrared Sensor).

MSS传感器在Landsat1-5使用，它的空间分辨率是60米（原始分辨率是`$79m*57m$` 在发布时重采样到60米）。由于已经有更好的传感器了，这里不讨论这个传感器。

TM传感器在Landsat4-5使用，它的空间分辨率是30米。

Bands | Resolution(meters) 
---|---
Band1 - Blue | 30
Band2 - Green | 30
Band3 - Red | 30
Band4 - Near Infrared (NIR) | 30
Band5 - Shortwave Infrared (SWIR)1 | 30
Band6 - Thermal  | 120(resample to 30)
Band7 - Shortwave Infrared (SWIR)2 | 30


ETM+传感器在Landsat7上使用， 它的空间分辨率是30米。

Bands | Resolution(meters) 
---|---
Band1 - Blue | 30
Band2 - Green | 30
Band3 - Red | 30
Band4 - Near Infrared (NIR) | 30
Band5 - Shortwave Infrared (SWIR)1 | 30
Band6 - Thermal  | 60(resample to 30)
Band7 - Shortwave Infrared (SWIR)2 | 30
Band8 - Panchromatic | 15

OLI and TIRS传感器在Landsat8上使用

Bands | Resolution(meters) 
---|---
Band1 - Ultra Blue | 30
Band2 - Blue | 30
Band3 - Green | 30
Band4 - Red | 30
Band5 - Near Infrared (NIR) | 30
Band6 - Shortwave Infrared (SWIR)1 | 30
Band7 - Shortwave Infrared (SWIR)1 | 30
Band8 - Panchromatic | 15
Band9 - Cirrus | 30
Band10 - Thermal Infrared(TIRS)1  | 100(resample to 30)
Band11 - Thermal Infrared(TIRS)1  | 100(resample to 30)

## 参考文献
1. [what-are-band-designations-landsat-satellites](https://landsat.usgs.gov/what-are-band-designations-landsat-satellites)