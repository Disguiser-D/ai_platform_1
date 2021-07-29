FROM python:3.7

#制作者信息
MAINTAINER tanzeyv280@gmail.com

#设置环境变量
ENV CODE_DIR=/main
 
#将main下的文件复制到镜像中的CODE_DIR目录
#COPY ./main $CODE_DIR/

ADD ./main /code

 
#安装项目依赖包
RUN pip3 install fastapi -i https://mirror.baidu.com/pypi/simple
RUN pip3 install uvicorn -i https://mirror.baidu.com/pypi/simple
RUN pip3 install paddlepaddle==1.6.3 -i https://mirror.baidu.com/pypi/simple
RUN pip3 install tensorflow==1.14.0 -i https://pypi.mirrors.ustc.edu.cn/simple/
RUN pip3 install scikit-image==0.15.0 -i https://mirror.baidu.com/pypi/simple
RUN pip3 install jieba==0.42.1 -i https://pypi.mirrors.ustc.edu.cn/simple/
RUN pip3 install nltk==3.4.5 -i https://mirror.baidu.com/pypi/simple
RUN pip3 install numpy==1.14.5 -i https://mirror.baidu.com/pypi/simple
RUN pip3 install six==1.11.0 -i https://mirror.baidu.com/pypi/simple
RUN pip3 install scikit-learn==0.20.4 -i https://mirror.baidu.com/pypi/simple
RUN pip3 install sentencepiece==0.1.83 -i https://mirror.baidu.com/pypi/simple
RUN pip3 install Senta -i https://mirror.baidu.com/pypi/simple
RUN pip3 install aiofiles==0.7.0 -i https://mirror.baidu.com/pypi/simple


#暴露端口
EXPOSE 8000

#启动项目
CMD ["python", "code/main.py"]