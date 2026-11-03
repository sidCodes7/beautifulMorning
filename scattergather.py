import csv
from concurrent.futures import ThreadPoolExecutor

# Matrix B
B = [
    [1, 0, 2, 1],
    [0, 1, 1, 0],
    [2, 1, 0, 1],
    [1, 0, 1, 2]
]

# Worker function
def worker(args):

    index, row = args

    print("Worker processing row:", index)

    result = []

    # Multiply row by matrix B
    for j in range(len(B[0])):

        total = 0

        for k in range(len(row)):
            total += row[k] * B[k][j]

        result.append(total)

    print("Worker completed row:", index)

    return result


def main():

    A = []

    # Read matrix A from CSV
    with open("scattergather.csv", "r", newline="") as file:

        reader = csv.reader(file)

        header = next(reader)

        for row in reader:
            # Skip first column (row ID)
            A.append([int(value) for value in row[1:]])

    print("========== MASTER PROCESS ==========")

    print("Matrix A:")
    for row in A:
        print(row)

    print("\nMatrix B:")
    for row in B:
        print(row)

    # Scatter rows to workers
    print("\n[SCATTER] Distributing matrix rows")

    tasks = [
        (i, A[i])
        for i in range(len(A))
    ]

    # Parallel execution
    with ThreadPoolExecutor(max_workers=4) as executor:

        results = list(executor.map(worker, tasks))

    # Gather results
    print("\n[GATHER] Collecting worker results")

    C = results

    print("\n========== FINAL MATRIX ==========")

    for row in C:
        print(row)

main()