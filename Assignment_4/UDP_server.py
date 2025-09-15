#!/usr/bin/env python3
"""
udp_video_server.py
Simple UDP video streamer (server). Waits for client "HELLO", then streams frames as JPEG chunks.

Usage (example):
    python udp_video_server.py --host 0.0.0.0 --port 5005 --source sample.mp4 --chunk 4096 --quality 80

If --source is "0" (string) server uses webcam index 0.
"""
import socket
import struct
import argparse
import time
import math
import cv2

HEADER_STRUCT = '!IHH'   # frame_id (uint32), packet_id (uint16), total_packets (uint16)
HEADER_SIZE = struct.calcsize(HEADER_STRUCT)

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--host', default='0.0.0.0', help='Server bind IP')
    p.add_argument('--port', type=int, default=5005, help='Server bind port (and where client sends HELLO)')
    p.add_argument('--source', default='0', help='Video source (file path) or "0" for webcam index 0')
    p.add_argument('--chunk', type=int, default=4096, help='Chunk size (bytes) to split each JPEG frame into')
    p.add_argument('--quality', type=int, default=80, help='JPEG quality (0-100)')
    p.add_argument('--max-w', type=int, default=640, help='Optional max width to resize frames (preserve aspect)')
    p.add_argument('--timeout', type=float, default=30.0, help='How long (s) to wait for client HELLO before exit')
    return p.parse_args()

def open_capture(source):
    if source == '0':
        src = 0
    else:
        src = source
    cap = cv2.VideoCapture(src)
    if not cap.isOpened():
        raise RuntimeError(f'Cannot open video source: {source}')
    return cap

def main():
    args = parse_args()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((args.host, args.port))
    sock.settimeout(args.timeout)
    print(f'[server] Bound to {args.host}:{args.port}. Waiting for client HELLO (timeout={args.timeout}s)...')

    try:
        data, client_addr = sock.recvfrom(1024)  # expect "HELLO" from client
    except socket.timeout:
        print('[server] No client HELLO received. Exiting.')
        return

    print(f'[server] Received initial message from {client_addr}: {data!r}. Starting stream.')

    cap = open_capture(args.source)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0 or math.isnan(fps):
        fps = 25.0
    frame_interval = 1.0 / fps
    print(f'[server] Video FPS={fps:.2f}, frame interval={frame_interval:.3f}s')

    frame_id = 0
    try:
        while True:
            t0 = time.perf_counter()
            ret, frame = cap.read()
            if not ret:
                print('[server] End of stream (video file ended) or camera failed. Exiting.')
                break

            # optional resize to limit bandwidth
            h, w = frame.shape[:2]
            if args.max_w and w > args.max_w:
                new_h = int(h * args.max_w / w)
                frame = cv2.resize(frame, (args.max_w, new_h))

            # encode to JPEG
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), args.quality]
            success, encoded = cv2.imencode('.jpg', frame, encode_param)
            if not success:
                print('[server] JPEG encoding failed for frame', frame_id)
                continue
            payload = encoded.tobytes()
            payload_len = len(payload)
            total_packets = math.ceil(payload_len / args.chunk)
            if total_packets >= 65535:
                # header uses uint16 for total_packets; this is extremely large frame
                print('[server] Frame too big to packetize with current chunk size. Skipping frame.')
                continue

            # send all packets for this frame
            for pkt_id in range(total_packets):
                start = pkt_id * args.chunk
                chunk = payload[start:start + args.chunk]
                header = struct.pack(HEADER_STRUCT, frame_id, pkt_id, total_packets)
                packet = header + chunk
                try:
                    sock.sendto(packet, client_addr)
                except Exception as e:
                    print('[server] sendto error:', e)
                    # continue attempting to send remaining packets/frames

            # advance frame id and respect FPS
            frame_id = (frame_id + 1) & 0xffffffff

            # Sleep to maintain FPS (account for elapsed time)
            elapsed = time.perf_counter() - t0
            to_sleep = frame_interval - elapsed
            if to_sleep > 0:
                time.sleep(to_sleep)
    except KeyboardInterrupt:
        print('\n[server] KeyboardInterrupt - stopping.')
    finally:
        cap.release()
        sock.close()
        print('[server] Clean exit.')

if __name__ == '__main__':
    main()
