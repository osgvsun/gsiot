# -*- coding:utf-8 -*-
import os,sys,numbers,time,numpy as np
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
from PIL import Image,ImageDraw,ImageFont

path = sys.path[0]
sys.path.append(path + "/../../..")
from lib import *
from lib.iot.gsdisplay import device

# Constants for interacting with display registers.
ILI9341_TFTWIDTH    = 240
ILI9341_TFTHEIGHT   = 320

ILI9341_NOP         = 0x00
ILI9341_SWRESET     = 0x01
ILI9341_RDDID       = 0x04
ILI9341_RDDST       = 0x09

ILI9341_SLPIN       = 0x10
ILI9341_SLPOUT      = 0x11
ILI9341_PTLON       = 0x12
ILI9341_NORON       = 0x13

ILI9341_RDMODE      = 0x0A
ILI9341_RDMADCTL    = 0x0B
ILI9341_RDPIXFMT    = 0x0C
ILI9341_RDIMGFMT    = 0x0A
ILI9341_RDSELFDIAG  = 0x0F

ILI9341_INVOFF      = 0x20
ILI9341_INVON       = 0x21
ILI9341_GAMMASET    = 0x26
ILI9341_DISPOFF     = 0x28
ILI9341_DISPON      = 0x29

ILI9341_CASET       = 0x2A
ILI9341_PASET       = 0x2B
ILI9341_RAMWR       = 0x2C
ILI9341_RAMRD       = 0x2E

ILI9341_PTLAR       = 0x30
ILI9341_MADCTL      = 0x36
ILI9341_PIXFMT      = 0x3A

ILI9341_FRMCTR1     = 0xB1
ILI9341_FRMCTR2     = 0xB2
ILI9341_FRMCTR3     = 0xB3
ILI9341_INVCTR      = 0xB4
ILI9341_DFUNCTR     = 0xB6

ILI9341_PWCTR1      = 0xC0
ILI9341_PWCTR2      = 0xC1
ILI9341_PWCTR3      = 0xC2
ILI9341_PWCTR4      = 0xC3
ILI9341_PWCTR5      = 0xC4
ILI9341_VMCTR1      = 0xC5
ILI9341_VMCTR2      = 0xC7

ILI9341_RDID1       = 0xDA
ILI9341_RDID2       = 0xDB
ILI9341_RDID3       = 0xDC
ILI9341_RDID4       = 0xDD

ILI9341_GMCTRP1     = 0xE0
ILI9341_GMCTRN1     = 0xE1

ILI9341_PWCTR6      = 0xFC

ILI9341_BLACK       = 0x0000
ILI9341_BLUE        = 0x001F
ILI9341_RED         = 0xF800
ILI9341_GREEN       = 0x07E0
ILI9341_CYAN        = 0x07FF
ILI9341_MAGENTA     = 0xF81F
ILI9341_YELLOW      = 0xFFE0
ILI9341_WHITE       = 0xFFFF


def color565(r, g, b):return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
def image_to_data(image):
    pb = np.array(image.convert('RGB')).astype('uint16')
    color = ((pb[:,:,0] & 0xF8) << 8) | ((pb[:,:,1] & 0xFC) << 3) | (pb[:,:,2] >> 3)
    return np.dstack(((color >> 8) & 0xFF, color & 0xFF)).flatten().tolist()
