class Product:
    def __init__(self, product_id, name, category, price, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price
        self.stock_quantity = stock_quantity

    def __str__(self):
        return f"ID: {self.product_id}, Name: {self.name}, Category: {self.category}, Price: {self.price}, Stock: {self.stock_quantity}"

    def update_stock(self, amount):
        if self.stock_quantity + amount < 0:
            raise ValueError("Insufficient stock to reduce.")
        self.stock_quantity += amount


class InventoryManagementSystem:
    def __init__(self):
        self.products = {}
        self.users = {'admin': {'password': 'admin123', 'role': 'Admin'}, 'user': {'password': 'user123', 'role': 'User'}}
        self.logged_in_user = None

    def login(self, username, password):
        if username in self.users and self.users[username]['password'] == password:
            self.logged_in_user = username
            print(f"Welcome, {username}!")
            return True
        else:
            print("Invalid login credentials.")
            return False

    def check_role(self):
        if self.logged_in_user:
            return self.users[self.logged_in_user]['role']
        return None

    def add_product(self, product_id, name, category, price, stock_quantity):
        if self.check_role() != 'Admin':
            print("Access Denied: Admin only.")
            return
        new_product = Product(product_id, name, category, price, stock_quantity)
        self.products[product_id] = new_product
        print(f"Product {name} added successfully.")

    def edit_product(self, product_id, name=None, category=None, price=None, stock_quantity=None):
        if self.check_role() != 'Admin':
            print("Access Denied: Admin only.")
            return
        if product_id in self.products:
            product = self.products[product_id]
            if name:
                product.name = name
            if category:
                product.category = category
            if price:
                product.price = price
            if stock_quantity is not None:
                product.stock_quantity = stock_quantity
            print(f"Product {product_id} updated.")
        else:
            print("Product not found.")

    def delete_product(self, product_id):
        if self.check_role() != 'Admin':
            print("Access Denied: Admin only.")
            return
        if product_id in self.products:
            del self.products[product_id]
            print(f"Product {product_id} deleted.")
        else:
            print("Product not found.")

    def view_products(self):
        if not self.products:
            print("No products available.")
            return
        for product in self.products.values():
            print(product)

    def search_product(self, name=None, category=None):
        found = False
        for product in self.products.values():
            if (name and name.lower() in product.name.lower()) or (category and category.lower() in product.category.lower()):
                print(product)
                found = True
        if not found:
            print("No matching products found.")

    def adjust_stock(self, product_id, amount):
        if self.check_role() != 'Admin':
            print("Access Denied: Admin only.")
            return
        if product_id in self.products:
            product = self.products[product_id]
            try:
                product.update_stock(amount)
                print(f"Stock for {product.name} updated. New stock: {product.stock_quantity}")
            except ValueError as e:
                print(e)
        else:
            print("Product not found.")

    def check_low_stock(self, threshold=5):
        if self.check_role() != 'Admin':
            print("Access Denied: Admin only.")
            return
        print("Low stock alert:")
        for product in self.products.values():
            if product.stock_quantity <= threshold:
                print(f"{product.name} (ID: {product.product_id}) has low stock: {product.stock_quantity}")


def main():
    ims = InventoryManagementSystem()

    # Sample login
    username = input("Username: ")
    password = input("Password: ")

    if ims.login(username, password):
        while True:
            role = ims.check_role()
            print(f"Logged in as {role}")
            print("1. View Products\n2. Add Product\n3. Edit Product\n4. Delete Product\n5. Search Products\n6. Adjust Stock\n7. Check Low Stock\n8. Logout")
            
            # Adjust the options based on the role
            if role == 'Admin':
                choice = input("Enter your choice: ")
            else:  # For regular user, limit the options
                print("1. View Products\n5. Search Products\n8. Logout")
                choice = input("Enter your choice: ")

            if choice == '1':
                ims.view_products()
            elif choice == '2' and role == 'Admin':
                product_id = input("Enter product ID: ")
                name = input("Enter product name: ")
                category = input("Enter product category: ")
                price = float(input("Enter product price: "))
                stock_quantity = int(input("Enter stock quantity: "))
                ims.add_product(product_id, name, category, price, stock_quantity)
            elif choice == '3' and role == 'Admin':
                product_id = input("Enter product ID to edit: ")
                name = input("Enter new product name (or leave empty): ")
                category = input("Enter new product category (or leave empty): ")
                price = input("Enter new product price (or leave empty): ")
                price = float(price) if price else None
                stock_quantity = input("Enter new stock quantity (or leave empty): ")
                stock_quantity = int(stock_quantity) if stock_quantity else None
                ims.edit_product(product_id, name, category, price, stock_quantity)
            elif choice == '4' and role == 'Admin':
                product_id = input("Enter product ID to delete: ")
                ims.delete_product(product_id)
            elif choice == '5':
                name = input("Enter product name (or leave empty): ")
                category = input("Enter product category (or leave empty): ")
                ims.search_product(name, category)
            elif choice == '6' and role == 'Admin':
                product_id = input("Enter product ID to adjust stock: ")
                amount = int(input("Enter stock adjustment (positive to restock, negative to reduce): "))
                ims.adjust_stock(product_id, amount)
            elif choice == '7' and role == 'Admin':
                ims.check_low_stock()
            elif choice == '8':
                print("Logging out...")
                ims.logged_in_user = None
                break
            else:
                print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
