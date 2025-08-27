"""
Group 2.11
Jack Wilson, Ahmed Abbas, Caroline Brincks

This is a database program.

1. A user can add, remove, and update new or existing products.
2. Each product has an ID, Name, Category, Price, and Quantity that is stored in the database.
3. All of this data is stored in a csv file called inventory.csv which gets updated as the database does.
4. The user has a few other options as well, such as diplaying a product's inventory, searching for a product, calculating the total value
in each section, and displaying all products in inventory. 
"""

from utilities import safe_input

# Capitalize function that capitalizes the first letter of each word in a string
def cap(text):
    """ Takes a string as an input and capitalizes the first letter of each word in the string """
    words = text.split()
    capwords = []
    sentence = ""
    for word in words:
        capwords.append(word.capitalize())
    for w in capwords:
        sentence += w + " "
    sentence = sentence[:-1]
    return sentence


# Set up a dictionary for items
product = dict()
items = dict(product)
itemid = 1


# Opens the inventory file in read mode
try:
    with open("inventory.csv", "r") as fh:

        # Reads each line and adds previous information back to the dictionary
        for line in fh:
            if line.startswith("id"):
                continue
            line = line.strip("\n")
            split = line.split(",")
            itemid = int(split[0])
            product['name'] = split[1]
            product['category'] = split[2]
            product['price'] = float(split[3])
            product['quantity'] = int(split[4])
            items[itemid] = product.copy()
except FileNotFoundError:
    pass


# Diplay welcome message and options
print("Welcome to Grocery Store Inventory Management!")
options = """1. (N) Add a new product
2. (R) Remove a product
3. (D) Display a product's inventory
4. (U) Update a product
5. (A) Display all products
6. (V) Calculate total value per category
7. (S) Search for a product
8. (O) Display the options
9. (E) Exit"""
print(options)


# Write a loop that iterates until the user decides to exit the program
while True:  
    x = 0
    y = 0
    print("--------------------------------------------------------------------------")
    choice = input("Enter your choice: ")
    
    
# ----------------------------------------------------------------------------------------------------------------    
    # (N or 1) Adding a new product
    if choice.lower() == "n" or choice == "1":
        
        # Takes name input
        name = input("Name: ").lower()
        
        # Checks if product is already in the database and displays a warning if so
        for key in items:
            if items[key]['name'] == name:
                itemid = key
                x = 2
                inp = input("WARNING: This product is already in the database. Are you sure you want to overwrite it and continue? (Y/N): ")
                if inp not in ["Y", "y", "Yes", "yes"]:
                    x = 1
                    break
            
            # Makes sure item ID is unique
            else:
                if itemid == key:
                    itemid += 1
        
        # If the user says no above, restart the whole loop
        if x == 1:
            continue            

        # Takes the rest of the product inputs
        category = input("Category: ").lower()
        price = safe_input("Price: $", "ERROR: Price must be a postitive float.", float, 0)
        quantity = safe_input("Quantity: ", "ERROR: Quantity must be a postitive integer.", int, 1)
        
        # Updates existing product dictionary for the single item
        product['name'] = name
        product['category'] = category
        product['price'] = price
        product['quantity'] = quantity  
        
        # Adds this product and its info to the larger dictionary with a unique item ID
        # Overwrites previous entry if the name already exists
        if x == 2:
            items[itemid] = product
        # Appends entry if the name is unique
        else:
            items[itemid] = product.copy()
        print("Item added successfully!")
    
    
# ----------------------------------------------------------------------------------------------------------------
    # (R or 2) Remove product
    elif choice.lower() == "r" or choice == "2":
        itemid = int(safe_input("Enter the ID of the product to remove: ", "ERROR: Please enter an ID", int))
        
        # Checks to make sure the item ID entered exists
        if itemid in items:
            
            # If the ID exists, removes the item
            del items[itemid]
            
            # Update the IDs of the old items
            newitems = {}
            for id, info in items.items():
                if itemid < id:
                    newid = id - 1
                    newitems[newid] = info
                else:
                    newitems[id] = info
            items = newitems
            print("Item removed successfully!")
        else:
            print("Item not found!")
    
