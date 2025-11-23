# FA Report Analyzer - 專案結構

## 📁 文件結構

```
fa-report-analyzer/
│
├── fa_report_analyzer.py      # 主程式 - FA 報告分析器
├── sample_fa_report.txt        # 範例 FA 報告
├── usage_examples.py           # 使用範例集合
├── quick_test.py               # 快速測試腳本
├── install_and_test.sh         # 自動安裝和測試腳本 (Bash)
├── requirements.txt            # Python 依賴套件清單
├── README.md                   # 完整使用說明
└── PROJECT_STRUCTURE.md        # 本文件 - 專案結構說明
```

## 🔧 核心文件說明

### 1. fa_report_analyzer.py
**主程式文件,包含完整的分析功能**

主要類別:
- `FAReportAnalyzer`: 核心分析器類別

主要方法:
- `read_report()`: 讀取各種格式的報告文件
- `analyze_with_ai()`: 使用 Claude AI 進行分析
- `generate_report()`: 生成評估報告
- `analyze_report()`: 完整分析流程

### 2. sample_fa_report.txt
**範例 FA 報告**

包含:
- 完整的 FA 報告結構
- 所有評估維度的內容
- 可用於測試和學習

### 3. usage_examples.py
**使用範例集合**

包含 5 個範例:
1. 基本使用 - 分析單一報告
2. 批次分析 - 分析多份報告
3. 自訂分析 - 查看各維度詳細評分
4. 匯出 JSON - 將結果匯出為 JSON 格式
5. 讀取文件 - 讀取不同格式的文件

### 4. quick_test.py
**快速測試腳本**

功能:
- 檢查 Python 版本
- 檢查依賴套件
- 自動安裝缺少的套件
- 執行完整測試

### 5. install_and_test.sh
**自動安裝腳本 (Bash)**

適用於 Linux/Mac 環境,自動完成:
- 環境檢查
- 依賴安裝
- 執行測試

## 📊 評估系統架構

### 評估維度 (6 個)
```
基本資訊完整性 (15%)
├── 產品資訊
├── 客戶資訊
├── FA 編號
└── 負責工程師

問題描述與定義 (15%)
├── 失效現象描述
├── 失效模式
├── 問題範圍
└── 失效率數據

分析方法與流程 (20%)
├── 分析方法適當性
├── 分析步驟邏輯性
├── 實驗設計
└── 設備使用正確性

數據與證據支持 (20%)
├── 數據充分性
├── 圖片清晰度
├── 量化數據
└── 對照組使用

根因分析 (20%)
├── 根本原因深度
├── 因果關係推導
├── 5-Why/Fishbone 應用
└── 其他可能原因排除

改善對策 (10%)
├── 短期/長期對策
├── 對策可行性
├── 預防措施
└── 驗證計畫
```

### 評分標準
```
A 級: 90-100 分 (卓越報告)
B 級: 80-89 分  (良好報告)
C 級: 70-79 分  (合格報告)
D 級: 60-69 分  (待改進報告)
F 級: <60 分    (不合格報告)
```

## 🔄 工作流程

```
[開始]
  ↓
[讀取 FA 報告]
  ↓
[內容預處理]
  ↓
[AI 分析評估] → 使用 Claude API
  ↓
[計算各維度分數]
  ↓
[生成評估報告]
  ↓
[輸出結果]
  ↓
[結束]
```

## 💾 輸出格式

### 文字報告 (.txt)
- 完整的評估結果
- 表格化的維度評分
- 具體的改善建議

### JSON 格式 (.json)
```json
{
  "total_score": 85.5,
  "grade": "B",
  "dimension_scores": {
    "基本資訊完整性": {
      "score": 13.5,
      "percentage": 90.0,
      "comment": "..."
    },
    ...
  },
  "strengths": [...],
  "improvements": [...],
  "summary": "..."
}
```

## 🎯 使用場景

### 場景 1: 單一報告評估
```python
analyzer = FAReportAnalyzer()
result = analyzer.analyze_report('fa_report.txt')
```

### 場景 2: 批次報告評估
```python
for report in reports:
    analyzer.analyze_report(report, f'eval_{report}')
```

### 場景 3: 持續改進追蹤
```python
# 分析歷史報告,追蹤改進趨勢
scores = []
for month in range(1, 13):
    result = analyzer.analyze_report(f'report_{month}.txt')
    scores.append(result['total_score'])
```

## 🔐 安全性考量

- API key 不應硬編碼在程式中
- 使用環境變數或參數傳遞 API key
- 報告內容可能包含敏感資訊,注意保密
- 生成的評估報告應妥善保管

## 📈 擴展性

### 可擴展的功能
1. **新增評估維度**
   - 修改 `dimensions` 字典
   - 調整提示詞

2. **自訂評分標準**
   - 修改 `grade_criteria` 字典
   - 調整分數區間

3. **支援新的文件格式**
   - 擴展 `read_report()` 方法
   - 加入新的解析邏輯

4. **整合到現有系統**
   - 作為 API 服務
   - 整合到 CI/CD 流程
   - 連接資料庫存儲結果

## 🛠️ 維護建議

### 定期維護
- 更新 Claude API 版本
- 優化分析提示詞
- 收集用戶反饋改進評估標準

### 版本控制
- 使用 Git 管理程式碼
- 記錄每次評估標準的變更
- 保留歷史評估結果供比較

## 📞 支援資源

### 文件資源
- `README.md` - 完整使用說明
- `usage_examples.py` - 程式碼範例
- Claude API 文檔: https://docs.anthropic.com/

### 問題排查
1. 檢查 Python 版本
2. 驗證依賴套件安裝
3. 確認 API key 設定
4. 查看錯誤訊息和日誌

---

**版本:** 1.0.0
**建立日期:** 2024-11-20
**維護者:** KennyKang
