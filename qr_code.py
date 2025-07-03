import qrcode

def generate_qrcode(text='test'):
    img = qrcode.make(text)
    img.show()