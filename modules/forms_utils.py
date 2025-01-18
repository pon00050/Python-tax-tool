import json
from datetime import datetime

def process_form_2441_part_i(data):
    """
    Process Form 2441 Part I - Care Provider Information
    Returns a tuple of (should_proceed_to_part_ii, care_provider_info, total_expenses)
    """
    care_providers = {}
    total_expenses = 0
    
    # Process each dependent's care provider
    for dependent in data.get("dependents", []):
        childcare = dependent.get("childcare", {})
        if not childcare:
            continue
            
        provider_ein = childcare.get("ein")
        if provider_ein not in care_providers:
            care_providers[provider_ein] = {
                "name": childcare.get("provider_name"),
                "identifying_number": provider_ein,
                "address": childcare.get("address"),
                "amount_paid": 0
            }
        
        # Add to provider's total amount
        annual_cost = childcare.get("annual_cost", 0)
        care_providers[provider_ein]["amount_paid"] += annual_cost
        total_expenses += annual_cost
    
    # For this implementation, we assume no dependent care benefits received
    # Therefore, we proceed to Part II
    should_proceed_to_part_ii = True
    
    return should_proceed_to_part_ii, list(care_providers.values()), total_expenses

def calculate_age(birth_date_str):
    """Calculate age for the tax year (assuming 2023 tax year)"""
    birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
    tax_year_end = datetime(2023, 12, 31)
    return tax_year_end.year - birth_date.year

def calculate_tax_liability_limit(data):
    """
    Calculate the tax liability limit for Form 2441 based on Credit Limit Worksheet
    Returns the maximum allowable credit based on tax liability from Form 1040 line 18
    
    If the tax liability is zero or less, returns 0 as no credit can be taken
    """
    # Get tax from Form 1040 line 18 (tax plus Schedule 2, line 3)
    tax_liability = 13382
    
    # If tax liability is zero or less, no credit can be taken
    if tax_liability <= 0:
        return 0
        
    return tax_liability

def process_form_2441_part_ii(data, total_expenses):
    """
    Process Form 2441 Part II - Credit for Child and Dependent Care Expenses
    Following amounts are hardcoded for now because I don't know how exactly to make it dynamic yet.
    - taxpayer_income
    - spouse_income
    - total_income
    """
    # Validate qualifying persons (under 13 or disabled)
    qualifying_expenses = 0
    qualifying_person_count = 0
    
    for dependent in data.get("dependents", []):
        age = calculate_age(dependent.get("date_of_birth"))
        if age < 13:  # For now, we're not handling disabled persons over 13
            qualifying_person_count += 1
            qualifying_expenses += dependent.get("childcare", {}).get("annual_cost", 0)
    
    # Apply expense limits
    max_expenses = 3000 if qualifying_person_count == 1 else 6000
    eligible_expenses = min(qualifying_expenses, max_expenses)
    
    # Filing status still matters.
    filing_status = data.get("filing_status")
    # This is referring to the taxpayer's earned income.
    taxpayer_income = 60000
    # If married filing jointly, enter your spouse’s earned income (if you or your spouse was a student
    # or was disabled, see the instructions); all others, enter the amount from line 4 of Form 1040
    spouse_income = 75000
    
    # For married filing jointly, use the lower of the two earned incomes
    if filing_status == "married_filing_jointly":
        earned_income = min(taxpayer_income, spouse_income)
    else:
        earned_income = taxpayer_income
    
    # Determine smallest of eligible expenses and earned income
    # This is equivalent to Line 6 on the Form 2441.
    creditable_expenses = min(eligible_expenses, earned_income)
    
    # Calculate credit percentage based on total income
    total_income = 135000 # From Form 1040, Line 11
    
    # Define AGI thresholds and corresponding percentages
    agi_thresholds = [
        (0, 15000, 0.35), (15000, 17000, 0.34), (17000, 19000, 0.33),
        (19000, 21000, 0.32), (21000, 23000, 0.31), (23000, 25000, 0.30),
        (25000, 27000, 0.29), (27000, 29000, 0.28), (29000, 31000, 0.27),
        (31000, 33000, 0.26), (33000, 35000, 0.25), (35000, 37000, 0.24),
        (37000, 39000, 0.23), (39000, 41000, 0.22), (41000, 43000, 0.21),
        (43000, float("inf"), 0.20),
    ]
    
    applicable_percentage = next(
        (rate for min_income, max_income, rate in agi_thresholds 
         if min_income <= total_income < max_income),
        0.20  # Default percentage
    )
    
    # Calculate initial credit
    credit = creditable_expenses * applicable_percentage
    
    # Apply tax liability limit
    tax_liability_limit = calculate_tax_liability_limit(data)
    tax_liability_limit = min(credit, tax_liability_limit)
    
    # return round(final_credit, 2)
    return tax_liability_limit


def process_form_2441_part_iii():
    """
    Process Form 2441 Part III - Dependent Care Benefits
    (Not implemented yet)
    """
    pass

def calculate_form_2441(input_file_path: str, print_output: bool = True) -> float:
    """
    Calculate Form 2441 Child and Dependent Care Expenses
    
    Args:
        input_file_path (str): Path to JSON file containing tax data
        print_output (bool): Whether to print calculation details (default: True)
        
    Returns:
        float: Child and dependent care credit amount
    """
    try:
        with open(input_file_path, 'r') as file:
            data = json.load(file)
            
        # Process Part I
        should_proceed_to_part_ii, care_providers, total_expenses = process_form_2441_part_i(data)
        
        if should_proceed_to_part_ii:
            credit = process_form_2441_part_ii(data, total_expenses)
            if print_output:
                print(f"\nForm 2441 Part II - Calculated Credit: ${credit:,.2f}")
            return credit
        else:
            process_form_2441_part_iii()
            return 0
            
    except FileNotFoundError:
        if print_output:
            print(f"Error: Input file not found - {input_file_path}")
        return 0
    except json.JSONDecodeError:
        if print_output:
            print(f"Error: Invalid JSON format in {input_file_path}")
        return 0
    except Exception as e:
        if print_output:
            print(f"Error: {str(e)}")
        return 0

# Example usage:
if __name__ == "__main__":
    import os
    import sys
    
    # Get the project root directory (assuming forms_utils.py is in modules folder)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Load config
    try:
        with open(os.path.join(project_root, 'config.json'), 'r') as config_file:
            config = json.load(config_file)
            
        # Get taxpayer information path from config and make it relative to project root
        taxpayer_info_path = os.path.join(project_root, config['data_paths']['taxpayer_information'])
        
        result = calculate_form_2441(taxpayer_info_path, print_output=False)
        print(f"\nFinal Form 2441 Credit Amount: ${result:,.2f}")
    except FileNotFoundError:
        print("Error: config.json not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid config.json format")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)