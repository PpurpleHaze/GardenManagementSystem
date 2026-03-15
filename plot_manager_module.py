from admin_module import (
    PLOTS_FILE, MEMBERS_FILE, BOOKINGS_FILE,
    read_records, write_records, append_record, generate_id
)

def plot_manager_menu():
    while True:
        print("\n--- Plot Manager Menu ---")
        print("1. Register new member")
        print("2. Book plot")
        print("3. Cancel booking")
        print("4. Return plot")
        print("5. View current bookings")
        print("6. View member booking history")
        print("0. Back")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            register_member()
        elif choice == "2":
            book_plot()
        elif choice == "3":
            cancel_booking()
        elif choice == "4":
            return_plot()
        elif choice == "5":
            view_current_bookings()
        elif choice == "6":
            view_member_booking_history()
        elif choice == "0":
            break
        else:
            print("Invalid option.")

def register_member():
    name = input("Enter member name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    phone = input("Enter phone number: ").strip()
    member_id = generate_id("M", MEMBERS_FILE)
    append_record(MEMBERS_FILE, [member_id, name, phone])
    print("✓ Member registered with ID:", member_id)

def show_available_plots():
    plots = read_records(PLOTS_FILE)
    print("\nAvailable Plots:")
    available = [p for p in plots if p[2] == "Available"]
    if not available:
        print("No available plots.")
        return
    for rec in available:
        print(f"ID: {rec[0]} | Size: {rec[1]}")

def book_plot():
    show_available_plots()
    plot_id = input("Enter plot ID to book: ").strip().capitalize()
    member_id = input("Enter member ID: ").strip().capitalize()
    start_date = input("Enter start date (YYYY-MM-DD): ").strip()
    end_date = input("Enter end date (YYYY-MM-DD): ").strip()

    plots = read_records(PLOTS_FILE)
    found_plot = None
    for rec in plots:
        if rec[0] == plot_id:
            found_plot = rec
            break

    if found_plot is None or found_plot[2] != "Available":
        print("Plot not available.")
        return

    booking_id = generate_id("B", BOOKINGS_FILE)
    status = "Active"
    append_record(BOOKINGS_FILE, [booking_id, plot_id, member_id, start_date, end_date, status])

    found_plot[2] = "Booked"
    write_records(PLOTS_FILE, plots)
    print("Booking created with ID:", booking_id)

def cancel_booking():
    bookings = read_records(BOOKINGS_FILE)
    booking_id = input("Enter booking ID to cancel: ").strip().upper()
    found = False
    plot_id = None
    for i, rec in enumerate(bookings):
        if rec[0] == booking_id and rec[5] == "Active":
            bookings[i][5] = "Cancelled"
            plot_id = rec[1]
            found = True
            break

    if not found:
        print("✗ Active booking not found.")
        return

    write_records(BOOKINGS_FILE, bookings)

    plots = read_records(PLOTS_FILE)
    for p in plots:
        if p[0] == plot_id:
            p[2] = "Available"
            break
    write_records(PLOTS_FILE, plots)
    print("Booking cancelled and plot freed.")

def return_plot():
    bookings = read_records(BOOKINGS_FILE)
    booking_id = input("Enter booking ID to return: ").strip().upper()
    found = False
    plot_id = None
    for i, rec in enumerate(bookings):
        if rec[0] == booking_id and rec[5] == "Active":
            bookings[i][5] = "Returned"
            plot_id = rec[1]
            found = True
            break

    if not found:
        print("✗ Active booking not found.")
        return

    write_records(BOOKINGS_FILE, bookings)

    plots = read_records(PLOTS_FILE)
    for p in plots:
        if p[0] == plot_id:
            p[2] = "Available"
            break
    write_records(PLOTS_FILE, plots)
    print("plot returned and set to Available.")

def view_current_bookings():
    bookings = read_records(BOOKINGS_FILE)
    print("\nCurrent Active Bookings:")
    active = [b for b in bookings if b[5] == "Active"]
    if not active:
        print("No active bookings.")
        return
    for rec in active:
        print(f"ID: {rec[0]} | Plot: {rec[1]} | Member: {rec[2]} | "
              f"Start: {rec[3]} | End: {rec[4]}")

def view_member_booking_history():
    member_id = input("Enter member ID: ").strip().upper()
    bookings = read_records(BOOKINGS_FILE)
    print(f"\nBooking history for member {member_id}:")
    history = [b for b in bookings if b[2] == member_id]
    if not history:
        print("No bookings found.")
        return
    for rec in history:
        print(f"ID: {rec[0]} | Plot: {rec[1]} | Start: {rec[3]} | "
              f"End: {rec[4]} | Status: {rec[5]}")
