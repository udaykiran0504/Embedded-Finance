from sqlalchemy import create_engine, text
import pandas as pd
import random
import string
import re
from openpyxl import load_workbook
import os
from datetime import datetime,timedelta
server_ip = '13.126.100.198'
database = 'VivifiQA_New'
username = 'udaykiran.mummina'
password = 'Hello@123'

connection_string = (
    f"mssql+pyodbc:///?odbc_connect="
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={server_ip};"
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    f"Encrypt=no"
)

pincodes = [500030, 500004, 500045, 500007, 500012, 500015, 500044, 500013, 500004, 501201, 
    500015, 500044, 501301, 501301, 501301, 500030, 500040, 500020, 500048, 500015, 
    500058, 500064, 500005, 500034, 500027, 500004, 500012, 500016, 500003, 500018, 
    500080, 500039, 501301, 500013, 500022, 500024, 500064, 501301, 501301, 500005, 
    500081, 500015, 500008, 500024, 500028, 500006, 500060, 500062, 500062, 500018, 
    500053, 500065, 500018, 500029, 500015, 500001, 500080, 501301, 500015, 500008, 
    500020, 500015, 500068, 500062, 500052, 500066]

ALLOWED_FIRST_LETTERS = 'ABCD'

def generate_random_string_pan(length, min_length, allowed_chars):
    return ''.join(random.choices(allowed_chars, k=length))

def generate_random_number_length_pan(length):
    return ''.join(random.choices(string.digits, k=length))

def generate_pan_number(existing_pan_numbers, first_letter):
    while True:
        # Generate 3 random uppercase letters
        rest_letters = ''.join(random.choices(string.ascii_uppercase, k=2))
        fourth_letter = "P"
        fifth_letter = random.choice(string.ascii_uppercase)

        digits = ''.join(random.choices(string.digits, k=4))
     
        last_letter = random.choice(string.ascii_uppercase)

        pan_number = f"{first_letter}{rest_letters}{fourth_letter}{fifth_letter}{digits}{last_letter}"

        if pan_number not in existing_pan_numbers:
            break

    return pan_number


engine = create_engine(connection_string)
def generate_valid_password(min_length=8):
    if min_length < 8:
        min_length = 8

    lowercase = random.choice(string.ascii_lowercase)
    uppercase = random.choice(string.ascii_uppercase)
    digit = random.choice(string.digits)
    special = random.choice('!@#&£$%^*_-+=;,:.?/\\|')

    remaining_length = min_length - 4
    all_chars = string.ascii_letters + string.digits + '!@#&£$%^*_-+=;,:.?/\\|'
    remaining_chars = ''.join(random.choices(all_chars, k=remaining_length))

    password = list(lowercase + uppercase + digit + special + remaining_chars)
    random.shuffle(password)

    return ''.join(password)


def generate_valid_first_name(first_letter, min_length=4, max_length=8):
    pattern = r'^[A-J][a-zA-Z ]*$'  
    while True:
        # Ensure the total length is within the specified range
        name_length = random.randint(min_length - 1, max_length - 1)
        # Generate the rest of the name
        name = first_letter + ''.join(random.choices(string.ascii_letters + ' ', k=name_length)).strip()
        if re.match(pattern, name):
            return name

def generate_valid_name(min_length=4, max_length=8):
    pattern = r'^[a-zA-Z]*$'
    while True:
        name = ''.join(random.choices(string.ascii_letters + ' ', k=random.randint(min_length, max_length))).strip()
        if re.match(pattern, name):
            return name

def generate_random_string(min_length, max_length, chars=string.ascii_letters + string.digits):
    length = random.randint(min_length, max_length)
    return ''.join(random.choices(chars, k=length))

def generate_unique_phone(existing_phones):
    while True:
        phone = random.choice('6789') + ''.join(random.choices(string.digits, k=9))
        if phone not in existing_phones:
            return phone
        
