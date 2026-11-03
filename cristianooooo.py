import csv

def syncClock(row):
    client_id = row["client_id"]
    t0_send_ms = int(row["t0_send_ms"])
    t_server_ms = int(row["t_server_ms"])
    t1_recv_ms = int(row["t1_recv_ms"])

    rtt = (t1_recv_ms-t0_send_ms)
    estimated_time = rtt/2 + t_server_ms

    print("\nClient:", client_id)
    print("RTT:", rtt, "ms")
    print("Server time:", t_server_ms, "ms")
    print("Estimated server time:", estimated_time, "ms")
    print("Clock offset:", abs(estimated_time-t1_recv_ms), "ms")
    print("Adjusted client time:", estimated_time, "ms")

def main():
    with open("cristian.csv", "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            syncClock(row)
            print()

main()

