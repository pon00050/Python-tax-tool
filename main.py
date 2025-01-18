# Import the functions from the module where they're saved
from tax_utils import get_tax_value, adjust_for_standard_deduction

# Define parameters for the function call
total_income = 40200  # Example income
filing_status = "single"  # Example filing status

# Calculate adjusted gross income by applying standard deduction
try:
    adjusted_gross_income = adjust_for_standard_deduction(total_income, filing_status)
    taxable_income = adjusted_gross_income
    
    # Calculate tax value based on adjusted income
    tax_value = get_tax_value(taxable_income, filing_status)
    print(f"Total income is ${total_income:,}, taxable income is ${taxable_income:,}, and tax is ${tax_value:,}.")
except ValueError as e:
    print(f"Error: {e}")
except FileNotFoundError:
    print("Error: The tax table JSON file could not be found.")
