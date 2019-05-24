#-*- coding:utf-8 -*-

from pyecharts.charts import Kline, Line, Page
from pyecharts import options as opts
import tushare as ts
import pandas as pd
import re




def stock_draw(labels,mode_combo,startdate,enddate,optInterval,width1, height1):
    #optInterval='D/W/M' labels
    print(labels)
    print(mode_combo)
    print(startdate)
    print(enddate)
    print(optInterval)
    print(width1)
    print(height1)

    startdate = startdate.replace("/", "-")  # 将参数日期转换为tushare的日期格式
    enddate = enddate.replace("/", "-")

    page = Page()


    for label in labels:  # 对于传入的labels一张张作图
        label1 = re.split("-", label)
        print(label1[0])
        print(label1[1])


        if mode_combo == "KLine":
            array = ts.get_k_data(label1[1], start=startdate, end=enddate, ktype=optInterval)
            # print(array)
            time = array['date'].tolist()  # array.date
            # 绘图方法

            if label1[2] == 'Kline':
                re_array = array[['open', 'close', 'high', 'low']]
                data_li = list(row.tolist() for index, row in re_array.iterrows())
                close = array['close'].tolist()
                #width=width1 * 10 / 11, height=(height1 * 10 / 11) / len(labels)

                kline = (
                    Kline()
                        .add_xaxis(time)
                        .add_yaxis(label1[0],data_li)
                        .set_global_opts(

                        xaxis_opts=opts.AxisOpts(is_scale=True),
                        yaxis_opts=opts.AxisOpts(
                            is_scale=True,
                            splitarea_opts=opts.SplitAreaOpts(
                                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                            ),
                        ),
                        datazoom_opts=[opts.DataZoomOpts(pos_bottom="-2%")],
                        title_opts=opts.TitleOpts(title=label1[0] + "-" + optInterval)


                    )
                )


                # 计算移动平均
                if len(close) > 10:
                    ma10 = CalculateMA(close, 10)

                    line1 = (
                        Line()
                            .add_xaxis(time)
                            .add_yaxis("MA10", ma10)
                            #.set_global_opts(title_opts=opts.TitleOpts(title="Line-基本示例"))
                            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                    )
                    kline.overlap(line1)

                if len(close) > 20:
                    ma20 = CalculateMA(close, 20)
                    line2 = (
                        Line()
                            .add_xaxis(time)
                            .add_yaxis("MA20", ma20)
                        # .set_global_opts(title_opts=opts.TitleOpts(title="Line-基本示例"))
                            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                    )
                    kline.overlap(line2)


                if len(close) > 30:
                    ma30 = CalculateMA(close, 30)

                    line3 = (
                        Line()
                            .add_xaxis(time)
                            .add_yaxis("MA30", ma30)
                        # .set_global_opts(title_opts=opts.TitleOpts(title="Line-基本示例"))
                            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                    )

                    kline.overlap(line3)

                page.add(kline)
            else:  # label1[2]==open/close/volume
                if label1[2] == 'Open':
                    list_aft = array['open'].tolist()
                elif label1[2] == 'Close':
                    list_aft = array['close'].tolist()
                elif label1[2] == 'High':
                    list_aft = array['high'].tolist()
                elif label1[2] == 'Low':
                    list_aft = array['low'].tolist()
                elif label1[2] == 'Volume':  # volume
                    list_aft = array['volume'].tolist()
                else:
                    list_aft = array['amount'].tolist()



                line = (
                    Line()
                        .add_xaxis(time)
                        .add_yaxis(label1[0] + "-" + label1[2], list_aft)
                        .set_global_opts(xaxis_opts=opts.AxisOpts(is_scale=True),
                                        yaxis_opts=opts.AxisOpts(
                                            is_scale=True,
                                            splitarea_opts=opts.SplitAreaOpts(
                                                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                                            ),
                                        ),
                                        datazoom_opts=[opts.DataZoomOpts(pos_bottom="-2%")],
                                        title_opts=opts.TitleOpts(title=label1[0] + "-" + label1[2]))
                        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))

                )


                page.add(line)

    page.render()


def CalculateMA(date,DayCount):
    result=pd.DataFrame(data=date)
    result=result.rolling(DayCount).mean()
    #print(result)
    result_list=result[0].tolist()
    #print(result_list)
    for i in range(len(result_list)):
        result_list[i]=round(result_list[i],3)

    return result_list

