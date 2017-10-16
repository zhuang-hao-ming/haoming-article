
---
title: geosos开发笔记
date: 2017-09-15 22:54:44
tags:
---
        昨天晚上和今天下午花了一些时间对geosos软件做了一点修改。

开发这个软件经历了很长一段时间，实际的开发时间倒是不长，因为常常是几个月才写一次代码。

这次的修改是，**把ca的模拟动画改动到地图层面**

以前，我们的ca模拟动画，是单独绘制在一个winform窗体中。

这样的做法虽然简单，但是导致了，地图彻底成为了动画，失去了空间参照信息。所以，我们希望直接对地图图层进行修改来实现动画效果。

为了实现这个目的，我们需要研究以下几个问题。

1. dotspatial的栅格地图符号化机制
2. 动态修改地图底层数据的方法
3. 跨线程调用dotspatial控件


以下，我们对每一个问题，分别讨论。

## dotspatial的栅格地图符号化机制

dotspatial的栅格地图符号化机制，一直以来，我们都没有仔细研究过。它也的确很奇怪。

通过阅读，symbology部分的代码，我对于符号化的内容有了一点小小了解。

具体来说，图层有一个symbolizer的属性。symbolizer有一个scheme的属性，这个属性控制了栅格图像的颜色模式。
还有一个EditorSettings属性，这个属性包含了一些元数据，比如有多少个颜色。

具体的颜色描述，在scheme的Categories属性中。


*值得注意的是，dotspatial似乎不支持唯一值的颜色模式，在我们的应用中要实现类似唯一值的颜色模式，只能指定两个像邻的数，例如“0-1”, 根据实验的结果，0-1代表 0< x <=1*

最后使用图层的WriteBitmap来刷新地图。

```
  var symbolizer = rasterLayer.Symbolizer;
                var scheme = symbolizer.Scheme;
                EditorSettings settings = symbolizer.EditorSettings;
                scheme.Categories.RemoveRange(0, scheme.Categories.Count);

                settings.NumBreaks = 6;
                
                scheme.CreateCategories(raster);

                scheme.Categories[0].LegendText = "1";
                scheme.Categories[0].Minimum = 0;
                scheme.Categories[0].Maximum = 1;                            
                scheme.Categories[0].LowColor = Color.Yellow;
                scheme.Categories[0].HighColor = Color.Yellow;

                scheme.Categories[1].LegendText = "2";
                scheme.Categories[1].Range = new Range("1-2");
                
                scheme.Categories[1].LowColor = Color.Green;
                scheme.Categories[1].HighColor = Color.Green;

                scheme.Categories[2].LegendText = "3";
                scheme.Categories[2].Range = new Range("2-3");
             
                scheme.Categories[2].LowColor = Color.LightGreen;
                scheme.Categories[2].HighColor = Color.LightGreen;

                scheme.Categories[3].LegendText = "4";
                scheme.Categories[3].Range = new Range("3-4");
          
                scheme.Categories[3].LowColor = Color.Blue;
                scheme.Categories[3].HighColor = Color.Blue;

                scheme.Categories[4].LegendText = "5";
                scheme.Categories[4].Range = new Range("4-5");
               
                scheme.Categories[4].LowColor = Color.Black;
                scheme.Categories[4].HighColor = Color.Black;

                scheme.Categories[5].LegendText = "6";
                scheme.Categories[5].Range = new Range("5-6");
          
                scheme.Categories[5].LowColor = Color.WhiteSmoke;
                scheme.Categories[5].HighColor = Color.WhiteSmoke;



                rasterLayer.WriteBitmap();


```


## 动态修改地图底层数据的方法

图层的底层数据在DataSet属性中，它是一个IRaster实例，我们要根据它的类型，把它转换为相应的Raster<T>类型实例，真正的数据在这个对象的Data属性中。



```

 var raster = this.rasterLayer.DataSet;

            switch (this.rasterLayer.DataType.ToString().ToUpper())
            {
                case "SYSTEM.INT32":
                case "SYSTEM.LONG":

                    break;
                case "SYSTEM.SHORT":

                    break;
                case "SYSTEM.DOUBLE":
                case "SYSTEM.SINGLE":

                    break;
                case "SYSTEM.FLOAT":

                    break;
                case "SYSTEM.BYTE":
                    Raster<byte> byteRaster = raster.ToRaster<byte>();
                    for (int row = 0; row < raster.NumRows; row++)
                    {
                        for (int col = 0; col < raster.NumColumns; col++)
                        {
                            int pos = row * raster.NumColumns + col;
                            byteRaster.Data[row][col] = (byte)middleBuffer[pos];
                        }
                    }

                    break;
                default:

                    break;
            }

```

## 跨线程调用dotspatial控件

有UI界面的编程，必然是涉及多线程（异步）的,否则，界面会堵塞，严重影响用户体验。

winform的UI是禁止跨线程调用的。解决UI跨线程调用的方法是利用控件的InvokeRequired属性。

在这里我们遇到的一个比较大的问题是，究竟我们要跨线性修改的控件是属于那个窗体呢？由于，dotspatial部分的代码是封装好的，这个问题并不好回答。

但是在当前的情况是，发现只要检查legend这个控件的InvokeRequired属性，即可。

```

/// <summary>
        /// 线程安全的刷新地图方法
        /// </summary>
        protected void WriteBitMapAsync()
        {
            /**
             * 目前遇到的，在其它线程调用主框架，唯一需要处理的控件就是Legend
             */ 
            var lengend = GIS.FrameWork.Application.App.Legend as Legend;

            if (lengend.InvokeRequired)
            {
                lengend.Invoke(new Action(() =>
                {

                    this.rasterLayer.WriteBitmap();

                }));
            }
            else
            {
                this.rasterLayer.WriteBitmap();
            }

        }
```