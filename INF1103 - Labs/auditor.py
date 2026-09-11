Inventory = 0 

Stock_quantity = str(input ("Enter a stock quantity : "))

while Stock_quantity != 500 :
    Stock_quantity = str(input ("Enter a stock quantity : "))
    Stock_quantity=Stock_quantity.lower
    if str(Stock_quantity)=="quit":
        break
    

print("Ended")
