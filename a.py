import socket
import struct
import time

# 配置组播后段地址范围和端口
MULTICAST_IP_SEGMENT = '183.30.200.'  # 指定组播后段 IP 地址范围前缀
MULTICAST_PORT = 10250  # 指定端口号
TTL = 1  # Time to Live, 限制组播消息的传播范围

# 创建 UDP 套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# 设置 TTL 以控制组播包的传递范围
ttl_bin = struct.pack('@I', TTL)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)

# 绑定监听端口，用于接收组播数据
sock.bind(('', MULTICAST_PORT))

# 订阅一个组播地址范围
def join_multicast_group(multicast_ip):
    """
    加入指定的组播组
    """
    mreq = struct.pack('4sl', socket.inet_aton(multicast_ip), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    print(f"已加入组播地址: {multicast_ip}")

def send_multicast_probe(multicast_ip):
    """
    向指定的组播地址发送探测报文
    """
    message = b"Multicast probe"
    sock.sendto(message, (multicast_ip, MULTICAST_PORT))
    print(f"已发送组播探测报文到 {multicast_ip}:{MULTICAST_PORT}")

def receive_multicast_response(timeout=10):
    """
    监听组播响应
    """
    print("开始监听组播响应...")
    sock.settimeout(timeout)  # 设置超时时间
    try:
        while True:
            data, addr = sock.recvfrom(1024)  # 接收组播数据
            print(f"收到来自 {addr} 的组播数据: {data}")
    except socket.timeout:
        print("监听超时，没有收到更多的组播数据。")

if __name__ == "__main__":
    # 扫描 IP 段 (239.255.0.0 - 239.255.0.255)
    for i in range(1, 255):
        multicast_ip = MULTICAST_IP_SEGMENT + str(i)
        
        # 加入组播组并发送探测报文
        join_multicast_group(multicast_ip)
        send_multicast_probe(multicast_ip)
        
        # 短暂等待
        time.sleep(1)
    
    # 监听响应
    receive_multicast_response(timeout=10)
