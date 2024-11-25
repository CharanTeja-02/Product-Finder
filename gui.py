import tkinter as tk
from tkinter import messagebox, Toplevel
import requests

BASE_URL = "http://127.0.0.1:5000"  # Flask server address

user_role = None  
username = None  

def login_user():
    def submit_login():
        global user_role, username
        user = entry_username.get()
        pwd = entry_password.get()

        if not (user and pwd):
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        data = {"username": user, "password": pwd}
        response = requests.post(f"{BASE_URL}/login", json=data)
        if response.status_code == 200:
            user_data = response.json()
            user_role = user_data["role"]
            username = user
            messagebox.showinfo("Success", f"Logged in as {user_role}.")
            login_window.destroy()
            main_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    login_window = Toplevel(root)
    login_window.title("Login")

    tk.Label(login_window, text="Username:", font=("Arial", 14)).grid(row=0, column=0)
    entry_username = tk.Entry(login_window, font=("Arial", 14))
    entry_username.grid(row=0, column=1)

    tk.Label(login_window, text="Password:", font=("Arial", 14)).grid(row=1, column=0)
    entry_password = tk.Entry(login_window, show="*", font=("Arial", 14))
    entry_password.grid(row=1, column=1)

    tk.Button(login_window, text="Submit", command=submit_login, font=("Arial", 14)).grid(row=2, column=1)
    tk.Button(login_window, text="Register", command=register_user, font=("Arial", 14)).grid(row=3, column=1)


def register_user():
    def submit_registration():
        user = entry_username.get()
        pwd = entry_password.get()
        role = role_var.get()
        store = entry_store.get() if role == "Owner" else None

        if not (user and pwd and role):
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        data = {"username": user, "password": pwd, "role": role, "store": store}
        response = requests.post(f"{BASE_URL}/register", json=data)
        if response.status_code == 201:
            messagebox.showinfo("Success", "Registration successful. Please log in.")
            register_window.destroy()
        else:
            messagebox.showerror("Error", response.json().get("error", "Registration failed."))

    register_window = Toplevel(root)
    register_window.title("Register")

    tk.Label(register_window, text="Username:", font=("Arial", 14)).grid(row=0, column=0)
    entry_username = tk.Entry(register_window, font=("Arial", 14))
    entry_username.grid(row=0, column=1)

    tk.Label(register_window, text="Password:", font=("Arial", 14)).grid(row=1, column=0)
    entry_password = tk.Entry(register_window, show="*", font=("Arial", 14))
    entry_password.grid(row=1, column=1)

    tk.Label(register_window, text="Role:", font=("Arial", 14)).grid(row=2, column=0)
    role_var = tk.StringVar(value="User")
    tk.OptionMenu(register_window, role_var, "User", "Owner").grid(row=2, column=1)

    tk.Label(register_window, text="Store (for Owner only):", font=("Arial", 14)).grid(row=3, column=0)
    entry_store = tk.Entry(register_window, font=("Arial", 14))
    entry_store.grid(row=3, column=1)

    tk.Button(register_window, text="Submit", command=submit_registration, font=("Arial", 14)).grid(row=4, column=1)



def search_product():
    product_name = entry_product_name.get()
    if not product_name:
        messagebox.showwarning("Input Error", "Please enter a product name.")
        return
    response = requests.get(f"{BASE_URL}/search_product/{product_name}")
    if response.status_code == 200:
        malls = response.json()
        if not malls:
            messagebox.showinfo("Not Found", "Product is not available in any stores.")
            return
        show_malls_popup(malls)
    else:
        messagebox.showerror("Error", "Failed to fetch product details.")


def show_malls_popup(malls):
    malls_window = Toplevel(root)
    malls_window.title("Available Malls")

    tk.Label(malls_window, text="Malls", font=("Arial", 14, "bold")).pack(pady=10)

    for mall_name, mall_data in malls.items():
        mall_color = "green" if mall_data['available'] else "red"
        mall_button = tk.Button(malls_window, text=mall_name, fg=mall_color,
                                command=lambda m=mall_name: show_stores_popup(malls, m))
        mall_button.pack(pady=5)


def show_stores_popup(malls, mall_name):
    stores_window = Toplevel(root)
    stores_window.title(f"Stores in {mall_name}")

    tk.Label(stores_window, text=f"Stores in {mall_name}", font=("Arial", 12, "bold")).pack(pady=10)

    stores = malls[mall_name]['stores']
    for store in stores:
        store_color = "green" if store['available'] else "red"
        store_button = tk.Button(stores_window, text=f"{store['store']} (Floor {store['floor']})",
                                 fg=store_color,
                                 command=lambda s=store: show_product_details_popup(s))
        store_button.pack(pady=5)


