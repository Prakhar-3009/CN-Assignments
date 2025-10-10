import random
import time
import logging

logging.basicConfig(
    filename="go_back_n_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def go_back_n(total_frames=10, window_size=4, loss_prob=0.2):
    logging.info("Starting Go-Back-N ARQ Simulation")
    print("=== Go-Back-N ARQ Simulation ===")

    base = 0
    while base < total_frames:
        end = min(base + window_size, total_frames)
        print(f"Sending frames {base} to {end - 1}")
        logging.info(f"Sent frames {base}-{end - 1}")

        lost_frame = None
        for frame in range(base, end):
            if random.random() < loss_prob:
                lost_frame = frame
                print(f"Frame {frame} lost, retransmitting frames {frame} to {end - 1}")
                logging.warning(f"Frame {frame} lost, retransmitting from {frame}")
                break

        if lost_frame is not None:
            base = lost_frame
            time.sleep(1)
            continue

        print(f"ACK {end - 1} received")
        logging.info(f"ACK {end - 1} received")
        base = end
        time.sleep(1)

    print("All frames transmitted successfully!")
    logging.info("All frames transmitted successfully!")


if __name__ == "__main__":
    go_back_n(total_frames=12, window_size=4, loss_prob=0.25)
