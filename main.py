# import re
# import os
# from util import File_to_Other
# from  util import String
# path="xxx/xxx/xx?9=?123123123php"
# s=String.String()
# print(s.sub_String(path,path.index("?"),len(path)))
# fe=File_to_Other.File_to_Other()
# param_list = fe.file_to_List(os.getcwd()+"/dict/param.txt")
# print(param_list)
import base64

# 以二进制模式打开图片文件
with open("img/jntm.jpeg", "rb") as image_file:
    # 读取图片内容并转换为base64编码
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

# 在HTML中插入base64编码字符串
html = '<img src="data:image/jpeg;base64,' + encoded_string + '" />'
print(html)
