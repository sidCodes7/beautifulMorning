import csv
from collections import defaultdict, deque

processes = ["P1", "P2", "P3"]

messages = defaultdict(deque)

clocks = {
    p: [0, 0, 0] for p in processes
}

events = []


def processEvent(row):

    event_id = row["event_id"]
    process_id = row["process_id"]
    event_action = row["event_action"].upper()

    index = processes.index(process_id)

    # INTERNAL EVENT
    if event_action == "INTERNAL":

        clocks[process_id][index] += 1

    # SEND EVENT
    elif event_action == "SEND":

        clocks[process_id][index] += 1

        rcvr = row["target_process"]

        # Copy sender's vector clock
        msg = clocks[process_id].copy()

        messages[(process_id, rcvr)].append(msg)

        print(f"\nMessage sent by {process_id} to {rcvr}")
        print("Message timestamp:", msg)

    # RECEIVE EVENT
    elif event_action == "RECEIVE":

        sndr = row["target_process"]

        if not messages[(sndr, process_id)]:
            print("No message available")
            return

        msg = messages[(sndr, process_id)].popleft()

        # Merge vector clocks
        clocks[process_id] = [
            max(a, b)
            for a, b in zip(clocks[process_id], msg)
        ]

        # Increment receiver's own clock
        clocks[process_id][index] += 1

    else:
        print("Invalid event:", event_action)
        return

    vector = clocks[process_id].copy()

    events.append({
        "event_id": event_id,
        "vector": vector
    })

    print(f"{event_id} | {process_id} => {vector}")


# Compare vector timestamps
def compare_vectors(v1, v2):

    less = all(a<=b for a,b in zip(v1,v2))
    greater = all(a>=b for a,b in zip(v1,v2))

    if less and v1!=v2:
        return "CAUSALLY PRECEDES"

    elif greater and v1 != v2:
        return "CAUSALLY FOLLOWS"

    elif v1 == v2:
        return "EQUIVALENT"

    else:
        return "CONCURRENT"


def main():

    with open("vector.csv", "r", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:
            processEvent(row)

    print("\n========== EVENT COMPARISON ==========")

    for i in range(len(events)):

        for j in range(i + 1, len(events)):

            e1 = events[i]
            e2 = events[j]

            result = compare_vectors(
                e1["vector"],
                e2["vector"]
            )

            print(
                e1["event_id"],
                e2["event_id"],
                ":",
                result
            )


if __name__ == "__main__":
    main()