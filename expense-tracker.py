
while True:
    decision = input("What would you like to do?\n    1: Add expense\n    2: View expenses\n    3: Exit\n")

    if (decision == 1):
        expense_profile = {}
        with open("expenses_file.txt","a") as exp:
            json.dump()
