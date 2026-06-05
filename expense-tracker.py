import json 
import os
import questionary
from questionary import Choice, Style

# finds the name of the folder the file is in
script_dir = os.path.dirname(os.path.abspath(__file__))
# finds the path of the file by joining the folderpath with the filename
file_path = os.path.join(script_dir, "expenses_file.txt")



def load_expenses_file():
    try:
        with open(file_path,"r") as exp:
            expenses = json.load(exp)
    except FileNotFoundError:
        expenses = []
    except json.JSONDecodeError:
        expenses = []
    return expenses



while True:

    decision = questionary.select("What would you like to do?", choices = ["Add Expense","View Expenses","Delete Expense","Exit"]).ask()
    expenses = load_expenses_file()
    item_count = len(expenses)


    if (decision == "Add Expense"):

        item = input("What did you purchase?\n")
        cost = float(input("How much did it cost?\n"))
        category = questionary.select("Which category is this a part of?", choices = ["Housing & Utilities","Food & Groceries","Transportation","Insurance & Debt","Lifestyle & Entertainment"]).ask()
        description = input("Please enter a description for the item\n")

        expenses = load_expenses_file()
        expenses.append({"ID":item_count+1,"expense":item, "cost":cost, "category":category, "description":description})


        with open(file_path, "w") as exp:
            json.dump(expenses, exp)
    


    elif (decision == "View Expenses"):
        expenses = load_expenses_file()
        
        print("----------------+----------------+----------------+-------------------------")
        print(f"ID              |item            |cost            |category                 ")
        print("----------------+----------------+----------------+-------------------------")
        for log in expenses:
            print(f"{log["ID"]:<16}|{log["expense"]:<16}|{log["cost"]:<16}|{log["category"]:<24}")
        
        # add further menu that asks whether theres any specific item they'd like to view, and then provide description for that item
        decision = questionary.select("Is there a specific log you'd like to view?", choices = ["Yes","No"]).ask()
        if (decision == "Yes"):
            choices = [Choice(title=f"{item["ID"]:<16} {item["expense"]:<16}") for i, item in enumerate(expenses)]
            decision = questionary.select("Which log would you like to view?",choices=choices).ask()
            for item in expenses:
                if f"{item["ID"]:<16} {item["expense"]:<16}" == decision:
                    print(f"{log["ID"]:<16}|{log["expense"]:<16}|{log["cost"]:<16}|{log["category"]:<24}\n")
                    print(f"{log["description"]}\n")
                



    elif (decision == "Delete Expense"):
        expenses = load_expenses_file()
        
        print("----------------+----------------")
        print(f"item            |cost            ")
        print("----------------+----------------")
        for log in expenses:
            print(f"{log["expense"]:<16}|{log["cost"]:<16}")
        
        # to_delete = input("Enter the index of the item to delete\n")
        choices=[Choice(title=f"{item["ID"]:<16} {item["expense"]:<16}") for i, item in enumerate(expenses)]
        index = questionary.select("Which item would you like to delete?",choices=choices).ask()
        print(index)
        
        for item in expenses:
            if f"{item["ID"]:<16} {item["expense"]:<16}" == index:
                expenses.remove(item)
                with open(file_path,"w") as exp:
                    json.dump(expenses, exp)
        
        expenses = load_expenses_file()

        for i in range(len(expenses)):
            expenses[i]["ID"] = i+1
        with open(file_path,"w") as exp:
            json.dump(expenses, exp)
        
    
    elif (decision == "Exit"):
        break;
