import os
import json
from tax_utils import compute_tax
from forms_utils import calculate_form_2441

def load_config():
    """Load configuration from config.json"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    with open(config_path, 'r') as f:
        return json.load(f)

CONFIG = load_config()

def calculate_credit_limit_worksheet_a() -> float:
    """
    Calculate credit limit using Credit Limit Worksheet A.
    Uses existing tax calculation with hardcoded values.
    
    Returns:
        float: Credit limit amount
    """
    try:
        # Step 1: Get tax amount from Form 1040, line 18
        taxable_income = 105800
        filing_status = "married_filing_jointly"
        
        # Get tax computation (note: removed rate_schedule_path as it's handled inside compute_tax)
        try:
            line_1_amount = compute_tax(taxable_income, filing_status) or 0
        except Exception as tax_error:
            print(f"An error occurred while computing tax: {tax_error}")
            line_1_amount = 0
        
        # Step 2: Use calculate_form_2441 to get the credit amount
        try:
            taxpayer_info_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), CONFIG['data_paths']['taxpayer_information'])
            line_2_amount = calculate_form_2441(taxpayer_info_path, print_output=False)
        except Exception as form_error:
            print(f"An error occurred while calculating Form 2441: {form_error}")
            line_2_amount = 0
        
        # Calculate line 3
        line_3_amount = line_1_amount - line_2_amount
        # print(f"Line 3 (line 1 - line 2): {line_3_amount}")

        # Calculate Line 4
        line_4_amount = 0 
        # print(f"Line 4: {line_4_amount}")

        # Calculate Line 5
        line_5_amount = line_3_amount - line_4_amount
        # print(f"Line 5 (line 3 - line 4): {line_5_amount}")

        return line_5_amount

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return 0
if __name__ == "__main__":
     result = calculate_credit_limit_worksheet_a()
     print(f"Final result: {result}")


def Credits_Qualifying_Children_and_Other_Dependents():
    """
    Calculate the credits for qualifying children and other dependents.
    """
    # Identify the adjusted gross income
    adjusted_gross_income = 135000


    # Line 2: Enter the amount from Form 2555, line 45, or Form 2555-EZ, line 50
    puerto_rico_exclusions = 0
    Form_2555_line_45_and_50 = 0
    Form_4563_line_15 = 0
    Additional_Exclusions = puerto_rico_exclusions + Form_2555_line_45_and_50 + Form_4563_line_15
    # Add Lines 1 and 2d (Additional_Exclusions)
    Line_3 = adjusted_gross_income + Additional_Exclusions

    # Regarding Lines 4 and 5
    # Load taxpayer information
    taxpayer_info_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), CONFIG['data_paths']['taxpayer_information'])
    with open(taxpayer_info_path, 'r') as f:
        taxpayer_data = json.load(f)
    
    # Count qualifying children (under age 17)
    from datetime import datetime
    current_year = datetime.now().year
    Number_of_Qualifying_Children = sum(
        1 for dependent in taxpayer_data.get('dependents', [])
        if (current_year - datetime.strptime(dependent['date_of_birth'], '%Y-%m-%d').year) < 17
    )
    
    Credit_per_Qualifying_Child = 2000
    # Line 6: Number of other dependents under age 17 or who do not the required social security number
    # Line 7: Credit per other dependent
    Number_of_Other_Dependents = 0
    Credit_per_Other_Dependent = 500

    # Line 8: Total credit for qualifying children and other dependents
    Total_Credit_for_Qualifying_Children_and_Other_Dependents = (Number_of_Qualifying_Children * Credit_per_Qualifying_Child) + (Number_of_Other_Dependents * Credit_per_Other_Dependent)

    # Line 9: Identify the threshold amount for the filing status
    filing_status = "married_filing_jointly"
    Threshold_Amount = 200000

    # Line 10: Subtract the threshold amount from line 3
    difference = Line_3 - Threshold_Amount
    if difference >= 0:
        Line_12 = Total_Credit_for_Qualifying_Children_and_Other_Dependents
    else:
        # If income is below threshold, no reduction needed
        Line_12 = Total_Credit_for_Qualifying_Children_and_Other_Dependents - max(0, (difference // 1000) * 50)

    Line_13 = calculate_credit_limit_worksheet_a()

    child_tax_credit_and_credit_for_other_dependents = min(Line_13, Line_12)
    return child_tax_credit_and_credit_for_other_dependents
if __name__ == "__main__":
    result = Credits_Qualifying_Children_and_Other_Dependents()
    print(f"Final result: {result}")