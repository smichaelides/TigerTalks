import json

def read_courses(table):
    with open(table, 'r') as file:
        data = json.load(file)
        return data

def read_departmentals(table):
    with open(table, 'r') as file:
        data = json.load(file)
        return data

def main():
    courses = read_courses("coursedetails.json")
    departmentals = read_departmentals("departmentals.json")
    print(courses)
    print(departmentals)

if __name__ == "__main__":
    main()