import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

FILE_DEFAULT = "sales_data.csv"


def initialize_default_dataset(filepath=FILE_DEFAULT):
    if not os.path.isfile(filepath):
        raw_info = {
            "SalesID": [101, 102, 103, 104, 105],
            "Product": [
                "Product A",
                "Product B",
                "Product C",
                "Product D",
                "Product E",
            ],
            "Region": ["North", "East", "West Coast", "South", "Central"],
            "Sales": [500, 600, 700, 800, 550],
            "Year": [2022, 2022, 2022, 2022, 2022],
        }
        dataset_df = pd.DataFrame(raw_info)
        dataset_df.to_csv(filepath, index=False)
        print(f"[Setup] Generated standard CSV dataset at '{filepath}'.")


class SalesAnalyzer:

    def __init__(self, target_path=None):
        self.df = None
        self.active_figure = None
        if target_path:
            self.load_csv(target_path)

    def __del__(self):
        plt.close("all")

    def load_csv(self, path):
        if not os.path.exists(path):
            print(f"Error: Specified file '{path}' does not exist.")
            return False
        try:
            self.df = pd.read_csv(path)
            print("CSV file successfully loaded into memory.")
            return True
        except Exception as error:
            print(f"Failed to load dataset: {error}")
            return False

    def inspect_dataset(self, selection):
        if self.df is None:
            print("No active dataset. Please load data prior to inspection.")
            return

        match selection:
            case 1:
                print("\n--- Top 5 Records ---")
                print(self.df.head())
            case 2:
                print("\n--- Bottom 5 Records ---")
                print(self.df.tail())
            case 3:
                print("\n--- Column Labels ---")
                print(list(self.df.columns))
            case 4:
                print("\n--- Data Types ---")
                print(self.df.dtypes)
            case 5:
                print("\n--- Dataset Overview ---")
                print(self.df.info())
            case _:
                print("Invalid selection choice.")

    def run_query_operations(self):
        if self.df is None:
            print("Dataset not loaded.")
            return

        print("\n--- Search / Sort / Filter Menu ---")
        print("1. Search column for matching string")
        print("2. Sort dataset by selected column")
        print("3. Apply numeric threshold filter")

        user_selection = input("Select an option (1-3): ").strip()

        if user_selection == "1":
            target_col = input("Target column: ").strip()
            query_val = input("Search keyword: ").strip()
            if target_col in self.df.columns:
                matches = self.df[
                    self.df[target_col]
                    .astype(str)
                    .str.contains(query_val, case=False, na=False)
                ]
                print(matches)
            else:
                print("Specified column does not exist.")

        elif user_selection == "2":
            sort_col = input("Column to sort: ").strip()
            is_asc = (
                input("Sort in ascending order? (y/n): ").strip().lower()
                == "y"
            )
            if sort_col in self.df.columns:
                sorted_records = self.df.sort_values(
                    by=sort_col, ascending=is_asc
                )
                print(sorted_records.head(10))
            else:
                print("Specified column does not exist.")

        elif user_selection == "3":
            num_col = input("Numeric column name: ").strip()
            if num_col in self.df.columns and np.issubdtype(
                self.df[num_col].dtype, np.number
            ):
                min_threshold = float(input(f"Show records where {num_col} > "))
                filtered_results = self.df[self.df[num_col] > min_threshold]
                print(filtered_results)
            else:
                print("Selected column is not a valid numeric column.")

    def build_pivot(self, idx_field, val_field, aggregation="sum"):
        """Creates a pivot table aggregation."""
        if self.df is None:
            print("Dataset not loaded.")
            return

        try:
            p_table = pd.pivot_table(
                self.df, values=val_field, index=idx_field, aggfunc=aggregation
            )
            print("\n--- Pivot Table Summary ---")
            print(p_table)
        except Exception as err:
            print(f"Unable to construct pivot table: {err}")

    def process_missing_values(self, clean_type):
        if self.df is None:
            print("Dataset not loaded.")
            return

        null_total = self.df.isnull().sum().sum()

        if clean_type == 1:
            if null_total == 0:
                print("\nNo missing values detected.")
            else:
                print("\n--- Records containing null values ---")
                print(self.df[self.df.isnull().any(axis=1)])
        elif clean_type == 2:
            numeric_fields = self.df.select_dtypes(include=[np.number]).columns
            self.df[numeric_fields] = self.df[numeric_fields].fillna(
                self.df[numeric_fields].mean()
            )
            print("Replaced missing values in numeric columns with mean values.")
        elif clean_type == 3:
            self.df.dropna(inplace=True)
            print("Removed all rows containing missing values.")
        elif clean_type == 4:
            custom_val = input("Enter replacement value: ").strip()
            self.df.fillna(custom_val, inplace=True)
            print(f"Replaced all missing entries with '{custom_val}'.")

    def print_statistical_summary(self):
        if self.df is None:
            print("Dataset not loaded.")
            return

        print("\n--- Summary Statistics ---")
        print(self.df.describe())

        numeric_data = self.df.select_dtypes(include=[np.number])
        if not numeric_data.empty:
            print("\nVariance Distribution:\n", numeric_data.var())
            print(
                "\nQuantiles (25% & 75%):\n",
                numeric_data.quantile([0.25, 0.75]),
            )

    def generate_chart(self, chart_choice):
        if self.df is None:
            print("Dataset not loaded.")
            return

        fig, axis = plt.subplots(figsize=(8, 5))
        sns.set_theme(style="whitegrid")

        try:
            if chart_choice == 1:  # Bar Chart
                x_name = input("X-axis column: ").strip()
                y_name = input("Y-axis column: ").strip()
                sns.barplot(data=self.df, x=x_name, y=y_name, ax=axis)
                plt.title(f"Bar Chart: {y_name} by {x_name}")

            elif chart_choice == 2:  # Line Chart
                x_name = input("X-axis column: ").strip()
                y_name = input("Y-axis column: ").strip()
                sns.lineplot(data=self.df, x=x_name, y=y_name, ax=axis)
                plt.title(f"Line Plot: {y_name} over {x_name}")

            elif chart_choice == 3:  # Scatter Plot
                x_name = input("X-axis column: ").strip()
                y_name = input("Y-axis column: ").strip()
                print("Rendering scatter plot...")
                sns.scatterplot(data=self.df, x=x_name, y=y_name, ax=axis)
                plt.title(f"Scatter Plot: {y_name} vs {x_name}")

            elif chart_choice == 4:  # Pie Chart
                cat_col = input("Category column for Pie Chart: ").strip()
                val_counts = self.df[cat_col].value_counts()
                axis.pie(
                    val_counts,
                    labels=val_counts.index,
                    autopct="%1.1f%%",
                    startangle=140,
                )
                plt.title(f"Distribution of {cat_col}")

            elif chart_choice == 5:  # Histogram
                num_col = input("Numeric column for distribution: ").strip()
                sns.histplot(self.df[num_col], kde=True, ax=axis)
                plt.title(f"Histogram: {num_col}")

            elif chart_choice == 6:  # Stack Plot
                numeric_cols = self.df.select_dtypes(
                    include=[np.number]
                ).columns[:3]
                if len(numeric_cols) > 1:
                    axis.stackplot(
                        range(len(self.df)),
                        [self.df[col] for col in numeric_cols],
                        labels=numeric_cols,
                    )
                    axis.legend(loc="upper left")
                    plt.title("Cumulative Area Stack Plot")
                else:
                    print("Not enough numerical columns for stack plot.")
                    plt.close(fig)
                    return

            else:
                print("Invalid plot selection.")
                plt.close(fig)
                return

            self.active_figure = fig
            plt.tight_layout()
            print("Visualization rendered successfully.")
            plt.show()

        except Exception as ex:
            print(f"Error rendering chart: {ex}")
            plt.close(fig)

    def export_chart(self, output_name):
        """Saves current plot figure to file."""
        if self.active_figure is None:
            print("No generated plot found to save.")
            return
        try:
            self.active_figure.savefig(
                output_name, dpi=300, bbox_inches="tight"
            )
            print(f"Plot saved as '{output_name}'.")
        except Exception as ex:
            print(f"Failed to export image: {ex}")


