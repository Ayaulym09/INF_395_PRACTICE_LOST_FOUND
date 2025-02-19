import json
from datetime import datetime, timedelta
import random
import tkinter as tk
from tkinter import ttk, messagebox
import time


class LostAndFoundSystem:
    """
    Core system class that handles data management and business logic
    for the Lost and Found system.
    """

    def __init__(self):
        # Initialize system variables
        self.items = []  # List to store all items
        self.next_id = 1  # Auto-incrementing ID for items
        self.user_points = {}  # Dictionary to store user points

        # Load existing data or create new file
        try:
            self.load_data()
        except FileNotFoundError:
            self.save_data()  # Create initial empty file

    def load_data(self):
        """Load system data from JSON file."""
        try:
            with open('lost_and_found.json', 'r') as file:
                data = json.load(file)
                self.items = data['items']
                self.next_id = data['next_id']
                self.user_points = data['user_points']
        except FileNotFoundError:
            # Initialize empty data if file doesn't exist
            self.items = []
            self.next_id = 1
            self.user_points = {}

    def save_data(self):
        """Save system data to JSON file."""
        with open('lost_and_found.json', 'w') as file:
            json.dump({
                'items': self.items,
                'next_id': self.next_id,
                'user_points': self.user_points
            }, file, indent=2)


