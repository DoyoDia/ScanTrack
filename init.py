import csv
import os
from barcode import Code128
from barcode.writer import ImageWriter
from PIL import Image, ImageDraw, ImageFont

def generate_barcodes(names_file, output_dir):
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    csv_file_path = os.path.join(output_dir, "barcode_data.csv")

    with open(names_file, 'r') as names_file, open(csv_file_path, 'w', newline='') as csv_file:
        names = [line.strip() for line in names_file if line.strip()]
        writer = csv.writer(csv_file)
        writer.writerow(["Name", "ID"])

        for index, name in enumerate(names, 1):
            unique_id = f"{index:03d}"
            # barcode_obj = Code128(unique_id, writer=ImageWriter())
            # barcode_file = os.path.join(output_dir, f"{unique_id}.png")
            # # 在条形码上添加名字和 ID
            # options = {
            #     'text': f'{name}\nID: {unique_id}',
            #     'font_size': 10,
            #     'text_distance': 2
            # }
            # barcode_obj.save(barcode_file, options)
            # writer.writerow([name, unique_id])
            generate_barcode_with_text(name, unique_id, output_dir)

    return csv_file_path

def generate_barcode_with_text(name, unique_id, output_dir):
    # 生成条形码，关闭自带的文本输出
    barcode_obj = Code128(unique_id, writer=ImageWriter())
    barcode_options = {'write_text': False,'quiet_zone': 1,}
    barcode_image = barcode_obj.render(writer_options=barcode_options)

    # 加载字体
    font = ImageFont.truetype(font_path, 24)
    # 创建 ImageDraw 对象
    draw = ImageDraw.Draw(barcode_image)
    # 计算文本尺寸
    text = f"{name} ID: {unique_id}"
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]

    # 确定文本和条形码在合成图像中的位置
    image_width = barcode_image.width
    text_x = (image_width - text_width) / 2
    text_y = 10  # 文本在顶部留出的空间

    # 调整条形码图像的高度
    barcode_image = barcode_image.crop((0, text_height + 20, image_width, barcode_image.height))

    # 创建新图像用于合成文本和条形码
    combined_image_height = text_y + text_height + 10 + barcode_image.height
    combined_image = Image.new('RGB', (image_width, combined_image_height), 'white')

    # 将文本和条形码绘制到新图像上
    combined_image.paste(barcode_image, (0, text_y + text_height + 10))
    draw = ImageDraw.Draw(combined_image)
    draw.text((text_x, text_y), text, fill="black", font=font)

    # 保存图片
    barcode_file = os.path.join(output_dir, f"{unique_id}.png")
    combined_image.save(barcode_file)

    return barcode_file

font_path = "SourceHanSansSC-VF.otf"
names_file = 'names.txt'  # 这里填入你的名单文件路径
output_dir = 'init'     # 这里填入你想要保存条形码图片和 CSV 文件的目录路径

# 调用函数生成条形码
generate_barcodes(names_file, output_dir)
