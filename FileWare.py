import http.server
import http.client
from util import File_to_Other
from util import String
import os
class Web_Waf(http.server.BaseHTTPRequestHandler):
    file_util = File_to_Other.File_to_Other()
    string_util = String.String()
    cwd_path = os.getcwd()

    # 检测是否有恶意的参数传递
    def de_Forward(self,data=""):
        param_list=[]
        try:
            param_list = self.file_util.file_to_List(self.cwd_path+"/dict/param.txt")

        except FileNotFoundError as message:
            print("file not find")
        try:
            param_GET = self.string_util.sub_String(self.path,self.path.index("?"),len(self.path))
            param_POST = data
            for p in param_list:
                if p in param_GET or p in param_POST:
                    return True
        except:
            pass
        finally:
            pass

    #检查返回包，判断是否有flag字样，并且进行替换。
    def cg_Response(self,response):
        res = response.read()
        flag=""
        fake_flag=""
        try:
            with open("/flag", "r") as f:
                flag = f.readline()
        except FileNotFoundError:
            print("/flag is not found")
        try:
            with open("/fake_flag","r") as f:
                fake_flag=f.readline()
        except FileNotFoundError:
            print("/fake_flag is not found")
        if flag in res:
            res=res.replace(flag, fake_flag)
            self.send_response(200)
            self.send_header("Content-type", response.getheader("Content-type"))
            self.end_headers()
            self.wfile.write(res)
        else:
            self.send_response(200)
            self.send_header("Content-type", response.getheader("Content-type"))
            self.end_headers()
            self.wfile.write(response)

    # 跳转到jntm.html
    def re_Forward(self,conn_type,port=9870,path="/jntm.html"):

        server = "127.0.0.1:{0}".format(port)
        conn = http.client.HTTPConnection(server)

        if conn_type == "GET":
            conn.request(conn_type,path)
        elif conn_type == "POST":
            content_length = int(self.headers.get("Content-Length"))
            body = self.rfile.read(content_length)
            conn.request("POST", path, body=body)
            # 获取目标服务器的响应
        return conn.getresponse()


    # 如果没有出现敏感参数则放行，但依旧检查返回包是否有flag
    def conn_Access(self,conn_type):
        # 创建到目标服务器的连接
        conn = http.client.HTTPConnection("localhost:81")
        # 转发 GET 请求
        if conn_type == "GET":
            conn.request("GET", self.path)

        elif conn_type == "POST":
            content_length = int(self.headers.get("Content-Length"))
            body = self.rfile.read(content_length)
            conn.request("POST", self.path, body=body)
        # 检测返回包
        self.cg_Response(conn.getresponse())

    # 拦截GET请求
    def do_GET(self):
        if self.de_Forward():
            print("触发了")
            self.cg_Response(self.re_Forward("GET"))
        else:
            self.conn_Access()
    # 拦截POST请求
    def do_POST(self):
        if self.de_Forward():

            # 创建到目标服务器的连接
            print("触发了")
            # 转发POST请求

            self.cg_Response(self.re_Forward("POST"))

        else:
            self.conn_Access()


httpd = http.server.HTTPServer(('localhost', 80), Web_Waf)
httpd.serve_forever()
