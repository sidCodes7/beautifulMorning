import csv

def round_robin():

    workers = ["Worker_1", "Worker_2", "Worker_3"]

    # Total compute load per worker
    loads = {
        worker: 0 for worker in workers
    }

    jobs = []

    # Read CSV file
    with open("LBrr.csv", "r", newline="") as file:

        reader = csv.DictReader(file)

        for row in reader:
            jobs.append({
                "job_id": row["job_id"],
                "compute_units": int(row["compute_units"]),
                "assigned_worker": "",
                "status": ""
            })

    print("========== ROUND ROBIN SCHEDULER ==========")

    for index, job in enumerate(jobs):

        job_id = job["job_id"]
        units = job["compute_units"]

        # Select worker using round robin
        worker = workers[index % len(workers)]

        # Assign job
        job["assigned_worker"] = worker
        job["status"] = "ASSIGNED"

        # Update worker load
        loads[worker] += units

        print("\nJob:", job_id)
        print("Assigned to:", worker)
        print("Compute units:", units)

        print("Current loads:", loads)

    print("\n========== FINAL SUMMARY ==========")

    for job in jobs:
        print(job)

    print("\nWorker loads:")

    for worker, load in loads.items():
        print(worker, ":", load)


if __name__ == "__main__":
    round_robin()