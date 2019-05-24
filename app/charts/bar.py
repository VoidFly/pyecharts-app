#-*- coding:utf-8 -*-

from pyecharts.charts import Kline, Line, Page
from pyecharts import options as opts
import tushare as ts
import pandas as pd
import re

#这个是股票行情的绘图函数 文件名bar.py是在其他地方有调用（还没改）

def stock_draw(labels,mode_combo,startdate,enddate,optInterval,width1, height1):
    #optInterval='D/W/M' labels
    print(labels)#需要绘制的信息列表
    print(mode_combo)#默认为KLine 不要改
    print(startdate)
    print(enddate)
    print(optInterval)#股票信息时间间隔  可选： D W M 5 15 30
    print(width1)  #长宽高还没有加到下面函数里面去
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

    return page


def CalculateMA(date,DayCount):
    result=pd.DataFrame(data=date)
    result=result.rolling(DayCount).mean()
    #print(result)
    result_list=result[0].tolist()
    #print(result_list)
    for i in range(len(result_list)):
        result_list[i]=round(result_list[i],3)

    return result_list





def create_charts():

    #绘图参数
    labels=['上证指数-sh-Kline', '深证成指-sz-Kline']
    mode_combo='KLine'
    startdate='2019/04/24'
    enddate='2019/05/24'
    optInterval='D'
    width1=0
    length1=0

    page = stock_draw(labels,mode_combo,startdate,enddate,optInterval,width1,length1)
    '''
    bar = (
        Bar()
            .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
            .add_yaxis("商家A", [5, 20, 36, 10, 75, 90])
            .set_global_opts(title_opts=opts.TitleOpts(title="主标题", subtitle="副标题"))
        # 或者直接使用字典参数
        # .set_global_opts(title_opts={"text": "主标题", "subtext": "副标题"})
    )
    page.add(bar)
    '''


    return page
