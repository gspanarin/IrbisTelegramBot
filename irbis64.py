# -*- coding: utf-8 -*-
import socket
import random
import irbis64_config 
import sys



port = 6666
host = '127.0.0.1'

login = '1'
password = '1'
arm = 'C'
proc_id = 0
command_num = 0



def irbis_search(text):
    global proc_id
    proc_id = random.randint(11111111,99999999)
    global command_num
    command_num = 1
    answer = ''
    
    #Регистрация на сервере Ирбиса
    retval = reg(login,password)
    #Поиск книг в базе
    retval = search('ibis',text,10,1,'@brief')
    #Вывод на печать результатов поиска
    if (int(retval['status']) == 0):
        i = 0
        answer = 'По вашему запросу: _"' + text + '"_ найдено *' + retval['count'] + '* записей в Электронном каталоге\n'
        while i < len(retval['result']):
            answer += '\n*' + str(i+1) + ':* ' + retval['result'][i]['rec'] + '\n'
            i += 1
    #Разрегистрация на сервере Ирбиса        
    retval = unreg(login,password)
    return answer





##################################
#  Функция регистрации на сервере
##################################
def reg(login, password):
    answer = ''
    packet = ''
    paramlist = ('A', arm, 'A', str(proc_id), str(command_num), '', '', '', '', '', login, password)
    packet = '\n'.join(paramlist)
    answer = send(packet)
    ###########################
    #Особенность регистрации - разбор ответа в кодировке cp1251
    ###########################
    answer = answer.decode('cp1251')
    answer = answer.split("\r\n")
    status = answer[10]
    return str(status)


##################################
#  Функция разрегистрации на сервере
##################################
def unreg(login,password):
    answer = ''
    status = ''
    packet = ''
    paramlist = ('B', arm, 'B', str(proc_id), str(command_num), '', '', '', '', '', login)
    packet = '\n'.join(paramlist)
    answer = send(packet)
    answer = answer.decode('utf8')
    answer = answer.split("\r\n")
    status = answer[10]
    return str(status)


##################################
#  Функция отправки команд на сервер
##################################
def send(packet):
    global command_num
    sock = socket.socket()
    sock.connect((host, port))
    #print ('\n\n####################################################\n')
    #print ('SIZE:' + str(len(packet)))
    #print ('SEND:')
    #print (packet)
    #print ('\n\n####################################################\n')
    #tmp = packet.decode('utf-8')
  
    packet = str(len(packet.encode('utf8'))) + '\n' + packet 
    #print (packet)
    sock.send(bytearray(packet,'utf8'))
    tmp = b''
    data = b''
    ################################
    tmp = sock.recv(1024)
    while sock:
        if not tmp:
            sock.close()
            break
        else:
            data += tmp
            tmp = sock.recv(1024)
    #########################     
    sock.close()
    #print ('\n\n####################################################\n')
    #print ('RECIVE: \n')
    #print (data)
    #print ('\n\n####################################################\n')
    command_num = command_num + 1
    return data


##################################
#  Функция поиска запискей в базе
##################################
def search(db_name, search_exp, num_records, first_record, formatpft):
    answer = ''
    paramlist = ('K', arm, 'K', str(proc_id), str(command_num), '', '', '', '', '',db_name, search_exp, str(num_records), str(first_record), formatpft)
    packet = '\n'.join(paramlist)
    answer = send(packet)
    answer = answer.decode('utf8')
    answer = answer.split("\r\n")
    status = answer[10]
    count = answer[11]
    result = []
    i = 12
    rec = ''
    mfn = ''
    while i < len(answer):
        if len(answer[i])>0:
            tmp = answer[i] 
            tmp = tmp.split('#', maxsplit=1)
            result.append ({'mfn' : tmp[0], 'rec' : tmp[1]})
        i += 1
            
    return {'status' : status, 'count' : count, 'result' : result}

    
##################################
#  Функция сохранения записи в базу
##################################
def writerecord():
   print ('!!!!!!!!!!!')
