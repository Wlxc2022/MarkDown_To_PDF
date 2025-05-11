from pathlib import Path
import markdown
import pdfkit
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import platform

# 指定 wkhtmltopdf 路径（请根据实际修改）
PDFKIT_CONFIG = pdfkit.configuration(wkhtmltopdf=r"D:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")

# 获取样式列表
def get_style_list():
    style_dir = Path("YS")
    if not style_dir.exists():
        messagebox.showerror("错误", "找不到 YS 样式文件夹")
        return []
    styles = [f.stem for f in style_dir.glob("*.css")]
    if not styles:
        messagebox.showwarning("提示", "YS 文件夹中没有任何 CSS 样式")
    return styles

# Markdown 转 PDF
def convert_md_to_pdf(md_file, css_name, output_file):
    css_path = Path("YS") / f"{css_name}.css"
    if not css_path.exists():
        messagebox.showerror("错误", f"样式文件不存在: {css_path}")
        return False

    try:
        md_text = Path(md_file).read_text(encoding="utf-8")
        css_text = css_path.read_text(encoding="utf-8")

        html = f"<style>{css_text}</style>" + markdown.markdown(
            md_text, extensions=["tables", "fenced_code"]
        )

        options = {
            'encoding': "UTF-8",
            'page-size': 'A4',
            'margin-top': '20mm',
            'margin-bottom': '20mm',
            'footer-right': '[page]/[topage]',
            'footer-font-size': '10',
        }

        pdfkit.from_string(html, output_file, options=options, configuration=PDFKIT_CONFIG)
        return True

    except Exception as e:
        messagebox.showerror("转换失败", f"PDF 生成过程中发生错误：\n{e}")
        return False

# 打开输出文件夹
def open_folder(path):
    folder = os.path.dirname(path)
    try:
        if platform.system() == 'Windows':
            os.startfile(folder)
        elif platform.system() == 'Darwin':
            os.system(f"open '{folder}'")
        else:
            os.system(f"xdg-open '{folder}'")
    except Exception:
        messagebox.showwarning("提示", "无法打开文件夹，请手动查找输出文件。")

# 主 GUI
def main():
    root = tk.Tk()
    root.title("Mk_To_PDF")
    root.geometry("600x360")
    root.configure(bg="#f9f9f9")

    try:
        root.iconbitmap("MTP.ico")  # 图标可选
    except Exception:
        pass

    md_file_path = tk.StringVar()
    selected_style = tk.StringVar()
    output_pdf_path = tk.StringVar()

    # 选择 Markdown 文件
    def browse_md():
        file = filedialog.askopenfilename(filetypes=[("Markdown 文件", "*.md")])
        if file:
            md_file_path.set(file)
            output_pdf_path.set(str(Path(file).with_suffix(".pdf")))

    # 选择输出路径
    def browse_output():
        file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF 文件", "*.pdf")])
        if file:
            output_pdf_path.set(file)

    # 执行转换
    def do_convert():
        if not md_file_path.get():
            messagebox.showwarning("提示", "请选择 Markdown 文件")
            return
        if not selected_style.get():
            messagebox.showwarning("提示", "请选择样式")
            return
        if not output_pdf_path.get():
            messagebox.showwarning("提示", "请选择输出路径")
            return

        success = convert_md_to_pdf(md_file_path.get(), selected_style.get(), output_pdf_path.get())
        if success:
            messagebox.showinfo("成功", f"已生成 PDF：\n{output_pdf_path.get()}")
            open_folder(output_pdf_path.get())

    # 界面布局
    frame = tk.Frame(root, bg="#458B74", padx=10, pady=10)
    frame.pack(expand=True, fill="both")

    tk.Label(frame, text=" 选择Markdown文件：", bg="#f9f9f9", font=("Arial", 12)).grid(row=0, column=0, sticky="w")
    tk.Entry(frame, textvariable=md_file_path, width=50).grid(row=1, column=0, padx=5, pady=2)
    tk.Button(frame, text="浏览", command=browse_md, width=10, bg="#d0e0ff").grid(row=1, column=1)

    tk.Label(frame, text=" 选择样式：", bg="#f9f9f9", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=(15, 0))
    style_menu = ttk.Combobox(frame, values=get_style_list(), textvariable=selected_style, state="readonly", width=47)
    style_menu.grid(row=3, column=0, padx=5, pady=2)
    tk.Label(frame, text="样式来自 YS 文件夹", bg="#f9f9f9", fg="gray").grid(row=3, column=1, columnspan=2, sticky="w")

    tk.Label(frame, text=" 输出 PDF 路径：", bg="#f9f9f9", font=("Arial", 12)).grid(row=4, column=0, sticky="w", pady=(15, 0))
    tk.Entry(frame, textvariable=output_pdf_path, width=50).grid(row=5, column=0, padx=5, pady=2)
    tk.Button(frame, text="保存到...", command=browse_output, width=10, bg="#ffe0d0").grid(row=5, column=1)

    tk.Button(frame, text="🚀 开始转换", command=do_convert, width=30, height=2, bg="#4CAF50", fg="white",
              font=("Arial", 12, "bold")).grid(row=6, column=0, columnspan=2, pady=25)

    root.mainloop()

if __name__ == "__main__":
    main()