class LostAndFoundGUI:
    """
    GUI class that handles all user interface elements and interactions.
    """

    def __init__(self, root):
        # Initialize main window
        self.root = root
        self.root.title("Lost and Found System")
        self.root.geometry("800x600")

        # Create instance of the core system
        self.system = LostAndFoundSystem()

        # Create tabbed interface
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=5)

        # Initialize tabs
        self.report_tab = ttk.Frame(self.notebook)
        self.search_tab = ttk.Frame(self.notebook)
        self.view_tab = ttk.Frame(self.notebook)
        self.claim_tab = ttk.Frame(self.notebook)

        # Add tabs to notebook
        self.notebook.add(self.report_tab, text="Report Item")
        self.notebook.add(self.search_tab, text="Search Items")
        self.notebook.add(self.view_tab, text="View Unclaimed")
        self.notebook.add(self.claim_tab, text="Claim Item")

        # Setup individual tabs
        self.setup_report_tab()
        self.setup_search_tab()
        self.setup_view_tab()
        self.setup_claim_tab()

    def setup_report_tab(self):
        """Setup the Report Item tab with form fields."""
        # Create main frame
        frame = ttk.LabelFrame(self.report_tab, text="Report a Found Item", padding="10")
        frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Item Name field
        ttk.Label(frame, text="Item Name:").grid(row=0, column=0, sticky='w', pady=5)
        self.item_name = ttk.Entry(frame, width=40)
        self.item_name.grid(row=0, column=1, sticky='w', pady=5)

        # Category dropdown
        ttk.Label(frame, text="Category:").grid(row=1, column=0, sticky='w', pady=5)
        self.category = ttk.Combobox(frame, values=["Electronics", "Clothing", "Books", "Other"], width=37)
        self.category.grid(row=1, column=1, sticky='w', pady=5)

        # Location field
        ttk.Label(frame, text="Location:").grid(row=2, column=0, sticky='w', pady=5)
        self.location = ttk.Entry(frame, width=40)
        self.location.grid(row=2, column=1, sticky='w', pady=5)

        # Reporter Name field
        ttk.Label(frame, text="Your Name:").grid(row=3, column=0, sticky='w', pady=5)
        self.reporter = ttk.Entry(frame, width=40)
        self.reporter.grid(row=3, column=1, sticky='w', pady=5)

        # Submit button
        ttk.Button(frame, text="Submit Report", command=self.report_item).grid(row=4, column=0, columnspan=2, pady=20)

    def setup_search_tab(self):
        """Setup the Search Items tab with search options and results display."""
        frame = ttk.LabelFrame(self.search_tab, text="Search Lost Items", padding="10")
        frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Search criteria selection
        ttk.Label(frame, text="Search By:").grid(row=0, column=0, sticky='w', pady=5)
        self.search_by = ttk.Combobox(frame, values=["Category", "Location", "Name"], width=37)
        self.search_by.grid(row=0, column=1, sticky='w', pady=5)

        # Search term input
        ttk.Label(frame, text="Search Term:").grid(row=1, column=0, sticky='w', pady=5)
        self.search_term = ttk.Entry(frame, width=40)
        self.search_term.grid(row=1, column=1, sticky='w', pady=5)

        # Search button
        ttk.Button(frame, text="Search", command=self.search_items).grid(row=2, column=0, columnspan=2, pady=20)

        # Results display tree
        self.search_tree = ttk.Treeview(frame, columns=("ID", "Name", "Category", "Location", "Date", "Status"),
                                        show="headings", height=10)
        self.setup_treeview(self.search_tree)
        self.search_tree.grid(row=3, column=0, columnspan=2, sticky='nsew', pady=5)

    def setup_view_tab(self):
        """Setup the View Unclaimed Items tab with refresh option and items display."""
        frame = ttk.LabelFrame(self.view_tab, text="Unclaimed Items", padding="10")
        frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Refresh button
        ttk.Button(frame, text="Refresh List", command=self.view_unclaimed).grid(row=0, column=0, pady=10)

        # Unclaimed items display tree
        self.unclaimed_tree = ttk.Treeview(frame, columns=("ID", "Name", "Category", "Location", "Date", "Status"),
                                           show="headings", height=15)
        self.setup_treeview(self.unclaimed_tree)
        self.unclaimed_tree.grid(row=1, column=0, sticky='nsew', pady=5)

    def setup_claim_tab(self):
        """Setup the Claim Item tab with ID input and claim button."""
        frame = ttk.LabelFrame(self.claim_tab, text="Claim an Item", padding="10")
        frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Item ID input
        ttk.Label(frame, text="Item ID:").grid(row=0, column=0, sticky='w', pady=5)
        self.claim_id = ttk.Entry(frame, width=20)
        self.claim_id.grid(row=0, column=1, sticky='w', pady=5)

        # Claim button
        ttk.Button(frame, text="Claim Item", command=self.claim_item).grid(row=1, column=0, columnspan=2, pady=20)

    def setup_treeview(self, tree):
        """Configure the columns and headings for a treeview widget."""
        # Setup column headings
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Category", text="Category")
        tree.heading("Location", text="Location")
        tree.heading("Date", text="Date Found")
        tree.heading("Status", text="Status")

        # Configure column widths
        tree.column("ID", width=50)
        tree.column("Name", width=150)
        tree.column("Category", width=100)
        tree.column("Location", width=100)
        tree.column("Date", width=100)
        tree.column("Status", width=80)

    def report_item(self):
        """Handle the submission of a new found item."""
        # Validate form fields
        if not all([self.item_name.get(), self.category.get(), self.location.get(), self.reporter.get()]):
            messagebox.showerror("Error", "Please fill in all fields")
            return

        # Create new item record
        item = {
            'id': self.system.next_id,
            'name': self.item_name.get(),
            'category': self.category.get(),
            'location': self.location.get(),
            'date_found': datetime.now().strftime("%Y-%m-%d"),
            'claimed': False,
            'reporter': self.reporter.get()
        }

        # Add item to system and update ID counter
        self.system.items.append(item)
        self.system.next_id += 1

        # Award and track points
        if item['reporter'] not in self.system.user_points:
            self.system.user_points[item['reporter']] = 0
        self.system.user_points[item['reporter']] += 10

        # Save changes
        self.system.save_data()

        # Show success message
        messagebox.showinfo("Success",
                            f"Item reported successfully!\nYou earned 10 points!\n"
                            f"Total points: {self.system.user_points[item['reporter']]}")

        # Clear form fields
        self.item_name.delete(0, tk.END)
        self.category.set('')
        self.location.delete(0, tk.END)
        self.reporter.delete(0, tk.END)

    def search_items(self):
        """Search for items based on user criteria and display results."""
        # Clear previous search results
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)

        search_term = self.search_term.get().lower()
        search_by = self.search_by.get()

        # Find matching items
        found_items = []
        for item in self.system.items:
            if search_by == "Category" and search_term in item['category'].lower():
                found_items.append(item)
            elif search_by == "Location" and search_term in item['location'].lower():
                found_items.append(item)
            elif search_by == "Name" and search_term in item['name'].lower():
                found_items.append(item)

        # Display results
        for item in found_items:
            status = "Claimed" if item['claimed'] else "Available"
            self.search_tree.insert("", "end", values=(item['id'], item['name'], item['category'],
                                                       item['location'], item['date_found'], status))

    def view_unclaimed(self):
        """Display all unclaimed items and check for auction status."""
        # Clear current display
        for item in self.unclaimed_tree.get_children():
            self.unclaimed_tree.delete(item)

        # Get unclaimed items
        unclaimed = [item for item in self.system.items if not item['claimed']]
        current_date = datetime.now()

        # Display items with auction status
        for item in unclaimed:
            status = "Available"
            item_date = datetime.strptime(item['date_found'], "%Y-%m-%d")
            if current_date - item_date > timedelta(days=30):
                status = "Auction"

            self.unclaimed_tree.insert("", "end", values=(item['id'], item['name'], item['category'],
                                                          item['location'], item['date_found'], status))

    def claim_item(self):
        """Process an item claim request."""
        try:
            # Validate and find item
            item_id = int(self.claim_id.get())
            item = next((item for item in self.system.items if item['id'] == item_id), None)

            if item:
                if not item['claimed']:
                    # Mark item as claimed
                    item['claimed'] = True
                    self.system.save_data()
                    messagebox.showinfo("Success", f"Item '{item['name']}' has been claimed successfully!")
                    self.claim_id.delete(0, tk.END)
                    self.view_unclaimed()  # Refresh the unclaimed items list
                else:
                    messagebox.showerror("Error", "This item has already been claimed.")
            else:
                messagebox.showerror("Error", "Item not found.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid item ID (number).")


def main():
    """Initialize and run the application."""
    root = tk.Tk()
    app = LostAndFoundGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()