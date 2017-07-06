#coding=utf-8
import numpy as np  
import matplotlib.pyplot as plt  
import matplotlib


zhfont1 = matplotlib.font_manager.FontProperties(fname="C:\Windows\Fonts\simsun.ttc",size=20)  
#设置x,y轴的数值（y=sinx）  
x = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])

y = np.array([8,41,168,717,2683,9609,28265,35641,35919,35942,35946,35946,35946,35946,35947,35947])
  
#创建绘图对象，figsize参数可以指定绘图对象的宽度和高度，单位为英寸，一英寸=80px  
plt.figure(figsize=(8,4))  
  
#在当前绘图对象中画图（x轴,y轴,给所绘制的曲线的名字，画线颜色，画线宽度）  
plt.plot(x,y,label="$N$",color="red",linewidth=2)  
  
#X轴的文字  
plt.xlabel(u"八叉树最大深度",fontproperties=zhfont1)  
  
#Y轴的文字  
plt.ylabel(u"保留数据点数",fontproperties=zhfont1)  
  
#图表的标题  
plt.title(u"八叉树最大深度参数与保留数据点数关系图",fontproperties=zhfont1)  
  
#Y轴的范围  
plt.ylim(0,37000)  
  
#显示图示  
plt.legend()  
  
#显示图  
plt.show()  
  
#保存图  
plt.savefig("sinx.jpg")  