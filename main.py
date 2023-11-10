# Importing required libraries
import os
import glob
import pandas as pd

SMS_GOAL    = 20000
CC_GOAL     = 10000
DM_GOAL     = 20000

def validate_row_count(excel_file, clients_goal):
    num_rows = len(pd.read_excel(excel_file))
    file_name = os.path.basename(excel_file)
    if num_rows != clients_goal:
        print(f"{file_name}: Number of Rows == Clients Goal: {num_rows == clients_goal}")

def validate_owner_columns(excel_file):
    df = pd.read_excel(excel_file)
    file_name = os.path.basename(excel_file)
    for col in ["OWNER FULL NAME", "OWNER FIRST NAME", "OWNER LAST NAME"]:
        if col not in df.columns or any(df[col] == "Not Available from the County"):
            print(f"{file_name}: {col} Passed: False")

def validate_duplicates(excel_file):
    df = pd.read_excel(excel_file)
    file_name = os.path.basename(excel_file)
    criteria_list = [
        ["MAILING ADDRESS", "MAILING ZIP"],
        ["FOLIO", "ADDRESS", "ZIP"]
    ]
    
    for criteria in criteria_list:
        if all(col in df.columns for col in criteria):
            duplicates = df[df.duplicated(subset=criteria, keep=False)].sort_values(by=criteria)
            if not duplicates.empty:
                print(f"{file_name}: Duplicates found based on {', '.join(criteria)}")
                print(duplicates[criteria])

def validate_blank_addresses(excel_file):
    df = pd.read_excel(excel_file)
    file_name = os.path.basename(excel_file)
    if "ADDRESS" not in df.columns or df["ADDRESS"].isna().any():
        print(f"{file_name}: No empty Property Address: False")

def validate_zero_score(excel_file):
    df = pd.read_excel(excel_file)
    file_name = os.path.basename(excel_file)
    if "SCORE" not in df.columns or (df["SCORE"] == 0).any():
        print(f"{file_name}: No properties with 0 score: FAILED")

def validate_columns_exist(excel_file, category):
    # Common columns across all categories
    common_columns = [
        "Folio", "Owner 1 Full Name", "Owner 1 First Name", "Owner 1 Last Name",
        "Property Address", "Property City", "Property State", "Property Zip", "Property County",
        "Mailing Address", "Mailing City", "Mailing State", "Mailing Zip",
        "Golden Address", "Golden City", "Golden State", "Golden Zip",
        "Action Plan", "Property Status", "Score",
        "Distress", "Avatar", "Property Type", "Link to property", "Tags",
        "Distresses"
    ]
    
    # Specific columns per category
    category_columns = {
        "Sms": ["Targeted Messages", "Phone Number", "Phone Type"],
        "Mail": ["Targeted messages"],
        "Calling": ["Owner 2 Full Name", "Property Link", "Phone Number", "Phone Type"]
    }

    # Get the dataframe
    df = pd.read_excel(excel_file)
    file_name = os.path.basename(excel_file)

    # Get the columns to check, uppercased
    columns_to_check = common_columns + category_columns.get(category, [])
    columns_to_check = [col.upper() for col in columns_to_check]

    # Validate columns
    for col in columns_to_check:
        exists = col in df.columns
        print(f"{file_name}: {col} Exists: {'PASSED' if exists else 'FAILED'}")

def start(category, goal, folder_path="fulfillments"):
    print("starting category: {}".format(category))
    if not os.path.exists(folder_path):
        return "Folder doesn't exist."
    for client_folder in os.listdir(folder_path):
        client_folder_path = os.path.join(folder_path, client_folder)
        if not os.path.isdir(client_folder_path):
            continue
        excel_files = glob.glob(os.path.join(client_folder_path, "*.xlsx"))
        for excel_file in excel_files:
            if category in excel_file:
                # validate_row_count(excel_file, goal)
                validate_owner_columns(excel_file)
                validate_duplicates(excel_file)
                validate_blank_addresses(excel_file)
                validate_zero_score(excel_file)
                # validate_columns_exist(excel_file, category)

if __name__ == "__main__":
    start("Sms",        SMS_GOAL)
    start("Mail",       DM_GOAL)
    start("Calling",    CC_GOAL)
