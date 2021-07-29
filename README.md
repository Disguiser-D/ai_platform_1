[toc]

# ai_platform_1

一个开源的集成AI平台 可以进行DFA敏感词过滤 jieba分词，关键词提取 NSFW图片识别



# 使用帮助

默认运行后在8000端口，可输入[ip:8000/docs]() 查看项目的swagger API文档



dfa分为judge filter，judge返回True或False，True表示内容为非敏感内容，反之则为敏感内容。filter会将敏感内容使用 * 进行替换。并且filter模式下误判率和检测力度会更高。



分词模式可选单个字符串或字符串列表 mode分为 streamline full_mode search_engines，具体含义请查询jieba的官方使用文档。



关键词提取详细含义请查询jieba官方文档



分词并输出词性 详情查看Jieba官方文档



NSFW图片识别，将图片进行base64转码后进行传输，注意将前面形如 data:image/bmp;base64, 的内容删除，否则会出现解析错误

