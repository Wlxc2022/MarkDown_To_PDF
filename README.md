## ✅ 步骤一：安装 wkhtmltopdf

### 🪟 Windows 安装：

1. 请访问 [wkhtmltopdf 下载页面](https://wkhtmltopdf.org/downloads.html)
2. 选择适合的 Windows 版本（32-bit 或 64-bit）进行下载并安装。
3. 安装完成后，将 `wkhtmltopdf.exe` 添加到环境变量中，这样 Python 可以找到它。

#### 添加到环境变量的方法：

- 找到安装路径（例如：`C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe`）
- 右键点击 “此电脑” → “属性” → “高级系统设置” → “环境变量”
- 在 “系统变量” 部分，选择 `Path` 变量，点击 “编辑”
- 添加 `wkhtmltopdf.exe` 所在文件夹的路径（**不是加 exe 文件本身，而是 bin 文件夹路径**）

