# -*- coding: utf-8 -*-
import Adafruit_GPIO.SPI as SPI
from PIL import Image,ImageFont,ImageDraw
from gsiot.v3.file.gsdisplay.ili9341 import ILI9341
import qrcode

size = 4
boxsize = 10
boxborder = 2

def make_logo_qr_file(str,log,save):make_logo_qr(str,log).save(save)
def make_qr_file(str, save):make_qr(str).save(save)
def make_qr(str):
    qr = qrcode.QRCode(
        version=size,  # 生成二维码尺寸的大小 1-40  1:21*21（21+(n-1)*4）
        error_correction=qrcode.constants.ERROR_CORRECT_M,  # L:7% M:15% Q:25% H:30%
        box_size=boxsize,  # 每个格子的像素大小
        border=boxborder  # 边框的格子宽度大小
    )
    qr.add_data(str)
    qr.make(fit=True)
    return  qr.make_image()
def make_logo_qr(str, logo):
    # 参数配置
    qr = qrcode.QRCode(
        version=size,  # 生成二维码尺寸的大小 1-40  1:21*21（21+(n-1)*4）
        error_correction=qrcode.constants.ERROR_CORRECT_Q,  # L:7% M:15% Q:25% H:30%
        box_size=boxsize,  # 每个格子的像素大小
        border=boxborder
    )

    # 添加转换内容
    qr.add_data(str)
    qr.make(fit=True)
    # 生成二维码
    img = qr.make_image()
    img = img.convert("RGBA")
    # 添加logo
    if logo and os.path.exists(logo):
        icon = Image.open(logo)
        # 获取二维码图片的大小
        img_w, img_h = img.size
        factor = 4
        size_w = int(img_w / factor)
        size_h = int(img_h / factor)
        # logo图片的大小不能超过二维码图片的1/4
        icon_w, icon_h = icon.size
        if icon_w > size_w:
            icon_w = size_w
        if icon_h > size_h:
            icon_h = size_h
        icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)

        # 详见：http://pillow.readthedocs.org/handbook/tutorial.html
        # 计算logo在二维码图中的位置
        w = int((img_w - icon_w) / 2)
        h = int((img_h - icon_h) / 2)
        icon = icon.convert("RGBA")
        img.paste(icon, (w, h), icon)
        # 详见：http://pillow.readthedocs.org/reference/Image.html#PIL.Image.Image.paste
    # 保存处理后图片
    return img