# FA Report Analyzer - 版本對照與遷移指南

## 📊 v1.0 vs v2.0 功能對照表

| 功能 | v1.0 | v2.0 | 說明 |
|------|------|------|------|
| **LLM 後端** |
| Anthropic Claude | ✅ | ✅ | 保留支援 |
| OpenAI API | ❌ | ✅ | 新增支援 |
| Ollama 地端模型 | ❌ | ✅⭐ | 新增，預設選項 |
| **文件格式** |
| TXT 純文字 | ✅ | ✅ | 持續支援 |
| PDF 文字提取 | ✅ | ✅ | 持續支援 |
| PDF 圖片提取 | ❌ | ✅ | 新增功能 |
| DOCX 文字 | ✅ | ✅ | 持續支援 |
| DOCX 圖片 | ❌ | ✅ | 新增功能 |
| PPTX 文字 | ❌ | ✅ | 新增支援 |
| PPTX 圖片 | ❌ | ✅ | 新增功能 |
| **圖片格式** |
| JPG/JPEG | ❌ | ✅ | 新增支援 |
| PNG | ❌ | ✅ | 新增支援 |
| GIF | ❌ | ✅ | 新增支援 |
| WEBP | ❌ | ✅ | 新增支援 |
| **分析功能** |
| 文字內容分析 | ✅ | ✅ | 持續支援 |
| 圖片內容分析 | ❌ | ✅ | 新增功能 |
| 多模態分析 | ❌ | ✅ | 新增功能 |
| **部署方式** |
| 需要外部 API | ✅ | ⭕ | 可選 |
| 完全本地化 | ❌ | ✅ | Ollama 支援 |
| **成本** |
| API 費用 | 必須 | 可選 | Ollama 免費 |

## 🔄 從 v1.0 遷移到 v2.0

### 方案 A: 保持原有用法（最小改動）

如果你只使用 Anthropic Claude，可以繼續使用 v1.0 的方式：

**v1.0 寫法:**
```bash
python fa_report_analyzer.py -i report.pdf -k YOUR_API_KEY
```

**v2.0 等效寫法:**
```bash
python fa_report_analyzer_v2.py -i report.pdf -b anthropic -k YOUR_API_KEY
```

**程式碼遷移:**
```python
# v1.0
from fa_report_analyzer import FAReportAnalyzer
analyzer = FAReportAnalyzer(api_key="your-key")
result = analyzer.analyze_report('report.pdf')

# v2.0（相容寫法）
from fa_report_analyzer_v2 import FAReportAnalyzer
analyzer = FAReportAnalyzer(backend="anthropic", api_key="your-key")
result = analyzer.analyze_report('report.pdf')
```

### 方案 B: 升級到 Ollama（推薦）

享受完全本地化和免費的優勢：

**安裝 Ollama:**
```bash
# 執行一鍵安裝
chmod +x install_ollama.sh
./install_ollama.sh
```

**使用方式:**
```bash
# 啟動 Ollama
ollama serve

# 使用 v2.0 分析（預設使用 Ollama）
python fa_report_analyzer_v2.py -i report.pdf
```

**程式碼:**
```python
from fa_report_analyzer_v2 import FAReportAnalyzer

# 預設使用 Ollama
analyzer = FAReportAnalyzer()
result = analyzer.analyze_report('report.pdf')
```

## 📦 依賴套件變更

### v1.0 依賴
```bash
pip install anthropic pandas PyPDF2 python-docx --break-system-packages
```

### v2.0 最小依賴（Ollama）
```bash
pip install ollama pandas Pillow PyPDF2 --break-system-packages
```

### v2.0 完整依賴（推薦）
```bash
pip install ollama pandas Pillow PyPDF2 PyMuPDF python-docx python-pptx --break-system-packages
```

## 🆕 v2.0 新增功能使用方式

### 1. 圖片分析

**分析單張圖片:**
```bash
python fa_report_analyzer_v2.py -i failure_photo.jpg
```

**分析 PDF 中的圖片:**
```bash
python fa_report_analyzer_v2.py -i report_with_images.pdf
```

**程式碼:**
```python
analyzer = FAReportAnalyzer()

# 讀取報告（包含圖片）
text, images = analyzer.read_report('report.pdf')
print(f"文字: {len(text)} 字元")
print(f"圖片: {len(images)} 張")

# 分析（自動包含圖片）
result = analyzer.analyze_report('report.pdf')
```

### 2. 多後端切換

**使用 Ollama:**
```python
analyzer = FAReportAnalyzer(backend="ollama")
```

**使用 OpenAI:**
```python
analyzer = FAReportAnalyzer(
    backend="openai",
    model="gpt-4o",
    api_key="your-key"
)
```

**使用 Anthropic:**
```python
analyzer = FAReportAnalyzer(
    backend="anthropic",
    model="claude-sonnet-4-20250514",
    api_key="your-key"
)
```