# ----------------------------------------------------------------------------------------------------------------
    # (D or 3) Display current inventory of a product
    elif choice.lower() == "d" or choice == "3":
        itemid = int(safe_input("Enter the ID of the product to display: ", "ERROR: Please enter an ID", int))
        
        # Checks to make sure the item ID entered exists
        if itemid in items:
            
            # If the ID exists, prints the information with the proper formatting
            print(f"ID: {itemid}")
            print(f"Name: {cap(items[itemid]['name'])}")
            print(f"Category: {cap(items[itemid]['category'])}")
            print(f"Price: ${items[itemid]['price']:.2f}")
            print(f"Quantity: {items[itemid]['quantity']}")
        else:
            print("Item not found!")
            

# ----------------------------------------------------------------------------------------------------------------
    # (U or 4) Update name, category, quantity and price of a product
    elif choice.lower() == "u" or choice == "4":
        itemid = int(safe_input("Enter the ID of the product to update: ", "ERROR: Please enter an ID", int))
        
        # Checks to make sure the item ID entered exists
        if itemid in items:
            
            # If the ID exists, takes new inputs
            # Input for product name
            inp = input("Would you like to update the product name? (Y/N): ")
            if inp in ["Y", "y", "Yes", "yes"]:
                oldname = items[itemid]['name']
                print(f"The current product name is: '{cap(oldname)}'")
                
                newname = input(f"Enter the new name for '{cap(oldname)}': ")
                items[itemid]['name'] = newname
                print(f"Name successfully updated from '{cap(oldname)}' to '{cap(newname)}'!")
                print()
            
            # Input for product category
            inp = input("Would you like to update the product category? (Y/N): ")
            if inp in ["Y", "y", "Yes", "yes"]:
                oldcat = items[itemid]['category']
                print(f"The current product category is: '{cap(oldcat)}'")
                
                newcat = input(f"Enter the new category for '{cap(items[itemid]['name'])}': ")
                items[itemid]['category'] = newcat
                print(f"Category successfully updated from '{cap(oldcat)}' to '{cap(newcat)}'!")
                print()
            
            # Input for product price
            inp = input("Would you like to update the product price? (Y/N): ")
            if inp in ["Y", "y", "Yes", "yes"]:
                oldprice = items[itemid]['price']
                print(f"The current product price is: ${oldprice:.2f}")
                
                newprice = price = safe_input(f"Enter the new price for '{cap(items[itemid]['name'])}': $", "ERROR: Price must be a postitive float.", float, 0)
                items[itemid]['price'] = newprice
                print(f"Price successfully updated from ${oldprice:.2f} to ${newprice:.2f}!")
                print()
            
            # Input for product quantity
            inp = input("Would you like to update the product quantity? (Y/N): ")
            if inp in ["Y", "y", "Yes", "yes"]:
                oldquantity = items[itemid]['quantity']
                print(f"The current product quantity is: {oldquantity}")
                
                newquantity = safe_input(f"Enter the new quantity for '{cap(items[itemid]['name'])}': ", "ERROR: Quantity must be a postitive integer.", int, 1)
                items[itemid]['quantity'] = newquantity
                print(f"Quantity successfully updated from {oldquantity} to {newquantity}!")
                print()
        else:
            print("Item not found!")
            
            
