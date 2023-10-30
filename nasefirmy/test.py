import os

images = []
for filename in os.listdir('nasefirmy/static/image/loga/'):
    if filename.endswith(".jpg"):
        images.append(os.path.join('../static/image/loga/', filename))
    else:
        continue
print(images)