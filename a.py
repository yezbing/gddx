import socket
import struct
import time

# 配置组播 IP 地址和端口
MULTICAST_IP = '183.30.200.1 - 183.30.200.255'  # 组播地址可以在224.0.0.0 - 239.255.255.255范围内选择
MULTICAST_PORT = 10250  # 任意可用的端口
TTL = 1  # Time to Live, 限制组播消息的传播范围

# 创建 UDP 套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# 设置套接字为允许发送组播
ttl_bin = struct.pack('@I', TTL)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)

# 绑定监听端口，用于接收返回的组播数据
sock.bind(('', MULTICAST_PORT))

# 订阅指定的组播地址
mreq = struct.pack('4sl', socket.inet_aton(MULTICAST_IP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

def send_multicast_probe():
    """
    发送组播探测报文
    """
    message = b"Multicast probe"
    sock.sendto(message, (MULTICAST_IP, MULTICAST_PORT))
    print(f"已发送组播探测报文到 {MULTICAST_IP}:{MULTICAST_PORT}")

def receive_multicast_response():
    """
    接收组播响应
    """
    print("开始监听组播响应...")
    sock.settimeout(10)  # 设置超时时间
    try:
        while True:
            data, addr = sock.recvfrom(1024)  # 接收响应
            print(f"收到来自 {addr} 的数据: {data}")
    except socket.timeout:
        print("监听超时，没有收到更多的组播数据。")

if __name__ == "__main__":
    send_multicast_probe()  # 发送探测
    time.sleep(1)  # 等待片刻
    receive_multicast_response()  # 监听响应
