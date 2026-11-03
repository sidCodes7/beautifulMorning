
from collections import defaultdict, deque
import csv

# process logical clocks
clocks = {}

# store sent messages timestamps
messages = defaultdict(deque)

# store processed events
event_results = []

def processEvent(row):
    event_id = row["event_id"]
    process_id = row["process_id"]
    event_type = row["event_type"].upper()

    # initialize process clocks only once
    if process_id not in clocks:
        clocks[process_id] = int(row["initial_clock"])

    print(f"\nProcessing: {event_id} | Process: {process_id}")

    # Internal process
    if event_type == "INTERNAL":
        clocks[process_id] += 1

    # Send
    elif event_type == "SEND":
        receiver = row["message_to"]
        clocks[process_id] += 1
        messages[(process_id, receiver)].append(clocks[process_id])

        print("Message sent to:", receiver)
        print("Message timestamp:", clocks[process_id])

    # Receive
    elif event_type == "RECEIVE":
        sender = row["message_to"]

        if not messages[(sender, process_id)]:
            print("[ERROR] No message available from", sender)
            return

        msg_timestamp = messages[(sender, process_id)].popleft()

        clocks[process_id] = max(
            clocks[process_id],
            msg_timestamp
        ) + 1

        print("Message received from:", sender)
        print("Received timestamp:", msg_timestamp)

    else:
        print("[ERROR] Invalid event type:", event_type)
        return

    timestamp = clocks[process_id]

    event_results.append({
        "event_id": event_id,
        "process_id": process_id,
        "timestamp": timestamp
    })

    print("[CLOCK UPDATE]", process_id, "=", timestamp)


def main():

    with open("lamport.csv", "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            processEvent(row)

    print("\n========== FINAL CAUSAL ORDER ==========")

    # Sort by timestamp, then process ID for deterministic ordering
    result = sorted(
        event_results,
        key=lambda x: (
            x["timestamp"],
            x["process_id"],
            x["event_id"]
        )
    )

    for event in result:
        print(
            event["event_id"],
            "| Process:", event["process_id"],
            "| Timestamp:", event["timestamp"]
        )


main()