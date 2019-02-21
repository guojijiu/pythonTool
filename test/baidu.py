from urllib import request

response = request.urlopen("http://www.baidu.com/")
fi = open("baidu.txt",'w')
page = fi.write(str(response.read()))
fi.close()
