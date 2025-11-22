import timg


def show_image():
    obj = timg.Renderer()
    obj.load_image_from_file('gerry.png')
    obj.resize(100, 40)
    obj.render(timg.Ansi24HblockMethod)
