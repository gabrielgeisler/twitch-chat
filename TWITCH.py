import socket
from KEYBOARD_KEYCODES import *
from SENSITIVE_KEYS import *

####### REALIZA A CONEXÃO E RECEBE A RESPOSTA DO CHAT DA TWITCH #######
sock = socket.socket()

sock.connect((server, port))
sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))

resp = sock.recv(1024).decode('utf-8')

######## LISTA DE COMANDOS QUE O CHAT DA TWITCH PODE ESCREVER #########
commands = {
    "pular"    : Z,
    "correr"   : A,
    "direita"  : RIGHT_ARROW,
    "esquerda" : LEFT_ARROW,
    "cima"     : UP_ARROW,
    "baixo"    : DOWN_ARROW
}

############## FILA E EXECUÇÃO DOS COMANDOS REGISTRADOS  ##############
queue = []

while True:
    resp = sock.recv(2048).decode('utf-8')
    respNorm = str.strip(resp[resp.rfind(':')+1:].lower())
    respNorm.lower()

    if len(queue) <= MAX_LIST_SIZE:
        queue.append(respNorm)

    def readChat():
        for registro in queue:
            for comando in commands:
                if registro == comando:
                    HoldAndReleaseKey(commands[respNorm], 0.7)
                    queue.pop(0)
            if registro not in commands:
                queue.pop(0)

    if len(queue) >= 1:
        print(queue)
        readChat()