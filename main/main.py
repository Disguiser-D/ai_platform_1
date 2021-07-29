from typing import Optional, List
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import ByteSize
import os

import configparser
import base64

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cf = configparser.ConfigParser()
cf.read(os.path.join(BASE_DIR, 'config.ini'))
secs = cf.sections()

import logger

loger = logger.setup_log("mylog")

import dfa
import jieba_module as jiebam
import nsfw_module as nsfw
import find_log

import senta_module

if (cf.get("JIEBA", "parallel") == '1'):
    jiebam.multiple(int(cf.get("JIEBA", "thread")))

"""
dto引入
"""
import dto_dfa
import dto_fenci_str
import dto_fenci_list
import dto_extract_keys_str
import dto_extract_keys_list
import dto_separately
import dto_separately_list
import dto_senta
import dto_senta_list
import dto_nsfw_yahoo

app = FastAPI()

gfw0 = dfa.choose_filter(cf.get("DFA", "filter"), "keywords")
gfw1 = dfa.choose_filter(cf.get("DFA", "filter"), "keywords1")

"""
判断是否存在敏感词汇
"""


@app.post("/dfa/judge")
def read_root(dfa_dto: dto_dfa.Dfa):
    try:
        cut_text = jiebam.fenci(dfa_dto.text, cf.get("DFA", "dfa_cut"))
        res = gfw0.judge(cut_text)
    except Exception as ex:
        loger.error(ex)
        return {"result": False, "message": "发生异常错误"}
    try:
        return {"result": res, "message": "操作成功"}
    except Exception as ex:
        loger.error(ex)


"""
将文本中存在的敏感词汇换为*
"""


@app.post("/dfa/filter")
def read_root(dfa_dto: dto_dfa.Dfa):
    try:
        res = gfw1.filter(dfa_dto.text)
    except Exception as ex:
        loger.error(ex)
        return {"result": res, "message": "发生异常错误"}
    try:
        return {"result": res, "message": "操作成功"}
    except Exception as ex:
        loger.error(ex)


"""
将文本分词(单个字符串)
"""


@app.post("/fenci/text")
def fenci_str(fenci_dto: dto_fenci_str.DataFenciStr):
    try:
        res = jiebam.fenci(fenci_dto.text, fenci_dto.mode)
        if res == None:
            return {"result": "所选的模式不存在", "message": "发生异常错误"}
    except Exception as ex:
        loger.error(ex)
        return {"result": "False", "message": "发生异常错误"}
    try:
        return {"result": res, "message": "操作成功"}
    except Exception as ex:
        loger.error(ex)


"""
将文本分词(list)
"""


@app.post("/fenci/text_list")
def fenci_list(fenci_dto: dto_fenci_list.DataFenciList):
    try:
        res = jiebam.fenci_list(fenci_dto.text, fenci_dto.mode)
        if res == None:
            return {"result": "所选的模式不存在", "message": "发生异常错误"}
    except Exception as ex:
        loger.error(ex)
        return {"result": "False", "message": "发生异常错误"}
    try:
        return {"result": res, "message": "操作成功"}
    except Exception as ex:
        loger.error(ex)


"""
提取文本中的关键词(str) textrank算法
"""


@app.post("/extract_key/textrank/text")
def extract_keys_textrank_str(extract_dto: dto_extract_keys_str.DataExtractStr, allowPOS: Optional[List[str]] = None,
                              withWeight: Optional[bool] = None):
    try:
        if allowPOS == None and withWeight == None:
            res = jiebam.extract_keys_textrank_str(extract_dto.text, extract_dto.topK)
        elif allowPOS == None and withWeight != None:
            res = jiebam.extract_keys_textrank_str(extract_dto.text, extract_dto.topK, withWeight_input=withWeight)
        elif allowPOS != None and withWeight == None:
            res = jiebam.extract_keys_textrank_str(extract_dto.text, extract_dto.topK, allowPOS_input=tuple(allowPOS))
        else:
            res = jiebam.extract_keys_textrank_str(extract_dto.text, extract_dto.topK, tuple(allowPOS), withWeight)
        if res == None:
            return {"result": "输入的allowPOS数量太少，无法返回结果", "message": "操作失败"}
    except Exception as ex:
        loger.error(ex)
        return {"result": "False", "message": "发生异常错误"}
    try:
        return {"result": res, "message": "操作成功"}
    except Exception as ex:
        loger.error(ex)


"""
提取文本中的关键词(list) textrank算法
"""


@app.post("/extract_key/textrank/text_list")
def extract_keys_textrank_list(extract_dto: dto_extract_keys_list.DataExtractList, allowPOS: Optional[List[str]] = None,
                               withWeight: Optional[bool] = None):
    try:
        if allowPOS == None and withWeight == None:
            res = jiebam.extract_keys_textrank_list(extract_dto.text, extract_dto.topK)
        elif allowPOS == None and withWeight != None:
            res = jiebam.extract_keys_textrank_list(extract_dto.text, extract_dto.topK, withWeight_input=withWeight)
        elif allowPOS != None and withWeight == None:
            res = jiebam.extract_keys_textrank_list(extract_dto.text, extract_dto.topK, allowPOS_input=tuple(allowPOS))
        else:
            res = jiebam.extract_keys_textrank_list(extract_dto.text, extract_dto.topK, tuple(allowPOS), withWeight)
        if res == None:
            return {"result": "输入的allowPOS数量太少，无法返回结果", "message": "操作失败"}
    except Exception as ex:
        loger.error(ex)
        return {"result": "False", "message": "发生异常错误"}
    try:
        return {"result": res, "message": "操作成功"}
    except Exception as ex:
        loger.error(ex)


