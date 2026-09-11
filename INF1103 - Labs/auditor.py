total_inventory = 0
failednumber=0


while True:
    entry = input("Enter stock quantity: ")

    if entry == "quit":
        break

    try:
        quantity = int(entry)
    except ValueError:
        print("Invalid number entered. Try again. ")
        failednumber += 1
        continue

    if quantity < 0:
        print("No negative numbers. Try again.")
        failednumber += 1
        continue

    if total_inventory > 500:
        print("Overstock detected.")
        
        break
    else:
        total_inventory = total_inventory+quantity
        print("Total Inventory: " + str(total_inventory))

print("Number of failed attempts is " + str(failednumber))
print("Total Inventory is " + str(total_inventory))