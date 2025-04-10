#!/bin/bash
# AppImage2Deb 直接运行脚本

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# 检查Python3是否安装
if ! command -v python3 &> /dev/null
then
    echo "错误: 需要Python3但未安装"
    echo "请先安装Python3: sudo apt install python3"
    exit 1
fi

# 检查PyQt6是否安装
if ! python3 -c "from PyQt6 import QtWidgets" &> /dev/null
then
    echo "错误: 需要PyQt6但未安装"
    echo "请先安装PyQt6: sudo apt install python3-pyqt6"
    exit 1
fi

# 设置PYTHONPATH并运行主程序
PYTHONPATH="$SCRIPT_DIR" python3 "$SCRIPT_DIR/appimage2deb/main.py"
