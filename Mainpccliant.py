import socket
import threading

# サーバーのIPアドレスとポートを指定
server_ip = '192.168.65.84'
server_port = 3000

# ソケットを作成し、サーバーに接続
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# 受信したidとtimeの値を格納するリスト
id_values = []
time_values = []

def Position_estimation(id_values,time_values):
    print(id_values)
    print(time_values)

def receive_messages():
    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"\n受信したメッセージ: {data}")
            # 文字列を分割してidとtimeを抽出
            parts = data.split(': ')
            if len(parts) == 2:
                id_time_string = parts[1]
                id_time_parts = id_time_string.split('&')
                id_value = None
                time_value = None
                

                for part in id_time_parts:
                    key_value = part.split('=')
                    if len(key_value) == 2:
                        key, value = key_value
                        if key == 'id':
                            id_value = value
                        elif key == 'time':
                            time_value = value
                print(id_value)
                print(time_value)
                """

                # idとtimeの値をリストに追加
                if id_value is not None:
                    id_values.append(id_value)
                if time_value is not None:
                    time_values.append(time_value)
                
                if len(id_values) == 4 and len(time_values) == 4:
                    # スレッドを作成して実行
                    thread = threading.Thread(target=Position_estimation, args=(id_values,time_values))
                    thread.start()
                    
                    # リストを空にする
                    id_values = []
                    time_values = []
                    """
        except ConnectionAbortedError:
            print("接続が中断されました。")
            break
                

# メッセージ受信スレッドを開始
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()



while True:
    # メッセージの入力
    message = input("宛先クライアント番号を選択してメッセージを入力してください (終了するには'exit'を入力): ")
    if message == 'exit':
        break

    # メッセージを宛先クライアントと一緒に送信
    client_socket.send(message.encode('utf-8'))

# ためられた4つのidとtimeの値を表示
print("受信した最初の4つのidとtimeの値:")
for i in range(4):
    if i < len(id_values):
        print(f"id={id_values[i]}, time={time_values[i]}")

client_socket.close()
