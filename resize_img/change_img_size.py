from PIL import Image


def change_size(path):
    pic = Image.open(path)
    pic = pic.resize((220, 220))
    return pic


if __name__ == '__main__':
    path = './img/img1.jpg'
    f = open(path, 'r')
    g = open('./img/img2.jpg', 'a+')
    r = change_size(path)
    r.save('./img/img2.jpg')
