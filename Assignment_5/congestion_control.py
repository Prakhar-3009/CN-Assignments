import matplotlib.pyplot as plt
import random
import logging

logging.basicConfig(
    filename="congestion_control_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def tcp_congestion_control(rounds=30, loss_prob=0.15):
    logging.info("Starting TCP Congestion Control Simulation")
    print("=== TCP Congestion Control Simulation ===")

    cwnd = 1
    ssthresh = 8
    cwnd_values = []

    for i in range(1, rounds + 1):
        cwnd_values.append(cwnd)
        print(f"Round {i}: cwnd={cwnd:.2f}")

        if random.random() < loss_prob:
            print(f"Packet loss detected! Timeout → cwnd reset, ssthresh={max(1, cwnd/2):.2f}")
            logging.warning(f"Loss detected at round {i}, cwnd={cwnd}, ssthresh={ssthresh}")
            ssthresh = max(1, cwnd / 2)
            cwnd = 1  
            continue

        if cwnd < ssthresh:
            cwnd *= 2 
            phase = "Slow Start"
        else:
            cwnd += 1  
            phase = "Congestion Avoidance"

        logging.info(f"Round {i}: cwnd={cwnd}, phase={phase}")

    plt.figure(figsize=(8, 4))
    plt.plot(range(1, rounds + 1), cwnd_values, marker='o', linestyle='-', label="Congestion Window (cwnd)")
    plt.title("TCP Congestion Control (Slow Start & Congestion Avoidance)")
    plt.xlabel("Transmission Rounds")
    plt.ylabel("Congestion Window Size (cwnd)")
    plt.legend()
    plt.grid(True)
    plt.savefig("cwnd_plot.png")
    plt.show()

    logging.info("Congestion Control Simulation Completed")


if __name__ == "__main__":
    tcp_congestion_control(rounds=25, loss_prob=0.2)
