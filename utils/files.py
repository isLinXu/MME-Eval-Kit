import base64

def save_image_to_base64(img_path):
    # 将图像转换为base64编码
    with open(img_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string