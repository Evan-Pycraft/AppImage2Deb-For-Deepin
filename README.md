# AppImage2Deb 转换工具

## 项目说明

AppImage2Deb是一个图形化工具，用于处理AppImage格式的应用程序。支持AppImage文件的分析和转换功能。

## 使用方式

直接运行脚本即可使用：
```bash
# 添加执行权限
chmod +x run-appimage2deb.sh

# 运行程序
./run-appimage2deb.sh
```

## 系统要求

- Deepin 20+ 或 UOS 系统
- Python 3.8+
- PyQt6

## 使用指南

### 图形界面使用
1. 启动程序：
```bash
./run-appimage2deb.sh
```
2. 选择要处理的AppImage文件
3. 根据需要进行操作

### 命令行使用
```bash
./appimage2deb/main.py /path/to/appimage [options]
```

## 常见问题

1. **依赖缺失错误**：
   ```bash
   sudo apt install python3-pyqt6
   ```

2. **权限问题**：
   ```bash
   chmod +x run-appimage2deb.sh
   ```

3. **其他问题**：
   请提交Issue到项目仓库

## 项目结构
```
appimage2deb/
├── core/        # 核心逻辑
├── ui/          # 用户界面
├── resources/   # 资源文件
└── main.py      # 程序入口
```

## 许可证
GPL-3.0 License
