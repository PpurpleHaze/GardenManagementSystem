PLOTS_FILE = "plots.txt"
MEMBERS_FILE = "members.txt"
BOOKINGS_FILE = "bookings.txt"
PAYMENTS_FILE = "payments.txt"

#imp functions
#do after the program

#oepen append file use a
def ensure_file(filename):
    try:
        f = open(filename, "a")
        f.close()
    except:
        print("Error creating file:", filename)

#read record (use r)
def read_records(filename):
    ensure_file(filename)
    records = []
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    records.append(line.split(","))
    except:
        pass
    return records


#recordwrite
def write_records(filename, records):
    try:
        with open(filename, "w") as f:
            for rec in records:
                f.write(",".join(rec) + "\n")
    except:
        print("Error writing to", filename)
#recordappend

def append_record(filename, record_list):
    try:
        with open(filename, "a") as f:
            f.write(",".join(record_list) + "\n")
    except:
        print("Error appending to", filename)
#generate id for unique function
def generate_id(prefix, filename):
    records = read_records(filename)
    return prefix + str(len(records) + 1)

#menu begin

def admin_menu():
    while True:
        print("\n--- Garden Administrator Menu ---")
        print("1. Add plot")
        print("2. Update plot")
        print("3. Remove plot")
        print("4. View all members")
        print("5. View all bookings")
        print("6. View all payments")
        print("7. Generate garden report")
        print("0. Back")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            add_plot()
        elif choice == "2":
            update_plot()
        elif choice == "3":
            remove_plot()
        elif choice == "4":
            view_all_members()
        elif choice == "5":
            view_all_bookings()
        elif choice == "6":
            view_all_payments()
        elif choice == "7":
            generate_garden_report()
        elif choice == "0":
            break
        else:
            print("Invalid option.")




#main method definition
def add_plot():
    size = input("Enter plot size (Small/Medium/Large): ").strip().capitalize()
    if not size:
        print("Plot size cannot be empty.")
        return
    plot_id = generate_id("P", PLOTS_FILE)
    status = "Available"
    append_record(PLOTS_FILE, [plot_id, size, status])
    print("Plot added with ID:", plot_id)

def update_plot():
    plots = read_records(PLOTS_FILE)
    plot_id = input("Enter plot ID to update: ").strip().upper()
    found = False
    for i, rec in enumerate(plots):
        if rec[0] == plot_id:
            print("Current: Size =", rec[1], "Status =", rec[2])
            new_size = input("New size (blank = no change): ").strip().capitalize()
            new_status = input("New status (blank = no change): ").strip()
            if new_size:
                plots[i][1] = new_size
            if new_status:
                plots[i][2] = new_status
            found = True
            break
    if found:
        write_records(PLOTS_FILE, plots)
        print("Plot updated.")
    else:
        print("Plot ID not found.")


def remove_plot():
    plots = read_records(PLOTS_FILE)
    plot_id = input("Enter plot ID to remove: ").strip().upper()
    new_plots = [rec for rec in plots if rec[0] != plot_id]

    if len(new_plots) == len(plots):
        print("Plot ID not found.")
    else:
        write_records(PLOTS_FILE, new_plots)
        print("Plot removed.")

def view_all_members():
    members = read_records(MEMBERS_FILE)
    print("\nAll Members:")
    if not members:
        print("No members.")
        return
    for rec in members:
        print(f"ID: {rec[0]} | Name: {rec[1]} | Phone: {rec[2]}")

def view_all_bookings():
    bookings = read_records(BOOKINGS_FILE)
    print("\nAll Bookings:")
    if not bookings:
        print("No bookings.")
        return
    for rec in bookings:
        print(f"ID: {rec[0]} | Plot: {rec[1]} | Member: {rec[2]} | "
              f"Start: {rec[3]} | End: {rec[4]} | Status: {rec[5]}")


def view_all_payments():
    payments = read_records(PAYMENTS_FILE)
    print("\nAll Payments:")
    if not payments:
        print("No payments.")
        return
    for rec in payments:
        print(f"ID: {rec[0]} | Booking: {rec[1]} | Amount: {rec[2]} | Date: {rec[3]}")


#remember to edit b4 16th
def generate_garden_report():
    plots = read_records(PLOTS_FILE)
    payments = read_records(PAYMENTS_FILE)

    total_plots = len(plots)
    booked = sum(1 for p in plots if p[2] == "Booked")
    available = sum(1 for p in plots if p[2] == "Available")
    income = 0.0

    for p in payments:
        try:
            if len(p) >= 6 and p[5].strip().lower() == "paid":
                income += float(p[3])
        except:
            pass

    print("\n=== Garden Activity Report ===")
    print(f"Total plots: {total_plots}")
    print(f"Booked plots: {booked}")
    print(f"Available plots: {available}")
    print(f"Total income: RM{income:.2f}")
