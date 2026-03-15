PAYMENT_FILE = "payments.txt"
BOOKINGS_FILE = "bookings.txt"
MEMBERS_FILE = "members.txt"


def read_records(filename):
    records = []
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if line:
                    records.append(line.split(","))
    except FileNotFoundError:
        pass
    return records


def generate_payment_id():
    payments = read_records(PAYMENT_FILE)
    return "P" + str(len(payments) + 1).zfill(3)


def find_booking(booking_id):
    bookings = read_records(BOOKINGS_FILE)
    for booking in bookings:
        if len(booking) >= 6 and booking[0].upper() == booking_id.upper():
            return booking
    return None


def find_member_name(member_id):
    members = read_records(MEMBERS_FILE)
    for member in members:
        if len(member) >= 2 and member[0].upper() == member_id.upper():
            return member[1]
    return "Unknown Member"


# -------- RECORD PAYMENT --------
def record_payment():
    pid = input("Enter Payment ID (leave blank for auto): ").strip().upper()
    if not pid:
        pid = generate_payment_id()

    bid = input("Enter Booking ID: ").strip().upper()
    booking = find_booking(bid)
    if booking is None:
        print("Booking ID not found")
        return

    member_id = booking[2]
    name = find_member_name(member_id)

    for payment in read_records(PAYMENT_FILE):
        if len(payment) >= 6 and payment[1].upper() == bid and payment[5].lower() == "paid":
            print("This booking already has a confirmed payment.")
            return

    try:
        amount = float(input("Enter Amount: "))
    except:
        print("Invalid amount")
        return

    date = input("Enter Date (YYYY-MM-DD): ").strip()
    status = "Paid"

    file = open(PAYMENT_FILE, "a")
    file.write(pid + "," + bid + "," + name + "," + str(amount) + "," + date + "," + status + "\n")
    file.close()

    print("✓ Payment recorded successfully")
    print("--- Payment Confirmation ---")
    print("Payment ID:", pid)
    print("Booking ID:", bid)
    print("Member ID:", member_id)
    print("Member Name:", name)
    print("Amount: RM", format(amount, ".2f"), sep="")
    print("Date:", date)
    print("Status:", status)


# -------- UPDATE PAYMENT STATUS --------
def update_payment():
    pid = input("Enter Payment ID to update: ").strip().upper()

    try:
        file = open(PAYMENT_FILE, "r")
        lines = file.readlines()
        file.close()
    except:
        print("No payment file found")
        return

    found = False
    new_lines = []
    updated_record = None

    for line in lines:
        data = line.strip().split(",")

        if len(data) >= 6 and data[0].upper() == pid:
            found = True
            new_status = input("Enter new status (Paid/Unpaid): ").strip().title()
            if new_status not in ["Paid", "Unpaid"]:
                print("Invalid status")
                return
            data[5] = new_status
            updated_record = data
            line = ",".join(data) + "\n"

        new_lines.append(line)

    if not found:
        print("Payment ID not found")
        return

    file = open(PAYMENT_FILE, "w")
    file.writelines(new_lines)
    file.close()

    print("✓ Payment updated successfully")
    if updated_record is not None:
        print("--- Updated Payment Status ---")
        print("Payment ID:", updated_record[0])
        print("Booking ID:", updated_record[1])
        print("Member Name:", updated_record[2])
        print("Amount: RM", updated_record[3], sep="")
        print("Date:", updated_record[4])
        print("Status:", updated_record[5])


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
