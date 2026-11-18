import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from abc import ABC, abstractmethod
from datetime import datetime

class Product:
    def __init__(self,name,price,quantity):
        self.name=name
        self.price=price
        self.__stock=quantity

    def get_stock(self):
        return self.__stock

    def add_stock(self,quantity):
        if quantity<=0:
            print("enter larger than 0") 
        else:
            self.__stock=self.__stock+quantity
            print("stock added")
    def sell(self,quantity):
        if quantity<=0:
            print("enter larger than 0")
        elif quantity>self.__stock:
            print("not enough quantity")
        else:
            self.__stock=self.__stock-quantity
            print("stock removed")

    def display(self):
        print("--- Product Details ---")
        print("Name:", self.name)
        print("Price: Rs.", self.price)
        print("Stock:", self.__stock)

class PerishableProduct(Product):

    def __init__(self, name, price, stock, expiry_date):
        super().__init__(name, price, stock)
        self.expiry_date = expiry_date

    def display(self):
        super().display()
        print("Expiry date:", self.expiry_date)

class Discount(ABC):
    @abstractmethod
    def calculate(self,amount):
        pass

class NoDiscount(Discount):
    def calculate(self,amount):
            return 0

class RegularDiscount(Discount):
    def calculate(self,amount):
        return amount * 10 / 100

class Shop:

    def __init__(self):
        self.products = {}
        self.sales = []

        self.products[1] = Product("Notebook", 50, 20)
        self.products[2] = Product("Pen", 10, 30)
        self.products[3] = Product("Pencil", 5, 25)

    def view_products(self):
            if len(self.products) == 0:
                print("No products available")
            else:
                for product_id, product in self.products.items():
                    print("Product ID:", product_id)
                    product.display()
                    print()

    def add_product(self):
        product_id = int(input("Enter product ID: "))
        if product_id <= 0:
            print("Product ID must be positive")
            return
        if product_id in self.products:
            print("Product ID already exists")
            return
        print("1. Normal product")
        print("2. Perishable product")
        product_type = int(input("Enter product type: "))

        if product_type != 1 and product_type !=2:
            print("Invalid product type")
            return
        name = input("Enter product name: ")
        price = float(input("Enter price: "))
        stock = int(input("Enter stock: "))
        if name == "" or price <= 0 or stock < 0:
                print("Invalid product details")
                return
        if product_type==1:
                product = Product(name, price, stock)
        else:
            expiry_date = input("Enter expiry date (DD-MM-YYYY): ")

            try:
                datetime.strptime(expiry_date, "%d-%m-%Y")
            except ValueError:
                print("Invalid expiry date")
                return
            product = PerishableProduct(name, price, stock, expiry_date)

        self.products[product_id] = product
        print("Product added successfully")
    def add_stock(self):
            product_id = int(input("Enter product ID: "))
            if product_id in self.products:
                quantity = int(input("Enter quantity to add: "))
                if quantity <= 0:
                    print("Quantity must be greater than zero")
                else:
                    self.products[product_id].add_stock(quantity)
            else:
                print("Product not found")

    def search_product(self):
            name = input("Enter product name: ")
            found = False
            for product_id, product in self.products.items():
                if name.lower() in product.name.lower():
                    print("Product ID:", product_id)
                    product.display()
                    found = True
            if found == False:
                print("Product not found")

    def create_bill(self):
            product_id = int(input("Enter product ID: "))
            
            if product_id not in self.products:
                print("Product not found")
                return
            
            product = self.products[product_id]
            quantity = int(input("Enter quantity: "))
    
            if quantity <= 0:
                print("Quantity must be greater than zero")
                return
    
            if quantity > product.get_stock():
                print("Insufficient stock")
                print("Available stock:", product.get_stock())
                return

            print("1. Normal customer")
            print("2. Regular customer - 10% discount")
            customer = int(input("Enter customer type: "))

            if customer == 1:
                 discount = NoDiscount()
            elif customer == 2:
                 discount = RegularDiscount()
            else:
                 print("Invalid customer type")
                 return
            total = product.price * quantity
            
            discount_amount = round(discount.calculate(total), 2)
            final_amount = round(total - discount_amount, 2)

            print("\n========== BILL ==========")
            print("Product:", product.name)
            print("Price:", product.price)
            print("Quantity:", quantity)
            print("Total:", total)
            print("Discount:", discount_amount)
            print("Amount to pay:", final_amount)
            print("==========================")

            confirm = input("Confirm sale? Enter yes or no: ")
            
            if confirm.lower() == "yes":
                product.sell(quantity)
            
                sale = {
                        "Product ID": product_id,
                        "Product": product.name,
                        "Quantity": quantity,
                        "Amount": final_amount
                          }
            
                self.sales.append(sale)
                print("Sale completed")
            else:
                print("Sale cancelled")

    def view_sales(self):
            if len(self.sales) == 0:
                print("No sales recorded")
            else:
                for sale in self.sales:
                    print("Product ID:", sale["Product ID"])
                    print("Product:", sale["Product"])
                    print("Quantity:", sale["Quantity"])
                    print("Amount:", sale["Amount"])
                    print("---------------------------------")

    def analyse_sales(self):
            if len(self.sales) == 0:
                print("No sales to analyse")
                return
            amounts = []
            total_quantity = 0
    
            for sale in self.sales:
                amounts.append(sale["Amount"])
                total_quantity += sale["Quantity"]
    
            amounts_array = np.array(amounts)
            print("\n===== SALES ANALYSIS =====")
            print("Number of sales:", len(self.sales))
            print("Total items sold:", total_quantity)
            print("Total revenue:", round(np.sum(amounts_array), 2))
            print("Average bill:", round(np.mean(amounts_array), 2))
            print("Highest bill:", np.max(amounts_array))
            print("Lowest bill:", np.min(amounts_array))
            print()
            print("\n===== SALES TABLE =====")
            table = pd.DataFrame(self.sales)
            print(table)
    def sales_chart(self):
            if len(self.sales) == 0:
                print("No sales to display")
                return
    
            sale_numbers = []
            amounts = []
            number = 1
    
            for sale in self.sales:
                sale_numbers.append(number)
                amounts.append(sale["Amount"])
                number += 1
    
            plt.bar(sale_numbers, amounts)
            plt.xlabel("Sale Number")
            plt.ylabel("Amount")
            plt.title("Shop Sales")
            plt.show()

shop = Shop()

while True:
    print("\n===== SHOP MANAGEMENT =====")
    print("1. View products")
    print("2. Add product")
    print("3. Add stock")
    print("4. Search product")
    print("5. Create bill")
    print("6. View sales")
    print("7. Sales analysis")
    print("8. Sales chart")
    print("0. Exit")

    try:
         choice = int(input("Enter your choice: "))
         if choice == 1:
              shop.view_products()
         elif choice == 2:
              shop.add_product()
         elif choice == 3:
              shop.add_stock()
         elif choice == 4:
              shop.search_product()
         elif choice == 5:
              shop.create_bill()
         elif choice == 6:
              shop.view_sales()
         elif choice == 7:
              shop.analyse_sales()
         elif choice == 8:
              shop.sales_chart()
         elif choice == 0:
              print("Thank you")
              break
         else:
            print("Invalid choice")
    except ValueError:
         print("Invalid input.")



                   