# -*- coding: big5
# 若程式中有使用中文，必須指明使用BIG5碼，前述的字碼定義必須在程式的第一或第二行
# 字碼定義的方式可參考：http://www.python.org/dev/peps/pep-0263/
# Python支援的字碼： http://www.python.org/doc/2.4/lib/standard-encodings.html

""" 此程式示作為檢查航照影像是否涵蓋機敏區的程式之GUI介面 """

import os, sys
import wx
# import exifread
import shapefile


import glob
#import datetime
#import numpy as np
#from skimage import io
#from skimage.transform import resize

# some global variables
inDir = ""
currDir = os.getcwd()
selFile = ""
shpFile = ""
kmlFile = ""

from math import sin, cos, tan, radians

from latlon2twd import LatLonToTWD97
from twd2latlon import TMToLatLon
from math import degrees,radians

# KML header, trailer, and template for placemark
kml_header = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2"  xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns:kml="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2005/Atom ">
<Folder>
'''
place_mark = '''<Placemark>  
  <name>{}</name>  

  <Point>  
    <coordinates>{},{},{}</coordinates>  
  </Point>  
</Placemark>  
'''
kml_trailer = '''</Folder>
</kml>
'''

#---------------------------------------------------------------------------

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        #Setup a new Frame
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY, title="EXIF Reader", size=(540,550),
                style = wx.DEFAULT_FRAME_STYLE & ~wx.MAXIMIZE_BOX ^ wx.RESIZE_BORDER)

        #logo_path = resource_path("image_name.bmp")
        #self.window.iconbitmap(image_path)
        ico = wx.Icon("image_name.bmp", wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
                
        # Add a Panel
        panel = wx.Panel(self, wx.ID_ANY)
        
        wx.StaticText(parent=panel, label="輸入檔案:", pos=(15,10))
        self.a = wx.TextCtrl(parent=panel,pos=(140,10),size=(325,20))
        self.btn1 = wx.Button(parent=panel,label="...",pos=(480,10),size=(40,20))
        self.Bind(wx.EVT_BUTTON, self.OnBtn1, self.btn1)

        wx.StaticText(parent=panel, label="輸出檔案:", pos=(15,40))
        self.b = wx.TextCtrl(parent=panel,pos=(140,40),size=(325,20))
        self.btn2 = wx.Button(parent=panel,label="...",pos=(480,40),size=(40,20))
        self.Bind(wx.EVT_BUTTON, self.OnBtn2, self.btn2)

        self.btn3 = wx.Button(parent=panel,label=" 清除訊息 ",pos=(15,70),size=(100,20))
        self.Bind(wx.EVT_BUTTON, self.OnBtn3, self.btn3)

        self.btn4 = wx.Button(parent=panel,label=" 確定 ",pos=(460,70),size=(60,20))
        self.Bind(wx.EVT_BUTTON, self.OnBtn4, self.btn4)

        self.txtCtrl = wx.TextCtrl(panel, id=wx.ID_ANY, style=wx.TE_MULTILINE, pos=(10,110), size=(510,390))

        #self.readConfigFile()
#            self.writeConfigFile()

    def OnBtn1(self, evt):
        global selFile
        # In this case we include a "New directory" button. DIR打開資料夾室窗。
        #dlg = wx.DirDialog(
        #    self, message="選擇輸入資料夾:",
        #    style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST
        #    )
                     
# Choose the output file. 
        dlg = wx.FileDialog(
            self, message="選擇SEL資料檔:",
            defaultDir=currDir, 
            defaultFile="",
            wildcard="*.sel",    #default file format: ".sel", you can edit file format according to your input file format.
            style= wx.FD_FILE_MUST_EXIST | wx.FD_OPEN #open file
            )
                    # If the user selects OK, then we process the dialog's data.
        # This is done by getting the path data from the dialog - BEFORE
        # we destroy it. 
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            path = dlg.GetPath()
            self.a.SetValue(path)
            selFile = self.a.GetValue()
            selFile = selFile.replace('\\', '/')
            
        # Only destroy a dialog after you're done with it.
        dlg.Destroy()

    def OnBtn2(self, evt):
        global shpFile
        
        # Choose the output file. 
        dlg = wx.FileDialog(
            self, message="選擇輸出檔案:",
            defaultDir=currDir, 
            defaultFile="",
            wildcard="*.shp",    #default file format: ".shp"
            style= wx.FD_OVERWRITE_PROMPT | wx.FD_SAVE #save file
            )
                     
        # If the user selects OK, then we process the dialog's data.
        # This is done by getting the path data from the dialog - BEFORE
        # we destroy it. 
        if dlg.ShowModal() == wx.ID_OK:
            # This returns a Python list of files that were selected.
            path = dlg.GetPath()
            self.b.SetValue(path)
            shpFile = self.b.GetValue()
            shpFile = shpFile.replace('\\', '/')
            
        # Only destroy a dialog after you're done with it.
        dlg.Destroy()

    def OnBtn3(self, evt):
        
        self.txtCtrl.Clear()

    def OnBtn4(self, evt):
        
        try:
            self.txtCtrl.WriteText('輸入檔案： %s\n' % selFile)
            self.shp_generate()
            
            self.txtCtrl.WriteText('輸出檔案： %s %s\n' % (shpFile, kmlFile))
            self.txtCtrl.WriteText('成功!\n')
        except:
            print('失敗!')
    
    # def shp_generate(fileIn, fileOut):
    def shp_generate(self):
        global selFile, shpFile, kmlFile
        kmlFile = shpFile[:-3] + 'kml'
        fout = open(kmlFile, 'w', encoding='utf-8')

        fout.write(kml_header)
 


        try:
            #開啟資料檔案，設定文字編碼為 Big5
            fin=open(selFile, encoding='big5')
            print("資料檔讀取成功，資料轉換中......")
        except:
            print("輸入資料檔名錯誤!")

        # Generate a point shapefile. File name is offered by user.
        shp = shapefile.Writer(shpFile, shapeType = shapefile.POINT)

        #Add attribute values(點號,橫坐標(X),縱座標(Y),正高(Z),控制點種類,測量方法,使用儀器,
        #測定日期(yyyymmdd),測量員,記錄者,點之記網頁,備註)
        #欄位格式定義請參考：https://pypi.org/project/pyshp/
        #
        shp.field('NAME','C',20) 
        shp.field('X_TWD97','N',15,3)
        shp.field('Y_TWD97','N',15,3)
        shp.field('H_TWD97','N',10,3)
        shp.field('X_TWD67','N',15,3)
        shp.field('Y_TWD67','N',15,3)
        shp.field('H_TWD67','N',10,3)
        shp.field('AIRLINE','N',5)
        shp.field('DATE','N',8)
        shp.field('TIME','N',4)
        shp.field('SECOND','N',5,3)
        shp.field('MAPID','C',8)
        shp.field('CameraID','N',1)
        shp.field('AIM','N',1)
        shp.field('Available','C',1)
        shp.field('heading','N',2)

        
        #列出欄位的定義，以供檢查新增的欄位是否正確
        print(shp.fields)
        
        #讀取第一列的檔頭，此為欄位說明，不屬於資料的一部分
        first_line = fin.readline()
        second_line = fin.readline()

        for line in fin:
            
            #line.strip() 首先去掉每一列輸入資料的結尾跳行符號
            #如果 len(s) == 0，表示此列為空白，可忽略之
            s = line.strip()
            if len(s) == 0:
                continue
        
            #s.split(',') 以逗號 (,) 分隔資料
            #每一列輸入的資料分隔後各別指派給等號左邊的變數
            name1,name2,x_97,y_97,h_97,x_67,y_67,h_67,airline,date,time,sec,Map,camera,aim,available,heading,a,b,c,d,e,f,g,h,i,j,k,l = s.split( )

            


            #從檔案讀進來的資料為文字格式 (string)，必須轉換為浮點數 (floating point) 才能進行運算
            NAME = name1+" "+name2
            X_97=float(x_97)
            Y_97=float(y_97)
            H_97=float(h_97)
            X_67=float(x_67)
            Y_67=float(y_67)
            H_67=float(h_67)
            AIRLINE = float(airline)
            DATE=float(date)
            TIME=float(time)
            SEC=float(sec)
            CAMERA=float(camera)
            AIM=float(aim)
            HEADING=float(heading)

            c = TMToLatLon()
            lat, lon = c.convert(X_97, Y_97)

            
            #加入點位空間資料(坐標)以及屬性資料
            shp.point(lat,lon)      #空間資料
            shp.record(NAME,lat,lon,H_97,X_67,Y_67,H_67,AIRLINE,DATE,TIME,SEC,Map,CAMERA,AIM,available,HEADING)    #屬性資料

            
            fout.write(place_mark.format(NAME,float(lon),float(lat),H_97))
            # fout.write(place_mark.format(NAME,Y_97,X_97,H_97))

        #存成檔名為fileOut的shapefile檔
        try:
            #關閉輸出的 shapefile 檔案才能確保資料寫入磁碟中
            shp.close()
            
            print("Shapefile圖檔 %s 產製成功!" % shpFile)
        except:
            print("Shapefile圖檔 %s 產製失敗!" % shpFile)
        
        fout.write(kml_trailer)
        fout.close()


        #關閉輸入資料檔案    
        fin.close()

    


class MyApp(wx.App):

    # wxWindows calls this method to initialize the application
    def OnInit(self):

        # Create an instance of our customized Frame class
        frame = MyFrame(None, -1, "Create Worldfile")
        frame.Show(True)

        # Tell wxWindows that this is our main window
        self.SetTopWindow(frame)

        # Return a success flag
        return True
        
#---------------------------------------------------------------------------
    
if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()
