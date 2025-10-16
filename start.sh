#!/bin/bash

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

clear

echo ""
echo -e "${RED}╔═══════════════════════════════════════════════════════════╗${NC}"
echo -e "${RED}║                                                           ║${NC}"
echo -e "${RED}║     ⚠️  请注意：不要直接使用 python3 命令！ ⚠️         ║${NC}"
echo -e "${RED}║                                                           ║${NC}"
echo -e "${RED}╚═══════════════════════════════════════════════════════════╝${NC}"
echo ""

echo -e "${YELLOW}您看到此消息是因为：${NC}"
echo "系统的 Python 3.13 没有 tkinter 支持"
echo ""

echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  正确的启动方式${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}选项 1（最简单）：${NC}"
echo "  ./run.sh"
echo ""
echo -e "${BLUE}选项 2（手动激活）：${NC}"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
echo -e "${BLUE}选项 3（一行命令）：${NC}"
echo "  source venv/bin/activate && python main.py"
echo ""
echo -e "${BLUE}选项 4（直接使用虚拟环境）：${NC}"
echo "  venv/bin/python main.py"
echo ""

echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo ""

# 询问用户是否要立即运行
echo -e "${YELLOW}是否现在启动程序？(y/n)${NC}"
read -r response

if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo ""
    echo -e "${GREEN}🚀 正在启动程序...${NC}"
    echo ""
    ./run.sh
else
    echo ""
    echo -e "${BLUE}好的，请在准备好时运行：${NC} ./run.sh"
    echo ""
fi
