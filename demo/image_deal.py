from PIL import Image
basewidth = 90
baseheight = 90
img = Image.open('zrd.jpg')
wpercent = (basewidth / float(img.size[0]))
hsize = int((float(img.size[1]) * float(wpercent)))
hpercent = (baseheight / float(img.size[1]))
wsize = int((float(img.size[0]) * float(hpercent)))
img = img.resize((wsize, hsize), Image.LANCZOS)
img.save('resized_image.jpg')