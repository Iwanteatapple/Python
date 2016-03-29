# encoding: utf-8
###############################################################################
import numpy as np
import wx
import matplotlib
import random

matplotlib.use("WXAgg")
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_wx import NavigationToolbar2Wx as NavigationToolbar
from matplotlib import pyplot as plt
from matplotlib import animation


g_list = []
g_node = 0

######################################################################################
class MPL_Panel(wx.Panel):
    
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent, id=-1)
        
        self.Figure = matplotlib.figure.Figure(figsize=(12,12))
        self.axes = self.Figure.add_axes([0.05,0.05,0.9,0.9])
        self.FigureCanvas = FigureCanvas(self,-1,self.Figure)
        
        self.axes.plot(10,10)
        self.axes.plot(-10,-10)
        
        self.FigureCanvas.mpl_connect('motion_notify_event',self.MPLOnMouseMove)
        self.FigureCanvas.mpl_connect('button_press_event',self.MPLOnMouseClick)
        
        self.NavigationToolbar = NavigationToolbar(self.FigureCanvas)
        
        self.StaticText = wx.StaticText(self,-1,label=u'座標')
        
        self.SubBoxSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SubBoxSizer.Add(self.NavigationToolbar,proportion =0, border = 2,flag = wx.ALL | wx.EXPAND)
        self.SubBoxSizer.Add(self.StaticText,proportion =-1, border = 2,flag = wx.ALL | wx.EXPAND)
        
        self.TopBoxSizer = wx.BoxSizer(wx.VERTICAL)
        self.TopBoxSizer.Add(self.SubBoxSizer,proportion =-1, border = 2,flag = wx.ALL | wx.EXPAND)
        self.TopBoxSizer.Add(self.FigureCanvas,proportion =-10, border = 2,flag = wx.ALL | wx.EXPAND)
        
        self.SetSizer(self.TopBoxSizer)
    
        self.FigureCanvas.draw()
        self.check_draw = 0
        self.add_list = []

    def change_draw(self):
        self.check_draw = 1
        
    def change_back(self):
        self.FigureCanvas.mpl_connect('button_press_event',self.MPLOnMouseClick)

    def MPLOnMouseMove(self,event):
        
        ex=event.xdata
        ey=event.ydata
        if ex  and ey :
            self.StaticText.SetLabel('%10.5f,%10.5f' % (float(ex),float(ey)))

    def MPLOnMouseClick(self, event):
        ex=event.xdata
        ey=event.ydata
        length = (225 - (ex ** 2) - (ey ** 2)) ** 0.5
        list = [ex , ey , length]
        self.add_list.append(list)
        print(list)

        if self.check_draw == 0:
            self.axes.plot(ex,ey,'o',color="gray")       
        elif self.check_draw == 1:
            c = frame.start.competitive(list)
            if c == 0:
                self.axes.plot(ex,ey,'o',color="red")
            elif c == 1:
                self.axes.plot(ex,ey,'o',color="blue")
            elif c == 2:
                self.axes.plot(ex,ey,'o',color="green")
            elif c == 3:
                self.axes.plot(ex,ey,'o',color="yellow")
            elif c == 4:
                self.axes.plot(ex,ey,'o',color="cyan")
            elif c == 5:
                self.axes.plot(ex,ey,'o',color="magenta")
            else:
                self.axes.plot(ex,ey,'o',color="gray")
                
        global g_node
        global g_list
        g_node += 1
        g_list = self.add_list
                
        self.FigureCanvas.draw()
        
    def run_draw(self,n,c):
        x = n[0]
        y = n[1]

        if c == 0:
            self.axes.plot(x,y,'o',color="red")
        elif c == 1:
            self.axes.plot(x,y,'o',color="blue")
        elif c == 2:
            self.axes.plot(x,y,'o',color="green")
        elif c == 3:
            self.axes.plot(x,y,'o',color="yellow")
        elif c == 4:
            self.axes.plot(x,y,'o',color="cyan")
        elif c == 5:
            self.axes.plot(x,y,'o',color="magenta")
        
        self.FigureCanvas.draw()

###############################################################################

