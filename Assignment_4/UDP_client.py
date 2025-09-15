"""
udp_video_client.py
Simple UDP video client that sends HELLO to server and receives JPEG chunks to display frames.

Usage (example):
    python udp_video_client.py --server-ip 127.0.0.1 --server-port 5005 --listen-port 5006
"""
import socket
import struct
import argparse
import cv2
import numpy as np
import time

HEADER_STRUCT = '!IHH'
HEADER_SIZE = struct.calcsize(HEADER_STRUCT)

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--server-ip', required=True, help='Server IP to send HELLO to')
    p.add_argument('--server-port', type=int, required=True, help='Server port to send HELLO to')
    p.add_argument('--listen-ip', default='0.0.0.0', help='Local IP to bind and receive on')
    p.add_argument('--listen-port', type=int, default=5006, help='Local port to bind and receive on')
    p.add_argument('--frame-timeout', type=float, default=2.0, help='Seconds to wait for remaining packets of a frame before dropping it')
    return p.parse_args()

def main():
    args = parse_args()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((args.listen_ip, args.listen_port))
    sock.settimeout(1.0)  
    server_addr = (args.server_ip, args.server_port)

    
    sock.sendto(b'HELLO', server_addr)
    print(f'[client] Sent HELLO to server at {server_addr}. Listening on {args.listen_ip}:{args.listen_port}')

   
    frames = {}  # frame_id -> {'total': int, 'parts': dict(pkt_id->bytes), 'ts': timestamp, 'received': int}
    last_displayed_frame = None

    try:
        while True:
            try:
                packet, addr = sock.recvfrom(65536)
            except socket.timeout:
                now = time.time()
                drop_keys = []
                for fid, info in frames.items():
                    if now - info['ts'] > args.frame_timeout:
                        drop_keys.append(fid)
                for k in drop_keys:
                    del frames[k]
                continue

            if len(packet) < HEADER_SIZE:
                continue

            frame_id, pkt_id, total_packets = struct.unpack(HEADER_STRUCT, packet[:HEADER_SIZE])
            payload = packet[HEADER_SIZE:]

            if frame_id not in frames:
                frames[frame_id] = {'total': total_packets, 'parts': {}, 'ts': time.time(), 'received': 0}

            info = frames[frame_id]
            if pkt_id not in info['parts']:
                info['parts'][pkt_id] = payload
                info['received'] += 1
                info['ts'] = time.time()

            if info['received'] == info['total']:
                try:
                    pieces = [info['parts'][i] for i in range(info['total'])]
                except KeyError:
                    del frames[frame_id]
                    continue
                jbuf = b''.join(pieces)
                arr = np.frombuffer(jbuf, dtype=np.uint8)
                frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
                if frame is not None:
                    cv2.imshow('UDP Video Client', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print('[client] Quit requested (q). Exiting.')
                        break
                del frames[frame_id]
    except KeyboardInterrupt:
        print('\n[client] KeyboardInterrupt - stopping.')
    finally:
        sock.close()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