### 3. PowerPoint 支援

**分析 PowerPoint:**
```bash
python fa_report_analyzer_v2.py -i presentation.pptx
```

**提取文字和圖片:**
```python
analyzer = FAReportAnalyzer()
text, images = analyzer.read_report('presentation.pptx')
print(f"幻燈片文字: {len(text)} 字元")
print(f"圖片: {len(images)} 張")
```

## 🔧 API 變更

### 類別初始化

**v1.0:**
```python
FAReportAnalyzer(api_key=None)
```

**v2.0:**
```python
FAReportAnalyzer(
    backend="ollama",    # 新增: 選擇後端
    model=None,          # 新增: 指定模型
    api_key=None,        # 保留
    base_url=None        # 新增: 自訂 API 端點
)
```

### read_report 方法

**v1.0 回傳:**
```python
content = analyzer.read_report('report.pdf')  # 只回傳文字
```

**v2.0 回傳:**
```python
text, images = analyzer.read_report('report.pdf')  # 回傳文字和圖片
```

### analyze_with_ai 方法

**v1.0:**
```python
result = analyzer.analyze_with_ai(report_content)
```

**v2.0:**
```python
result = analyzer.analyze_with_ai(report_content, images)  # 新增圖片參數
```

## 📋 遷移檢查清單

- [ ] 安裝 Ollama（如果使用本地模型）
- [ ] 下載所需模型 (`ollama pull llama3.2-vision:latest`)
- [ ] 更新 Python 依賴套件
- [ ] 更新程式碼引入（如有）
- [ ] 測試現有報告分析
- [ ] 驗證輸出結果格式
- [ ] 更新文檔和腳本

## 🎯 推薦遷移路徑

### 情境 1: 單機使用，注重隱私
**推薦:** v2.0 + Ollama
- ✅ 數據完全本地化
- ✅ 無 API 費用
- ✅ 無網路依賴

### 情境 2: 追求最高精度
**推薦:** v2.0 + OpenAI GPT-4o
- ✅ 業界領先的模型
- ✅ 最佳圖片理解能力
- ⚠️ 需要付費

### 情境 3: 批次處理大量報告
**推薦:** v2.0 + Ollama + GPU
- ✅ 無使用限制
- ✅ 快速處理
- ✅ 可並行執行

### 情境 4: 團隊協作使用
**推薦:** v2.0 + OpenAI/Anthropic API
- ✅ 統一品質標準
- ✅ 易於部署
- ✅ 無硬體需求

## 💡 最佳實踐

### 開發環境
```bash
# 使用 Ollama 進行開發和測試（免費）
python fa_report_analyzer_v2.py -i test_report.pdf
```

### 生產環境
```bash
# 根據需求選擇最適合的後端
# 選項 1: Ollama（本地化）
python fa_report_analyzer_v2.py -i report.pdf

# 選項 2: OpenAI（高精度）
python fa_report_analyzer_v2.py -i report.pdf -b openai -k $API_KEY

# 選項 3: Anthropic（平衡）
python fa_report_analyzer_v2.py -i report.pdf -b anthropic -k $API_KEY
```

### 批次處理
```python
from fa_report_analyzer_v2 import FAReportAnalyzer
import glob

# 使用 Ollama 進行批次處理
analyzer = FAReportAnalyzer(backend="ollama")

for report_file in glob.glob("reports/*.pdf"):
    print(f"分析: {report_file}")
    result = analyzer.analyze_report(report_file)
    print(f"  分數: {result['total_score']:.1f}")
```

## 🐛 疑難排解

### 問題: 找不到 ollama 模組
```bash
pip install ollama --break-system-packages
```

### 問題: 圖片無法提取
```bash
pip install PyMuPDF python-docx python-pptx --break-system-packages
```

### 問題: v1.0 和 v2.0 同時存在
兩個版本可以共存，使用不同的檔案名：
- `fa_report_analyzer.py` - v1.0
- `fa_report_analyzer_v2.py` - v2.0

### 問題: Ollama 連接失敗
```bash
# 確保服務運行
ollama serve

# 檢查狀態
curl http://localhost:11434
```

## 📞 獲取幫助

如果遇到遷移問題：

1. 查看錯誤訊息
2. 確認依賴套件已安裝
3. 檢查 Ollama 服務狀態（如使用）
4. 參考完整文檔（README_v2.md）
5. 提供詳細資訊尋求協助

## 🔗 相關文檔

- **快速開始**: QUICKSTART_v2.txt
- **完整說明**: README_v2.md
- **Ollama 配置**: OLLAMA_SETUP.md
- **原始文檔**: README.md (v1.0)

---

**建議:** 優先使用 v2.0 + Ollama 享受完全本地化和免費的優勢！
