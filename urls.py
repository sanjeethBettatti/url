import subprocess
import os
import re

class c_url:

    #defining constructor to get url
    def __init__(self,url):
        self.url = url

    #giving a request to the url
    def request_url(self):
        
        #giving the url a request and generating a log file
        cmd = "curl -v -s -o /dev/null -w '\n%{time_total}\t%{size_header}' --stderr - " + self.url + " > logfile"
        os.system(cmd)

        #opening the log file which contains all the information
        l = open("logfile","r")

        #constructing regular expressio for capturing request and response headers
        obj = re.compile("^>.*$")
        obj1 = re.compile("^<.*$")
        self.req = []
        self.resh = []
    
        #iterating through the lines of the log file for checking request and response headers
        for i in l:
            for match in re.finditer(obj,i):
                self.req.append(match.group())
            for match in re.finditer(obj1,i):
                self.resh.append(match.group())


    #generating log file with response time, header size, request and response headers
    def log_generator(self):
        log_file = open("log","a")
        response_time = subprocess.check_output(['tail','-n2','logfile']).decode("utf-8")
        reobj = re.compile("\d+")
        res = re.findall(reobj,response_time)
        res = [int(i) for i in res]
        rtime = str(res[0]/1000000) + " seconds" 
        rsize = str(res[1]) + " bytes"
        log_file.write("\n")
        log_file.write(self.url)
        log_file.write("\nResponse time:\n")
        log_file.write(rtime)
        log_file.write("\nresponse size:\n")
        log_file.write(rsize)
        log_file.write("\n")
        log_file.write("\nRequest header:\n")

        for i in self.req:
            log_file.write(i)
            log_file.write("\n")
        log_file.write("\nResponse header\n")

        for i in self.resh:
            log_file.write(str(i))
            log_file.write("\n")


urls = ['http://google.com','http://yahoo.com','http://finance.yahoo.com','http://wikipedia.org']

if os.path.isfile("log"):
    os.system("rm log")
for i in range(len(urls)):
    s = "object_" + str(i)
    s = c_url(urls[0])
    s.request_url()
    s.log_generator()
os.system("rm logfile")
print("Success!\nplease check the \"log\" file for details")





