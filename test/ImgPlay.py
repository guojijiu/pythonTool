# python下的图像处理库
from PIL import Image, ImageSequence
# 系统模块
import os

# 用于读取gif动图
im = Image.open("D:/img/timg.gif")

# 保存的路径
savePath = im.filename.replace(".%s" % (im.format).lower(), "")

# 保存的文件名
pathName = savePath.split('/')[-1]

# 保存的目录
saveDir = savePath.replace(pathName, "")

# gif图片流的迭代器
iter = ImageSequence.Iterator(im)

index = 1

for frame in iter:
    # 每一帧图片
    print("image %d: mode %s, size %s,%s" % (index, frame.mode, frame.size, savePath))

    if pathName not in os.listdir(saveDir):
        os.makedirs(savePath)

    # 将每一帧图片保存到imgs文件夹下
    frame.save("%s/frame_%d.png" % (savePath, index))
    index += 1

# 将gif拆分成图片流
imgs = [frame.copy() for frame in ImageSequence.Iterator(im)]

# 输出原图
# imgs[0].save("./out.gif", save_all=True, append_images=imgs[1:])

# 将图片流反序
imgs.reverse()

# 将反序后的图片流保存并输出
imgs[0].save("%s/reverse_out.gif" % (savePath), save_all=True, append_images=imgs[1:])
