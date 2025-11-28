import timg


def show_image():
    obj = timg.Renderer()
    obj.load_image_from_file('gerry.png')
    obj.resize(155, 95)
    obj.render(timg.Ansi24HblockMethod)
