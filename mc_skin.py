import os
from PIL import Image, ImageOps

def convert_image(input_image_path, output_image_path):
    # 打开原始图像
    original = Image.open(input_image_path)
    
    # 设置输出图像的大小和透明背景
    result = Image.new('RGBA', (64, 64), (255, 255, 255, 0))

    # 将原始图像的上半部分粘贴到新图像的上半部分
    upper_half = original.crop((0, 0, 64, 32))
    result.paste(upper_half, (0, 0))
    
    # 定义要合成的图像片段的位置和大小
    crops = [
        (4, 16, 8, 20), (8, 16, 12, 20), (8, 20, 12, 32),
        (4, 20, 8, 32), (0, 20, 4, 32), (12, 20, 16, 32),
        (44, 16, 48, 20), (48, 16, 52, 20), (48, 20, 52, 32),
        (44, 20, 48, 32), (40, 20, 44, 32), (52, 20, 56, 32)
    ]
    
    # 定义每个片段在输出图像上的位置
    positions = [
        (20, 48), (24, 48), (16, 52), (20, 52), (24, 52), (28, 52),
        (36, 48), (40, 48), (32, 52), (36, 52), (40, 52), (44, 52)
    ]
    
    # 循环遍历每个片段，裁剪、翻转并合成到输出图像
    for i, crop in enumerate(crops):
        segment = original.crop(crop)
        segment = ImageOps.mirror(segment)
        result.paste(segment, positions[i], segment)
    
    # 保存转换后的图像
    result.save(output_image_path)

def batch_convert_images():
    # 获取脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 定义输入和输出目录
    input_dir = os.path.join(script_dir, "input")
    output_dir = os.path.join(script_dir, "output")
    
    # 如果输出文件夹不存在，则创建
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 获取input目录中的所有图片文件
    for file_name in os.listdir(input_dir):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_image_path = os.path.join(input_dir, file_name)
            output_image_name = f"{os.path.splitext(file_name)[0]}-converted.png"
            output_image_path = os.path.join(output_dir, output_image_name)
            convert_image(input_image_path, output_image_path)

# 执行批量转换
batch_convert_images()
