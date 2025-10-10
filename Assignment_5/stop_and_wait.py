import random
import time
import logging

logging.basicConfig(
    filename="stop_and_wait_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def stop_and_wait(total_frames=5, loss_prob=0.3, timeout=2):
    logging.info("Starting Stop-and-Wait ARQ Simulation")
    print("=== Stop-and-Wait ARQ Simulation ===")

    frame_no = 0
    while frame_no < total_frames:
        print(f"Sending Frame {frame_no}")
        logging.info(f"Sent Frame {frame_no}")

        if random.random() < loss_prob:
            print(f"Frame {frame_no} lost, retransmitting ...")
            logging.warning(f"Frame {frame_no} lost, retransmitting ...")
            time.sleep(timeout)
            continue  

        print(f"ACK {frame_no} received")
        logging.info(f"ACK {frame_no} received successfully")
        frame_no += 1
        time.sleep(1)

    print("All frames transmitted successfully!")
    logging.info("All frames transmitted successfully!")


if __name__ == "__main__":
    stop_and_wait(total_frames=6, loss_prob=0.3)
