import socket
import struct
import time

# 设置组播地址范围和端口
multicast_address = '183.30.200.1'  # 组播地址的起始地址
port = 10250                     # 组播端口号
multicast_range = 255             # 扫描的组播地址范围，例如224.0.0.0到224.0.0.255

# 初始化socket，设置为UDP协议
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.settimeout(1)  # 设置超时时间
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 绑定到指定端口
sock.bind(('', port))

# 开始扫描组播IP段
for i in range(multicast_range):
    # 计算当前组播地址
    current_address = f"224.0.0.{i}"
    print(f"Scanning {current_address}:{port}")
    
    # 加入组播组
    mreq = struct.pack("4sl", socket.inet_aton(current_address), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    try:
        # 监听返回的数据
        data, addr = sock.recvfrom(1024)
        print(f"Received data from {addr}: {data}")
    except socket.timeout:
        # 如果超时没有数据，继续扫描
        print(f"No data from {current_address}")
    finally:
        # 离开组播组
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)

    # 添加适当的等待时间，避免对网络造成过大压力
    time.sleep(0.1)

# 关闭socket
sock.close()