def generate_retail_id(existing_ids):
    while True:
        # Generate the parts
        prefix = ''.join(random.choices(string.ascii_uppercase, k=2))
        middle = str(random.randint(0, 9999999)).zfill(7)
        suffix = str(random.randint(0, 999)).zfill(3)

        # Combine to final format
        retail_id = f"{prefix}-{middle}-{suffix}"

        # Check if it's unique
        if retail_id not in existing_ids:
            return retail_id

def generate_random_number_length(length):
    if length == 1:
        return random.choice(string.digits[1:]) 
    first_digit = random.choice(string.digits[1:])  
    other_digits = ''.join(random.choices(string.digits, k=length-1))
    return first_digit + other_digits

def generate_invalid_string(pattern, min_length, max_length):
    while True:
        candidate = generate_random_string(min_length, max_length)
        if not re.match(pattern, candidate):
            return candidate

def generate_valid_address(min_length=4, max_length=10):
    pattern = r'^(?!.*\|).{4,}$'
    
    while True:
        valid_chars = string.ascii_letters + string.digits + ' '
        random_string = ''.join(random.choices(valid_chars, k=random.randint(min_length, max_length)))
        
        if re.match(pattern, random_string):
            return random_string

def generate_invalid_email():
    local_part = generate_random_string(5, 8)
    domain = generate_random_string(2, 3)
    separators = ['!','#','$','%','^','&','*']
    separator = random.choice(separators)
    invalid_email = f'{local_part}{separator}{domain}.com'
    return invalid_email

def generate_random_number(min_length, max_length):
    if min_length > max_length:
        raise ValueError("min_length should not be greater than max_length")
    
    length = random.randint(min_length, max_length)
    
    if length == 1:
        return random.choice(string.digits[1:]) 
    
    first_digit = random.choice(string.digits[1:]) 
    other_digits = ''.join(random.choices(string.digits, k=length-1))
    
    return first_digit + other_digits

def generate_invalid_string_with_pipe(min_length, max_length):
    length = random.randint(min_length, max_length)
    if length <= min_length:
        length = min_length + 1
    base_string = generate_random_string(min_length, length - 1)
    insert_pos = random.randint(0, len(base_string))
    invalid_string = base_string[:insert_pos] + '|' + base_string[insert_pos:]
    if len(invalid_string) > length:
        invalid_string = invalid_string[:length]
    return invalid_string

def genrate_udhyam_number():
    # Two uppercase letters
    first_part = ''.join(random.choices(string.ascii_uppercase, k=2))
    
    # Exactly 9 digits
    second_part = ''.join(random.choices(string.digits, k=9))
    
    return first_part + second_part

def generate_valid_upi_id(min_length=5, max_length=10):
    pattern = r'^\w.+@\w+$'
    
    while True:
        first_part_length = random.randint(2, max_length - 4)
        first_part = random.choice(string.ascii_letters + string.digits + '_') + ''.join(random.choices(string.ascii_letters + string.digits + '._-', k=first_part_length - 1))
        
        second_part_length = random.randint(2, max_length - first_part_length - 1)
        second_part = ''.join(random.choices(string.ascii_letters + string.digits + '_', k=second_part_length))
        generated_string = f'{first_part}@{second_part}'
        
        if re.match(pattern, generated_string):
            return generated_string


def generate_random_email(min_length=8, max_length=10):
    pattern = r'^[0-9a-zA-Z]+([0-9a-zA-Z]*[-._+])*[0-9a-zA-Z]+@[0-9a-zA-Z]+([-.][0-9a-zA-Z]+)*\.com$'
    
    while True:
        total_fixed_length = len('@.com')  # 5 characters
        max_allowed = max_length - total_fixed_length
        min_allowed = max(min_length - total_fixed_length, 4 + 1)  # At least 4 for local and 1 for domain

        # Local part must be at least 4 characters
        local_part_min = 4
        local_part_max = max_allowed - 1  # Leave room for domain

        if local_part_max < local_part_min:
            raise ValueError("max_length too small to satisfy local part minimum length of 4.")

        local_part_length = random.randint(local_part_min, local_part_max)
        domain_part_length = max_allowed - local_part_length

        if domain_part_length < 1:
            continue  # Try again

        local_chars = string.ascii_lowercase + string.digits
        domain_chars = string.ascii_lowercase + string.digits

        local_part = ''.join(random.choices(local_chars, k=local_part_length))
        domain_part = ''.join(random.choices(domain_chars, k=domain_part_length))

        email = f'{local_part}@{domain_part}.com'

        if min_length <= len(email) <= max_length and re.match(pattern, email):
            return email



