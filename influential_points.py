# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 05:18:00 2025
@author: RebeLab
"""

from scipy.stats import f
import pandas as pd

def calculate_influential_cutoffs():
    """
    Prompts user for regression parameters and calculates Cook's Distance 
    and Leverage point cut-offs based on statistical models.
    """
    while True:
        try:
            P = int(input('Please enter the number of predictors including the intercept (P): '))
            n = int(input('Please enter the number of data points (n): '))
            d = int(input('Please enter the number of independent variables excluding the intercept (d): '))

            if n <= P:
                print("Error: Number of data points (n) must be greater than the number of predictors (P).")
                continue  

            break  
        except ValueError:
            print('Error: Please enter valid numeric values.')

    df1 = P
    df2 = n - P
    alpha = 0.20  

    # Compute cutoffs
    f_critical1 = f.ppf(1 - alpha, df1, df2)  # Cook's Distance (Method i)
    f_critical2 = 4 / (n - d - 1)  # Cook's Distance (Method ii)
    f_critical3 = (2 * P) / n  # Leverage Cut-off

    # Print cut-off values in a formatted table
    print("\n🔹 **Data Points Cutoff** 🔹")
    print("=" * 60)
    print(f"{'Reference':<10}{'Criterion':<30}{'Cut-off Value':<20}")
    print("=" * 60)
    print(f"{'i':<10}{'Cook’s Distance Cut-off':<30}{f_critical1:<20.4f}")
    print(f"{'ii':<10}{'Cook’s Distance Cut-off':<30}{f_critical2:<20.4f}")
    print(f"{'i':<10}{'Leverage Point Cut-off':<30}{f_critical3:<20.4f}")
    print("=" * 60)
    
    # References
    print("\n📖 **References:**")
    print("(i) Kutner et al., 2004. *Applied Linear Statistical Models*")
    print("(ii) Fox, 2016. *Applied Regression Analysis and Generalized Linear Models*")
    
    # Instruction for formatting the Cook's and Leverage points
    print("\n📌 **Your Cook's Distance and Leverage Points should be in this format:**")
    print("Index,Cooks_Distance,Leverage")
    print("1,0.12,0.25")
    print("2,0.45,0.30")
    print("3,0.90,0.50")
    
    # Ask if the user wants to create a sample CSV
    create_csv = input("Do you need a sample CSV file? (yes/no): ").strip().lower()
    if create_csv == "yes":
        sample_data = pd.DataFrame({
            "Index": [1, 2, 3],
            "Cooks_Distance": [0.12, 0.45, 0.90],
            "Leverage": [0.25, 0.30, 0.50]
        })
        sample_data.to_csv("sample_data.csv", index=False)
        print("✅ A sample file named 'sample_data.csv' has been created.")
    else:
        print("No sample CSV has been created...")

    # Ask user for filename
    filename = input("\nEnter the CSV filename (including .csv extension) or the full file path: ").strip()

    # Read the CSV file and process influential points
    try:
        df = pd.read_csv(filename)

        # Check if required columns are present
        required_columns = ["Index", "Cooks_Distance", "Leverage"]
        if not all(column in df.columns for column in required_columns):
            raise ValueError("❌ Error: The CSV file is missing one or more required columns.")

        # Convert DataFrame to list of lists
        results = df.values.tolist()

        # Identify Influential Points
        influential_results = []
        for row in results:
            high_cooks_distance_one = row[1] > f_critical1
            high_cooks_distance_two = row[1] > f_critical2
            high_leverage = row[2] > f_critical3

            if high_cooks_distance_one and high_cooks_distance_two and high_leverage:
                status = "Influential"
            elif high_cooks_distance_one and high_leverage:
                status = "Influential(i)"
            elif high_cooks_distance_two and high_leverage:
                status = "Influential(ii)"
            else:
                status = "Normal"
            
            # Store only Influential Points
            if "Influential" in status:
                influential_results.append((row[0], row[1], row[2], status))

        # Print table with only Influential Points
        if influential_results:
            print("\n📌 **Influential Data Points**:")
            print("=" * 60)
            print(f"{'Index':<10}{'Cook’s Distance':<20}{'Leverage':<15}{'Status':<20}")
            print("=" * 60)

            for row in influential_results:
                print(f"{int(row[0]):<10}{row[1]:<20.4f}{row[2]:<15.4f}{row[3]:<20}")

            print("=" * 60)
        else:
            print("\n✅ No influential data points found.")

    except FileNotFoundError:
        print(f"❌ Error: The file '{filename}' was not found. Please try again.")
    except pd.errors.EmptyDataError:
        print(f"❌ Error: The file '{filename}' is empty. Please provide a valid CSV file.")
    except pd.errors.ParserError:
        print(f"❌ Error: The file '{filename}' is not formatted correctly. Check for missing or extra commas.")
    except ValueError as e:
        print(e)

# Ensuring the script runs only if executed directly
if __name__ == "__main__":
    calculate_influential_cutoffs()
