# 文件转换类，用于读取文件的内容转换成其他数据类型
class File_to_Other():
    #读取文件转换成列表
    def file_to_List(self,file):
        list_tmp=[]
        list_new=[]
        with open(file,"r") as f:
            list_tmp = f.readlines()
        for p in list_tmp:
            list_new.append(p.strip())
        return list_new
