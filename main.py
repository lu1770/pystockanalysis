#!/usr/bin/python
# -*- coding: UTF-8 -*-

import numpy as np
import csv
import os
import random
from matplotlib import pyplot as plt
import chardet
from sklearn import linear_model        #表示，可以调用sklearn中的linear_model模块进行线性回归。
import numpy as np

print(("预测一张12英寸匹萨价格：{:.2f}".format(model.predict([[12]])[0][0])))

class Artist():
    '''
        用于画画的类是不是应该叫做艺术家
    '''

    def __init__(self, x_index, y_index, days):
        '''
        完成初始化
        '''
        self.x_label_index = x_index
        self.y_label_index = y_index
        self.days = days

    def check_code(self, text):
        adchar = chardet.detect(text)
        # 由于windows系统的编码有可能是Windows-1254,打印出来后还是乱码,所以不直接用adchar['encoding']编码
        # if adchar['encoding'] is not None:
        # true_text = text.decode(adchar['encoding'], "ignore")
        if adchar['encoding'] == 'gbk' or adchar['encoding'] == 'GBK' or adchar['encoding'] == 'GB2312':
            true_text = text.decode('GBK', "ignore")
        else:
            true_text = text.decode('utf-8', "ignore")
        return true_text

    def getData(self):
        '''
        获取数据
        '''
        lines = self.getFileData()
        self.head = lines[0].split(',')
        body = lines[1:]
        body.reverse()
        data = [
            [y.split(',')[self.x_label_index] for y in body if len(y) >= 1],
            [float(y.split(',')[6]) for y in body if len(y) >= 1],
        ]
        return data

    def getFileData(self):
        '''
        获取文件数据
        '''
        return self.getCSVdata()

    def getCSVdata(self):
        '''
        从CSV获取数据
        '''
        with open("300117.csv", "rb") as f:
            text = self.check_code(f.read())
            return text.split('\n')

    def getTitle(self):
        '''
        设置图形标题
        '''
        return "%s 天趋势" % self.days

    def linearRegression(self,x,y):
        model = linear_model.LinearRegression()
        model.fit(x, y)
        print((model.intercept_))  #截距
        print((model.coef_))  #线性模型的系数
        a = model.predict([[12]])
        return model.coef_
        
    def paint(self):
        '''
        绘制图形
        '''
        data = self.getData()
        x = data[0][:self.days]
        y = data[1][:self.days]

        x.reverse()
        y.reverse()

        # 解决中文显示问题
        plt.rcParams['font.sans-serif'] = ['KaiTi']  # 指定默认字体
        plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

        plt.title(self.getTitle())
        plt.xlabel('日期')
        plt.ylabel('价格')
        plt.plot(x, y)

        for i in range(1, 3):
            dx = self.linearRegression(list(range(1,3)),y[i-1:i+1])
            # y = dx*x + b
            # y[i] = dx * i + b
            print([i, y[i+1], y[i-1], dx, y])
            y_arr = [dx*(j-1)+y[0] for j in range(1, self.days+1)]
            plt.plot(x, y_arr)

        # y=dx*x+b

        # line.set_color('r')
        # line.set_linewidth(2.0)
        plt.show()


artist = Artist(1, 6, 15)
artist.paint()