def generate_dob(age_min=25, age_max=45):
    today = datetime.today()
    
    # Calculate date range
    start_date = today.replace(year=today.year - age_max)  # oldest
    end_date = today.replace(year=today.year - age_min)    # youngest
    
    # Generate random date in range
    random_days = random.randint(0, (end_date - start_date).days)
    dob = start_date + timedelta(days=random_days)
    
    # Format as DDMMYYYY
    return dob.strftime("%d%m%Y")


def generate_random_salary(min_salary, max_salary):
    return random.randint(min_salary, max_salary)

num_records = 100

with engine.connect() as connection:

    matching_prefix_query = "SELECT distinct IFSccode from CanarifiV3.dbo.OneMoneySupportedBankList where IsActive = 1"
    matching_prefix = [row[0] for row in connection.execute(text(matching_prefix_query)).fetchall()]

    existing_accounts_query = """
            SELECT DISTINCT cb.AccountNumber 
            FROM customerBank cb
            INNER JOIN CustomerLogin cl
                ON cb.CustomerID = cl.CustomerID
            WHERE cl.IsActive = 1 
            AND cl.outletid = 4 
            AND cb.AccountNumber IS NOT NULL
            ORDER BY AccountNumber DESC;
                            """
    existing_accounts = [row[0] for row in connection.execute(text(existing_accounts_query)).fetchall()]

    existing_pan_numbers_query = """
        WITH CustomerPan AS (
            SELECT ci.pannumber
            FROM customer c
            JOIN customeridentity ci ON c.customerid = ci.customerid
            WHERE c.outletid = 4 
            AND ci.pannumber IS NOT NULL
            AND ci.pannumber LIKE '[A-Z][A-Z][A-Z]P[A-Z][0-9][0-9][0-9][0-9][A-Z]'
            AND ci.status = 0
        ),
        PanDetailsPan AS (
            SELECT DISTINCT panid
            FROM PanDetails
            WHERE panid IS NOT NULL
            AND panid LIKE '[A-Z][A-Z][A-Z]P[A-Z][0-9][0-9][0-9][0-9][A-Z]'
            AND panstatus = 'E'
        )
        -- Final query to match and display the common PAN numbers
        SELECT cp.pannumber
        FROM CustomerPan cp
        JOIN PanDetailsPan pd ON cp.pannumber = pd.panid
        ORDER BY cp.pannumber DESC;
    """
    existing_pan_numbers = [row[0] for row in connection.execute(text(existing_pan_numbers_query)).fetchall()]

    pincode_query = "SELECT ZipCode FROM zip where isactive=1 order by 1 DESC;"
    # pincodes = [row[0] for row in connection.execute(text(pincode_query)).fetchall()]

    ifsc_codes_query = f"""
        SELECT DISTINCT cb.IFSC
        FROM RazorpayTransaction rt
        JOIN customerBank cb ON rt.CustomerID = cb.CustomerID
        WHERE rt.TransactionStatus = 'confirmed' 
        AND rt.status = 0
        AND rt.Amount != 0
        AND cb.IFSC IS NOT NULL 
        AND LEFT(cb.IFSC, 4) IN (
            SELECT DISTINCT IFSccode 
            FROM CanarifiV3.dbo.OneMoneySupportedBankList 
            WHERE IsActive = 1
        ) 
    """
    ifsc_codes = [row[0] for row in connection.execute(text(ifsc_codes_query)).fetchall()]

    unsuported_ifsc_codes_query = f"""

        WITH SupportedBanks AS (
            SELECT BankCode 
            FROM LTEMandateSupportedBanks 
            WHERE IsEMandateSupported = 0
        ),
        ActiveBankCodes AS (
            SELECT IFSCCode AS BankCode
            FROM CanarifiV3.dbo.OneMoneySupportedBankList
            WHERE IsActive = 1
        )

        SELECT cb.IFSC
        FROM customerbank cb
        JOIN RazorpayTransaction rt ON rt.CustomerID = cb.CustomerID
        WHERE LEFT(cb.IFSC, LEN(cb.IFSC) - LEN(SUBSTRING(cb.IFSC, PATINDEX('%[0-9]%', cb.IFSC), LEN(cb.IFSC)))) NOT IN 
            (SELECT BankCode FROM ActiveBankCodes)
        AND LEFT(cb.IFSC, LEN(cb.IFSC) - LEN(SUBSTRING(cb.IFSC, PATINDEX('%[0-9]%', cb.IFSC), LEN(cb.IFSC)))) IN 
            (SELECT BankCode FROM SupportedBanks)
        AND rt.TransactionStatus in ('confirmed' , 'authorized' )
        AND rt.status = 0
        AND rt.Amount != 0
        ORDER BY cb.IFSC DESC;

    """
    unsupported_ifsc_codes = [row[0] for row in connection.execute(text(unsuported_ifsc_codes_query)).fetchall()]


    existing_phones_query = """
        SELECT DISTINCT cp.PhoneNumber
        FROM CustomerPhone cp
        JOIN Customer c ON c.CustomerID = cp.CustomerID
        JOIN CustomerLogin cl ON c.CustomerID = cl.CustomerID
        WHERE cl.IsActive = 1 
        AND cl.outletid = 4 
        AND c.CustomerStatusCodeID = 10
        And c.OutletId = 4
        AND cp.IsPrimaryVerified = 1
        AND cp.PhoneNumber IS NOT NULL
        ORDER BY cp.PhoneNumber DESC;
    """
    existing_phones = [row[0] for row in connection.execute(text(existing_phones_query)).fetchall()]

    existing_emails_query = """
        SELECT DISTINCT c.email 
        FROM customer c
        INNER JOIN CustomerLogin cl
            ON c.CustomerID = cl.CustomerID
        WHERE cl.IsActive = 1 
        AND cl.outletid = 4 
        AND c.CustomerStatusCodeID = 10
        AND c.Email IS NOT NULL
        ORDER BY c.email DESC;
    """
    existing_emails = [row[0] for row in connection.execute(text(existing_emails_query)).fetchall()]

    existing_ids_query = 'select Retailerid from RetailerData'
    existing_ids = [row[0] for row in connection.execute(text(existing_ids_query)).fetchall()]


