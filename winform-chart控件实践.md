
---
title: winform-chart控件实践
date: 2017-09-15 22:54:44
tags:
---
        
-------

本文简单介绍一下使用winform中chart控件动态更新图表的实现。

-----

我们直接使用代码来讲解。

所有代码的上下文是`System.Windows.Forms.Form`类。

```

        private void InitialChart(LandUseClassificationInfo landUseClassificationInfo)
        {
            this.chartTypeCount.Series.Clear(); // 清空已有的图表
            int size = landUseClassificationInfo.NumOfLandUseTypes; // 折线的数目
            for (int j = 0; j < landUseClassificationInfo.AllTypes.Count; j++)
            {                
                var series = new Series()
                {
                    Name = landType.LandUseTypeName, // 折线代表的类型
                    Color = Color.FromArgb(landType.LandUseTypeColor), // 折线的颜色
                    ChartType = SeriesChartType.Line, // 图表的类型是折线
                    IsVisibleInLegend = true // 该折线将会添加到legend中
                };
                this.chartTypeCount.Series.Add(series); // 将这个折线添加到图表域中
            }           
        }

```
先初始化图表。
图表的初始化，基于你的应用而不同。
这里初始化折线图表，指定每个折线的颜色，legend的名字。

```

        private void UpdateChart(int[] cellCount1, int time1, LandUseClassificationInfo landUseInfo)
        {
            for(int i = 0; i < cellCount1.Length; i++)
            {
                this.chartTypeCount.Series[i].Points.AddXY(time1, cellCount1[i]);
            }
        }


```
winform的chart控件有一个很好的特性，就是加到points列表中的点会动态更新出来。

所以我们这里的更新操作很简单。假设图表域中有5条折线，那么每次传入一个数组，代表5个新的数据点，添加到数组中。即可以动态更新。

## 另外一个例子

```

namespace WindowsFormsApplication2
{
    
    public partial class Form1 : Form
    {
        private Random rnd;
        private int xV = 0;
        private double begin1 = 100;
        private double begin2 = 100;
        private void refreshChar()
        {
            this.chart1.Series.Clear();

           rnd = new Random();

            var series1 = new Series()
            {
                Name = "red",
                Color = Color.Red,
                ChartType = SeriesChartType.Line
            };

            var series2 = new Series()
            {
                Name = "green",
                Color = Color.Green,
                ChartType = SeriesChartType.Line
            };




            this.chart1.Series.Add(series1);
            this.chart1.Series.Add(series2);
            this.chart1.Invalidate();
        }

        public Form1()
        {
            InitializeComponent();
            refreshChar();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            this.begin1 += rnd.NextDouble() * 100;
            this.begin2 += rnd.NextDouble() * 100;
            this.chart1.Series[0].Points.AddXY(xV, this.begin1);
            this.chart1.Series[1].Points.AddXY(xV, this.begin2);
            xV++;
            // MessageBox.Show("helo");
        }
    }
}

```


参考文献:

1. [Chart creating dynamically. in .net, c#](http://stackoverflow.com/questions/10622674/chart-creating-dynamically-in-net-c-sharp)
2. [Tutorial: Creating a Basic Chart](https://msdn.microsoft.com/en-us/library/dd489237.aspx)
