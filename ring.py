import csv

def ringElection():

    next_node = {}
    active = {}

    with open("ring.csv", "r", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:

            node = int(row["node_id"])

            next_node[node] = int(row["next_node_id"])

            active[node] = row["is_active"].strip().lower() == "true"

    # Get active nodes
    active_nodes = [
        node for node in active
        if active[node]
    ]

    if not active_nodes:
        print("No active nodes available!")
        return

    print("Coordinator failure detected!")

    # Start election from smallest active node
    start = min(active_nodes)

    curr = start
    visited = set()
    participants = []

    print("\n========== TOKEN CIRCULATION ==========")

    while curr not in visited:

        visited.add(curr)

        if active[curr]:

            participants.append(curr)

            print(f"Token received by Node: {curr}")

        else:

            print("Node", curr, "is inactive. Skipping.")

        curr = next_node[curr]

    # Select highest active node ID
    leader = max(participants)

    print("\n========== ELECTION RESULT ==========")

    print("Active participants:", participants)

    print("New Coordinator:", leader)

    print("COORDINATOR message broadcasted")


ringElection()