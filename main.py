from admin_module import ensure_file, PLOTS_FILE, MEMBERS_FILE, BOOKINGS_FILE, PAYMENTS_FILE, admin_menu
from plot_manager_module import plot_manager_menu
from member_module import member_menu
from maintenance_staff import update_plot_status
from acc import accountant_menu

def main_menu():
    while True:
        print("\n === Community Garden Management System==")
        print("1. Garden Administrator")
        print("2. Plot Manager")
        print("3. Garden Member")
        print("4. Maintenance ")
        print("5. Accounts Management")
        print("0. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            admin_menu()
        elif choice == "2":
            plot_manager_menu()
        elif choice == "3":
            member_menu()
        elif choice == "4":
            update_plot_status()
        elif choice == "5":
            accountant_menu()
        elif choice == "0":
            print("Thank you for using GreenThumb Gardens system!")
            break
        else:
            print("Invalid option. Please enter a choice from 0, 1, 2, 3 or 4.")

if __name__ == "__main__":
    print("Initializing files")
    ensure_file(PLOTS_FILE)
    ensure_file(MEMBERS_FILE)
    ensure_file(BOOKINGS_FILE)
    ensure_file(PAYMENTS_FILE)
    main_menu()
