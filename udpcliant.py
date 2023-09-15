import socket

# 受信用のIPアドレスとポート番号を指定
udp_listen_ip = '0.0.0.0'  # すべてのネットワークインターフェースからの受信
udp_listen_port = 3001  # サーバーが送信したUDPメッセージを受信するポート

# UDPソケットを作成してバインド
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((udp_listen_ip, udp_listen_port))

print(f"UDPメッセージの受信を開始しました（ポート {udp_listen_port}）")

while True:
    data, addr = udp_socket.recvfrom(1024)
    print(f"UDPメッセージを受信しました: {data.decode('utf-8')} 送信元アドレス: {addr}")
