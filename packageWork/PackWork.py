import os
import shutil
from pathlib import Path
import zipfile

# 配置变量
CONFIG = {
    'source_dir': 'solve',      # 源文件夹，存放markdown文件的目录
    'output_dir': 'packages',   # 输出文件夹，存放打包后的zip文件
}

def pack_markdown_with_assets(markdown_file):
    """
    打包单个markdown文件及其资源
    :param markdown_file: markdown文件的完整路径
    """
    try:
        # 获取markdown文件名（不含扩展名）和所在目录
        md_name = os.path.splitext(os.path.basename(markdown_file))[0]
        md_dir = os.path.dirname(markdown_file)
        
        # 构建输出目录和zip文件路径
        output_dir = os.path.join(CONFIG['output_dir'])
        os.makedirs(output_dir, exist_ok=True)
        zip_path = os.path.join(output_dir, f"{md_name}.zip")
        
        # 创建zip文件
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 添加markdown文件
            zipf.write(markdown_file, os.path.basename(markdown_file))
            
            # 检查并添加assets文件夹
            assets_dir = os.path.join(md_dir, f"{md_name}.assets")
            if os.path.exists(assets_dir):
                for root, _, files in os.walk(assets_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # 将文件添加到zip中，保持assets目录结构
                        arcname = os.path.join(
                            f"{md_name}.assets",
                            os.path.relpath(file_path, assets_dir)
                        )
                        zipf.write(file_path, arcname)
        
        print(f"已完成打包：{zip_path}")
        return True
    
    except Exception as e:
        print(f"打包 {markdown_file} 时出错：{str(e)}")
        return False

def main():
    """主函数"""
    # 确保输出目录存在
    os.makedirs(CONFIG['output_dir'], exist_ok=True)
    
    # 获取所有markdown文件
    success_count = 0
    fail_count = 0
    
    for root, _, files in os.walk(CONFIG['source_dir']):
        for file in files:
            if file.endswith('.md'):
                markdown_path = os.path.join(root, file)
                print(f"\n正在处理：{markdown_path}")
                
                if pack_markdown_with_assets(markdown_path):
                    success_count += 1
                else:
                    fail_count += 1
    
    print(f"\n打包完成！")
    print(f"成功：{success_count} 个文件")
    print(f"失败：{fail_count} 个文件")
    print(f"打包文件保存在：{os.path.abspath(CONFIG['output_dir'])}")

if __name__ == '__main__':
    main() 