﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Threading;
using System.Net.Sockets;
using System.Net;
using Newtonsoft.Json;

namespace J_LivingSlave
{
    class J_NetWork
    {
        public Socket socketSlave;
        public IPAddress ip;
        public int port = 0;
        List<string> job_Types = new List<string>()
        { "add_job","remove_job", "get_job_list","start_job","stop_job","start_slave","stop_slave"};
        //读取ip和端口
        public J_NetWork(string _ip, string _port)
        {
            socketSlave = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            if (!IPAddress.TryParse(_ip, out ip))
            {
                Console.WriteLine("start slave failed,check ip setting!");
                return;
            }

            if (!int.TryParse(_port, out port))
            {
                Console.WriteLine("start slave failed,check port setting!");
                return;
            }
            socketSlave.Bind(new IPEndPoint(ip, port));
            socketSlave.Listen(10);
            Console.WriteLine("start listening.");
            //开始监听
            while (true)
            {
                Socket _clientSocket = socketSlave.Accept();
                Thread slaveThread = new Thread(ListenClient);
                slaveThread.Start(_clientSocket);
            }

        }
        //执行任务操作
        void ListenClient(object _clientSocket)
        {            

            Console.WriteLine(socketSlave.LocalEndPoint.ToString());
            //客户端通信
            J_Client client = new J_Client(_clientSocket as Socket);
            
        }
    }
    //网络通信
    class J_Client
    {
        Socket listenClient;
        J_JobManage j_JobManage = J_JobManage.GetJ_JobManage();
        private static byte[] result = new byte[4096];
        public J_Client(Socket _socket)
        {
            listenClient = _socket;
            //string reciveStr = "";
            Console.WriteLine("client created");
            while (listenClient.Connected)
            {
                try
                {
                    int dataLength = listenClient.Receive(result);
                    //Console.WriteLine("shuju:"+ dataLength);
                    if (dataLength > 0)
                    {
                        string job_type = Encoding.ASCII.GetString(result, 0, dataLength);
                        if (job_type.Contains(job_type))
                        {
                            if (job_type == "get_job_list")
                            {
                                foreach (J_JsonJobData temp in j_JobManage.jobList)
                                {
                                    listenClient.Send(Encoding.UTF8.GetBytes(temp.ToString()));
                                    dataLength = listenClient.Receive(result);
                                }
                                break;
                            }
                            else
                            {
                                //string res=j_JobManage.J_JobOperation(job_type);
                                listenClient.Send(Encoding.UTF8.GetBytes("operation :" + job_type));
                                
                                dataLength = listenClient.Receive(result);
                                string job_data = Encoding.ASCII.GetString(result, 0, dataLength);
                                try
                                {
                                    J_JsonJobData tempData = JsonConvert.DeserializeObject<J_JsonJobData>(job_data);
                                    string res = j_JobManage.J_JobOperation(job_type, tempData);
                                    listenClient.Send(Encoding.UTF8.GetBytes(res));
                                }
                                catch
                                {
                                    listenClient.Send(Encoding.UTF8.GetBytes(job_type + " failed"));
                                }
                            }
                        }
                        else
                        {
                            listenClient.Send(Encoding.UTF8.GetBytes("operation not defiend"));break;
                        }
                        /*
                        else
                        {                            
                            try
                            {                                
                                J_JsonJobData tempData = JsonConvert.DeserializeObject<J_JsonJobData>(reciveStr);
                                Console.WriteLine(tempData.job_name);
                            }
                            catch
                            {
                                Console.WriteLine("json failed");
                            }
                            Console.WriteLine(Encoding.ASCII.GetString(result, 0, dataLength) + "\n");
                            listenClient.Send(Encoding.UTF8.GetBytes("测试"));
                        }*/
                    }
                    //listenClient.Connected;
                }
                catch
                {
                    //listenClient.Close(); 

                    break;
                }
            }
        }
    }
}
