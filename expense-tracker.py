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

def get_yearly_spend(year):
    total = 0
    expenses = load_expenses_file()
    for item in expenses:
        item_year = str(item["date"][6:8])
        if item_year == year:
            total += item["cost"]
    return total

def get_earliest_year():
    expenses = load_expenses_file()
    earliest_year = 99
    for items in expenses:
        if items["date"][6:8] < earliest_year:
            earliest_year = items["date"][6:8]
    return earliest_year

def get_latest_year():
    expenses = load_expenses_file()
    latest_year = 0
    for items in expenses:
        if items["date"][6:8] > latest_year:
            latest_year = items["date"][6:8]
    return latest_year

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
    expenses = load_expenses_file()
    print("----------------+----------------+----------------+------------------------+----------------")
    print(f"ID              |item            |cost            |category                |date            ")
    print("----------------+----------------+----------------+------------------------+----------------")
    for item in expenses:
        if item["date"][0:2] == mon:
            print(f"{item["ID"]:<16}|{item["expense"]:<16}|{item["cost"]:<16}|{item["category"]:<24}|{item["date"]:<16}")

    HnU_spend = 0
    FnG_spend = 0
    TP_spend = 0
    InD_spend = 0
    LnE_spend = 0

    for item in expenses:
        if item["category"] == "Housing & Utilities" and item["date"][0:2] == mon:
            HnU_spend += item["cost"]
        elif item["category"] == "Food & Groceries" and item["date"][0:2] == mon:
            FnG_spend += item["cost"]
        elif item["category"] == "Transportation" and item["date"][0:2] == mon:
            TP_spend += item["cost"]
        elif item["category"] == "Insurance & Debt" and item["date"][0:2] == mon:
            InD_spend += item["cost"]
        elif item["category"] == "Lifestyle & Entertainment" and item["date"][0:2] == mon:
            LnE_spend += item["cost"]
        total_spend = HnU_spend+FnG_spend+TP_spend+InD_spend+LnE_spend
    print(f"\nHousing & Utilities         : ", HnU_spend,f"\nFood & Groceries            : ", FnG_spend, f"\nTransportation              : ",TP_spend, f"\nInsurance & Debt            : ", InD_spend, f"\nLifestyle & Entertainment   : ", LnE_spend,"\n")




def yearly_summary(year):
    budget_file = load_budget()
    yearly_budget = budget_file["Yearly_budget"]
        
    total_spend = get_yearly_spend(year)
    print("Total spend: ", total_spend, "\n")
    total_spend_proportion = math.floor(total_spend/yearly_budget * 10)
    progress_bar = ""   

    if total_spend_proportion >= 10:
        print("WARNING! YOU HAVE EXCEEDED YOUR MONTHLY BUDGET!")
    for i in range(10):
        if i < total_spend_proportion:
            progress_bar += ("██")
        else:
            progress_bar += ("░░")
    print(progress_bar,"\n")
    expenses = load_expenses_file()
    print("----------------+----------------+----------------+------------------------+----------------")
    print(f"ID              |item            |cost            |category                |date            ")
    print("----------------+----------------+----------------+------------------------+----------------")
    for item in expenses:
        if item["date"][6:8] == year:
            print(f"{item["ID"]:<16}|{item["expense"]:<16}|{item["cost"]:<16}|{item["category"]:<24}|{item["date"]:<16}")

    HnU_spend = 0
    FnG_spend = 0
    TP_spend = 0
    InD_spend = 0
    LnE_spend = 0

    for item in expenses:
        if item["category"] == "Housing & Utilities" and item["date"][6:8] == year:
            HnU_spend += item["cost"]
        elif item["category"] == "Food & Groceries" and item["date"][6:8] == year:
            FnG_spend += item["cost"]
        elif item["category"] == "Transportation" and item["date"][6:8] == year:
            TP_spend += item["cost"]
        elif item["category"] == "Insurance & Debt" and item["date"][6:8] == year:
            InD_spend += item["cost"]
        elif item["category"] == "Lifestyle & Entertainment" and item["date"][6:8] == year:
            LnE_spend += item["cost"]
        total_spend = HnU_spend+FnG_spend+TP_spend+InD_spend+LnE_spend
    print(f"\nHousing & Utilities         : ", HnU_spend,f"\nFood & Groceries            : ", FnG_spend, f"\nTransportation              : ",TP_spend, f"\nInsurance & Debt            : ", InD_spend, f"\nLifestyle & Entertainment   : ", LnE_spend,"\n")



