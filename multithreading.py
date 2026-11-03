import threading
import time 
import csv

# shared resources
lock = threading.Lock()
completed_tasks = []

# worker func
def processTask(row):
    task_id = row["task_id"]
    thread_name = row["thread_name"]
    burst_ms = int(row["burst_ms"])

    print(f"\n[{thread_name}] started {task_id}")

    # sim task processing
    time.sleep(burst_ms/1000)

    # critical section
    lock.acquire()

    try:
        print(f"[{thread_name}] Lock acquired for {task_id}")
        completed_tasks.append(task_id)
        print(f"[{thread_name}] marked {task_id} completed")
    finally:
        print(f"[{thread_name}] released lock for {task_id}")
        lock.release()

def main():

    with open("multithreading.csv", "r", newline="") as file:
        reader = csv.DictReader(file)
        threads = []

        for row in reader:
            t = threading.Thread(target=processTask, args=(row,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        print(f"\n all tasks completed:{completed_tasks}")

main()
