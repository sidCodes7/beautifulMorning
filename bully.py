import csv
from collections import deque


def bully_election():

    nodes = []

    # Read CSV file
    with open("bully.csv", "r", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            nodes.append({
                "node_id": int(row["node_id"]),
                "is_alive": row["is_alive"].strip().lower() == "true",
                "is_current_coordinator":
                    row["is_current_coordinator"].strip().lower() == "true"
            })

    # Get alive nodes
    alive_nodes = [
        node["node_id"]
        for node in nodes
        if node["is_alive"]
    ]

    # Check coordinator failure
    failed_coordinator = any(
        node["is_current_coordinator"] and not node["is_alive"]
        for node in nodes
    )

    print("========== BULLY ELECTION ==========")

    if not failed_coordinator:
        print("No coordinator failure detected")
        return

    if not alive_nodes:
        print("No alive nodes available!")
        return

    print("Coordinator failure detected!")

    # Select initiator
    initiator = min(alive_nodes)

    print("\nElection initiated by Node:", initiator)

    # Queue of processes starting elections
    election_queue = deque([initiator])

    # Track processes that have started elections
    election_started = set()

    print("\n========== ELECTION MESSAGES ==========")

    while election_queue:

        current = election_queue.popleft()

        if current in election_started:
            continue

        election_started.add(current)

        # Find higher alive nodes
        higher_nodes = [
            node for node in alive_nodes
            if node > current
        ]

        if not higher_nodes:

            print("Node", current, "has no higher alive nodes")

            continue

        received_ok = False

        for node in higher_nodes:

            print(
                "Node", current,
                "-> ELECTION -> Node", node
            )

            print(
                "Node", node,
                "-> OK -> Node", current
            )

            received_ok = True

            # Higher node starts its own election
            if node not in election_started:
                election_queue.append(node)

        if received_ok:
            print("Node", current, "waits for higher nodes")

    # Highest alive node becomes coordinator
    leader = max(alive_nodes)

    print("\n========== COORDINATOR ELECTION ==========")

    print("Node", leader, "declares itself coordinator")

    # Broadcast coordinator message
    print("\n========== COORDINATOR MESSAGE ==========")

    for node in alive_nodes:

        if node != leader:

            print(
                "Node", leader,
                "-> COORDINATOR -> Node", node
            )

            print(
                "Node", node,
                "updated coordinator to", leader
            )

    print("\nNew Coordinator:", leader)


bully_election()