import auth
import inventory
import sales
import reports

def main():
    print("Welcome to Smart Inventory Manager\n")
    user = None
    while not user:
        print("1. Login\n2. Register\n3. Exit\n")
        choice = input("Enter choice: ").strip()
        if choice == '1':
            user = auth.login()
        elif choice == '2':
            auth.register()
        elif choice == '3':
            print("Goodbye!")
            return
        else:
            print("Invalid choice. Try again.\n")
    while True:
        print("\n--- Main Menu ---")
        print("1. Manage Inventory")
        print("2. Customer Buying")
        print("3. Record Sale (View Sales)")
        print("4. Restock Product")
        print("5. View Reports")
        print("6. Logout\n")
        choice = input("Enter choice: ").strip()
        if choice == '1':
            inventory.inventory_menu(user)
        elif choice == '2':
            sales.customer_buying(user)
        elif choice == '3':
            sales.record_sale(user)
        elif choice == '4':
            sales.restock_product(user)
        elif choice == '5':
            reports.reports_menu(user)
        elif choice == '6':
            print("Logging out...\n✔️ Session ended. See you again!")
            break
        else:
            print("Invalid choice. Try again.\n")

if __name__ == "__main__":
    main() 