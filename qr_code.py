import re

class Qrcode():
    def make_qr(self, text):
        m = re.findall(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+', text)
        return "https://milk0824.sakura.ne.jp/linebot/mid/sample.php?data=" + m[0]