import os
import json
from worksheet_utils import calculate_credit_limit_worksheet_a
from forms_utils import calculate_form_2441

def load_config():
    """Load configuration from config.json"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
    with open(config_path, 'r') as f:
        return json.load(f)

CONFIG = load_config()

def schedule3_Form1040(file_path: str) -> float:
    ''' 
    Currently, this function attempts to capture only Part I of Schedule 3, which deals with nonrefundable credits.
    
    Args:
        file_path (str): Path to the taxpayer information JSON file
    
    Returns:
        float: Total nonrefundable credits from Schedule 3
    '''
    # Part I: Nonrefundable credits
    CreditforChildandDependentCareExpenses = calculate_form_2441(file_path, print_output=True)
    TotalNonrefundableCredits = CreditforChildandDependentCareExpenses
    return TotalNonrefundableCredits    

if __name__ == "__main__":
    taxpayer_info_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), CONFIG['data_paths']['taxpayer_information'])
    result = schedule3_Form1040(taxpayer_info_path)
    print(f"Total Nonrefundable Credits: ${result:,.2f}")    

