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