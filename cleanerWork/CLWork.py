import os
import re
import shutil
from pathlib import Path

def find_markdown_resources(markdown_file):
    """查找 Markdown 文件中的资源引用"""
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 匹配图片、视频和音频的正则表达式
    image_patterns = [
        r'!\[.*?\]\((.*?)\)',  # Markdown 图片语法
        r'<img.*?src=[\'\"](.*?)[\'\"].*?>'  # HTML 图片标签
    ]
    video_pattern = r'<video.*?src=[\'\"](.*?)[\'\"].*?>'
    audio_pattern = r'<audio.*?src=[\'\"](.*?)[\'\"].*?>'
    
    resources = []
    line_number = 1
    
    for line in content.split('\n'):
        # 查找所有图片资源
        for pattern in image_patterns:
            images = re.findall(pattern, line)
            for img in images:
                resources.append(('image', img, line_number))
        
        # 查找视频和音频资源
        videos = re.findall(video_pattern, line)
        audios = re.findall(audio_pattern, line)
        
        for video in videos:
            resources.append(('video', video, line_number))
        for audio in audios:
            resources.append(('audio', audio, line_number))
            
        line_number += 1
    
    return resources

def check_resources(markdown_file):
    """检查资源文件是否存在并处理缺失资源"""
    # 获取 markdown 文件名（不含扩展名）
    md_name = os.path.splitext(os.path.basename(markdown_file))[0]
    assets_dir = os.path.join('solve', f'{md_name}.assets')
    missing_file = os.path.join('solve', '缺失资源.txt')
    
    # 确保目录存在
    os.makedirs(os.path.dirname(missing_file), exist_ok=True)
    os.makedirs(assets_dir, exist_ok=True)
    
    # 获取所有引用的资源
    resources = find_markdown_resources(markdown_file)
    referenced_files = set()
    
    # 检查每个资源
    with open(missing_file, 'a', encoding='utf-8') as f:
        for res_type, res_path, line_num in resources:
            # 获取资源文件名
            filename = os.path.basename(res_path)
            asset_path = os.path.join(assets_dir, filename)
            referenced_files.add(filename)
            
            if not os.path.exists(asset_path):
                f.write(f"{markdown_file} - 第 {line_num} 行缺失{res_type}文件: {filename}\n")
    
    # 检查未引用的资源文件
    clean_dirs = {
        'image': os.path.join('solve', 'clean', 'images'),
        'video': os.path.join('solve', 'clean', 'videos'),
        'audio': os.path.join('solve', 'clean', 'audios')
    }
    
    # 创建清理目录
    for clean_dir in clean_dirs.values():
        os.makedirs(clean_dir, exist_ok=True)
    
    # 检查 assets 目录中的文件
    if os.path.exists(assets_dir):
        for file in os.listdir(assets_dir):
            if file not in referenced_files:
                file_path = os.path.join(assets_dir, file)
                # 根据文件扩展名判断类型
                ext = os.path.splitext(file)[1].lower()
                if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
                    dest_dir = clean_dirs['image']
                elif ext in ['.mp4', '.avi', '.mov']:
                    dest_dir = clean_dirs['video']
                elif ext in ['.mp3', '.wav', '.ogg']:
                    dest_dir = clean_dirs['audio']
                else:
                    continue
                
                # 移动文件
                shutil.move(file_path, os.path.join(dest_dir, file))

def main():
    """主函数"""
    solve_dir = 'solve'
    if not os.path.exists(solve_dir):
        os.makedirs(solve_dir)
        
    # 只查找 solve 目录下的所有 markdown 文件
    for root, dirs, files in os.walk(solve_dir):
        for file in files:
            if file.endswith('.md'):
                markdown_path = os.path.join(root, file)
                print(f"正在处理: {markdown_path}")
                check_resources(markdown_path)

if __name__ == '__main__':
    main() 