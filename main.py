#PRACTICA
from Estrucutras import AVL, BlockChain, Pila
from Nodos import Bloque, NodoAVL, NodoPila
from datetime import datetime
import json
import csv
import threading

#SOCKET
import socket
import select
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#if len(sys.argv) != 3:
#    print("Error, debe de ser: python3 \'SCRIPT\' \'IP_ADRESS\' \'PORT_NUMBER\'")
#    exit()
#IP_address = str(sys.argv[1])
#Port = int(sys.argv[2])
IP_address = str('127.0.0.1')
Port = int('8080')
server.connect((IP_address,Port))

bc = BlockChain()
arbol = AVL()
espera = Pila()

def sock():
    while True:
        socket_list = [sys.stdin,server]
        read_s, write_s, error_s = select.select(socket_list,[],[])

        for socks in read_s:
            if socks == server:
                message = socks.recv(2048)
                aux = str(message.decode('utf-8'))
                if aux != 'true' and aux != 'false' and aux[0] == '{':
                    bloqueEspera = verificar(aux)
                    if bloqueEspera != None:
                        espera.push(bloqueEspera)
                        server.sendall('true'.encode('utf-8'))
                    else:
                        server.sendall('false'.encode('utf-8'))
                else:
                    if aux == 'true':
                        inse = espera.pop()
                        bc.Insert(inse.b)
                        print('\n=== Insertado ===')
                    elif aux == 'false':
                        espera.pop()
                        print('\n=== Rechazado ===')

