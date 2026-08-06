
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class RetailStore:

    def __init__(self, file_name):
        self.data = pd.read_csv(file_name)

    def show_data(self):
        print("\nRetail Sales Data")
        print(self.data)

    def total_sales(self):
        total = self.data["Total Sales"].sum()
        print("\nTotal Sales =", total)

    def quantity_report(self):
        quantity = np.array(self.data["Quantity Sold"])

        print("\nQuantity Report")
        print(quantity)

        print("Maximum Quantity :", np.max(quantity))
        print("Minimum Quantity :", np.min(quantity))
        print("Average Quantity :", np.mean(quantity))

    def filter_category(self):
        category = input("Enter Category : ")

        filtered = self.data[self.data["Category"] == category]

        print("\nFiltered Data")
        print(filtered)

    def summary_report(self):
        print("\nSummary Report")
        print("Total Products :", len(self.data))
        print("Total Sales :", self.data["Total Sales"].sum())
        print("Average Sales :", self.data["Total Sales"].mean())

    def bar_chart(self):
        sales = self.data.groupby("Category")["Total Sales"].sum()

        plt.bar(sales.index, sales.values)
        plt.title("Category Wise Sales")
        plt.xlabel("Category")
        plt.ylabel("Sales")
        plt.show()

    def line_graph(self):
        plt.plot(self.data["Product"], self.data["Total Sales"], marker="o")
        plt.title("Product Wise Sales")
        plt.xlabel("Product")
        plt.ylabel("Sales")
        plt.xticks(rotation=45)
        plt.show()

    def heat_map(self):
        data = self.data[["Price", "Quantity Sold", "Total Sales"]]
        sns.heatmap(data.corr(), annot=True)
        plt.title("Heatmap")
        plt.show()


def get_choice(prompt, valid_choices):
    """Safely reads an integer choice, re-prompting on bad input."""
    while True:
        raw = input(prompt)
        if raw.isdigit() and int(raw) in valid_choices:
            return int(raw)
        print("Invalid Choice")


def main():
    store = RetailStore(r"C:\Users\Rapid02\Downloads\retail_sales.csv")

    menu_text = """
RETAIL SALES ANALYZER
1. Show Data
2. Total Sales
3. Quantity Report
4. Filter Category
5. Summary Report
6. Bar Chart
7. Line Graph
8. Heatmap
9. Exit
"""

    while True:
        print(menu_text)
        choice = get_choice("Enter Your Choice : ", range(1, 10))

        if choice == 1:
            store.show_data()
        elif choice == 2:
            store.total_sales()
        elif choice == 3:
            store.quantity_report()
        elif choice == 4:
            store.filter_category()
        elif choice == 5:
            store.summary_report()
        elif choice == 6:
            store.bar_chart()
        elif choice == 7:
            store.line_graph()
        elif choice == 8:
            store.heat_map()
        elif choice == 9:
            print("Thank You")
            break


if __name__ == "__main__":
    main()