"""
提取文本中的关键词(str) TF-IDF算法
"""


@app.post("/extract_key/tf-idf/text")
def extract_keys_tf_idf_str(extract_dto: dto_extract_keys_str.DataExtractStr, allowPOS: Optional[List[str]] = None,
                            withWeight: Optional[bool] = None):
    try:
        if allowPOS == None:
            allowPOS = []
        if withWeight == None:
            res = jiebam.extract_keys_tf_idf_str(extract_dto.text, extract_dto.topK, tuple(allowPOS))
        else:
            res = jiebam.extract_keys_tf_idf_str(extract_dto.text, extract_dto.topK, tuple(allowPOS), withWeight)
        if res == None:
            return {"result": "输入的allowPOS数量太少，无法返回结果", "message": "操作失败"}
    except Exception as ex:
        loger.error(ex)
        return {"result": "False", "message": "发生异常错误"}
    try:
        return {"result": res, "message": "操作成功"}
    except Exception as ex:
        loger.error(ex)


"""
提取文本中的关键词(list) TF-IDF算法
"""


@app.post("/extract_key/tf-idf/text_list")
def extract_keys_tf_idf_list(extract_dto: dto_extract_keys_list.DataExtractList, allowPOS: Optional[List[str]] = None,
                             withWeight: Optional[bool] = None):
    try:
        if allowPOS == None:
            allowPOS = []
        if withWeight == None:
            res = jiebam.extract_keys_tf_idf_list(extract_dto.text, extract_dto.topK, tuple(allowPOS))
        else:
            res = jiebam.extract_keys_tf_idf_list(extract_dto.text, extract_dto.topK, tuple(allowPOS), withWeight)
        if res == None:
            return {"result": "输入的allowPOS数量太少，无法返回结果", "message": "操作失败"}
    except Exception as ex:
        loger.error(ex)
        return {"result": "False", "message": "发生异常错误"}
    try:
        return {"result": res, "message": "操作成功"}
    except Exception as ex:
        loger.error(ex)


"""
词性标注(str)
"""


@app.post("/separately/text")
def separately_text(separately_dto: dto_separately.SeparatelyText):
    try:
        res = jiebam.separately_text(separately_dto.text)
    except Exception as ex:
        loger.error(ex)
        return {"result": "False", "message": "发生异常错误"}
    try:
        return {"result": res, "message": "操作成功"}
    except Exception as ex:
        loger.error(ex)


"""
词性标注(list)
"""


@app.post("/separately/text_list")
def separately_text_list(separately_dto: dto_separately_list.SeparatelyTextList):
    try:
        res = jiebam.separately_text_list(separately_dto.text)
    except Exception as ex:
        loger.error(ex)
        return {"result": "False", "message": "发生异常错误"}
    try:
        return {"result": res, "message": "操作成功"}
    except Exception as ex:
        loger.error(ex)


"""
情感分析(str) CH
"""


@app.post("/senta/ch/text")
def senta_ch_text(senta_dto: dto_senta.SentaText):
    try:
        res = senta_module.senta_ch_text(senta_dto.text)
    except Exception as ex:
        loger.error(ex)
        return {"result": "False", "message": "发生异常错误"}
    try:
        return {"result": res, "message": "操作成功"}
    except Exception as ex:
        loger.error(ex)


"""
情感分析(list) CH
"""


@app.post("/senta/ch/text_list")
def senta_ch_text_list(senta_dto: dto_senta_list.SentaTextList):
    try:
        res = senta_module.senta_ch_text_list(senta_dto.text)
    except Exception as ex:
        loger.error(ex)
        return {"result": "False", "message": "发生异常错误"}
    try:
        return {"result": res, "message": "操作成功"}
    except Exception as ex:
        loger.error(ex)


"""
情感分析(str) EN
"""


@app.post("/senta/en/text")
def senta_en_text(senta_dto: dto_senta.SentaText):
    try:
        res = senta_module.senta_en_text(senta_dto.text)
    except Exception as ex:
        loger.error(ex)
        return {"result": "False", "message": "发生异常错误"}
    try:
        return {"result": res, "message": "操作成功"}
    except Exception as ex:
        loger.error(ex)


"""
情感分析(list) EN
"""


@app.post("/senta/en/text_list")
def senta_en_text_list(senta_dto: dto_senta_list.SentaTextList):
    try:
        res = senta_module.senta_en_text_list(senta_dto.text)
    except Exception as ex:
        loger.error(ex)
        return {"result": "False", "message": "发生异常错误"}
    try:
        return {"result": res, "message": "操作成功"}
    except Exception as ex:
        loger.error(ex)


"""
NSFW
"""


@app.post("/nsfw/yahoo")
def nsfw_yahoo(data: dto_nsfw_yahoo.NSFW):
    img_data = base64.b64decode(data.image)
    print(type(img_data))
    return nsfw.process_start(img_data)


"""
日志查询
"""


@app.post("/log")
def logger_search():
    return find_log.search_log()


"""
日志下载
"""


@app.get("/log/download")
def download_log(log: str):
    path = './log/' + log
    return FileResponse(path)


if __name__ == '__main__':
    import uvicorn
    import multiprocessing

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, workers=multiprocessing.cpu_count())
