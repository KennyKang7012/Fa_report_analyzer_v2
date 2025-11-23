#!/bin/bash

# PPT 到 PPTX 批次轉換工具
# 用於將舊版 PowerPoint 文件轉換為新版格式

set -e

# 顏色輸出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║           PPT 到 PPTX 批次轉換工具                            ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# 檢查參數
INPUT_DIR="${1:-.}"
OUTPUT_DIR="${2:-./converted_pptx}"

if [ ! -d "$INPUT_DIR" ]; then
    echo -e "${RED}✗ 錯誤: 輸入目錄不存在: $INPUT_DIR${NC}"
    exit 1
fi

# 創建輸出目錄
mkdir -p "$OUTPUT_DIR"

echo "輸入目錄: $INPUT_DIR"
echo "輸出目錄: $OUTPUT_DIR"
echo ""

# 檢測作業系統
OS="unknown"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    echo -e "${YELLOW}⚠️  警告: 不支援的作業系統: $OSTYPE${NC}"
    echo "此腳本支援 Linux 和 macOS"
    exit 1
fi

# 尋找 LibreOffice
echo "[1/3] 檢查 LibreOffice..."

LIBREOFFICE_CMD=""
LIBREOFFICE_PATHS=(
    "libreoffice"
    "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    "/usr/bin/libreoffice"
    "/usr/local/bin/libreoffice"
)

for path in "${LIBREOFFICE_PATHS[@]}"; do
    if command -v "$path" &> /dev/null || [ -x "$path" ]; then
        LIBREOFFICE_CMD="$path"
        break
    fi
done

if [ -z "$LIBREOFFICE_CMD" ]; then
    echo -e "${RED}✗ 找不到 LibreOffice${NC}"
    echo ""
    echo "請先安裝 LibreOffice:"
    if [ "$OS" = "macos" ]; then
        echo "  brew install --cask libreoffice"
    else
        echo "  sudo apt install libreoffice  # Ubuntu/Debian"
        echo "  sudo dnf install libreoffice  # Fedora"
    fi
    exit 1
fi

echo -e "${GREEN}✓ 找到 LibreOffice: $LIBREOFFICE_CMD${NC}"

# 檢查版本
VERSION=$($LIBREOFFICE_CMD --version 2>&1 | head -n 1)
echo "  版本: $VERSION"
echo ""

# 搜尋 PPT 文件
echo "[2/3] 搜尋 PPT 文件..."

PPT_FILES=()
while IFS= read -r -d '' file; do
    PPT_FILES+=("$file")
done < <(find "$INPUT_DIR" -type f -iname "*.ppt" -not -iname "*.pptx" -print0)

if [ ${#PPT_FILES[@]} -eq 0 ]; then
    echo -e "${YELLOW}⚠️  在 $INPUT_DIR 中找不到 .ppt 文件${NC}"
    exit 0
fi

echo -e "${GREEN}✓ 找到 ${#PPT_FILES[@]} 個 PPT 文件${NC}"
echo ""

# 轉換文件
echo "[3/3] 開始轉換..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

SUCCESS_COUNT=0
FAILED_COUNT=0
FAILED_FILES=()

for i in "${!PPT_FILES[@]}"; do
    file="${PPT_FILES[$i]}"
    filename=$(basename "$file")
    num=$((i + 1))
    
    echo -e "\n[$num/${#PPT_FILES[@]}] 轉換: ${YELLOW}$filename${NC}"
    
    # 執行轉換
    if "$LIBREOFFICE_CMD" --headless --convert-to pptx --outdir "$OUTPUT_DIR" "$file" > /dev/null 2>&1; then
        echo -e "  ${GREEN}✓ 成功${NC}"
        ((SUCCESS_COUNT++))
    else
        echo -e "  ${RED}✗ 失敗${NC}"
        ((FAILED_COUNT++))
        FAILED_FILES+=("$filename")
    fi
done

# 顯示統計
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "轉換完成!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "總文件數: ${#PPT_FILES[@]}"
echo -e "${GREEN}成功: $SUCCESS_COUNT${NC}"

if [ $FAILED_COUNT -gt 0 ]; then
    echo -e "${RED}失敗: $FAILED_COUNT${NC}"
    echo ""
    echo "失敗的文件:"
    for file in "${FAILED_FILES[@]}"; do
        echo "  • $file"
    done
fi

echo ""
echo "輸出目錄: $OUTPUT_DIR"
echo ""

# 列出轉換後的文件
if [ $SUCCESS_COUNT -gt 0 ]; then
    echo "轉換後的文件:"
    ls -lh "$OUTPUT_DIR"/*.pptx 2>/dev/null | awk '{print "  • " $9 " (" $5 ")"}'
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "下一步: 使用轉換後的 PPTX 文件進行分析"
echo ""
echo "範例:"
echo "  python fa_report_analyzer_v2.py -i \"$OUTPUT_DIR/your_file.pptx\""
echo ""
echo "批次分析:"
echo "  for file in \"$OUTPUT_DIR\"/*.pptx; do"
echo "      python fa_report_analyzer_v2.py -i \"\$file\""
echo "  done"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
