"""    
created by jetjinser
changed by BigOrangeQWQ
date: 2022-11-9
"""

from PIL import Image, ImageDraw, ImageFilter, ImageFont
import matplotlib.pyplot as plt
from PIL.ImageDraw import Draw
from pathlib import Path
from httpx import AsyncClient
import os

DATA = Path("./data/resource")
FONT1 = DATA / '王汉宗中隶书繁.ttf'
FONT2 = DATA / 'REEJI-HonghuangLiGB-SemiBold-2.ttf'
DEMO = DATA / 'demo.jpg'
FRAMEW = DATA / 'framework.png'


async def get_image(user_id: int) -> str:
    """QQ头像的获取

    Args:
        user_id (int): QQ ID

    Returns:
        str: path
    """
    async with AsyncClient() as client:
        r = await client.get(f'http://q1.qlogo.cn/g?b=qq&nk={str(user_id)}&s=5')
        with open(DEMO.as_posix(), 'wb') as f:
            chuck = f.write(r.content)
        return DEMO.as_posix()


class ImageProcessing:
    """
    签到图片的处理
    (高斯模糊)
    用于QQ机器人
    """

    def __init__(self, small_size: int = 256, name: str = 'rp', data: dict = {}):
        """
        初始化构图

        Args:
            small_size (int, optional): 小图标尺寸. Defaults to 256.
            name (str, optional): 处理后的图片名. Defaults to 'rp'.
            data (dict, optional): 文字数据. Defaults to {}.
        """
        self._small_size = small_size
        self._name: str = name
        self._image: Image.Image
        # Data by tes
        self._txt: str = data['txt']  # 文字
        self._text: str = data['text']  # Tips
        self.jrday: str = data['jrday']  # 累计签到天数
        self.user_id: int = data['user_id']  # QQ号

    async def gaussian_blur(self):
        """
        高斯模糊处理

        Returns:
            模糊后的图片
        """
        img = self._image.filter(ImageFilter.GaussianBlur(radius=7))
        return img

    async def circle(self):
        """
        alpha圆框
        用于处理小图标

        Returns:
            处理后的圆框
        """
        size = self._small_size
        circle = Image.new('L', (size, size), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, size, size), fill=255)

        return circle

    async def alpha_circle(self):
        """
        小图标的圆形处理

        Returns:
            处理后的RGBA图像
        """
        size = self._small_size
        img = self._image.copy()
        img = img.resize((size, size))
        img.putalpha(await self.circle())

        return img

    async def process(self):
        """
        合并处理图片
        创建文字框架
        写入文字信息
        嵌入图标框架

        Returns:
            处理后的图片
        """
        w = 640
        size = self._small_size

        # 创建白色画布
        target = Image.new('RGBA', (640, 640), (0, 0, 0, 0))
        # 贴上高斯模糊后的图片
        target.paste(await self.gaussian_blur())
        # 创建小图标的框架
        framework = Image.open(FRAMEW).convert('L')
        framework = framework.resize((size + 30, size + 30))
        target_l = Image.new('RGBA', (size + 30, size + 30), (0, 0, 0, 0))
        target_l.putalpha(framework)

        # 贴上小图标的框架
        target.paste(target_l,
                     (w // 2 - size // 2 - 15, w // 2 - size // 2 - 50 - 15),
                     target_l)

        # 在原图中间 y-50 的位置贴上小图标
        target.paste(await self.alpha_circle(),
                     (w // 2 - size // 2, w // 2 - size // 2 - 50),
                     await self.alpha_circle())

        # 创建文字框架
        txt_frame = Image.new('RGBA', (540, 160), (0, 0, 0, 140))
        # 贴上文字框架
        target.paste(txt_frame, (50, 425), txt_frame)

        # 累签文字
        draw = ImageDraw.Draw(target)
        font = ImageFont.truetype(FONT1.as_posix(), 24)
        draw.text((15, 15), f'> 累簽：{self.jrday}',
                  (150, 150, 150), font=font)  # type: ignore

        # 指定文字, 文字的字体和位置
        txt = self._txt.split('\n')
        font = ImageFont.truetype(FONT2.as_posix(), 24)
        pix = (255, 255, 255)
        count = 0
        for i in txt:
            text_size = font.getsize(i)
            where = (
                (self._image.size[0] - text_size[0]) / 2, (self._image.size[1] - text_size[1]) / 2 + 125 + 30 * count)  # type: ignore

            # 写入文字
            draw = ImageDraw.Draw(target)
            draw.text(where, i, pix, font=font)  # type: ignore

            count += 1

        values = self._text

        # 写入tips
        draw = ImageDraw.Draw(target)
        font = ImageFont.truetype(FONT2.as_posix(), 18)
        writer_size = font.getsize(values)
        pix = (230, 230, 230)
        draw.text(((self._image.size[0] - writer_size[0]) / 2, 585 - 26),
                  values.replace('\n', ''), pix, font=font)  # type: ignore

        return target

    async def save(self) -> Path | str:
        """
        保存图片
        """
        self.image_file = await get_image(self.user_id)

        _image = Image.open(self.image_file).convert('RGBA')
        if _image.size != (640, 640):
            _image = _image.resize((640, 640))

        self._image = _image
        output_img = await self.process()
        output_img.save(DATA / (self._name+'.png'))
        return DATA / (self._name+'.png')

    async def remove(self):
        os.remove(DATA / (self._name+'.png'))


class LuckImage():

    def __init__(self, lucklist: list, user_id: int, txt: str):
        """
        绘制近几日的人品波动图

        Args:
            lucklist (list): luckp points
            user_id (int): QQ id
            txt (str): tips
        """
        self._lucklist: list = lucklist
        self._user_id: int = user_id
        self._txt: str = txt
        self._name = 'LuckPoint'
        self._image: Image.Image

    async def gaussian_blur(self):
        """
        高斯模糊处理
        :return: 模糊后的图片
        """
        img = self._image.filter(
            ImageFilter.GaussianBlur(radius=7))  # type:ignore
        return img

    async def LuckDarw(self) -> str:
        """
        绘制走向图后保存

        Returns:
            str: path of image
        """
        plt.subplots()
        plt.xticks([1, 2, 3, 4, 5], ['1', '2', '3', '4', '5'])
        plt.plot([1, 2, 3, 4, 5], self._lucklist, color='orange',
                 linewidth=7.0, ms=7.0, marker='*')
        plt.tick_params(labelsize=15)
        plt.ylabel('Luck Point', fontdict={'weight': 'normal', 'size': 20})
        plt.title("Luck Changed (5 Days)", fontdict={
            'weight': 'normal', 'size': 20})
        plt.savefig(DATA / "luck.png", dpi=320, transparent=True)
        plt.close()

        return (DATA / "luck.png").as_posix()

    async def process(self):
        # 创建画板
        target = Image.new('RGBA', (640, 640), (0, 0, 0, 0))

        # 贴上高斯模糊
        target.paste(await self.gaussian_blur())

        # 绘制 LuckPoint走向图
        Darw = Image.open(await self.LuckDarw()).convert('RGBA')
        Darw = Darw.resize((450, 346))
        target.paste(Darw, (95, 87), Darw)

        # 创建文字框架
        txt_frame = Image.new('RGBA', (500, 100), (0, 0, 0, 140))
        # 贴上文字框架
        target.paste(txt_frame, (70, 460), txt_frame)

        txt = self._txt.split('\n')
        font = ImageFont.truetype(
            FONT2.as_posix(), 24)
        pix = (255, 255, 255)
        count = 0
        for i in txt:
            text_size = font.getsize(i)
            where = (
                (self._image.size[0] - text_size[0]) / 2, (self._image.size[1] - text_size[1]) / 2 + 158 + 30 * count)  # type:ignore

            # 写入文字
            draw = ImageDraw.Draw(target)
            draw.text(where, i, pix, font=font)  # type: ignore

            count += 1

        draw = ImageDraw.Draw(target)
        font = ImageFont.truetype(
            FONT2.as_posix(), 18)
        writer_size = font.getsize(str(self._lucklist))
        pix = (230, 230, 230)

        draw.text(((self._image.size[0] - writer_size[0]) / 2, 585 - 50),
                  str(self._lucklist), pix, font=font)  # type:ignore

        return target

    async def save(self):
        """
        保存图片
        """
        _image_path = await get_image(self._user_id)
        _image = Image.open(_image_path).convert('RGBA')

        if _image.size != (640, 640):
            _image = _image.resize((640, 640))

        self._image = _image
        output_img = await self.process()
        output_img.save(DATA / (self._name + '.png'))
        return

    async def remove(self):
        os.remove(DATA / (self._name + '.png'))
