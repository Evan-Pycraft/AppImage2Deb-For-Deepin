import sys
import os
import subprocess
from datetime import datetime
from PyQt6.QtWidgets import QApplication, QMessageBox
from appimage2deb.ui.main_window import MainWindow

class AppImage2Deb:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        
        # 连接信号
        self.window.convert_btn.clicked.connect(self._convert_appimage)
        
        # 初始化日志
        self.window.log_status("AppImage转Deb工具已启动")
        self.window.log_status("请选择AppImage文件并填写必要信息")

    def run(self):
        """运行应用程序"""
        self.window.show()
        sys.exit(self.app.exec())

    def _convert_appimage(self):
        """执行转换操作"""
        try:
            # 获取输入参数
            appimage_path = self.window.appimage_path.text()
            if not appimage_path:
                self.window.log_status("错误: 请先选择AppImage文件")
                QMessageBox.warning(self.window, "错误", "请先选择AppImage文件")
                return

            # 验证文件存在
            if not os.path.exists(appimage_path):
                self.window.log_status(f"错误: 文件不存在 {appimage_path}")
                QMessageBox.warning(self.window, "错误", "指定的AppImage文件不存在")
                return

            # 获取输出目录
            output_dir = os.path.dirname(appimage_path)
            
            # 获取其他参数
            package_name = self.window.package_name.text()
            software_name = self.window.software_name.text()
            version = self.window.version.text()
            architecture = self.window.architecture.currentText()
            category = self.window.category.currentText()
            
            # 开始转换
            self.window.log_status("开始转换过程...")
            self.window.log_status(f"输入文件: {appimage_path}")
            self.window.log_status(f"输出目录: {output_dir}")
            self.window.log_status(f"包名: {package_name}")
            self.window.log_status(f"版本: {version}")
            self.window.log_status(f"架构: {architecture}")
            
            # 创建临时工作目录
            import tempfile
            import shutil
            from pathlib import Path
            
            self.window.log_status("创建临时工作目录...")
            self.window.progress.setRange(0, 100)
            self.window.progress.setValue(10)
            self.window.progress.setFormat("准备环境...")
            self.app.processEvents()  # 强制更新UI
            with tempfile.TemporaryDirectory() as tmp_dir:
                # 确保进度条在异常时也能重置
                self.window.progress.setRange(0, 100)
                # 1. 准备DEBIAN目录结构
                deb_root = os.path.join(tmp_dir, f"{package_name}_{version}_{architecture}")
                debian_dir = os.path.join(deb_root, "DEBIAN")
                os.makedirs(debian_dir, exist_ok=True)
                    
                # 2. 创建control文件
                control_content = f"""Package: {package_name}
Version: {version}
Architecture: {architecture}
Maintainer: {self.window.maintainer.text()} <{self.window.maintainer_mail.text()}>
Description: {self.window.simple_description.text()}
 {self.window.detailed_description.toPlainText()}
Section: {category}
Priority: optional
"""
                control_path = os.path.join(debian_dir, "control")
                with open(control_path, "w") as f:
                    f.write(control_content)
                self.window.log_status(f"已创建control文件: {control_path}")
                    
                # 3. 复制AppImage到/usr/bin
                self.window.progress.setValue(30)
                self.window.progress.setFormat("复制文件...")
                self.app.processEvents()
                
                usr_bin_dir = os.path.join(deb_root, "usr", "bin")
                os.makedirs(usr_bin_dir, exist_ok=True)
                dest_path = os.path.join(usr_bin_dir, os.path.basename(appimage_path))
                shutil.copy2(appimage_path, dest_path)
                os.chmod(dest_path, 0o755)  # 确保可执行权限
                self.window.log_status(f"已复制AppImage到: {dest_path}")
                
                self.window.progress.setValue(50)
                self.window.progress.setFormat("准备构建...")
                self.app.processEvents()
                
                # 4. 构建deb包
                self.window.log_status("开始构建deb包...")
                self.window.progress.setRange(0, 0)  # 设置为不确定模式
                self.window.progress.setFormat("正在构建deb包...")
                self.app.processEvents()  # 强制更新UI
                
                deb_path = os.path.join(output_dir, f"{package_name}_{version}_{architecture}.deb")
                process = subprocess.Popen(
                    ["dpkg-deb", "--build", deb_root, deb_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    universal_newlines=True
                )
                
                # 实时读取输出并更新UI
                while True:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output:
                        self.window.log_status(output.strip())
                        self.app.processEvents()  # 强制更新UI
                
                return_code = process.poll()
                self.window.progress.setRange(0, 100)
                self.window.progress.setValue(100)
                self.window.progress.setFormat("完成")
                
                if return_code == 0:
                    self.window.log_status(f"转换成功完成! 生成的deb包: {deb_path}")
                    QMessageBox.information(self.window, "成功", f"AppImage转换成功!\n{deb_path}")
                else:
                    error = process.stderr.read()
                    self.window.log_status(f"dpkg-deb构建失败: {error}")
                    QMessageBox.critical(self.window, "错误", f"dpkg-deb构建失败: {error}")
                
        except Exception as e:
            self.window.log_status(f"发生异常: {str(e)}")
            QMessageBox.critical(self.window, "错误", f"发生异常: {str(e)}")

def main():
    converter = AppImage2Deb()
    converter.run()

if __name__ == "__main__":
    main()
