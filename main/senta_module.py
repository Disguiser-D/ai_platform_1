from senta import Senta

my_senta_ch = Senta()
my_senta_en = Senta()

use_cuda = False

my_senta_ch.init_model(model_class="ernie_1.0_skep_large_ch", task="sentiment_classify", use_cuda=use_cuda)
my_senta_en.init_model(model_class="ernie_2.0_skep_large_en", task="sentiment_classify", use_cuda=use_cuda)


def senta_ch_text(text):
    return my_senta_ch.predict(text)


def senta_ch_text_list(texts):
    res = []
    for i in texts:
        res.append(my_senta_ch.predict(i))
    return res


def senta_en_text(text):
    return my_senta_en.predict(text)


def senta_en_text_list(texts):
    res = []
    for i in texts:
        res.append(my_senta_en.predict(i))
    return res
