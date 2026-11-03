import csv

# server functions
def processData(val):
    print(f"[SERVER EXECUTION] Processing Value: {val}")
    return val*2

def calculateLoad(val):
    print(f"[SERVER EXECUTION] Calculating Load: {val}")
    return val+100

# server dispatcher
def serverDispatch(meth, param):
    meths = {
        "processData": processData,
        "calculateLoad": calculateLoad
    }

    if meth not in meths:
        raise ValueError("Unknown Remote Method")

    result = meths[meth](param)

    return result

# client request(row)

def clientReq(row):
    call_id = row["call_id"]
    client_name = row["client_name"]
    method = row["method_name"]
    param = float(row["param_value"])
    timestamp = row["timestamp"]

    print("\n-----------------------------")
    print(f"[DISPATCH] Call ID: {call_id}")
    print(f"[CLIENT] {client_name}")
    print(f"[METHOD] {method}")
    print(f"[TIMESTAMP] {timestamp}")

    # Marshalling sim
    request = {
        "method": method,
        "value": param
    }

    print("[MARSHALLING] Request prepared")

    try:
        result = serverDispatch(
            request["method"],
            request["value"]
        )

        print(f"[RETURN] Result: {result}")
    
    except:
        print(f"[ERROR]: {error}")

def main():
    filename = 'rpc_calls.csv'
    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            clientReq(row)

main()