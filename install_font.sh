#!/bin/bash

# 字体安装脚本 - 将像素字体安装到 macOS 系统

echo "======================================================"
echo "像素字体安装脚本"
echo "======================================================"
echo ""

FONT_DIR="$HOME/Library/Fonts"

# 字体文件列表
FONTS=(
    "Coral_Pixels/CoralPixels-Regular.ttf"
    "Coral_Pixels/Jersey10Charted-Regular.ttf"
)

# 创建用户字体目录（如果不存在）
if [ ! -d "$FONT_DIR" ]; then
    mkdir -p "$FONT_DIR"
    echo "✓ 创建字体目录: $FONT_DIR"
fi

echo "正在安装字体到系统..."
echo ""

SUCCESS_COUNT=0
FAIL_COUNT=0

for FONT_FILE in "${FONTS[@]}"; do
    if [ ! -f "$FONT_FILE" ]; then
        echo "✗ 找不到字体文件: $FONT_FILE"
        FAIL_COUNT=$((FAIL_COUNT + 1))
        continue
    fi
    
    FONT_NAME=$(basename "$FONT_FILE")
    echo "安装: $FONT_NAME"
    
    cp "$FONT_FILE" "$FONT_DIR/"
    
    if [ $? -eq 0 ]; then
        echo "  ✓ 已复制到: $FONT_DIR"
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
    else
        echo "  ✗ 复制失败"
        FAIL_COUNT=$((FAIL_COUNT + 1))
    fi
    echo ""
done

echo "======================================================"
echo "安装结果: $SUCCESS_COUNT 成功, $FAIL_COUNT 失败"
echo "======================================================"
echo ""

if [ $SUCCESS_COUNT -gt 0 ]; then
    echo "后续步骤:"
    echo "1. 打开 Font Book (字体册) 应用验证字体"
    echo "2. 重启 Python 程序即可使用像素字体"
    echo ""
    echo "运行程序:"
    echo "  source venv/bin/activate && python main.py"
    echo ""
fi
