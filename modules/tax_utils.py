import json
import os

def load_config():
    """Load configuration from config.json"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    with open(config_path, 'r') as f:
        return json.load(f)

CONFIG = load_config()

def adjust_for_standard_deduction(income, filing_status):
    """
    Adjust income by subtracting the standard deduction for the given filing status.
    
    Parameters:
        income (float): The income amount to adjust
        filing_status (str): The filing status to determine standard deduction
        
    Returns:
        float: Income minus standard deduction (minimum 0)
    """
    # Load standard deductions from JSON file
    deductions_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), CONFIG['data_paths']['standard_deductions'])
    with open(deductions_path, 'r') as file:
        deductions = json.load(file)
        
    # Validate filing status
    if filing_status not in deductions:
        raise ValueError(f"Invalid filing status. Must be one of: {list(deductions.keys())}")
        
    # Subtract standard deduction and ensure result is not negative
    return max(0, income - deductions[filing_status])

# Example usage
print(adjust_for_standard_deduction(135000, "married_filing_jointly"))



import json

def compute_tax(taxable_income, filing_status):
    """
    Compute the tax for a given taxable income and filing status, using tax tables for income < $100,000
    and tax rate schedules for income >= $100,000.

    Parameters:
        taxable_income (float): The taxable income.
        filing_status (str): The filing status. One of "single", "married_filing_jointly",
                             "married_filing_separately", "head_of_household".

    Returns:
        float: The computed tax amount.
        None: If the filing status is invalid or no matching tax bracket is found.
    """
    try:
        if taxable_income < 100000:
            # Use tax table for incomes below $100,000
            tax_table_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), CONFIG['data_paths']['tax_table'])
            with open(tax_table_path, 'r') as file:
                tax_table = json.load(file)

            # Validate filing status
            filing_status = filing_status.lower()
            valid_statuses = ["single", "married_filing_jointly", "married_filing_separately", "head_of_household"]
            if filing_status not in valid_statuses:
                raise ValueError(f"Invalid filing status. Must be one of: {valid_statuses}")

            # Search for the matching tax range
            for entry in tax_table:
                lower_bound = float(entry["taxable_income_range"]["LowerBound"])
                upper_bound = float(entry["taxable_income_range"]["UpperBound"])

                if lower_bound <= taxable_income < upper_bound:
                    return float(entry[filing_status])

        else:
            # Use tax rate schedule for incomes $100,000 or more
            rate_schedule_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), CONFIG['data_paths']['rate_schedule'])
            with open(rate_schedule_path, 'r') as json_file:
                tax_data = json.load(json_file)

            # Validate filing status
            if filing_status not in tax_data['tax_brackets']:
                raise ValueError(f"Invalid filing status. Available options are: {list(tax_data['tax_brackets'].keys())}")

            # Iterate through the data to find the applicable tax bracket
            for entry in tax_data['tax_brackets'][filing_status]:
                lower_bound = entry['income_range']['min']
                upper_bound = entry['income_range']['max'] if entry['income_range']['max'] is not None else float('inf')

                if lower_bound <= taxable_income < upper_bound:
                    tax_rate = entry['tax_rate']
                    subtract_amount = entry['subtract_amount']
                    return (taxable_income * tax_rate) - subtract_amount

        # If no matching bracket is found, return None
        return None

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Required tax file not found: {e}")
    except KeyError as e:
        raise KeyError(f"Missing expected key in tax file: {e}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while computing tax: {e}")

# Example usage:
# tax = compute_tax(95000, "single")
# print(tax)
# tax = compute_tax(105800, "married_filing_jointly")
# print(tax)
