from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QProgressBar,
                            QTextEdit, QFormLayout, QComboBox)
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("AppImage 转 Deb 工具")
        self.setMinimumSize(800, 600)
        
        # 主布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        
        # 左侧输入区域
        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        
        # 输入表单
        form = QFormLayout()
        
        # AppImage相关
        appimage_row = QHBoxLayout()
        self.appimage_path = QLineEdit()
        self.appimage_path.setPlaceholderText("选择 AppImage 文件路径")
        browse_btn = QPushButton("选择...")
        browse_btn.clicked.connect(self._browse_appimage)
        appimage_row.addWidget(self.appimage_path)
        appimage_row.addWidget(browse_btn)
        form.addRow("AppImage 文件:", appimage_row)
        
        # 包信息
        self.package_name = QLineEdit()
        self.package_name.setPlaceholderText("自动从AppImage文件名生成")
        form.addRow("Deb包名:", self.package_name)
        
        self.software_name = QLineEdit()
        self.software_name.setPlaceholderText("自动从AppImage文件名生成")
        form.addRow("软件名:", self.software_name)
        
        # 架构选择
        self.architecture = QComboBox()
        self.architecture.addItems(["amd64", "i386", "arm64", "armhf"])
        form.addRow("软件架构:", self.architecture)
        
        self.version = QLineEdit()
        self.version.setPlaceholderText("例如: 1.0.0")
        form.addRow("软件版本:", self.version)
        
        # 开发者信息
        self.developer = QLineEdit()
        self.developer.setPlaceholderText("开发者姓名")
        form.addRow("开发者姓名:", self.developer)
        
        self.developer_mail = QLineEdit()
        self.developer_mail.setPlaceholderText("developer@example.com")
        form.addRow("开发者邮箱:", self.developer_mail)
        
        # 维护者信息
        self.maintainer = QLineEdit()
        self.maintainer.setPlaceholderText("维护者姓名")
        form.addRow("维护者姓名:", self.maintainer)
        
        self.maintainer_mail = QLineEdit()
        self.maintainer_mail.setPlaceholderText("maintainer@example.com")
        form.addRow("维护者邮箱:", self.maintainer_mail)
        
        # 分类选择
        self.category = QComboBox()
        self.category.addItems([
            "影音", "开发", "教育", 
            "游戏", "图形", "网络", 
            "办公", "科学", "设置", 
            "系统", "工具"
        ])
        form.addRow("应用分类:", self.category)
        
        # 描述信息
        self.simple_description = QLineEdit()
        self.simple_description.setPlaceholderText("一句话描述")
        form.addRow("一句话介绍:", self.simple_description)
        
        self.detailed_description = QTextEdit()
        self.detailed_description.setMaximumHeight(100)
        form.addRow("详细介绍:", self.detailed_description)
        
        self.homepage = QLineEdit()
        self.homepage.setPlaceholderText("https://example.com")
        form.addRow("应用主页:", self.homepage)
        
        input_layout.addLayout(form)
        
        # 转换按钮
        self.convert_btn = QPushButton("开始转换")
        input_layout.addWidget(self.convert_btn)
        
        # 进度条
        self.progress = QProgressBar()
        input_layout.addWidget(self.progress)
        
        # 右侧状态区域
        status_widget = QWidget()
        status_layout = QVBoxLayout(status_widget)
        
        self.status_log = QTextEdit()
        self.status_log.setReadOnly(True)
        status_layout.addWidget(QLabel("转换状态:"))
        status_layout.addWidget(self.status_log)
        
        # 添加左右区域到主布局
        main_layout.addWidget(input_widget, stretch=2)
        main_layout.addWidget(status_widget, stretch=3)
        
        # 设置默认值
        self._set_default_values()
    
    def _browse_appimage(self):
        """打开文件对话框选择AppImage文件"""
        from PyQt6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "选择AppImage文件", 
            "", 
            "AppImage文件 (*.AppImage *.appimage)"
        )
        if file_path:
            self.appimage_path.setText(file_path)
            # 从文件名自动生成包名和软件名
            import os
            filename = os.path.basename(file_path)
            # 生成包名: 小写、去掉扩展名、替换特殊字符为连字符
            package_name = os.path.splitext(filename)[0].lower()
            package_name = ''.join(c if c.isalnum() else '-' for c in package_name)
            package_name = package_name.strip('-')
            # 生成软件名: 保留原始文件名但去掉扩展名
            software_name = os.path.splitext(filename)[0]
            self.package_name.setText(package_name)
            self.software_name.setText(software_name)

    def _set_default_values(self):
        """设置输入字段的默认值"""
        self.package_name.setText("")
        self.software_name.setText("")
        self.architecture.setCurrentText("amd64")
        self.version.setText("1.0.0")
        self.developer.setText("Unknown")
        self.developer_mail.setText("unknown@example.com")
        self.maintainer.setText("Unknown")
        self.maintainer_mail.setText("unknown@example.com")
        self.category.setCurrentText("Utility")
        self.simple_description.setText("A simple application")
        self.detailed_description.setPlainText("This is a detailed description of the application.")
        self.homepage.setText("https://example.com")
        
    def log_status(self, message):
        """在状态区域添加日志消息"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.status_log.append(f"[{timestamp}] {message}")
        self.status_log.ensureCursorVisible()
