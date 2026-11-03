import csv

def berkeley_algorithm():

    # Read CSV file
    with open("berkeley.csv", "r", newline="") as file:
        reader = csv.DictReader(file)
        nodes = []

        for row in reader:
            nodes.append({
                "node_id": row["node_id"],
                "clock_time_sec": float(row["clock_time_sec"]),
                "is_faulty": row["is_faulty"].strip().lower() == "true"
            })

    print("========== POLLING NODE CLOCKS ==========")

    for node in nodes:
        print(node["node_id"], ":", node["clock_time_sec"])

    # Separate faulty and healthy nodes
    healthy = []
    faulty = []

    for node in nodes:
        if node["is_faulty"]:
            faulty.append(node)
        else:
            healthy.append(node)

    print("\nFaulty nodes discarded:")

    for node in faulty:
        print(node["node_id"])

    # Calculate average clock time of healthy nodes
    total = 0

    for node in healthy:
        total += node["clock_time_sec"]

    average = total / len(healthy)

    print("\nAverage clock time:", average)

    # Calculate adjustments
    print("\n========== CLOCK ADJUSTMENTS ==========")

    for node in healthy:

        node_id = node["node_id"]
        current_time = node["clock_time_sec"]

        adjustment = average - current_time

        print("\nNode:", node_id)
        print("Current time:", current_time)
        print("Adjustment:", adjustment)

        if adjustment > 0:
            print("Move clock forward")
        elif adjustment < 0:
            print("Move clock backward")
        else:
            print("No adjustment required")


berkeley_algorithm()