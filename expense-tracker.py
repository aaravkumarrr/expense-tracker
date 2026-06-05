import json 
import os
import questionary
from questionary import Choice, Style
import datetime
import math

# finds the name of the folder the file is in
script_dir = os.path.dirname(os.path.abspath(__file__))
# finds the path of the file by joining the folderpath with the filename
expenses_file_path = os.path.join(script_dir, "expenses_file.txt")

budget_file_path = os.path.join(script_dir,"budget_file.txt")



def load_expenses_file():
    try:
        with open(expenses_file_path,"r") as exp:
            expenses = json.load(exp)
    except FileNotFoundError:
        expenses = []
    except json.JSONDecodeError:
        expenses = []
    return expenses

def load_budget():
    try:
        with open(budget_file_path,"r") as budget_file:
            budget = json.load(budget_file)
    except FileNotFoundError:
        budget = 1
    except json.JSONDecodeError:
        budget = 1
    return budget

def get_monthly_spend(mon):
    total = 0
    expenses = load_expenses_file()
    for item in expenses:
        item_month = str(item["date"])[0:2]
        if item_month == mon:
            total += item["cost"] 
    return total

def monthly_summary(mon):
    budget_file = load_budget()
    monthly_budget = budget_file["Monthly_budget"]
    
    print("Total spend: ", get_monthly_spend(mon),"\n")
    total_spend = get_monthly_spend(mon)
    total_spend_proportion = math.floor(total_spend/monthly_budget * 10)
    progress_bar = ""   

    if total_spend_proportion >= 10:
        print("WARNING! YOU HAVE EXCEEDED YOUR MONTHLY BUDGET!")
    for i in range(10):
        if i < total_spend_proportion:
            progress_bar += ("██")
        else:
            progress_bar += ("░░")
    print(progress_bar,"\n")

while True:

    decision = questionary.select("What would you like to do?", choices = ["Add Expense","View Expenses","Delete Expense","Exit","Summarise Spending","Set Budgets"]).ask()
    expenses = load_expenses_file()
    item_count = len(expenses)


    if (decision == "Add Expense"):

        item = input("What did you purchase?\n")
        cost = float(input("How much did it cost?\n"))
        category = questionary.select("Which category is this a part of?", choices = ["Housing & Utilities","Food & Groceries","Transportation","Insurance & Debt","Lifestyle & Entertainment"]).ask()
        description = input("Please enter a description for the item\n")
        date = datetime.datetime.now()

        formatted_date = date.strftime("%x")

        expenses = load_expenses_file()
        expenses.append({"ID":item_count+1,"expense":item, "cost":cost, "category":category, "description":description,"date":formatted_date})


        with open(expenses_file_path, "w") as exp:
            json.dump(expenses, exp)
    


    elif (decision == "View Expenses"):
        expenses = load_expenses_file()
        
        print("----------------+----------------+----------------+------------------------+----------------")
        print(f"ID              |item            |cost            |category                |date            ")
        print("----------------+----------------+----------------+------------------------+----------------")
        for log in expenses:
            print(f"{log["ID"]:<16}|{log["expense"]:<16}|{log["cost"]:<16}|{log["category"]:<24}|{log["date"]:<16}")
        
        # add further menu that asks whether theres any specific item they'd like to view, and then provide description for that item
        decision = questionary.select("Is there a specific log you'd like to view?", choices = ["Yes","No"]).ask()
        if (decision == "Yes"):
            choices = [Choice(title=f"{item["ID"]:<16} {item["expense"]:<16}") for i, item in enumerate(expenses)]
            decision = questionary.select("Which log would you like to view?",choices=choices).ask()
            for item in expenses:
                if f"{item["ID"]:<16} {item["expense"]:<16}" == decision:
                    print(f"{item["ID"]:<16}|{item["expense"]:<16}|{item["cost"]:<16}|{item["category"]:<24}|{item["date"]:<16}\n")
                    print(f"{item["description"]}\n")
                



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
                with open(expenses_file_path,"w") as exp:
                    json.dump(expenses, exp)
        
        expenses = load_expenses_file()

        for i in range(len(expenses)):
            expenses[i]["ID"] = i+1
        with open(expenses_file_path,"w") as exp:
            json.dump(expenses, exp)
        
    
    elif (decision == "Exit"):
        break;

    elif (decision == "Summarise Spending"):

        decision = questionary.select("Would you like to sort by month, year, or overall?",choices=["Month","Year","Overall"]).ask()
        if decision == "Month":
            decision = questionary.select("Which month would you like to see?", choices = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]).ask()
            match decision:
                case "Jan":
                    monthly_summary("01")
                case "Feb":
                    monthly_summary("02")
                case "Mar":
                    monthly_summary("03")
                case "Apr":
                    monthly_summary("04")
                case "May":
                    monthly_summary("05")
                case "Jun":
                    monthly_summary("06")
                case "Jul":
                    monthly_summary("07")
                case "Aug":
                    monthly_summary("08")
                case "Sep":
                    monthly_summary("09")
                case "Oct":
                    monthly_summary("10")
                case "Nov":
                    monthly_summary("11")
                case "Dec":
                    monthly_summary("12")
    

        expenses = load_expenses_file()

        # "Housing & Utilities","Food & Groceries","Transportation","Insurance & Debt","Lifestyle & Entertainment"

# ---------------------BELOW CODE IS FOR ENTIRE YEAR------------------------------- #

        # HnU_spend = 0
        # FnG_spend = 0
        # TP_spend = 0
        # InD_spend = 0
        # LnE_spend = 0

        # for item in expenses:
        #     if item["category"] == "Housing & Utilities":
        #         HnU_spend += item["cost"]
        #     elif item["category"] == "Food & Groceries":
        #         FnG_spend += item["cost"]
        #     elif item["category"] == "Transportation":
        #         TP_spend += item["cost"]
        #     elif item["category"] == "Insurance & Debt":
        #         InD_spend += item["cost"]
        #     elif item["category"] == "Lifestyle & Entertainment":
        #         LnE_spend += item["cost"]
        #     total_spend = HnU_spend+FnG_spend+TP_spend+InD_spend+LnE_spend
        # print(f"Housing & Utilities         : ", HnU_spend,f"\nFood & Groceries            : ", FnG_spend, f"\nTransportation              : ",TP_spend, f"\nInsurance & Debt            : ", InD_spend, f"\nLifestyle & Entertainment   : ", LnE_spend,"\n")



    elif (decision == "Set Budgets"):
        while True:
            monthly_budget = float(input("Please set a monthly budget: "))
            yearly_budget = float(input("Please set a yearly budget: "))
            if (monthly_budget<yearly_budget):
                break
            else:
                print("Monthly budget cannot exceed yearly budget!")

        budget = {"Monthly_budget":monthly_budget, "Yearly_budget": yearly_budget}
        with open(budget_file_path, "w") as budget_file:
            json.dump(budget, budget_file)
            

