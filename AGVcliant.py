import socket
import threading

# サーバーのIPアドレスとポートを指定
server_ip = '127.0.0.1'
server_port = 3000

# ソケットを作成し、サーバーに接続
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

def receive_messages():
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break
        print(f"受信したメッセージ: {data}")

# 別スレッドでメッセージを受信
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# クライアント番号を入力
client_number = input("クライアント番号を入力してください (1, 2, 3): ")
client_socket.send(client_number.encode('utf-8'))

while True:
    # メッセージの入力
    message = input("宛先クライアント番号を選択してメッセージを入力してください (終了するには'exit'を入力): ")
    if message == 'exit':
        break

    # メッセージを宛先クライアントと一緒に送信
    client_socket.send(message.encode('utf-8'))

client_socket.close()
