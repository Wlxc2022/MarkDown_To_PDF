from pathlib import Path
import markdown
import pdfkit
import os

def convert_md_to_pdf(md_file: Path, css_text: str, output_folder: Path):
    md_text = md_file.read_text(encoding="utf-8")
    html = f"<style>{css_text}</style>" + markdown.markdown(md_text, extensions=["tables", "fenced_code"])

    output_pdf = output_folder / (md_file.stem + ".pdf")

    options = {
        'encoding': "UTF-8",
        'page-size': 'A4',
        'margin-top': '20mm',
        'margin-bottom': '20mm',
        'footer-right': '[page]/[topage]',
        'footer-font-size': '10',
    }

    pdfkit.from_string(html, str(output_pdf), options=options)
    print(f"✅ 成功生成: {output_pdf.name}")

def batch_convert_md_folder(md_folder: str, style_name: str, output_folder: str):
    md_path = Path(md_folder)
    out_path = Path(output_folder)
    css_file = Path("YS") / f"{style_name}.css"  # 使用样式名构造路径

    if not css_file.exists():
        print(f"❌ 样式文件未找到: {css_file}")
        return

    css_text = css_file.read_text(encoding="utf-8")

    if not out_path.exists():
        out_path.mkdir(parents=True)

    md_files = list(md_path.glob("*.md"))
    if not md_files:
        print("⚠️ 当前目录中没有找到 .md 文件")
        return

    for md_file in md_files:
        convert_md_to_pdf(md_file, css_text, out_path)

# 🚀 启动：选择样式（YS1、YS2...）
if __name__ == "__main__":
    import sys

    # 可以从命令行传样式名，也可以写死
    if len(sys.argv) < 2:
        style = input("请输入样式名（如 YS1、YS2）：").strip()
    else:
        style = sys.argv[1]

    batch_convert_md_folder(
        md_folder=".",
        style_name=style,
        output_folder="pdfs"
    )