def run_app():
    initialize_default_dataset(FILE_DEFAULT)
    app_engine = SalesAnalyzer()

    while True:
        print("\n" + "=" * 50)
        print("     SALES DATA ANALYZER & VISUALIZER")
        print("=" * 50)
        print("1. Load Dataset")
        print("2. Explore Data")
        print("3. DataFrame Operations")
        print("4. Clean Missing Data")
        print("5. Descriptive Statistics")
        print("6. Data Visualization")
        print("7. Export Plot to Image")
        print("8. Exit Application")
        print("=" * 50)

        user_input = input("\nEnter choice (1-8): ").strip()

        if user_input == "1":
            print("\n-- Load File --")
            file_path = input(
                "Enter CSV path (Leave empty for default): "
            ).strip()
            if not file_path:
                file_path = FILE_DEFAULT
            app_engine.load_csv(file_path)

        elif user_input == "2":
            print("\n-- Data Exploration --")
            print("1. View first 5 rows")
            print("2. View last 5 rows")
            print("3. View column names")
            print("4. View column data types")
            print("5. View summary info")
            sub_choice = input("Enter choice: ").strip()
            if sub_choice.isdigit():
                app_engine.inspect_dataset(int(sub_choice))

        elif user_input == "3":
            print("\n-- Data Manipulation --")
            print("1. Search, Sort, or Filter Data")
            print("2. Create Pivot Table")
            print("3. Export Column to NumPy Array")
            sub_choice = input("Select operation (1-3): ").strip()

            if sub_choice == "1":
                app_engine.run_query_operations()
            elif sub_choice == "2":
                idx_field = input("Row index column: ").strip()
                val_field = input("Target value column: ").strip()
                app_engine.build_pivot(idx_field, val_field)
            elif sub_choice == "3":
                col_name = input("Column name: ").strip()
                if (
                    app_engine.df is not None
                    and col_name in app_engine.df.columns
                ):
                    np_array = app_engine.df[col_name].to_numpy()
                    print(f"Converted Array:\n{np_array}")
                else:
                    print("Invalid column selection or dataset uninitialized.")

        elif user_input == "4":
            print("\n-- Missing Data Handler --")
            print("1. Find rows containing missing entries")
            print("2. Impute missing numeric values with mean")
            print("3. Drop rows containing missing entries")
            print("4. Fill missing entries with custom value")
            sub_choice = input("Enter choice: ").strip()
            if sub_choice.isdigit():
                app_engine.process_missing_values(int(sub_choice))

        elif user_input == "5":
            app_engine.print_statistical_summary()

        elif user_input == "6":
            print("\n-- Visualization Suite --")
            print(
                "1. Bar Chart\n2. Line Chart\n3. Scatter Plot\n4. Pie Chart\n5. Histogram\n6. Stack Plot"
            )
            sub_choice = input("Select plot type (1-6): ").strip()
            if sub_choice.isdigit():
                app_engine.generate_chart(int(sub_choice))

        elif user_input == "7":
            out_filename = input("Output image name (e.g. plot.png): ").strip()
            if out_filename:
                app_engine.export_chart(out_filename)

        elif user_input == "8":
            print("Terminating program. Goodbye!")
            break
        else:
            print("Invalid input. Please enter a number between 1 and 8.")


if __name__ == "__main__":
    run_app()