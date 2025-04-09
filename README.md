# AppImage2Deb 转换工具

## 项目说明

AppImage2Deb是一个图形化工具，用于将AppImage格式的应用程序转换为Deepin/UOS系统的deb安装包。支持自动提取AppImage内容、生成桌面快捷方式、系统集成等功能。

## 系统要求

- Deepin 20+ 或 UOS 系统
- Python 3.8+
- PyQt6
- dpkg工具链

## 安装方法

1. 安装依赖：
```bash
sudo apt install python3-pyqt6 dpkg-dev
```

2. 克隆项目：
```bash
git clone https://github.com/Evan-Pycraft/AppImage2Deb-For-Deepin.git
cd AppImage2Deb-For-Deepin
```

3. 打包安装：
```bash
chmod +x make-deb.sh
sudo ./make-deb.sh
```

## 使用指南

### 图形界面使用
1. 启动程序：
```bash
/usr/bin/appimage2deb/main.py
```
2. 选择要转换的AppImage文件
3. 填写软件包信息(名称、版本等)
4. 点击"转换"按钮

### 命令行使用
```bash
./appimage2deb/main.py /path/to/appimage [options]
```

## 错误处理

### 常见错误及解决方案

1. **依赖缺失错误**：
   ```
   ImportError: No module named 'PyQt6'
   ```
   解决方案：安装PyQt6
   ```bash
   sudo apt install python3-pyqt6
   ```

2. **权限不足错误**：
   ```
   Permission denied when running make-deb.sh
   ```
   解决方案：使用sudo执行脚本

3. **AppImage提取失败**：
   ```
   Error extracting AppImage
   ```
   解决方案：
   - 确保AppImage文件完整
   - 检查文件权限
   - 尝试手动运行AppImage确认是否可执行

4. **打包失败**：
   ```
   dpkg-deb: error
   ```
   解决方案：
   - 检查是否有足够的磁盘空间
   - 确认dpkg-dev已安装

## 开发说明

### 项目结构
```
appimage2deb/
├── core/        # 核心转换逻辑
├── ui/          # 用户界面
├── resources/   # 资源文件
└── main.py      # 程序入口
```

### 构建deb包
```bash
./make-deb.sh
```

### 贡献指南
欢迎提交Pull Request或Issue报告问题

## 许可证
GPL-3.0 License
# AppImage2Deb-For-Deepin