###############################################################################
class MPL_Frame(wx.Frame):
    
    def __init__(self,title="Competitive Learning",size=(1000,600)):
        wx.Frame.__init__(self,parent=None,title = title,size=size)
        
        self.MPL = MPL_Panel(self)
        self.Figure = self.MPL.Figure
        self.axes = self.MPL.axes
        self.FigureCanvas = self.MPL.FigureCanvas
        
        self.RightPanel = wx.Panel(self,-1)
        
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(12)
        prompt = u"請輸入分幾類："
        st1 = wx.StaticText(self.RightPanel, -1, prompt)
        st1.SetFont(font)
        self.many = wx.TextCtrl(self.RightPanel, -1)
        prompt2 = u"請輸入學習速率："
        st2 = wx.StaticText(self.RightPanel, -1, prompt2)
        st2.SetFont(font)
        self.speed = wx.TextCtrl(self.RightPanel, -1)
        self.Button1 = wx.Button(self.RightPanel,1,u"開始：距離",size=(100,40),pos=(10,10))
        self.Button1.Bind(wx.EVT_BUTTON,self.Button1Event,id = 1)
        self.Button1_2 = wx.Button(self.RightPanel,2,u"開始：內積",size=(100,40),pos=(10,10))
        self.Button1_2.Bind(wx.EVT_BUTTON,self.Button1Event_2 , id =2)
        self.Button2 = wx.Button(self.RightPanel,-1,u"清除",size=(100,40),pos=(10,10))
        self.Button2.Bind(wx.EVT_BUTTON,self.Button2Event)

        self.message = wx.StaticText(self.RightPanel, -1)
        self.message.SetFont(font)
        
        self.FlexGridSizer=wx.FlexGridSizer( rows=10, cols=1, vgap=10,hgap=10)
        self.FlexGridSizer.SetFlexibleDirection(wx.BOTH)
        
        self.FlexGridSizer.Add(st1,proportion =0, border = 5,flag = wx.ALL | wx.EXPAND)
        self.FlexGridSizer.Add(self.many,proportion =0, border = 5,flag = wx.ALL | wx.EXPAND)
        self.FlexGridSizer.Add(st2,proportion =0, border = 5,flag = wx.ALL | wx.EXPAND)
        self.FlexGridSizer.Add(self.speed,proportion =0, border = 5,flag = wx.ALL | wx.EXPAND)
        self.FlexGridSizer.Add(self.Button1,proportion =0, border = 5,flag = wx.ALL | wx.EXPAND)
        self.FlexGridSizer.Add(self.Button1_2,proportion =0, border = 5,flag = wx.ALL | wx.EXPAND)
        self.FlexGridSizer.Add(self.Button2,proportion =0, border = 5,flag = wx.ALL | wx.EXPAND)
        self.FlexGridSizer.Add(self.message,proportion =0, border = 5,flag = wx.ALL | wx.EXPAND)
        
        self.RightPanel.SetSizer(self.FlexGridSizer)
        
        self.BoxSizer=wx.BoxSizer(wx.HORIZONTAL)
        self.BoxSizer.Add(self.MPL,proportion =-10, border = 2,flag = wx.ALL | wx.EXPAND)
        self.BoxSizer.Add(self.RightPanel,proportion =0, border = 2,flag = wx.ALL | wx.EXPAND)
        
        self.SetSizer(self.BoxSizer)
        
        self.Centre(wx.BOTH)
    
    def Button1Event(self,event):
        self.start = CL(self.many.GetValue(),self.speed.GetValue(),0)
    
        message = u"訓練完成"
        self.message.SetLabel(message)

    def Button1Event_2(self,event):
        self.start = CL(self.many.GetValue(),self.speed.GetValue(),1)
        
        message = u"訓練完成"
        self.message.SetLabel(message)
    
    def Button2Event(self,event):
        
        message = u""
        self.message.SetLabel(message)
        
        self.MPL.axes.cla()
        
        self.MPL.axes.plot(10,10)
        self.MPL.axes.plot(-10,-10)
        
        self.MPL.FigureCanvas.draw()
        self.MPL.change_back()

        global g_node
        global g_list
        g_node = 0
        g_list = []
        
        self.MPL.check_draw = 0

        self.MPL.add_list = []

########################################################################
class CL:
    def __init__(self,many,speed,which):
        self.many = many
        self.speed = speed
        self.node = g_list
        self.number = g_node
        self.which = which
        
        self.average = self.average_node()
        self.weight = []
        self.rand_weight()
        self.run()
    
    def average_node(self):
        
        sum = [0 , 0 , 0]
        
#        for x in self.node:
#            sum[0] += x[0]
#            sum[1] += x[1]
#            sum[2] += x[2]
#
#        sum[0] /= float(self.number)
#        sum[1] /= float(self.number)
#        sum[2] /= float(self.number)
#        sum[2] += 5

        return sum
    
    def rand_weight(self):
        for x in range(0 , int(self.many) , 1):                 #input
            weight_list = []
            
            r = random.randint(0, int(self.number)-1)
#            sum = (1 - (r ** 2)) ** 0.5
#            weight_list.append(r)
#            weight_list.append(sum)
#            r = random.uniform(-15, -10)
#            weight_list.append(-10)

            weight_list.extend(self.node[r])
