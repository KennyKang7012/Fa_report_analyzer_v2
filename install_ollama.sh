#!/bin/bash

# FA Report Analyzer v2.0 - 一鍵安裝腳本
# 支援 Ollama + 完整功能

set -e  # 遇到錯誤時退出

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     FA Report Analyzer v2.0 - 一鍵安裝腳本                    ║"
echo "║     支援 Ollama 地端模型 + 圖片分析功能                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# 檢測作業系統
OS="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    echo "⚠️  警告: 不支援的作業系統: $OSTYPE"
    echo "此腳本支援 Linux 和 macOS"
    exit 1
fi

echo "檢測到作業系統: $OS"
echo ""

# ============================================
# 步驟 1: 檢查 Python 版本
# ============================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[1/5] 檢查 Python 環境"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    echo "✓ Python 版本: $PYTHON_VERSION"
else
    echo "✗ 找不到 Python 3"
    echo "請先安裝 Python 3.8 或更高版本"
    exit 1
fi
echo ""

# ============================================
# 步驟 2: 安裝 Ollama
# ============================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[2/5] 安裝 Ollama"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if command -v ollama &> /dev/null; then
    OLLAMA_VERSION=$(ollama --version 2>&1)
    echo "✓ Ollama 已安裝: $OLLAMA_VERSION"
else
    echo "正在安裝 Ollama..."
    
    if [ "$OS" = "linux" ]; then
        curl -fsSL https://ollama.com/install.sh | sh
    elif [ "$OS" = "macos" ]; then
        if command -v brew &> /dev/null; then
            brew install ollama
        else
            echo "⚠️  請手動安裝 Ollama:"
            echo "   訪問 https://ollama.com/download"
            exit 1
        fi
    fi
    
    echo "✓ Ollama 安裝完成"
fi
echo ""

# ============================================
# 步驟 3: 啟動 Ollama 服務
# ============================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[3/5] 啟動 Ollama 服務"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 檢查 Ollama 是否正在運行
if curl -s http://localhost:11434 &> /dev/null; then
    echo "✓ Ollama 服務已運行"
else
    echo "正在啟動 Ollama 服務..."
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    sleep 3
    
    if curl -s http://localhost:11434 &> /dev/null; then
        echo "✓ Ollama 服務啟動成功"
    else
        echo "⚠️  Ollama 服務啟動失敗"
        echo "請手動執行: ollama serve"
    fi
fi
echo ""

# ============================================
# 步驟 4: 下載模型
# ============================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[4/5] 下載 AI 模型"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 檢查模型是否已下載
if ollama list | grep -q "llama3.2-vision"; then
    echo "✓ llama3.2-vision 模型已存在"
else
    echo "正在下載 llama3.2-vision 模型 (約 8GB，可能需要幾分鐘)..."
    echo ""
    read -p "是否下載模型? (y/n): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ollama pull llama3.2-vision:latest
        echo "✓ 模型下載完成"
    else
        echo "⚠️  跳過模型下載"
        echo "稍後請手動執行: ollama pull llama3.2-vision:latest"
    fi
fi
echo ""

# ============================================
# 步驟 5: 安裝 Python 依賴
# ============================================
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[5/5] 安裝 Python 依賴套件"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo "正在安裝核心套件..."
python3 -m pip install ollama pandas Pillow PyPDF2 --break-system-packages -q
echo "✓ 核心套件安裝完成"

echo ""
read -p "是否安裝完整功能 (PDF 圖片提取、Word、PowerPoint)? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "正在安裝完整功能套件..."
    python3 -m pip install PyMuPDF python-docx python-pptx --break-system-packages -q
    echo "✓ 完整功能套件安裝完成"
else
    echo "⚠️  跳過完整功能安裝"
    echo "如需完整功能，請執行:"
    echo "  pip install PyMuPDF python-docx python-pptx --break-system-packages"
fi
echo ""

# ============================================
# 完成
# ============================================
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    🎉 安裝完成! 🎉                              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "✅ 已安裝的組件:"
echo "  • Ollama (地端 LLM 服務)"
echo "  • Python 依賴套件"
echo "  • FA Report Analyzer v2.0"
echo ""
echo "📋 快速開始:"
echo "  1. 確保 Ollama 服務運行: ollama serve"
echo "  2. 分析報告: python3 fa_report_analyzer_v2.py -i your_report.pdf"
echo ""
echo "📖 查看文檔:"
echo "  • 完整說明: cat README_v2.md"
echo "  • Ollama 配置: cat OLLAMA_SETUP.md"
echo ""
echo "🧪 執行測試:"
echo "  python3 fa_report_analyzer_v2.py -i sample_fa_report.txt"
echo ""
echo "🔧 管理 Ollama:"
echo "  • 列出模型: ollama list"
echo "  • 下載模型: ollama pull llama3.2-vision:latest"
echo "  • 測試模型: ollama run llama3.2-vision:latest"
echo ""
