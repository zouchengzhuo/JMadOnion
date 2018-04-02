# -*-coding:utf-8 -*-
import socket
import subprocess
import os 
import random
import time
#建立远程链接服务端 #param 服务端ip
def J_createServer(serverIp):
    server =socket.socket()
    server.bind((serverIp,9992))
    print "runing"
    server.listen(50)
    while True:
        connects,addr=server.accept()
        print ('%s is connecting' %(addr[0]))
        res=connects.recv(1024)
        connects.send('connected')
        J_runRemote(res)
    server.close
#获取本地活动网卡ip
def J_getIpAddr():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('172.31.87.141', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip
#在指定路径,讲本机ip作为文件名建立文件 #param 路径  ip
def J_writeFileWithIpInit(J_filePath,J_fileName):
    file=open(J_filePath+'/'+J_fileName,'w')
    file.write('0')
#读取指定目录下的文件,取文件名中的ip  #param  搜索路径
def J_readFile(J_filePath):
    serverList=[]
    fileid=0
    for item in os.listdir(J_filePath):
        if os.path.isfile(J_filePath+'/'+item):
            print item
            serverList.append(item)
    if len(serverList)>0:
        fileid=random.randrange(0,len(serverList),1)
        
    return fileid
#服务端运行远程琢磨 #param  客户ip
def J_runRemote(J_clientIp):
    #add pass\
    if J_clientIp.strip():
        print 'add user pass word'
        subPKey=subprocess.Popen('Cmdkey /add:'+J_clientIp+' /user:administrator /pass:8SQEtBJw~_~*')
        print ('remote to '+J_clientIp)
        try:
            subPRDP=subprocess.Popen('mstsc /console /v:'+J_clientIp)
            time.sleep(30)
            subPRDP.terminate()
        except:
            print "connection failed"
        
#客户端连接服务端 #param 服务端ip
def J_createClient(serverIp):
    client =socket.socket()
    client.connect((serverIp,9992))
    
    temp=J_getIpAddr()
    print ('myIP is %s' %(temp))
    client.send(temp)
    res=client.recv(1024)
    for connectTImes in range(1,20):
        if len(res)<1:
            client.send(temp)
            res=client.recv(1024)
    client.close()
    
    
if   __name__=='__main__':
    J_createServer('192.168.90.225')
