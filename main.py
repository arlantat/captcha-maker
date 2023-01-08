from PIL import Image, ImageDraw, ImageFont
import random
from os import listdir
from os.path import isfile, join

TEXT_LENGTH = 6  # captcha text length

# create a blank image with a random white-to-gray background parameter
width, height = 200, 50
gray_shade = random.randint(235, 255)
image = Image.new("RGBA", (width, height), (gray_shade, gray_shade, gray_shade, 255))

# create a draw object to draw on the image
draw = ImageDraw.Draw(image)

# choose a random font. the files variable should be in the form of
# ['A.ttf', 'B.ttf']
files = [f for f in listdir('fonts') if isfile(join('fonts', f))]
font_path = f"fonts/{random.choice(files)}"  # change the path as desired
font_size = 24
font = ImageFont.truetype(font_path, font_size)

# generate a random string of letters and digits
characters = "abcdefghijklmnopqrstuvwxyz0123456789"
captcha_text = "".join(random.choices(characters, k=TEXT_LENGTH))

# for each char create an image instance to cover it, transform the image,
# then place the char image into the final captcha image
char_im_size = 35  
next_x = 10
next_y = (height - char_im_size) // 2
for char in captcha_text:
    char_im = Image.new('RGBA', (char_im_size,char_im_size), (255,255,255,0))  # RGBA for transparent background
    char_draw = ImageDraw.Draw(char_im)
    char_bbox = char_draw.textbbox((0,0), char, font)
    char_width, char_height = char_bbox[2], char_bbox[3]
    # center each char in their own original image
    x = (char_im_size - char_width) // 2
    y = (char_im_size - char_height) // 2
    char_draw.text((x,y), char, fill= "black", font=font)
    rand_rot = random.randint(-30,30)  # random rotation from -30 to 30 degree
    # rotate and place the char into its position in the captcha image
    image.paste(char_im.rotate(rand_rot), (next_x, next_y), char_im.rotate(rand_rot))
    next_x += random.randint(18,30)  # random distance from this to next char

# draw random points for noises
for _ in range(800):
    draw.point((random.randint(0,200),random.randint(0,50)), fill = "black")

# save the image
image.save("captcha.png")