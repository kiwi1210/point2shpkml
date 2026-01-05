# point2shpkml
Convert point data to shapefile and KML with GUI (Graphical User Interface).
記錄自己在2021年末時的其中一項作業，撰寫圖形使用介面(Graphical User Interface，GUI)，將航攝紀錄的點位坐標資料轉換成 Shapefile 和 KML 圖檔。

## Reference
http://blog.ez2learn.com/2009/08/15/lat-lon-to-twd97/


## 資料介紹
林務局農林航空測量所 (農航所) 使用高解像力數位相機 DMC (Digital Mapping Camera) 拍攝航空照片，並紀錄每張航空照片之相關資料，包括：任務編號、照片號碼、品質、投影中心座標、拍照時間、對應基本圖圖號、相機代號等，航空攝影紀錄資料可從農航所網站下載。
下載一個記錄檔，裡面包含*.dbf, *.sel, *.shp, *.shx。
這次下載主要是為了sel檔，檔案裡的資料內容可參考DMC 航空攝影紀錄檔格式說明

另外，這次的程式碼也import latlon2twd.py和twd2latlon.py這兩支程式碼，因為不是我寫的，所以就不放上來了。

## 準備工作
下載wxPython。根據維基百科，wxPython是Python語言的GUI工具包，作為Python的擴充模組實現，包裝了wxWidgets。wxPython是跨平台的，開源的。

$ pip install wxpython
也可以利用Qt Designer的視覺化操作來設計介面。

## 打包成exe檔
打開Anaconda Prompt，切換路徑到上面程式檔案所在位置。
接著輸入以下程式碼。

conda install pyinstaller
跑到一半會出現 Proceed([y]/n)?
輸入 “y” 即可。
看到”done”即成功。
接著輸入:

pyinstaller --onefile fileName
fileName填入欲打包成exe檔之程式檔案名稱。

## 測試
由於我只是要檢測這支程式碼是否有成功執行，為加快速度我只取了sel檔中前100筆資料下去測試。
先來檢視產生出的kml檔，利用google earth測試。
再來檢視產生出shp檔，利用ArcGIS Pro測試。
由於沒有定義座標系統，使用 define projection 定義座標系統。