def menu():
    bloque = None
    print('EDD PRACTICA 2 -- 2019\n')
    op = -1
    while op != '4':
        op = -1
        print('========== MAIN MENU ==========\n')
        print('1. Insert Block')
        print('2. Select Block')
        print('3. Reports\n')
        print('4. Exit\n')

        op = input('Choose an Option: ')

        if op == '1':
            print('\n---------- Insert Block ----------\n')
            arch = input('Type the data file (.csv): ')
            arch = 'bloques/' + arch
            print('')

            classe = ''
            data = ''
            
            try:
                with open(arch) as csv_f:
                    csv_r = csv.reader(csv_f,delimiter=',')
                    for row in csv_r:
                        if row[0] == 'class':
                            classe = row[1]
                        elif row[0] == 'data':
                            data = row[1]
                csv_f.close()
                dt = datetime.now()
                timestamp = str(dt.day) + '-' + str(dt.month) + '-' + str(dt.year) + '::' + str(dt.hour) + ':' + str(dt.minute) + ':' + str(dt.second)
                ind = ""
                prev = ""
                if bc.ultimo == None:
                    ind = 0
                    prev = '0000'
                else:
                    ind = int(bc.ultimo.INDEX) + 1
                    prev = bc.ultimo.HASH
                
                var1 = json.loads(data)
                var2 = json.dumps(var1)

                bloqueEspera = Bloque(str(ind),timestamp,classe,str(var2),prev)
                
                sendstring = "{\n"
                sendstring += "\"INDEX\":\"" + str(bloqueEspera.INDEX) + "\",\n"
                sendstring += "\"TIMESTAMP\":\"" + str(bloqueEspera.TIMESTAMP) + "\",\n"
                sendstring += "\"CLASS\":\"" + str(bloqueEspera.CLASS) + "\",\n"
                sendstring += "\"DATA\":" + str(var2) + ",\n"
                sendstring += "\"PREVIOUSHASH\":\"" + str(bloqueEspera.PREVIOUSHASH) + "\",\n"
                sendstring += "\"HASH\":\"" + str(bloqueEspera.HASH) + "\"\n"
                sendstring += "}"
                
                espera.push(bloqueEspera)
                
                server.sendall(sendstring.encode('utf-8'))
            except:
                print('\nError con el archivo {}\n'.format(arch))
        elif op == '2':
            bloque = None
            print('\n---------- Select Block ----------\n')
            aux = bc.primero
            if aux is None:
                print("BlockChain is Empty\n")
            else:
                while aux != None:
                    print(aux.INDEX,". ",aux.CLASS)
                    aux = aux.siguiente
                
                opb = input("\nSelect a block: ")

                find = False
                aux = bc.primero
                while aux != None:
                    if str(aux.INDEX) == opb:
                        bloque = aux
                        find = True
                        break
                    else:
                        aux = aux.siguiente
                print('')
                if find == False:
                    print('Error with the Index, try again...')
                else:
                    print('BLOCK IS SELECTED:')
                    print("\rINDEX: ",bloque.INDEX)
                    print('\rTIMESTAMP: ',bloque.TIMESTAMP)
                    print('\rCLASS: ',bloque.CLASS)
                    cont = 0
                    string = ""
                    for x in bloque.DATA:
                        string += x
                        cont += 1
                        if cont == 50:
                            break

                    print('\rDATA: ',string)
                    print('\rPREV. HASH :',bloque.PREVIOUSHASH)
                    print('\rHASH :',bloque.HASH)
                print('')
        elif op == '3':
            print('\n---------- Reports ----------\n')
            if bc.primero != None:
                opr = ""
                while opr != '3':
                    print('1. BlockChain Report')
                    print('2. Tree Report')
                    print('3. Exit\n')
                    opr = input('Type an option: ')
                    print('')
                    if opr == '1':
                        bc.graficar()
                        print('')
                    elif opr == '2':
                        if bloque == None:
                            print('Ther is not a selected block to report\n')
                        else:
                            x = json.loads(bloque.DATA)
                            convertAVL(x)
                            oprt = ""
                            while oprt != '3':
                                print('----- Tree Report -----')
                                print('1. Visualize Tree')
                                print('2. Trasversals')
                                print('3. Exit\n')
                                oprt = input('Type an option: ')
                                print('')
                                if oprt == '1':
                                    arbol.graficar()
                                elif oprt == '2':
                                    arbol.graficarPRE()
                                    arbol.graficarIN()
                                    arbol.graficarPOST()
                                elif oprt == '3':
                                    break
                                else:
                                    print('\nInvalid option, try again...\n')
                            arbol.root = None
                    elif opr == '3':
                        break
                    else:
                        print('\nInvalid option, try again...\n')
            else:
                print('No blocks in the BlockChain to report\n')
        elif op == '4':
            sys.exit()
            break
        else:
            print('\nInvalid Option\n')

def convertAVL(json):
    if json != None:
        v = json["value"]
        vals = v.split('-')
        arbol.insert(vals[0],vals[1])
        convertAVL(json["left"])
        convertAVL(json["right"])

def verificar2(y):
    lol = json.loads(y)
    has = lol["HASH"]
    
    jsondata = lol['DATA']
    jsonstring = json.dumps(jsondata)

    block2 = Bloque(lol["INDEX"],lol["TIMESTAMP"],lol["CLASS"],jsonstring,lol["PREVIOUSHASH"])
    return block2.HASH

def verificar(y):
    lol = json.loads(y)
    has = lol["HASH"]
    varA = json.dumps(lol['DATA'])

    block2 = ''
    if bc.ultimo is None:
        block2 = Bloque(lol["INDEX"],lol["TIMESTAMP"],lol["CLASS"],str(varA),'0000')
    else:
        block2 = Bloque(lol["INDEX"],lol["TIMESTAMP"],lol["CLASS"],str(varA),bc.ultimo.HASH)

    if block2.HASH == has:
        #print('\n\nHASH IGUALES')
        return block2
    else:
        print('\n\nHASH NO IGUALES')
        print("Vino: " + has)
        print('Me salio: ' + block2.HASH)
        return None

if __name__ == '__main__':
    hilo1 = threading.Thread(name='Menu', target=menu)
    hilo2 = threading.Thread(name='Oir', target=sock)
    hilo1.start()
    hilo2.start()