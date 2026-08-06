Sales Data Analyzer & Visualizer

Project Overview

Sales Data Analyzer & Visualizer is a Python project that loads sales data from a CSV file, performs data analysis, handles missing values, generates statistical summaries, and creates different types of charts using Pandas, NumPy, Matplotlib, and Seaborn.

Features
Load CSV dataset
View first and last records
 Display column names and data types
 Search, sort, and filter data
 Create Pivot Tables
 Convert DataFrame columns to NumPy arrays
 Handle missing values
 Generate descriptive statistics
 Create charts:
   Bar Chart
   Line Chart
   Scatter Plot
   Pie Chart
   Histogram
   Stack Plot
 Export generated charts as image files

Technologies Used

 Python 3
 Pandas
 NumPy
 Matplotlib
 Seaborn

Required Libraries

Install the required libraries using:

pip install pandas numpy matplotlib seaborn

Project Structure

Sales_Data_Analyzer/
 sales_analyzer.py
 sales_data.csv
 README.md

How to Run
Run the project using:
python sales_analyzer.py
Menu Options

 Load Dataset
  Explore Data
 DataFrame Operations
 Clean Missing Data
 Descriptive Statistics
 Data Visualization
 Export Plot to Image
 Exit Application

Sample Dataset

The program automatically creates a default "sales_data.csv" file if it does not exist.

Columns:
SalesID
 Product
 Region
 Sales
 Year

Output

The application can:

 Display dataset information
 Perform analysis
 Show graphs
 Save graphs as PNG image files
