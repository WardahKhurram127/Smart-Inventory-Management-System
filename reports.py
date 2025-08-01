from firebase_config import db
from datetime import datetime

def reports_menu(user):
    while True:
        print("\n--- Reports ---")
        print("1. View Current Stock Levels")
        print("2. Products Running Low")
        print("3. Top Selling Items")
        print("4. Inventory Value")
        print("5. Back to Main Menu\n")
        choice = input("Enter choice: ").strip()
        if choice == '1':
            view_stock()
        elif choice == '2':
            products_running_low()
        elif choice == '3':
            top_selling_items()
        elif choice == '4':
            inventory_value()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Try again.\n")

def view_stock():
    print("--- Current Stock Levels ---")
    products = db.collection("Products").stream()
    for p in products:
        d = p.to_dict()
        if d is not None:
            print(f"{d.get('name','')} (SKU: {d.get('sku','')}): {d.get('quantity','')}")

def products_running_low():
    print("--- Products Running Low ---")
    products = db.collection("Products").stream()
    low = []
    for p in products:
        d = p.to_dict()
        if d is not None and d.get('quantity', 0) <= 10:
            low.append((d.get('name',''), d.get('quantity',0)))
    if not low:
        print("No products running low.")
    else:
        print("| Name   | Quantity |")
        print("|--------|----------|")
        for name, qty in low:
            print(f"| {name:<6} | {qty:<8} |")

def top_selling_items():
    print("--- Top Selling Items ---")
    sales = db.collection("Sales").stream()
    tally = {}
    for s in sales:
        d = s.to_dict()
        if d is not None:
            sku = d.get('sku','')
            tally[sku] = tally.get(sku, 0) + d.get('quantity_sold',0)
    sorted_items = sorted(tally.items(), key=lambda x: x[1], reverse=True)
    print("| SKU     | Quantity Sold |")
    print("|---------|---------------|")
    for sku, qty in sorted_items[:5]:
        print(f"| {sku:<7} | {qty:<13} |")

def inventory_value():
    print("--- Inventory Value ---")
    products = db.collection("Products").stream()
    total = 0
    for p in products:
        d = p.to_dict()
        if d is not None:
            total += d.get('quantity',0) * d.get('unit_price',0)
    print(f"Total Inventory Value: {total:.2f}") 