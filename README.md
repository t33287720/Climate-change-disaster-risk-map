介紹
=
基於自身擁有之.kml檔案

以 selenium 開啟風險圖台頁面(https://dra.ncdr.nat.gov.tw/Frontend/Tools/ShowMapBoxWMS#)

自行輸入並分析檔案內各處之風險級別

前置作業
=
1. 於 google 地球自行標示位置，匯出一份 .kml 檔案(https://earth.google.com/)
2. 下載 Microsoft Edge 的 webdriver，跟 main 放置於同資料夾(注意版本)

使用
=
將kml改為自己的檔案名

將xmlns改為kml裡的KML xmlns(不確定)

動作分析
=
調整透明度方便分析顏色

讀取 .kml 檔案，找出全部地點之經緯度

以 selenium 爬蟲照順序貼上"氣候變遷災害風險圖臺"經緯度查詢

尋找位置後依顏色判斷第一級~第五級

![test](https://github.com/t33287720/Climate-change-disaster-risk-map/assets/150265747/ea278286-73aa-4787-8ea3-1bc059530fb6)