#            print(r)
#            print(weight_list)
            self.weight.append(weight_list)
        
        for x in range(0 , int(self.many) , 1):
            for x in range(0 , int(self.many) , 1):
                for x in self.node :
                
                    self.chang_ini_weight(self.competitive(x) , x)

            
        for x in range(0 , int(self.many) , 1):
            self.weight_length1(x)

    def run(self):              #執行ＣＬ
        check = 0
        while check < int(self.number):
            check = 0
            for x in self.node :
                c = self.competitive(x)
                self.chang_weight(self.competitive(x) , x)
                frame.MPL.run_draw(x,self.competitive(x))
                if c == self.competitive(x):
                    check += 1
        
            if check == int(self.number):
                check = 0
                for x in self.node :
                    c = self.competitive(x)
                    self.chang_weight(self.competitive(x) , x)
                    frame.MPL.run_draw(x,self.competitive(x))
                    if c == self.competitive(x):
                        check += 1
    
        print("完成訓練")
        frame.MPL.change_draw()

    def competitive(self , n):  #比大小 競爭
        sum = 0
        min = 100000000000
        min_num = -1
        
        sum_n = ((n[0] - self.average[0]) ** 2 + (n[1] - self.average[1]) ** 2 + (n[2] - self.average[2]) ** 2) ** 0.5
        max = -1000000000
        max_num = -1
        
        for y in range(0 , int(self.many) , 1):
#            sum = (n[0] - self.average[0] - self.weight[y][0]) ** 2 + (n[1] - self.average[1] - self.weight[y][1]) ** 2
            sum = ((n[0] - self.average[0] - self.weight[y][0]) ** 2) + ((n[1] - self.average[1] - self.weight[y][1]) ** 2) + ((n[2] - self.average[2] - self.weight[y][2]) ** 2)
            
            sum_max = ((n[0] - self.average[0]) / sum_n) * self.weight[y][0] + ((n[1] - self.average[1]) / sum_n) * self.weight[y][1]  + ((n[2] - self.average[2]) / sum_n) * self.weight[y][2]

            if sum < min:
                min = sum
                min_num = y
    
            if sum_max > max:
                max = sum_max
                max_num = y

        if self.which == 0:

            return min_num

        else:
    
            return max_num

    def chang_weight(self , y ,n):  #更新權重
    
#        sum_n = ((n[0] - self.average[0]) ** 2 + (n[1] - self.average[1]) ** 2) ** 0.5
#        self.weight[y][0] = self.weight[y][0] + float(self.speed) * (((n[0] - self.average[0]) / sum_n) - self.weight[y][0])
#        self.weight[y][1] = self.weight[y][1] + float(self.speed) * (((n[1] - self.average[1]) / sum_n) - self.weight[y][1])
        sum_n = ((n[0] - self.average[0]) ** 2 + (n[1] - self.average[1]) ** 2 + (n[2] - self.average[2]) ** 2) ** 0.5
        self.weight[y][0] = self.weight[y][0] + float(self.speed) * ((n[0] - self.average[0] / sum_n) - self.weight[y][0])
        self.weight[y][1] = self.weight[y][1] + float(self.speed) * ((n[1] - self.average[1] / sum_n) - self.weight[y][1])
        self.weight[y][2] = self.weight[y][2] + float(self.speed) * ((n[2] - self.average[2] / sum_n) - self.weight[y][2])
        self.weight_length1(y)


    def chang_ini_weight(self, y ,n):   #初始化權重
    
        self.weight[y][0] = self.weight[y][0] + 0.5 * (n[0] - self.weight[y][0])
        self.weight[y][1] = self.weight[y][1] + 0.5 * (n[1] - self.weight[y][1])
        self.weight[y][2] = self.weight[y][2] + 0.5 * (n[2] - self.weight[y][2])

    def weight_length1(self, y):        #權重單位化
    
#        sum = ((self.weight[y][0] ** 2) + (self.weight[y][1] ** 2)) ** 0.5
#        self.weight[y][0] = self.weight[y][0] / sum
#        self.weight[y][1] = self.weight[y][1] / sum
        sum = ((self.weight[y][0] ** 2) + (self.weight[y][1] ** 2) + (self.weight[y][2] ** 2)) ** 0.5
        self.weight[y][0] = self.weight[y][0] / sum
        self.weight[y][1] = self.weight[y][1] / sum
        self.weight[y][2] = self.weight[y][2] / sum


########################################################################

if __name__ == '__main__':
    app = wx.PySimpleApp()
    #frame = MPL2_Frame()
    frame =MPL_Frame()
    frame.Center()
    frame.Show()
    app.MainLoop()