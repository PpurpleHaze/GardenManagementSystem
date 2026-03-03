# ============================================
# COMMUNITY GARDEN MANAGEMENT SYSTEM
# Role: Maintenance Staff
# ============================================

PLOTS_FILE = "plots.txt"
MAINTENANCE_FILE = "maintenance.txt"


# ============================================
# Utility Functions
# ============================================

def ensure_file_exists(filename):
    """Create file if it does not exist"""
    try:
        open(filename, "a").close()
    except:
        print("Error creating file.")


def read_plots():
    """Read all plots from plots.txt"""
    plots = []
    try:
        with open(PLOTS_FILE, "r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) >= 2:
                    plots.append(data)
    except FileNotFoundError:
        print("plots.txt not found.")
    return plots


def plot_exists(plot_id):
    """Check if plot ID exists"""
    plots = read_plots()
    for plot in plots:
        if plot[0] == plot_id:
            return True
    return False


# ============================================
# 1️⃣ Update Garden Plot Maintenance Status
# ============================================

def update_plot_status():
    print("\n--- Update Garden Plot Maintenance Status ---")

    plot_id = input("Enter Plot ID: ").strip()

    if not plot_exists(plot_id):
        print("Invalid Plot ID. Plot does not exist.")
        return

    print("\nMaintenance Type:")
    print("1. Watering")
    print("2. Soil Preparation")
    print("3. Repair")

    choice = input("Select activity (1-3): ")

    if choice == "1":
        activity = "Watering"
    elif choice == "2":
        activity = "Soil Preparation"
    elif choice == "3":
        activity = "Repair"
    else:
        print("Invalid choice.")
        return

    status = input("Enter Status (Pending / Completed): ").strip()
    remarks = input("Enter Remarks: ").strip()
    date = input("Enter Date (YYYY-MM-DD): ").strip()

    try:
        with open(MAINTENANCE_FILE, "a") as file:
            file.write(f"{plot_id},{date},{activity},{status},{remarks}\n")
        print("Maintenance status updated successfully.")
    except:
        print("Error writing to maintenance file.")


# ============================================
# 2️⃣ Log Maintenance Record
# ============================================

def log_maintenance_record():
    print("\n--- Log Maintenance Record ---")

    plot_id = input("Enter Plot ID: ").strip()

    if not plot_exists(plot_id):
        print("Invalid Plot ID.")
        return

    date = input("Enter Date (YYYY-MM-DD): ").strip()
    activity = input("Enter Activity: ").strip()
    status = input("Enter Status: ").strip()
    remarks = input("Enter Remarks: ").strip()

    try:
        with open(MAINTENANCE_FILE, "a") as file:
            file.write(f"{plot_id},{date},{activity},{status},{remarks}\n")
        print("Maintenance record logged successfully.")
    except:
        print("Error logging maintenance record.")


# ============================================
# 3️⃣ Generate Maintenance Summary Report
# ============================================

def generate_maintenance_report():
    print("\n--- Maintenance Summary Report ---")

    total = 0
    watering = 0
    soil = 0
    repair = 0
    completed = 0
    pending = 0

    try:
        with open(MAINTENANCE_FILE, "r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) >= 5:
                    total += 1

                    if data[2] == "Watering":
                        watering += 1
                    elif data[2] == "Soil Preparation":
                        soil += 1
                    elif data[2] == "Repair":
                        repair += 1

                    if data[3].lower() == "completed":
                        completed += 1
                    elif data[3].lower() == "pending":
                        pending += 1

        print("\nTotal Maintenance Records:", total)
        print("Watering Tasks:", watering)
        print("Soil Preparation Tasks:", soil)
        print("Repair Tasks:", repair)
        print("Completed Tasks:", completed)
        print("Pending Tasks:", pending)

    except FileNotFoundError:
        print("No maintenance records found.")


# ============================================
# Maintenance Staff Menu
# ============================================

def maintenance_menu():
    ensure_file_exists(MAINTENANCE_FILE)
    ensure_file_exists(PLOTS_FILE)

    while True:
        print("\n========== Maintenance Staff Menu ==========")
        print("1. Update Garden Plot Maintenance Status")
        print("2. Log Maintenance Record")
        print("3. Generate Maintenance Summary Report")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            update_plot_status()
        elif choice == "2":
            log_maintenance_record()
        elif choice == "3":
            generate_maintenance_report()
        elif choice == "4":
            print("Exiting Maintenance Staff Module...")
            break
        else:
            print("Invalid choice. Please try again.")


# ============================================
# Run Module
# ============================================

if __name__ == "__main__":
    maintenance_menu()