# ----------------------------------------------------------------------------------------------------------------
    # (A or 5) Display all products
    elif choice.lower() == "a" or choice == "5":
        
        # Prints the header with correct spacing
        print("%-3s %-35s %-14s %10s %5s" % \
              ("ID", "Name", "Category", "Price", "Quantity"))
        
        # For each item ID prints: ID, Name, Category, Price, and Quantity with correct formatting
        for itemid in items:
            name = cap(items[itemid]['name'])
            category = cap(items[itemid]['category'])
            price = items[itemid]['price']
            quantity = items[itemid]['quantity']

            if len(name) > 30:
                name = name[0:30] + "..."
            if len(category) > 13:
                category = category[0:13] + "..."
            
            if price < 999:
                price = f"{items[itemid]['price']:.2f}"
            elif price > 999 and price <= 999999:
                price = (str(f"{price:.2f}"))[:-6] + "k"
            elif price > 999999 and price <= 999999999:
                price = (str(f"{price:.2f}"))[:-9] + "M"
            else:
                price = "999M+"
            
            if quantity < 999:
                pass
            elif quantity > 999 and quantity <= 999999:
                quantity = (str(f"{quantity:.2f}"))[:-6] + "k"
            elif quantity > 999999 and quantity <= 999999999:
                quantity = (str(f"{quantity:.2f}"))[:-9] + "M"
            else:
                quantity = "999M+"
            
            print("%-3s %-35s %-14s %10s %8s" % \
                  (itemid, name , category, price, quantity))
           
            
# ----------------------------------------------------------------------------------------------------------------
    # (V or 6) Calculate the total value of category
    elif choice.lower() == "v" or choice == "6":
        
        # Creates a temporary dictionary "c"
        c = dict()
        
        # Prints the header with correct spacing
        print("%-15s %-5s" % \
              ("Category", "Value"))
        
        # Collects category, price, and quantity for each item ID
        for itemid in items:
            category = items[itemid]['category']
            price = items[itemid]['price']
            quantity = items[itemid]['quantity']
            
            # For each unique category, creates a dictionary with a corresponding price
            if category not in c:
                c[category] = price * quantity
            else:
                c[category] += price * quantity
        
        # Calculates total value by summing all the values across all categories
        totalvalue = sum(c.values())
        
        # For each category, prints the category name and its total value
        for key in c:
            print("%-15s %-5s" % \
                  (cap(key), f"${c[key]:.2f}"))
        
        # Prints the total value
        print("%-15s %-5s" % \
              ("All Products", f"${totalvalue:.2f}"))
                
                
# ----------------------------------------------------------------------------------------------------------------
    # (S or 7) Search for a product
    elif choice.lower() == "s" or choice == "7":
        name = input("Enter the name of the product to search: ").lower()
        
        # For each item ID checks to see if the searched name matches
        for itemid in items:
            
            # If the name matches, prints the product information
            if name in items[itemid]['name']:
                print(f"ID: {itemid}")
                print(f"Name: {cap(items[itemid]['name'])}")
                print(f"Category: {cap(items[itemid]['category'])}")
                print(f"Price: ${items[itemid]['price']:.2f}")
                print(f"Quantity: {items[itemid]['quantity']}")
                y = 1
        
        # If there are no matches, shows an error
        if y == 0:
            print("Item not found!")
                
                
# ----------------------------------------------------------------------------------------------------------------           
    # (O or 8) Display options
    elif choice.lower() == "o" or choice == "8":
        print(options)
        continue


# ----------------------------------------------------------------------------------------------------------------    
    # (E or 9) Exit
    elif choice.lower() == "e" or choice == "9":
        
        # Opens the inventory file in write mode
        fh = open("inventory.csv", "w")
        
        # Writes the header
        fh.write("id,name,category,price,quantity\n")
        
        # Writes each item in the current dictionary back into the inventory file
        for itemid in items:
            name = items[itemid]['name']
            category = items[itemid]['category']
            price = items[itemid]['price']
            quantity = items[itemid]['quantity']
            fh.write(f"{itemid},{name},{category},{price},{quantity}\n")
        fh.close()
        break
    

# ----------------------------------------------------------------------------------------------------------------    
    # Displays an error if an invalid option is entered
    else:
        print("Invalid option entered. Enter 8 or O to see the options.")


# ----------------------------------------------------------------------------------------------------------------     
print("Goodbye!")
            
             
        
    