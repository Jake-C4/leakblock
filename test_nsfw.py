# test_nsfw.py
from PIL import Image
from core import nsfw_detector

img = Image.open("nsfw_sample.jpg")
result = nsfw_detector.is_nsfw(img)
print("NSFW detected?" , result)
