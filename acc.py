PAYMENT_FILE = "payments.txt"


# -------- RECORD PAYMENT --------
def record_payment():
    pid = input("Enter Payment ID: ")
    bid = input("Enter Booking ID: ")
    name = input("Enter Member Name: ")

    try:
        amount = float(input("Enter Amount: "))
    except:
        print("Invalid amount")
        return

    date = input("Enter Date (YYYY-MM-DD): ")
    status = "Paid"

    file = open(PAYMENT_FILE, "a")
    file.write(pid + "," + bid + "," + name + "," + str(amount) + "," + date + "," + status + "\n")
    file.close()

    print("Payment saved successfully")


# -------- UPDATE PAYMENT STATUS --------
def update_payment():

    pid = input("Enter Payment ID to update: ")

    try:
        file = open(PAYMENT_FILE, "r")
        lines = file.readlines()
        file.close()
    except:
        print("No payment file found")
        return

    found = False
    new_lines = []

    for line in lines:

        data = line.strip().split(",")

        if data[0] == pid:
            found = True
            new_status = input("Enter new status (Paid/Unpaid): ")
            data[5] = new_status
            line = ",".join(data) + "\n"

        new_lines.append(line)

    if not found:
        print("Payment ID not found")
        return

    file = open(PAYMENT_FILE, "w")
    file.writelines(new_lines)
    file.close()

    print("Payment updated successfully")


# -------- INCOME SUMMARY --------
def income_summary():

    total = 0

    try:
        file = open(PAYMENT_FILE, "r")

        for line in file:
            data = line.strip().split(",")

            if len(data) >= 6 and data[5] == "Paid":
                total += float(data[3])

        file.close()

        print("Total Income =", total)

    except:
        print("No payment records found")


# -------- OUTSTANDING PAYMENTS --------
def outstanding_payments():

    found = False

    try:
        file = open(PAYMENT_FILE, "r")

        print("\nOutstanding Payments:")

        for line in file:
            data = line.strip().split(",")

            if len(data) >= 6 and data[5] == "Unpaid":
                print(line.strip())
                found = True

        file.close()

        if not found:
            print("No outstanding payments")

    except:
        print("No payment file found")


# -------- MONTHLY SUMMARY --------
def monthly_summary():

    month = input("Enter month (YYYY-MM): ")
    total = 0

    try:
        file = open(PAYMENT_FILE, "r")

        for line in file:
            data = line.strip().split(",")

            if len(data) >= 6 and data[5] == "Paid":
                if data[4].startswith(month):
                    total += float(data[3])

        file.close()

        print("Total income for", month, "=", total)

    except:
        print("No payment file found")


# -------- MENU --------
def accountant_menu():

    while True:

        print("\nACCOUNTANT MENU")
        print("1 Record Payment")
        print("2 Update Payment")
        print("3 Income Summary")
        print("4 Outstanding Payments")
        print("5 Monthly Summary")
        print("6 Exit")

        choice = input("Choose option: ")

        if choice == "1":
            record_payment()

        elif choice == "2":
            update_payment()

        elif choice == "3":
            income_summary()

        elif choice == "4":
            outstanding_payments()

        elif choice == "5":
            monthly_summary()

        elif choice == "6":
            print("Exit")
            break

        else:
            print("Invalid choice")

