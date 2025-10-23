#!/bin/bash

# ===================================================================
# Image to 8-bit Melody Converter - 启动指南
# ===================================================================

echo "🎵 Image to 8-bit Melody Converter"
echo "===================================="
echo ""

# 检查虚拟环境是否存在
if [ ! -d "venv" ] && [ ! -d ".venv" ]; then
    echo "❌ 虚拟环境不存在！"
    echo ""
    echo "请先运行以下命令创建虚拟环境："
    echo "  /opt/homebrew/bin/python3.12 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    echo ""
    exit 1
fi

echo "✅ 找到虚拟环境"
echo "🚀 启动程序..."
echo ""

# 优先使用 Anaconda Python 3.12（有所有依赖）
if [ -f "/opt/anaconda3/bin/python3.12" ]; then
    /opt/anaconda3/bin/python3.12 main.py
# 否则尝试激活虚拟环境
elif [ -d "venv" ]; then
    source venv/bin/activate
    python main.py
elif [ -d ".venv" ]; then
    .venv/bin/python main.py
fi

# 如果程序退出，显示消息
echo ""
echo "程序已退出"
