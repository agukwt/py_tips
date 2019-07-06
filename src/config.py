import json


def main():
    path = r'./configs/test_case_param.json'

    with open(path, 'r') as f:
        test_case = json.load(f)

    return test_case
