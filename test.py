import csv

with open("tasks.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        print(row)
        burst = int(row["burst_ms"])
        print(f"burst: {type(burst)}")

events = [
    ("E1", 5),
    ("E2", 2),
    ("E3", 8)
]

events.sort(key=lambda x: x[1])

print(events)