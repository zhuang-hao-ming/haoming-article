
---
title: gdaldem彩色合成研究
date: 2017-09-15 22:54:44
tags:
---
        ## problem：

假设我们需要从一个单波段的栅格地图来生成瓦片地图，我们会遇到一个问题：瓦片地图的符号化应该如何决定。GIS软件可以用多种方法来显示单波段地图，如灰度图像，假彩色合成等。而且，这些操作是通过算法（映射表）进行的，并不需要真的对单波段地图的数据进行修改。但是作为瓦片地图客户端的浏览器只具有显示传统图片如PNG,JPEG图片的能力，为了使得生产出来的瓦片可以有正常的色彩显示，我们可以采取的一个方法就是把单波段图像转换为真彩色图像，然后再进行瓦片生成工作（也可以修改生成瓦片的算法，在瓦片生产的过程中应用色彩映射）。

## solution：

将一个单波段图像转换为一个真彩色图像的思路很很简单，把单波段图像利用色彩映射表进行绘制的结果保存回硬盘就完成了转换。

### gdaldem:

gdal中的工具gdaldem可以很好的完成这个转换

```
gdaldem color-relief input_dem color_text_file output_color_relief_map
                [-alpha] [-exact_color_entry | -nearest_color_entry]
                [-b Band (default=1)] [-of format] [-co "NAME=VALUE"]* [-q]
```

解释：
1. input_dem: 输入的图像
2. color_text_file: 颜色映射表
```
1 0 197 255
2 0 115 76
3 163 255 115
4 255 170 0
5 168 0 0
6 204 204 204
nv 255 255 255
```
颜色颜色表是一个csv文件（支持的分隔符包括space，tab，comma），第一列代表栅格数值，后3列代表RGB值。如果添加了[-alpha]选项，可以指定第4列代表opacity（不透明度）,在这种情况下如果不指定第4列，那么它的值是255代表完全不透明。nv指代了nodataval需要映射到的颜色。
这个颜色映射表文件可以通过arcgis的`export colormap`工具导出，但是导出的文件不包含nv行，需要我们手动添加
3. output_color_relief_map： 输出图像
4. -alpha: 指示在输出结果中添加一个alpha波段
5. [-exact_color_entry | -nearest_color_entry], 默认情况下工具对于没有匹配到颜色映射表中的栅格数值使用线性插值的方法来决定它的颜色。但是也可以使用-exact_color_entry要求工具做严格匹配，对于没有匹配到的栅格值使用（0，0，0，0）(黑色，透明)作为它的颜色，或者使用-nearest_color_entry做最近值匹配
6. [-b band] 如果输入的图像是一个多波段图像，那么需要指定一个波段，波段计数从1开始
7. [-of format] 输出的图像的格式， 默认是 tif
8. [-co "NAME=VALUE"]* 输出图像的压缩选项
9. [-q] 静默输出

示例：
clr.txt
```
0 black
1 white
nv 0 0 0
```
```
gdaldem color-relief urban1990.tif clr.txt out1.tif
```
这个示例对灰度图像进行了假彩色合成





