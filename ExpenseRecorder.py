import json
import datetime

expenseFile = "expenseRecorderSystemFile.json"

CATEGORIES = ["Groceries", "Transportation", "Entertainment", "Utilities"]

def loadExpenses() :
    try :
        with open(expenseFile , "r") as file : 
            return json.load(file)
    except(FileNotFoundError , json.JSONDecodeError) :
        return []

def saveExpenses(expenses) :
    with open(expenseFile , "w") as file :
        return json.dump(expenses , file , indent= 4)
    

def displayCategories() :
    print()
    for i , category in enumerate(CATEGORIES , 1) :
        print(f"{i}. {category}")
    print(f"{len(CATEGORIES) + 1}. Add new Category")

    
def addExpense(expenses) :
    try :
        amount = float(input("Enter the expenses : "))
        description = input("Enter the description : ")
        
        displayCategories();
        categoryChoice = int(input("Enter category number : "))
        
        if 1 <= categoryChoice <= len(CATEGORIES) :
            category = CATEGORIES[categoryChoice - 1]
        elif categoryChoice == len(CATEGORIES) + 1 :
            category = input("Enter the new category : ")
            CATEGORIES.append(category) # For new Category...
        else :
            print("Invalid choice!")
            category = "OTHERS"
            
        dateInput = input("Enter date(YYYY-MM-DD) or click enter for today : ")
        date = dateInput if dateInput else str(datetime.date.today())
        
        expenses.append({"amount" : amount , "description" : description , "category" : category , "date" : date})
        saveExpenses(expenses)
        
        print("\nExpenses addded successfully!\n")
    
    except ValueError :
        print("Invalid input! Please enter a valid number for amount.")
        

def viewExpenses(expenses) :
    if not expenses :
        print("\nNo expenses recorded.")
        return
    
    print("\nYour Expenses:")
    for exp in expenses :
        print(f"- {exp['date']} : {exp['description']} (Rs.{exp['amount']}) [{exp['category']}]")
    print()
    

def filterExpeneses(expenses , period) :
    today = datetime.date.today()
    filteredExp = []
    
    if period == "daily" :
        for exp in expenses :
            if exp["date"] == str(today) :
                filteredExp.append(exp)
                
    elif period == "weekly" :
        startingWeek = today - datetime.timedelta(days=today.weekday())
        for exp in expenses :
            expDate = datetime.date.fromisoformat(exp["date"])
            if startingWeek <= expDate <= today :
                filteredExp.append(exp)
                
    elif period == "monthly" :
        currentMonth = str(today)[:7] #Extract YYYY-MM
        for exp in expenses :
            expMonth = exp["date"][:7]
            if expMonth == currentMonth :
                filteredExp.append(exp)
                
    return filteredExp

def summary(expenses) :
    if not expenses :
        print("\nNo expenses to summarize.")
        return
    
    print("\nView summary for:")
    print("1. Daily")
    print("2. Weekly")
    print("3. Monthly")
    print("4. All Time")
    
    choice = input("Enter your choice: ")
    
    periodMap = {"1" : "daily" , "2" : "weekly" , "3" : "monthly" , "4" : "all"}
    period = periodMap.get(choice , "all")
    
    filteredExp = filterExpeneses(expenses , period) if period != "all" else expenses
    
    totalExp = sum(exp["amount"] for exp in filteredExp)
    categorySummary = {}
    
    for exp in filteredExp :
        categorySummary[exp["category"]] = categorySummary.get(exp["category"] , 0) + exp["amount"]
        
    print(f"\nTotal Spent ({period.capitalize()}): Rs.{totalExp : .2f}")
    print("Spending by Category : ")
    for category , amount in categorySummary.items() :
        print(f"- {category} : Rs.{amount : .2f}")
    print()


def main() :
    """Main menu to run the program."""
    expenses = loadExpenses()
    
    while True:
        print("\n1. View Category")
        print("2. Add Expense")
        print("3. View Expenses")
        print("4. View Summary")
        print("5. Exit")
        
        choice = input("Enter choice: ")

        if choice == "1":
            displayCategories()
        elif choice == "2":
            addExpense(expenses)
        elif choice == "3":
            viewExpenses(expenses)
        elif choice == "4" :
            summary(expenses)
        elif choice == "5":
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice. Try again!")

if __name__ == "__main__":
    main()
