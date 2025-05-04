'''
请帮我写一个 python 脚本,用于对md文件中的图片文件的路径进行修改，主要实现的功能步骤如下:
1. 获取该md文件的文件名
2. 扫描所有图片资源路径，获取原来的图片资源文件夹的路径
3. 扫描md文件中的所有的图片文件路径，将所有的图片文件路径替换为 "md文件的文件名(没有后缀名).assets/图片文件名"。
4. 将原来的图片资源文件夹重命名为"md文件的文件名(没有后缀名).assets"
注意，所有的操作均在solve文件夹下操作，也就是说，限定操作的文件夹只有该python问价目录下的solve文件夹
'''

import os
import re
import shutil
from pathlib import Path

def get_md_files(solve_dir):
    """获取solve目录下的所有md文件"""
    return list(Path(solve_dir).glob("*.md"))

def get_image_folder(md_file):
    """获取与md文件关联的图片资源文件夹"""
    md_dir = md_file.parent
    # 查找第一个包含图片的文件夹
    for item in md_dir.iterdir():
        if item.is_dir():
            # 检查是否包含常见图片格式
            if any(item.glob('*.png')) or any(item.glob('*.jpg')) or any(item.glob('*.jpeg')) or any(item.glob('*.gif')):
                return item  # 找到第一个包含图片的文件夹就返回
    return None

def update_image_paths(md_file, old_folder, new_folder):
    """更新md文件中的图片路径"""
    with open(md_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 匹配 Markdown 和 HTML 格式的图片
    md_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    html_pattern = r'<img[^>]*src=["\'](.*?)["\'][^>]*>'
    
    def replace_md_path(match):
        alt_text = match.group(1)
        old_path = match.group(2)
        img_name = os.path.basename(old_path.replace('\\', '/'))
        new_path = f"{new_folder.name}/{img_name}"
        return f"![{alt_text}]({new_path})"
    
    def replace_html_path(match):
        full_tag = match.group(0)
        old_path = match.group(1)
        img_name = os.path.basename(old_path.replace('\\', '/'))
        new_path = f"{new_folder.name}/{img_name}"
        return full_tag.replace(old_path, new_path)
    
    # 先处理 Markdown 格式
    content = re.sub(md_pattern, replace_md_path, content)
    # 再处理 HTML 格式
    content = re.sub(html_pattern, replace_html_path, content)
    
    # 写入更新后的内容
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"已更新文件 {md_file.name} 中的图片路径")

def main():
    # 获取当前脚本所在目录下的solve文件夹
    solve_dir = Path(__file__).parent / 'solve'
    if not solve_dir.exists():
        print(f"错误：solve文件夹不存在于 {solve_dir}")
        return

    # 处理每个md文件
    for md_file in get_md_files(solve_dir):
        print(f"处理文件：{md_file.name}")
        
        # 获取不带后缀的文件名
        md_name = md_file.stem.strip()  # 移除可能存在的空格
        
        # 查找关联的图片文件夹
        old_img_folder = get_image_folder(md_file)
        if not old_img_folder:
            print(f"警告：未找到与 {md_file.name} 关联的图片文件夹")
            continue
            
        # 构建新的文件夹名（确保没有空格）
        new_folder_name = f"{md_name}.assets"
        new_img_folder = old_img_folder.parent / new_folder_name
        
        # 更新md文件中的图片路径
        update_image_paths(md_file, old_img_folder, new_img_folder)
        
        # 重命名图片文件夹
        if old_img_folder.name != new_folder_name:
            try:
                # 如果目标文件夹已存在，先删除
                if new_img_folder.exists():
                    shutil.rmtree(new_img_folder)
                old_img_folder.rename(new_img_folder)
                print(f"已将图片文件夹重命名为：{new_folder_name}")
            except Exception as e:
                print(f"重命名文件夹时出错：{e}")

if __name__ == "__main__":
    main()