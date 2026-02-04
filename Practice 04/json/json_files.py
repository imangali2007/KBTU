import json

data = {
    "emp1": {
        "name": "Lisa",
        "designation": "programmer",
        "age": "34",
        "salary": "54000"
    },
    "emp2": {
        "name": "Elis",
        "designation": "Trainee",
        "age": "24",
        "salary": "40000"
    },
}

with open("mydata.json", "w") as file:
    json.dump(data, file, indent=4)

with open("mydata.json", "r") as file:
    loaded_data = json.load(file)
    print(loaded_data)
