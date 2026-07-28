import json

def input_retrieval(trace: dict) -> dict:
    trace = trace[0]["trace"]
    pass

def main():
    file_path = "test-aide4.json"
    with open(file_path, "r") as file:
        trace = json.load(file)
    input_retrieval(trace)

main()