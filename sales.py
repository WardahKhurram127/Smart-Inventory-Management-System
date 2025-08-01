from firebase_config import db
from inventory import update_stock
from datetime import datetime

def record_sale(user):
    print("--- Record Sale ---")
    sales = db.collection("Sales").stream()
    print("| Product | Quantity | Price | Date/Time | Customer | User |")
    print("|---------|----------|-------|-----------|----------|------|")
    for s in sales:
        d = s.to_dict()
        if d is not None:
            print(f"| {d.get('product_name',''):<7} | {d.get('quantity_sold',0):<8} | {d.get('sale_price',0):<5} | {d.get('date','')[:19]:<10} | {d.get('customer',''):<8} | {d.get('user',''):<4} |")

def customer_buying(user):
    print("--- Customer Buying (Cart Mode) ---")
    cart = []
    while True:
        sku = input("Enter Product SKU (or 'done' to finish): ").strip()
        if sku.lower() == 'done':
            break
        doc = db.collection("Products").document(sku).get()
        if not doc.exists:
            print("Product not found.")
            continue
        d = doc.to_dict()
        if d is None:
            print("Product data is missing or corrupted.")
            continue
        name = d.get('name','')
        current_stock = d.get('quantity', 0)
        print(f"Current stock for {name} (SKU: {sku}): {current_stock}")
        qty = int(input("Quantity to buy: ").strip())
        if qty > current_stock:
            print(f"❌ Not enough stock. Only {current_stock} available.")
            continue
        price = float(input("Sale Price (per unit): ").strip())
        cart.append({
            'sku': sku,
            'name': name,
            'qty': qty,
            'price': price,
            'current_stock': current_stock
        })
    if not cart:
        print("No items in cart. Sale cancelled.")
        return
    customer = input("Customer Name: ").strip()
    now = datetime.now().isoformat()
    for item in cart:
        update_stock(item['sku'], -item['qty'])
        sale = {
            "sku": item['sku'],
            "product_name": item['name'],
            "quantity_sold": item['qty'],
            "sale_price": item['price'],
            "date": now,
            "customer": customer,
            "user": user['email']
        }
        db.collection("Sales").add(sale)
        print(f"✔️ Sold {item['qty']} x {item['name']} at {item['price']} each. Remaining stock: {item['current_stock'] - item['qty']}")
    print("All items processed and recorded.")

def restock_product(user):
    print("--- Restock Product ---")
    # Show full inventory and highlight low stock
    products = db.collection("Products").stream()
    print("| Name   | SKU     | Category | Qty | Price | Supplier | Status |")
    print("|--------|---------|----------|-----|-------|----------|--------|")
    low_skus = set()
    for p in products:
        d = p.to_dict()
        if d is not None:
            status = ""
            if d.get('quantity', 0) <= 10:
                status = "⚠️ This product is running low and needs to be restocked!"
                low_skus.add(d.get('sku',''))
            print(f"| {d.get('name',''):<6} | {d.get('sku',''):<7} | {d.get('category',''):<8} | {d.get('quantity',''):<3} | {d.get('unit_price',0):<5.2f} | {d.get('supplier',''):<8} | {status:<6} |")
    sku = input("Enter SKU of product to restock: ").strip()
    doc = db.collection("Products").document(sku).get()
    if not doc.exists:
        print("Product not found.")
        return
    d = doc.to_dict()
    if d is None:
        print("Product data is missing or corrupted.")
        return
    current_stock = d.get('quantity', 0)
    print(f"Current stock for {d.get('name','')} (SKU: {sku}): {current_stock}")
    if sku in low_skus:
        print("⚠️ This product is running low and needs to be restocked!")
    qty_added = int(input("Quantity Added: ").strip())
    update_stock(sku, qty_added)
    restock = {
        "sku": sku,
        "product_name": d.get('name',''),
        "quantity_added": qty_added,
        "date": datetime.now().isoformat(),
        "user": user['email']
    }
    db.collection("Restocks").add(restock)
    print(f"✔️ Restock successful. New stock: {current_stock + qty_added}") 