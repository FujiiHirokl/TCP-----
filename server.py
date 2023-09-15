import socket
import threading

# サーバーのIPアドレスとポートを指定
server_ip = '192.168.65.84'
server_port = 3000

# ソケットを作成し、指定したIPアドレスとポートでリッスン
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen(10)  # 最大10クライアントを受け入れる

print(f"サーバーが {server_ip}:{server_port} で起動しました。")

clients = {}  # クライアントの情報を格納する辞書

# UDPブロードキャストを送信する関数
def send_broadcast_message():
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    message = "UDPブロードキャストメッセージ"
    udp_sock.sendto(message.encode(), ('255.255.255.255', 3001))
    udp_sock.close()

# クライアント間通信用の関数
def send_message_to_clients(message, sender_client_number):
    # すべてのクライアントにメッセージを送信
    for client_number, client_socket in clients.items():
        if client_number != sender_client_number:
            try:
                client_socket.send(f"\nクライアント {sender_client_number}: {message}".encode('utf-8'))
            except OSError as e:
                print(f"クライアント {sender_client_number} へのメッセージ送信中にエラーが発生しました: {e}")

# クライアントを処理する関数
def handle_client(client_socket, client_number):
    # クライアントへの最初のメッセージを送信
    message_to_client = f"\nサーバー: あなたのクライアント番号は {client_number} です。"
    client_socket.send(message_to_client.encode('utf-8'))
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
        
            print(f"クライアント {client_number} からのメッセージ: {data}\n")
            # クライアントの辞書を表示
            print("接続中のクライアント:", clients)

            # メッセージの宛先を確認して転送
            if "udp" in data:
                send_broadcast_message()  # メッセージに "udp" が含まれていればUDPブロードキャストを送信
                print("UDPブロードキャストメッセージを送信しました")
            else:
                parts = data.split(': ')
                if len(parts) == 2:
                    destination_client = parts[0]
                    message = parts[1]

                    if destination_client in clients:
                        destination_socket = clients[destination_client]
                        try:
                            destination_socket.send(f"クライアント {client_number}: {message}\n".encode('utf-8'))
                        except OSError as e:
                            print(f"クライアント {destination_client} へのメッセージ送信中にエラーが発生しました: {e}")
                else:
                    # "udp"メッセージ以外のメッセージはクライアント間通信として処理
                    send_message_to_clients(data, client_number)
        except ConnectionResetError as e:
            print(f"クライアント {client_number} の接続が強制的に切断されました: {e}\n")
            break
        finally:
            # クライアントが辞書に存在する場合にのみ削除する
            if str(client_number) in clients:
                del clients[str(client_number)]  # クライアントを辞書から削除

    client_socket.close()
    del clients[client_number]

client_number = 1

while True:
    client_socket, client_address = server_socket.accept()
    print(f"クライアント {client_number} が接続しました。\n")
    clients[str(client_number)] = client_socket
    
    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_number))
    client_handler.start()

    client_number += 1
