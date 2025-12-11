import csv

products = []
with open("Products.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        products.append(row)

print("----- Product List -----")
for p in products:
    print(f"ID: {p['product_id']}, Name: {p['product_name']}, Category: {p['category']}, Price: {p['price']}, Qty: {p['quantity']}")


print("\n-> Total rows:", len(products))

count_above_500 = 0
for p in products:
    if int(p['price']) > 500:
        count_above_500 += 1

print("->Products priced above 500:", count_above_500)

total_price = 0
for p in products:
    total_price += int(p['price'])

average_price = total_price / len(products)
print("->Average price:", average_price)

category_input = input("\n Enter category name: ")

print(f"\n->Products in category '{category_input}':")
for p in products:
    if p['category'].lower() == category_input.lower():
        print(p['product_name'])

total_qty = 0
for p in products:
    total_qty += int(p['quantity'])

print("\n->Total quantity of all items in stock:", total_qty)
