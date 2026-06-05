import json 
import os

# finds the name of the folder the file is in
script_dir = os.path.dirname(os.path.abspath(__file__))
# finds the path of the file by joining the folderpath with the filename
file_path = os.path.join(script_dir, "expenses_file.txt")

while True:

    decision = int(input("What would you like to do?\n    1: Add expense\n    2: View expenses\n    3: Exit\n\n"))

    if (decision == 1):

        item = input("What did you purchase?\n")
        cost = float(input("How much did it cost?\n"))

        try:
            with open(file_path,"r") as exp:
                expenses = json.load(exp)
        except FileNotFoundError:
            expenses = []
        
        expenses.append({"expense":item, "cost":cost})

        with open(file_path, "w") as exp:
            json.dump(expenses, exp)
    
    elif (decision == 2):
        try:
            with open(file_path,"r") as exp:
                expenses = json.load(exp)
        except FileNotFoundError:
            expenses = []
        
        print("----------+----------")
        print(f"item      |cost      ")
        print("----------+----------")
        for log in expenses:
            print(f"{log["expense"]:<10}|{log["cost"]:<10}")