def show_product_details_popup(store):
    details_window = Toplevel(root)
    details_window.title("Product Details")

    product_details = f"""
    Store: {store['store']}
    Floor: {store['floor']}
    Availability: {'Available' if store['available'] else 'Not Available'}
    """

    tk.Label(details_window, text="Product Details", font=("Arial", 12, "bold")).pack(pady=10)
    tk.Label(details_window, text=product_details, justify="left", font=("Arial", 10)).pack(pady=5)

def add_product():
    def submit_product():
        name = entry_name.get()
        mall = entry_mall.get()
        floor = entry_floor.get()
        available = var_available.get()

        if not (name and mall and floor):
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        data = {
            "username": username,
            "name": name,
            "mall": mall,
            "floor": floor,
            "available": available,
        }
        response = requests.post(f"{BASE_URL}/add_product", json=data)
        if response.status_code == 201:
            messagebox.showinfo("Success", "Product added successfully.")
            add_window.destroy()
        else:
            messagebox.showerror("Error", response.json().get("error", "Failed to add product."))

    add_window = Toplevel(root)
    add_window.title("Add Product")

    tk.Label(add_window, text="Product Name:", font=("Arial", 14)).grid(row=0, column=0)
    entry_name = tk.Entry(add_window, font=("Arial", 14))
    entry_name.grid(row=0, column=1)

    tk.Label(add_window, text="Mall:", font=("Arial", 14)).grid(row=1, column=0)
    entry_mall = tk.Entry(add_window, font=("Arial", 14))
    entry_mall.grid(row=1, column=1)

    tk.Label(add_window, text="Floor:", font=("Arial", 14)).grid(row=2, column=0)
    entry_floor = tk.Entry(add_window, font=("Arial", 14))
    entry_floor.grid(row=2, column=1)

    var_available = tk.BooleanVar()
    tk.Checkbutton(add_window, text="Available", variable=var_available, font=("Arial", 14)).grid(row=3, column=1)

    tk.Button(add_window, text="Submit", command=submit_product, font=("Arial", 14)).grid(row=4, column=1)


def delete_product():
    product_name = entry_product_name.get()
    if not product_name:
        messagebox.showwarning("Input Error", "Please enter a product name.")
        return

    data = {"username": username}
    response = requests.delete(f"{BASE_URL}/delete_product/{product_name}", json=data)
    if response.status_code == 200:
        messagebox.showinfo("Success", "Product deleted successfully.")
    else:
        messagebox.showerror("Error", response.json().get("error", "Failed to delete product."))


def update_product():
    def submit_update():
        product_name = entry_product_name.get()
        if not product_name:
            messagebox.showwarning("Input Error", "Please enter a product name.")
            return

        available = var_available.get()

        data = {"username": username, "name": product_name, "available": available}
        response = requests.put(f"{BASE_URL}/update_product", json=data)
        if response.status_code == 200:
            messagebox.showinfo("Success", response.json().get("message"))
            update_window.destroy()
        else:
            messagebox.showerror("Error", response.json().get("error", "Failed to update product."))

    update_window = Toplevel(root)
    update_window.title("Update Product")

    var_available = tk.BooleanVar()
    tk.Label(update_window, text="Set Availability:", font=("Arial", 14)).grid(row=0, column=0)
    tk.Checkbutton(update_window, text="Available", variable=var_available, font=("Arial", 14)).grid(row=0, column=1)

    tk.Button(update_window, text="Submit", command=submit_update, font=("Arial", 14)).grid(row=1, column=1)


def main_screen():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Product Finder", font=("Arial", 24)).grid(row=0, column=0, columnspan=2)

    tk.Label(root, text="Product Name:", font=("Arial", 14)).grid(row=1, column=0)
    global entry_product_name
    entry_product_name = tk.Entry(root, font=("Arial", 14))
    entry_product_name.grid(row=1, column=1)

    tk.Button(root, text="Search", command=search_product, font=("Arial", 14)).grid(row=2, column=0)

    if user_role == "Owner":
        tk.Button(root, text="Add Product", command=add_product, font=("Arial", 14)).grid(row=3, column=0)
        tk.Button(root, text="Update Product", command=update_product, font=("Arial", 14)).grid(row=3, column=1)
        tk.Button(root, text="Delete Product", command=delete_product, font=("Arial", 14)).grid(row=4, column=0)

# Initialize the application
root = tk.Tk()
root.title("Product Finder")
root.state("zoomed")  # Set the window to fullscreen mode

tk.Label(root, text="Welcome to Product Finder", font=("Arial", 20)).pack(pady=20)
tk.Button(root, text="Login", command=login_user, font=("Arial", 14)).pack(pady=10)
tk.Button(root, text="Register", command=register_user, font=("Arial", 14)).pack(pady=10)

root.mainloop()

