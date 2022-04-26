# DSAI HW2  
## 資料集  
```
training.csv  
testing.csv  
```  
## 執行  
`python app.py --training=training.csv --testing=testing.csv --output=output.csv`
  
## 前處理  
由於沒有明確時間，所以就直接產生假日期，不分平日假日。  

使用股票技術分析，計算布林通道、KD值、RSV、MACD、MA5、MA10等數值。  
* **布林通道**: 以中央的移動平均線（Simple Moving Average：SMA）加減標準差（2σ）所算出，上布林線及下布林線。    
* **RSV**: 從n天週期計算出隨機指標時，首先須找出最近n天當中曾經出現過的最高價、最低價與第n天的收盤價，然後利用這三個數字來計算第n天的未成熟隨機值(RSV)。    

     <img width="332" alt="image" src="https://user-images.githubusercontent.com/65431754/164912144-984210c2-1d12-406c-b407-8527562f93a1.png">   
* **KD值**:是一種技術分析中判斷價格的相對走勢與轉折點的動量分析方法。  
     <img width="286" alt="image" src="https://user-images.githubusercontent.com/65431754/164912159-cfecc4fb-caf4-4170-b13d-964875facf89.png">  
	 
* **MACD**:MACD指標的原理是透過比較兩條長短天數的指數移動平均線(EMA)，相減算出 差離值(DIF)後，對差離值再進行一次指數移動平均線的計算。  
	<img width="382" alt="image" src="https://user-images.githubusercontent.com/65431754/164912213-519024a5-ffe1-4a3c-ba42-8439b3b11cc2.png">
* **MA5、MA10**:將過去(含最新)5天和10天收盤價加總，除以5和10    
## 執行  
由於只有短期交易，所以只用股票策略來判斷買賣動作。  
大致動作為:  


| 條件 | 動作| 
| -------- | -------- |
| RSV>85    | -1     | 
| RSV<15    | 1     |
| 收盤價 > 上布林    | -1     | 
| 收盤價 < 下布林    | 1     |
| 5MA < 10MA    | -1     | 
| 5MA > 10MA    | 1     |
| K > 90    | -1     | 
| D<10    | 1     |    

## 圖表示意圖
![image](https://user-images.githubusercontent.com/65431754/165274917-bd224e8b-719f-422a-9ec8-1b1bb32907e3.png)

## 結果  

| company_name | profit| 
| -------- | -------- |
| apple  | 4.32     | 
| tesla    | 92     |
| amc   | 5.87     | 
| tiwtter    | 4.31     |
| unknown | 4.95     | 
   