data = []

for i in range(num_records):

    first_letter = random.choice(ALLOWED_FIRST_LETTERS)
    first_name = generate_valid_first_name(first_letter)
    pan_number = generate_pan_number(existing_pan_numbers, first_letter)
    account_number = generate_random_number(10, 17)
    while account_number in existing_accounts:
        account_number = generate_random_number(10, 17)

    email = generate_random_email()
    while email in existing_emails:
        email = generate_random_email()
    data.append({
        # Personal Information
        # 'Aadhar_Number': str(generate_random_number_length(12)),
        'First_Name': first_name,
        'Last_Name': generate_valid_name(),
        # 'Invalid_First_Name': generate_invalid_string(r'^[a-zA-Z ]*$', 4, 10),
        # 'Invalid_Last_Name': generate_invalid_string(r'^[a-zA-Z ]*$', 4, 10),
        # 'Reference_First': generate_valid_name(),
        # 'Reference_Last': generate_valid_name(),
        # 'Invalid_Reference_Last': generate_invalid_string(r'^[a-zA-Z ]*$', 4, 10),
        # 'Phone_Number_Existing': str(random.choice(existing_phones)),  
        'Phone_Number_New': generate_unique_phone(existing_phones),
        # 'Invalid_Phone': generate_random_string(9, 10),
        'Valid_Email': email,
        # 'Existing_Email': str(random.choice(existing_emails)),
        # 'Invalid_Email': generate_invalid_string(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#&£$%^*_\-+=;,:.?/\\|])[\S]{8,}$', 4, 10),
        'PAN_Number': pan_number,
        'DOB' : generate_dob(),
        'Business_open_date' : generate_dob(age_min=2,age_max=10),
        # 'Existing_Pan_Number': str(random.choice(existing_pan_numbers)),
        # 'Invalid_Pan_Number': generate_invalid_string(r'^[A-Za-z]{5}[0-9]{4}[A-Za-z]$', 10, 10),

        # # Account Information
        'Account_Number': str(account_number),
        'Confirm_Account': str(account_number),
        # 'Mismatch_Confirm_Account': str(generate_random_number(10, 17)),
        # 'Existing_Account': str(random.choice(existing_accounts)),
        # 'Invalid_Account_Number': generate_invalid_string(r'^[0-9]{9,17}$', 9, 17),
        'IFSC_Code': str(random.choice(ifsc_codes)),
        'Approve_amount' : str(generate_random_salary(30000, 100000)),
        # 'Unsupported_IFSC': str(random.choice(unsupported_ifsc_codes)),
        # 'Invalid_IFSC_Code': generate_invalid_string(r'^[A-Za-z]{4}0[A-Z0-9a-z]{6}$', 12, 12),

        # # Address Information
        'Address': generate_valid_address(),
        'Business_Address': generate_valid_address(),
        # 'Permanent_Address': generate_valid_address(),
        'Business_desc': generate_valid_address(),
        # 'Invalid_Address': generate_invalid_string_with_pipe(5, 15),
        'Pincode': str(random.choice(pincodes)),
        # 'Permanent_Pincode': str(random.choice(pincodes)),
        # 'Invalid_Pincode': str(generate_random_number(7, 8)),

        # # Financial Information
        'Salary': str(generate_random_salary(30000, 74000)),
        'Turn_Over': str(generate_random_salary(150000, 250000)),
        # 'Less_Salary': str(generate_random_salary(1000, 8000)),
        # 'Above_Salary': str(generate_random_salary(75000, 100000)),

        # # UPI and Password
        'Valid_UPI': generate_valid_upi_id(),
        'Udhyam_Number' : genrate_udhyam_number(),
        'Password': 'Password@123',
        'Invoice_Number': str(generate_random_number_length(9)),
        

        # # Miscellaneous
        'Company_Name': generate_valid_name(),
        # 'Designation': random.choice(['Manager', 'Director', 'Engineer', 'Developer', 'Analyst', 'Coordinator', 'Specialist', 'Consultant', 'Architect', 'Administrator']),
        # 'Device_Name': 'Google',
        # 'Model_Name': 'sdk_gphone64_x86_64',
        'Office_Phone': generate_unique_phone(existing_phones),
        'Business_link': generate_random_string(4, 6),
        # 'reference': generate_random_string(4, 6),    
        'Retailerid' : generate_retail_id(existing_ids)
    })


df = pd.DataFrame(data).astype(str)

output_file = 'Udhyam.xlsx'

sheet_name = 'Registration'
df.to_excel(output_file, sheet_name=sheet_name, index=False)

wb = load_workbook(output_file)
ws = wb[sheet_name]

for column in ws.columns:
    max_length = 0
    column_letter = column[0].column_letter
    for cell in column:
        try:
            if len(str(cell.value)) > max_length:
                max_length = len(cell.value)
        except:
            pass
    adjusted_width = (max_length + 2) * 1.2
    ws.column_dimensions[column_letter].width = adjusted_width

wb.save(output_file)

if __name__ == "__main__":
    print("Generating Udhyam.xlsx data...")

    # CALL YOUR MAIN FUNCTION HERE
    #pythgenerate_udhyam_excel()
    
    print("Done! Udhyam.xlsx updated.")

