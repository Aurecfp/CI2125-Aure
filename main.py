import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventory Management System")
        self.root.geometry("800x600")
        self.root.configure(bg="#f2f2f2")

        # Database connection
        self.conn = sqlite3.connect("inventory.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        # GUI Components
        self.create_widgets()
        self.check_low_stock()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL
        )
        """)
        self.conn.commit()

    def create_widgets(self):
        # Frame for form inputs
        form_frame = tk.Frame(self.root, bg="#f2f2f2", padx=10, pady=10)
        form_frame.pack(fill="x", pady=10)

        # Labels and Entry widgets
        tk.Label(form_frame, text="Product Name:", bg="#f2f2f2", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.product_name = tk.Entry(form_frame, font=("Arial", 12), width=30)
        self.product_name.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Quantity:", bg="#f2f2f2", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.quantity = tk.Entry(form_frame, font=("Arial", 12), width=30)
        self.quantity.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Price:", bg="#f2f2f2", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.price = tk.Entry(form_frame, font=("Arial", 12), width=30)
        self.price.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Search:", bg="#f2f2f2", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.search = tk.Entry(form_frame, font=("Arial", 12), width=30)
        self.search.grid(row=3, column=1, padx=10, pady=5)

        tk.Button(form_frame, text="Search", command=self.search_item, bg="#4CAF50", fg="white", font=("Arial", 12)).grid(row=3, column=2, padx=10, pady=5)

        # Frame for buttons
        button_frame = tk.Frame(self.root, bg="#f2f2f2", pady=10)
        button_frame.pack(fill="x")

        tk.Button(button_frame, text="Add Item", command=self.add_item, bg="#4CAF50", fg="white", font=("Arial", 12), width=15).pack(side="left", padx=10)
        tk.Button(button_frame, text="Update Item", command=self.update_item, bg="#2196F3", fg="white", font=("Arial", 12), width=15).pack(side="left", padx=10)
        tk.Button(button_frame, text="Delete Item", command=self.delete_item, bg="#f44336", fg="white", font=("Arial", 12), width=15).pack(side="left", padx=10)
        tk.Button(button_frame, text="Check Stock", command=self.check_stock_levels, bg="#FFC107", fg="black", font=("Arial", 12), width=15).pack(side="left", padx=10)

        # Frame for Treeview
        tree_frame = tk.Frame(self.root, bg="#f2f2f2")
        tree_frame.pack(fill="both", expand=True, pady=10, padx=10)

        columns = ("id", "name", "quantity", "price")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Product Name")
        self.tree.heading("quantity", text="Quantity")
        self.tree.heading("price", text="Price")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=200, anchor="w")
        self.tree.column("quantity", width=100, anchor="center")
        self.tree.column("price", width=100, anchor="center")

        self.tree.pack(fill="both", expand=True, pady=10)

        # Style Treeview
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 12), rowheight=25, fieldbackground="#ffffff", background="#ffffff")
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#E0E0E0")
        style.map("Treeview", background=[("selected", "#D3D3D3")])

        # Bind row selection
        self.tree.bind("<Double-1>", self.load_selected_item)

        self.refresh_tree()

    def add_item(self):
        name = self.product_name.get()
        quantity = self.quantity.get()
        price = self.price.get()

        if not name or not quantity.isdigit() or not price.replace('.', '', 1).isdigit():
            messagebox.showerror("Input Error", "Please enter valid inputs.")
            return

        self.cursor.execute("INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)", (name, int(quantity), float(price)))
        self.conn.commit()
        self.refresh_tree()
        self.clear_entries()

    def update_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select an item to update.")
            return

        item_id = self.tree.item(selected_item, "values")[0]
        name = self.product_name.get()
        quantity = self.quantity.get()
        price = self.price.get()

        if not name or not quantity.isdigit() or not price.replace('.', '', 1).isdigit():
            messagebox.showerror("Input Error", "Please enter valid inputs.")
            return

        self.cursor.execute("UPDATE inventory SET name = ?, quantity = ?, price = ? WHERE id = ?", (name, int(quantity), float(price), item_id))
        self.conn.commit()
        self.refresh_tree()
        self.clear_entries()

    def delete_item(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select an item to delete.")
            return

        item_id = self.tree.item(selected_item, "values")[0]
        self.cursor.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
        self.conn.commit()
        self.refresh_tree()
        self.clear_entries()

    def search_item(self):
        search_term = self.search.get().lower()
        if not search_term:
            messagebox.showerror("Search Error", "Please enter a term to search.")
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.cursor.execute("SELECT * FROM inventory WHERE LOWER(name) LIKE ?", (f"%{search_term}%",))
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def refresh_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.cursor.execute("SELECT * FROM inventory")
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def clear_entries(self):
        self.product_name.delete(0, tk.END)
        self.quantity.delete(0, tk.END)
        self.price.delete(0, tk.END)
        self.search.delete(0, tk.END)

    def load_selected_item(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item_id, name, quantity, price = self.tree.item(selected_item, "values")

        self.product_name.delete(0, tk.END)
        self.product_name.insert(0, name)

        self.quantity.delete(0, tk.END)
        self.quantity.insert(0, quantity)

        self.price.delete(0, tk.END)
        self.price.insert(0, price)

    def check_stock_levels(self):
        stock_levels = []
        self.cursor.execute("SELECT name, quantity FROM inventory")
        for name, quantity in self.cursor.fetchall():
            stock_levels.append(f"{name}: {quantity} units")

        if stock_levels:
            messagebox.showinfo("Stock Levels", "\n".join(stock_levels))
        else:
            messagebox.showinfo("Stock Levels", "No items in inventory.")

    def check_low_stock(self):
        low_stock_items = []
        self.cursor.execute("SELECT name, quantity FROM inventory WHERE quantity < 10")
        for name, quantity in self.cursor.fetchall():
            low_stock_items.append(f"{name} (Only {quantity} units left)")

        if low_stock_items:
            messagebox.showwarning("Low Stock Alert", "\n".join(low_stock_items))

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
