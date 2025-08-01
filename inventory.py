from firebase_config import db

def inventory_menu(user):
    while True:
        print("\n--- Inventory Management ---")
        print("1. Add New Product")
        print("2. View All Products")
        print("3. Search Products")
        print("4. Edit Product")
        print("5. Delete Product")
        print("6. Back to Main Menu\n")
        choice = input("Enter choice: ").strip()
        if choice == '1':
            add_product()
        elif choice == '2':
            view_products()
        elif choice == '3':
            search_products()
        elif choice == '4':
            edit_product()
        elif choice == '5':
            delete_product()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Try again.\n")

def add_product():
    print("--- Add New Product ---")
    name = input("Product Name: ").strip()
    sku = input("SKU: ").strip()
    desc = input("Description: ").strip()
    category = input("Category: ").strip()
    qty = int(input("Quantity: ").strip())
    price = float(input("Unit Price: ").strip())
    supplier = input("Supplier: ").strip()
    product = {
        "name": name,
        "sku": sku,
        "description": desc,
        "category": category,
        "quantity": qty,
        "unit_price": price,
        "supplier": supplier
    }
    db.collection("Products").document(sku).set(product)
    print("✔️ Product added successfully.")

def view_products():
    print("--- View All Products ---")
    products = db.collection("Products").stream()
    print("| Name   | SKU     | Category | Qty | Price | Supplier |")
    print("|--------|---------|----------|-----|-------|----------|")
    for p in products:
        d = p.to_dict()
        if d is not None:
            print(f"| {d.get('name',''):<6} | {d.get('sku',''):<7} | {d.get('category',''):<8} | {d.get('quantity',''):<3} | {d.get('unit_price',0):<5.2f} | {d.get('supplier',''):<8} |")

def search_products():
    print("--- Search Products ---")
    term = input("Enter product name, category, or supplier: ").strip().lower()
    products = db.collection("Products").stream()
    found = False
    for p in products:
        d = p.to_dict()
        if d is not None:
            if term in d.get('name','').lower() or term in d.get('category','').lower() or term in d.get('supplier','').lower():
                print(d)
                found = True
    if not found:
        print("No matching products found.")

def edit_product():
    print("--- Edit Product ---")
    sku = input("Enter SKU of product to edit: ").strip()
    doc = db.collection("Products").document(sku).get()
    if not doc.exists:
        print("Product not found.")
        return
    d = doc.to_dict()
    if d is None:
        print("Product data is missing or corrupted.")
        return
    print(f"Editing {d.get('name','')} (SKU: {sku})")
    name = input(f"Product Name [{d.get('name','')}]: ").strip() or d.get('name','')
    desc = input(f"Description [{d.get('description','')}]: ").strip() or d.get('description','')
    category = input(f"Category [{d.get('category','')}]: ").strip() or d.get('category','')
    qty = input(f"Quantity [{d.get('quantity','')}]: ").strip() or d.get('quantity','')
    price = input(f"Unit Price [{d.get('unit_price','')}]: ").strip() or d.get('unit_price','')
    supplier = input(f"Supplier [{d.get('supplier','')}]: ").strip() or d.get('supplier','')
    product = {
        "name": name,
        "sku": sku,
        "description": desc,
        "category": category,
        "quantity": int(qty),
        "unit_price": float(price),
        "supplier": supplier
    }
    db.collection("Products").document(sku).set(product)
    print("✔️ Product updated.")

def delete_product():
    print("--- Delete Product ---")
    sku = input("Enter SKU of product to delete: ").strip()
    db.collection("Products").document(sku).delete()
    print("✔️ Product deleted.")

def update_stock(sku, qty_change):
    doc = db.collection("Products").document(sku).get()
    if not doc.exists:
        print("Product not found.")
        return
    d = doc.to_dict()
    if d is None:
        print("Product data is missing or corrupted.")
        return
    new_qty = d.get('quantity', 0) + qty_change
    db.collection("Products").document(sku).update({"quantity": new_qty}) 