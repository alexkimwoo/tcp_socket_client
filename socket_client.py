import socket
import time
import os
import ConfigParser
import thread
import datetime
#=======================================================================================================================
def now():
    return datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')
#=======================================================================================================================
def read_parameter(section,name):
    value = config.get(section, name)
    try:
        return int(value)
    except Exception:
        return value
#=======================================================================================================================
def thread_client(name,delay,message):

    connected = 0

    while True:
        #===============================================================================================================
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((server_ip_address, server_ip_port))
            s.settimeout(3)
            time.sleep(0.5)
            connected = 1
            srv_ip = s.getpeername()[0]
            srv_port = s.getsockname()[1]
            print "[%s] SERVER CONNECTED => %s:%s" % (now(), srv_ip, srv_port)
            time.sleep(0.5)

        except Exception,e:
            print "[%s] CONNECTION FAILED => %s" % (now(), e)
            connected = 0
            time.sleep(1)
        #===============================================================================================================
        while connected:
            try:
                #startTime = datetime.datetime.now()
                s.send(message)
                data = s.recv(200)
                #endTime = datetime.datetime.now()
                #diff = endTime - startTime
                #elapsed_ms = (diff.days * 86400000) + (diff.seconds * 1000) + (diff.microseconds / 1000)
                #print "elapsed_ms: ",elapsed_ms
                data_str = str(data)
                try:
                    srv_resp = data_str.replace('\r\n','')
                except Exception:
                    srv_resp = data_str

                print "[%s] CONNECTED TO %s:%s | SEND: %s => RESP: %s" % (now(),srv_ip,srv_port, message, srv_resp)
                time.sleep(delay)
            #===========================================================================================================
            except Exception, e:
                print "[%s] | %s RETRY CONNECTION" % (now(),name)
                s.close()
                data = ""
                connected = 0
                time.sleep(1)
#=======================================================================================================================
file_name = os.path.basename(__file__)
py_file = os.path.abspath(__file__)
ini_file = py_file.replace(".py", ".ini")
print "  ARQUIVO PY:  ",py_file
print "  ARQUIVO INI: ",ini_file
time.sleep(0.5)
#=======================================================================================================================
messages = []
config = ConfigParser.ConfigParser()
config.read(ini_file)
server_ip_address  = read_parameter("parameters", "server_ip_address")
server_ip_port     = read_parameter("parameters", "server_ip_port")
messages   = read_parameter("parameters", "messages")

print "=============================================================="
print " TCP TEST CLIENT"
print " SERVER IP: %s" % server_ip_address
print " SERVER PORT: %d" % server_ip_port
print "=============================================================="

msg = messages.replace('[','')
msg = msg.replace(']','')
msg = msg.replace('),','#')
msg = msg.replace('(','')
msg = msg.replace(')','')

msg_list = msg.split('#')

new_list = []
for item in msg_list:
    new_list.append(item.split(','))

def start_tread(msg,freq):
    thread.start_new_thread(thread_client, (msg, freq, msg) )
    time.sleep(0.5)

#=======================================================================================================================
try:
    for n in new_list:
        msg_to_server = n[0]
        freq = int(n[1])
        start_tread(msg_to_server,freq)
    #thread.start_new_thread(thread_client, ("PINH", 2, "ping") )
    #time.sleep(0.1)
except Exception,e:
    print "\n  DESCRICAO FALHA: ", e
#=======================================================================================================================
while True:
    pass
#=======================================================================================================================