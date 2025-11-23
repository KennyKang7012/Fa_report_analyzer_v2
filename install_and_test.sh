#!/bin/bash

# FA Report Analyzer - 快速安裝和測試腳本
# 適用於 Linux/Mac 環境

echo "================================================"
echo "FA Report Analyzer - 快速安裝和測試"
echo "================================================"
echo ""

# 檢查 Python 版本
echo "[1/4] 檢查 Python 版本..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python 版本: $python_version"
echo ""

# 安裝基本依賴
echo "[2/4] 安裝基本依賴套件..."
pip install anthropic pandas --break-system-packages
echo "✓ 基本依賴安裝完成"
echo ""

# 安裝可選依賴
echo "[3/4] 安裝可選依賴套件..."
read -p "是否安裝 PDF 支援? (y/n): " install_pdf
if [ "$install_pdf" = "y" ] || [ "$install_pdf" = "Y" ]; then
    pip install PyPDF2 --break-system-packages
    echo "✓ PDF 支援已安裝"
fi

read -p "是否安裝 Word 支援? (y/n): " install_word
if [ "$install_word" = "y" ] || [ "$install_word" = "Y" ]; then
    pip install python-docx --break-system-packages
    echo "✓ Word 支援已安裝"
fi
echo ""

# 執行測試
echo "[4/4] 執行測試..."
if [ -f "sample_fa_report.txt" ]; then
    echo "找到範例報告,開始分析..."
    python3 fa_report_analyzer.py -i sample_fa_report.txt
    echo ""
    echo "================================================"
    echo "✓ 安裝和測試完成!"
    echo "================================================"
    echo ""
    echo "使用說明:"
    echo "  查看完整文檔: cat README.md"
    echo "  分析報告: python3 fa_report_analyzer.py -i your_report.txt"
else
    echo "⚠ 找不到範例報告檔案"
    echo "請確保 sample_fa_report.txt 在當前目錄"
fi