while True:

    decision = questionary.select("What would you like to do?", choices = ["Add Expense","View Expenses","Delete Expense","Summarise Spending","Set Budgets","Exit"]).ask()
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
        decision = questionary.select("Further action?", choices = ["View specific log","Return to Menu","Filter by category"]).ask()
        if (decision == "View specific log"):
            choices = [Choice(title=f"{item["ID"]:<16} {item["expense"]:<16}") for i, item in enumerate(expenses)]
            decision = questionary.select("Which log would you like to view?",choices=choices).ask()
            for item in expenses:
                if f"{item["ID"]:<16} {item["expense"]:<16}" == decision:
                    print(f"{item["ID"]:<16}|{item["expense"]:<16}|{item["cost"]:<16}|{item["category"]:<24}|{item["date"]:<16}\n")
                    print(f"{item["description"]}\n")
                    decision = questionary.select("Would you like to edit this log?", choices=["Edit","Return"]).ask()
                    if decision == "Edit":
                        print(f"{item["ID"]:<16}|{item["expense"]:<16}|{item["cost"]:<16}|{item["category"]:<24}")
                        print(f"{item["description"]}")
                        decision = questionary.select("What would you like to edit?",choices = ["expense","cost","description","category"]).ask()
                        if decision == "expense":
                            item["expense"] = input("Enter updated expense\n")
                        elif decision == "cost":
                            item["cost"] = float(input("Enter updated cost\n"))
                        elif decision == "description":
                            item["description"] = input("Enter new description\n")
                        elif decision == "category":
                            decision = questionary.select("Please select a new category: ",choices = ["Housing & Utilities","Food & Groceries","Transportation","Insurance & Debt","Lifestyle & Entertainment"]).ask()
                            item["category"] = decision
                        with open(expenses_file_path,"w") as exp:
                            json.dump(expenses, exp)
            

            
        elif (decision == "Filter by category"):
            decision = questionary.select("Which category?", choices = ["Housing & Utilities","Food & Groceries","Transportation","Insurance & Debt","Lifestyle & Entertainment"]).ask()
            match decision:
                case "Housing & Utilities":
                    for item in expenses:
                        if item["category"] == "Housing & Utilities":
                            print(f"{item["ID"]:<16}|{item["expense"]:<16}|{item["cost"]:<16}|{item["category"]:<24}|{item["date"]:<16}")
                case "Food & Groceries":
                    for item in expenses:
                        if item["category"] == "Food & Groceries":
                            print(f"{item["ID"]:<16}|{item["expense"]:<16}|{item["cost"]:<16}|{item["category"]:<24}|{item["date"]:<16}")
                case "Transportation":
                    for item in expenses:
                        if item["category"] == "Transportation":
                            print(f"{item["ID"]:<16}|{item["expense"]:<16}|{item["cost"]:<16}|{item["category"]:<24}|{item["date"]:<16}")
                case "Insurance & Debt":
                    for item in expenses:
                        if item["category"] == "Insurance & Debt":
                            print(f"{item["ID"]:<16}|{item["expense"]:<16}|{item["cost"]:<16}|{item["category"]:<24}|{item["date"]:<16}")
                case "Lifestyle & Entertainment":
                    for item in expenses:
                        if item["category"] == "Lifestyle & Entertainment":
                            print(f"{item["ID"]:<16}|{item["expense"]:<16}|{item["cost"]:<16}|{item["category"]:<24}|{item["date"]:<16}")
                



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

        decision = questionary.select("Would you like to sort by month, year, or lifetime?",choices=["Month","Year","Lifetime"]).ask()
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
        elif (decision == "Year"):
            years = sorted(set(item["date"][6:8] for item in expenses))
            decision = questionary.select("Which year?",years).ask()
            yearly_summary(decision)

        elif (decision == "Lifetime"):
            total_spend = 0

            for item in expenses:
                total_spend += item["cost"]

            HnU_spend = 0
            FnG_spend = 0
            TP_spend = 0
            InD_spend = 0
            LnE_spend = 0

            for item in expenses:
                if item["category"] == "Housing & Utilities":
                    HnU_spend += item["cost"]
                elif item["category"] == "Food & Groceries":
                    FnG_spend += item["cost"]
                elif item["category"] == "Transportation":
                    TP_spend += item["cost"]
                elif item["category"] == "Insurance & Debt":
                    InD_spend += item["cost"]
                elif item["category"] == "Lifestyle & Entertainment":
                    LnE_spend += item["cost"]
                total_spend = HnU_spend+FnG_spend+TP_spend+InD_spend+LnE_spend
            print(f"Housing & Utilities         : ", HnU_spend,f"\nFood & Groceries            : ", FnG_spend, f"\nTransportation              : ",TP_spend, f"\nInsurance & Debt            : ", InD_spend, f"\nLifestyle & Entertainment   : ", LnE_spend,"\n")
            print("Total Spend: ", total_spend)


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
            