class container(device):
    def __init__(self, **argv):
        device.__init__(self,**argv)

        self._dc =argv["dc"]
        self._rst=None
        if ("rst" in argv):self._rst=argv["rst"]

        port=0
        if ("port" in argv):port=argv["port"]
        spi_device=0
        if ("device" in argv):spi_device=argv["device"]
        self._spi = SPI.SpiDev(port, spi_device, max_speed_hz=64000000)
        self._gpio=None
        if ("gpio" in argv):self._gpio=argv["gpio"]
        if self._gpio is None:self._gpio = GPIO.get_platform_gpio()
        self._gpio.setup(self._dc, GPIO.OUT)
        if self._rst is not None:
            self._gpio.setup(self._rst, GPIO.OUT)
        # 设置spi的模式为0.
        self._spi.set_mode(0)
        self._spi.set_bit_order(SPI.MSBFIRST)
        self._spi.set_clock_hz(64000000)
        self.font=ImageFont.truetype(path+"/font/simhei.ttf", 16)
    def send(self, data, is_data=True, chunk_size=4096):
        self._gpio.output(self._dc, is_data)
        if isinstance(data, numbers.Number):
            data = [data & 0xFF]
        # Write data a chunk at a time.
        for start in range(0, len(data), chunk_size):
            end = min(start+chunk_size, len(data))
            self._spi.write(data[start:end])
    def command(self, data):self.send(data, False)
    def data(self, data):self.send(data, True)
    def reset(self):
        if self._rst is not None:
            self._gpio.set_high(self._rst)
            time.sleep(0.005)
            self._gpio.set_low(self._rst)
            time.sleep(0.02)
            self._gpio.set_high(self._rst)
            time.sleep(0.150)
    def _init(self):
        self.command(0xEF)
        self.data(0x03)
        self.data(0x80)
        self.data(0x02)
        self.command(0xCF)
        self.data(0x00)
        self.data(0XC1)
        self.data(0X30)
        self.command(0xED)
        self.data(0x64)
        self.data(0x03)
        self.data(0X12)
        self.data(0X81)
        self.command(0xE8)
        self.data(0x85)
        self.data(0x00)
        self.data(0x78)
        self.command(0xCB)
        self.data(0x39)
        self.data(0x2C)
        self.data(0x00)
        self.data(0x34)
        self.data(0x02)
        self.command(0xF7)
        self.data(0x20)
        self.command(0xEA)
        self.data(0x00)
        self.data(0x00)
        self.command(ILI9341_PWCTR1)    # Power control
        self.data(0x23)                    # VRH[5:0]
        self.command(ILI9341_PWCTR2)    # Power control
        self.data(0x10)                    # SAP[2:0];BT[3:0]
        self.command(ILI9341_VMCTR1)    # VCM control
        self.data(0x3e)
        self.data(0x28)
        self.command(ILI9341_VMCTR2)    # VCM control2
        self.data(0x86)                    # --
        self.command(ILI9341_MADCTL)    #  Memory Access Control
        self.data(0x48)
        self.command(ILI9341_PIXFMT)
        self.data(0x55)
        self.command(ILI9341_FRMCTR1)
        self.data(0x00)
        self.data(0x18)
        self.command(ILI9341_DFUNCTR)    #  Display Function Control
        self.data(0x08)
        self.data(0x82)
        self.data(0x27)
        self.command(0xF2)                #  3Gamma Function Disable
        self.data(0x00)
        self.command(ILI9341_GAMMASET)    # Gamma curve selected
        self.data(0x01)
        self.command(ILI9341_GMCTRP1)    # Set Gamma
        self.data(0x0F)
        self.data(0x31)
        self.data(0x2B)
        self.data(0x0C)
        self.data(0x0E)
        self.data(0x08)
        self.data(0x4E)
        self.data(0xF1)
        self.data(0x37)
        self.data(0x07)
        self.data(0x10)
        self.data(0x03)
        self.data(0x0E)
        self.data(0x09)
        self.data(0x00)
        self.command(ILI9341_GMCTRN1)    # Set Gamma
        self.data(0x00)
        self.data(0x0E)
        self.data(0x14)
        self.data(0x03)
        self.data(0x11)
        self.data(0x07)
        self.data(0x31)
        self.data(0xC1)
        self.data(0x48)
        self.data(0x08)
        self.data(0x0F)
        self.data(0x0C)
        self.data(0x31)
        self.data(0x36)
        self.data(0x0F)
        self.command(ILI9341_SLPOUT)    # Exit Sleep
        time.sleep(0.120)
        self.command(ILI9341_DISPON)    # Display on
    def begin(self):
        self.reset()
        self._init()
    def set_window(self, x0=None, y0=None, x1=None, y1=None):
        if x0 is None:x0 = self.width-1
        if y0 is None:y0 = self.height-1
        if x1 is None:x1 = self.width-1
        if y1 is None:y1 = self.height-1
        self.command(ILI9341_CASET)        # Column addr set
        self.data(x0 >> 8)
        self.data(x0)                    # XSTART
        self.data(x1 >> 8)
        self.data(x1)                    # XEND
        self.command(ILI9341_PASET)        # Row addr set
        self.data(y0 >> 8)
        self.data(y0)                    # YSTART
        self.data(y1 >> 8)
        self.data(y1)                    # YEND
        self.command(ILI9341_RAMWR)        # write to RAM
    def disp3(self, image=None):
        if image is None:image = self.buffer
        self.set_window(x0=120, y0=198, x1=239, y1=319)
        pixelbytes = list(image_to_data(image))
        self.data(pixelbytes)
    def dispimg(self, image=None):
        """Write the display buffer or provided image to the hardware.  If no
        image parameter is provided the display buffer will be written to the
        hardware.  If an image is provided, it should be RGB format and the
        same dimensions as the display hardware.
        """
        # By default write the internal buffer to the display.
        if image is None:
            image = self.buffer
        # Set address bounds to entire display.
        self.set_window(x0=0, y0=199, x1=119, y1=319)
        # Convert image to array of 16bit 565 RGB data bytes.
        # Unfortunate that this copy has to occur, but the SPI byte writing
        # function needs to take an array of bytes and PIL doesn't natively
        # store images in 16-bit 565 RGB format.
        pixelbytes = list(image_to_data(image))
        # Write data to hardware.
        self.data(pixelbytes)
    def disp(self, image=None):
        if image is None:image = self.buffer
        self.set_window(x0=0, y0=0, x1=239, y1=198)
        self.data(list(image_to_data(image)))
    def display(self, image=None):
        if image is None:image = self.buffer
        self.set_window(x0=0, y0=0, x1=239, y1=319)
        self.data(list(image_to_data(image)))
        time.sleep(0.1)
    def clear(self, color=(0,0,0)):
        width, height = self.buffer.size
        self.buffer.putdata([color]*(width*height))
    def clearall(self, color=(0,0,0)):
        width, height = 240,320
        self.buffer.putdata([color]*(240*320))
    def draw(self):return ImageDraw.Draw(self.buffer)
    def start(self):pass
if __name__=="__main__":
    dev=container(dc=4,rst=25,angle=270,expend=1)
    dev.begin()
    dev.loadfont(fontname=16,font=ImageFont.truetype(path+"/font/simhei.ttf", 16))
    dev.loadfont(fontname=32,font=ImageFont.truetype(path+"/font/simhei.ttf", 32))
    while True:
            data=['如果安装失败，根据提示先把缺失','的包（比如openjpeg）装上']
            
            for i in range(0,len(data)):
                o=dev.getunit()
                o.type="image"
                o.left=0
                o.top=i*16
                o.font=dev.font
                o.text=data[i]#str(i).rjust(2,"0")+":"
                o.value=dev.getimagefromtext(o)
                dev.layers.append(o)
            dev.show()
            time.sleep(1)
            # break
    dev.start()