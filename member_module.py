from admin_module import (
    PLOTS_FILE, BOOKINGS_FILE, PAYMENTS_FILE,
    read_records, write_records, append_record, generate_id
)


def member_menu():
    while True:
        print("\n--- Garden Member Menu ---")
        print("1. View available plots")
        print("2. Request booking")
        print("3. Request extension")
        print("4. View my booking and payment history")
        print("0. Back")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            show_available_plots()
        elif choice == "2":
            member_request_booking()
        elif choice == "3":
            member_request_extension()
        elif choice == "4":
            member_view_history()
        elif choice == "0":
            break
        else:
            print("Invalid option.")


def show_available_plots():
    plots = read_records(PLOTS_FILE)
    print("\nAvailable Plots:")
    available = [p for p in plots if len(p) >= 3 and p[2] == "Available"]
    if not available:
        print("No available plots.")
        return
    for rec in available:
        print(f"ID: {rec[0]} | Size: {rec[1]}")


def member_request_booking():
    member_id = input("Enter your member ID: ").strip().upper()
    show_available_plots()
    plot_id = input("Enter plot ID to book: ").strip().upper()
    start_date = input("Enter start date (YYYY-MM-DD): ").strip()
    end_date = input("Enter end date (YYYY-MM-DD): ").strip()

    plots = read_records(PLOTS_FILE)
    found_plot = None
    for rec in plots:
        if rec[0].upper() == plot_id:
            found_plot = rec
            break

    if found_plot is None or found_plot[2] != "Available":
        print("✗ Plot not available.")
        return

    booking_id = generate_id("B", BOOKINGS_FILE)
    status = "Active"
    append_record(BOOKINGS_FILE, [booking_id, plot_id, member_id, start_date, end_date, status])
    found_plot[2] = "Booked"
    write_records(PLOTS_FILE, plots)
    print("✓ Booking requested. ID:", booking_id)
    print("Please proceed to Accounts Management to record and confirm payment.")


def member_request_extension():
    member_id = input("Enter your member ID: ").strip().upper()
    bookings = read_records(BOOKINGS_FILE)
    print("\nYour active bookings:")
    active = [b for b in bookings if len(b) >= 6 and b[2].upper() == member_id and b[5] == "Active"]
    if not active:
        print("No active bookings.")
        return
    for rec in active:
        print(f"ID: {rec[0]} | Plot: {rec[1]} | End: {rec[4]}")

    booking_id = input("Enter booking ID to extend: ").strip().upper()
    new_end = input("Enter new end date (YYYY-MM-DD): ").strip()

    updated = False
    for i, rec in enumerate(bookings):
        if len(rec) >= 6 and rec[0].upper() == booking_id and rec[2].upper() == member_id and rec[5] == "Active":
            bookings[i][4] = new_end
            updated = True
            break

    if updated:
        write_records(BOOKINGS_FILE, bookings)
        print("✓ Booking extended.")
    else:
        print("✗ Booking not found or not active.")


def member_view_history():
    member_id = input("Enter your member ID: ").strip().upper()
    print(f"\nYour bookings (Member {member_id}):")

    bookings = read_records(BOOKINGS_FILE)
    history = [b for b in bookings if len(b) >= 6 and b[2].upper() == member_id]
    if not history:
        print("No bookings.")
    else:
        for rec in history:
            print(f"ID: {rec[0]} | Plot: {rec[1]} | Start: {rec[3]} | End: {rec[4]} | Status: {rec[5]}")

    print("\nYour payments:")
    payments = read_records(PAYMENTS_FILE)
    member_booking_ids = {b[0].upper() for b in history if len(b) >= 1}

    member_payments = []
    for p in payments:
        if len(p) >= 6 and p[1].upper() in member_booking_ids:
            member_payments.append(p)

    if not member_payments:
        print("No payments.")
    else:
        for rec in member_payments:
            print(
                f"PaymentID: {rec[0]} | Booking: {rec[1]} | Member: {rec[2]} | "
                f"Amount: RM{rec[3]} | Date: {rec[4]} | Status: {rec[5]}"
            )
