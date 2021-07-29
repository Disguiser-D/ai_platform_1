import jieba
import jieba.posseg as pseg
import jieba.analyse as analyse
import codecs

jieba.initialize()


def multiple(num):
    jieba.enable_parallel(num)


def fenci(text, option):
    if option == "streamline":
        return "/".join(jieba.lcut(text))
    elif option == "full_mode":
        return "/".join(jieba.lcut(text, cut_all=True))
    elif option == "search_engines":
        return "/".join(jieba.lcut_for_search(text))
    else:
        return None


def fenci_list(text_list, option):
    if text_list == []:
        if option == "streamline":
            res.append("/".join(jieba.lcut(i)))
        elif option == "full_mode":
            res.append("/".join(jieba.lcut(i, cut_all=True)))
        elif option == "search_engines":
            res.append("/".join(jieba.lcut_for_search(i)))
        else:
            return None
    res = []
    for i in text_list:
        if option == "streamline":
            res.append("/".join(jieba.lcut(i)))
        elif option == "full_mode":
            res.append("/".join(jieba.lcut(i, cut_all=True)))
        elif option == "search_engines":
            res.append("/".join(jieba.lcut_for_search(i)))
        else:
            return None
    return res


def extract_keys_textrank_str(text_input, topK_input, allowPOS_input=('ns', 'n', 'v', 'w'), withWeight_input=False):
    res = {}
    try:
        if withWeight_input == False:
            for x in analyse.textrank(text_input, topK=topK_input, allowPOS=allowPOS_input,
                                      withWeight=withWeight_input):
                res[x] = None
        else:
            for x, w in analyse.textrank(text_input, topK=topK_input, allowPOS=allowPOS_input,
                                         withWeight=withWeight_input):
                res[x] = w
    except ValueError:
        return None
    return res


def extract_keys_textrank_list(text_input, topK_input, allowPOS_input=('ns', 'n', 'v', 'w'), withWeight_input=False):
    res = []
    for i in text_input:
        try:
            dict_tmp = {}
            if withWeight_input == False:
                for x in analyse.textrank(i, topK=topK_input, allowPOS=allowPOS_input, withWeight=withWeight_input):
                    dict_tmp[x] = None
            else:
                for x, w in analyse.textrank(i, topK=topK_input, allowPOS=allowPOS_input, withWeight=withWeight_input):
                    dict_tmp[x] = w
            res.append(dict_tmp)
        except ValueError:
            return None
    return res


def extract_keys_tf_idf_str(text_input, topK_input, allowPOS_input, withWeight_input=False):
    res = {}
    try:
        if withWeight_input == False and allowPOS_input != ():
            for x in analyse.extract_tags(text_input, topK=topK_input, allowPOS=allowPOS_input,
                                          withWeight=withWeight_input):
                res[x] = None
        elif withWeight_input == False and allowPOS_input == ():
            for x in analyse.extract_tags(text_input, topK=topK_input, withWeight=withWeight_input):
                res[x] = None
        elif withWeight_input == True and allowPOS_input == ():
            for x, w in analyse.extract_tags(text_input, topK=topK_input, withWeight=withWeight_input):
                res[x] = w
        else:
            for x, w in analyse.extract_tags(text_input, topK=topK_input, allowPOS=allowPOS_input,
                                             withWeight=withWeight_input):
                res[x] = w
    except ValueError:
        return None
    return res


def extract_keys_tf_idf_list(text_input, topK_input, allowPOS_input, withWeight_input=False):
    res = []
    for i in text_input:
        try:
            dict_tmp = {}
            if withWeight_input == False and allowPOS_input != ():
                for x in analyse.extract_tags(i, topK=topK_input, allowPOS=allowPOS_input,
                                              withWeight=withWeight_input):
                    dict_tmp[x] = None
            elif withWeight_input == False and allowPOS_input == ():
                for x in analyse.extract_tags(i, topK=topK_input, withWeight=withWeight_input):
                    dict_tmp[x] = None
            elif withWeight_input == True and allowPOS_input == ():
                for x, w in analyse.extract_tags(i, topK=topK_input, withWeight=withWeight_input):
                    dict_tmp[x] = w
            else:
                for x, w in analyse.extract_tags(i, topK=topK_input, allowPOS=allowPOS_input,
                                                 withWeight=withWeight_input):
                    dict_tmp[x] = w
            res.append(dict_tmp)
        except ValueError:
            return None
    return res


def separately_text(text):
    res = {}
    for word, flag in pseg.cut(text):
        res[word] = flag
    return res


def separately_text_list(text):
    res = []
    for i in text:
        dict_tmp = {}
        for word, flag in pseg.cut(i):
            dict_tmp[word] = flag
        res.append(dict_tmp)
    return res
