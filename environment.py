import os
import logging
from datetime import datetime
import traceback
import pandas as pd
from steps.Declarations import Registration

logging.basicConfig(filename='application.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
scenarios = []

reg = Registration()
test_case_headers = {
    'TC_001': [
        'Device_Name', 'Model_Name', 'Referal_Code', 'Invalid_Phone', 'Phone_Number_Existing', 'Phone_Number_New',
        'Wrong_Otp', 'Invalid_Password', 'Password', 'First_Name', 'Last_Name', 'PAN_Number', 'Valid_Email',
        'Address', 'Pincode', 'Existing_Pan_Number', 'Company_Name', 'Salary', 'IFSC_Code', 'Account_Number',
        'Confirm_Account', 'Valid_UPI', 'Reference_First', 'Invalid_Reference_Last', 'Invalid_Account_Number',
        'Mismatch_Confirm_Account', 'Less_Salary', 'Reference_Last', 'Invalid_IFSC_Code'
    ],

    'TC_002': [
        'Device_Name', 'Model_Name', 'Referal_Code', 'Invalid_Phone', 'Phone_Number_Existing', 'Phone_Number_New',
        'Wrong_Otp', 'Invalid_Password', 'Password', 'First_Name', 'Last_Name', 'PAN_Number', 'Valid_Email',
        'Address', 'Pincode', 'Existing_Pan_Number', 'Company_Name', 'Salary', 'IFSC_Code', 'Account_Number',
        'Confirm_Account', 'Valid_UPI', 'Reference_First', 'Invalid_Reference_Last', 'Invalid_Account_Number',
        'Mismatch_Confirm_Account', 'Less_Salary', 'Reference_Last', 'Invalid_IFSC_Code'
    ]
}


def delete_second_row(file_path='Udhyam.xlsx', sheet_name='Registration'): 
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        df = df.drop(index=0)
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    except Exception as e:
        logging.error(f"Error deleting second row: {e}")
        raise

def before_all(context):
    context.start_time = datetime.now()
    context.failed_scenarios = []
    logging.info("Test execution started.")

def before_scenario(context, scenario):
    delete_second_row()

def before_step(context, step):
    step.start_time = datetime.now()

def after_step(context, step):
    step.end_time = datetime.now()

    if step.status.name == 'failed':
        context.exception = ''.join(traceback.format_exception(*step.exc_info)) if step.exc_info else "Exception details not available"
        test_case_id = next((tag for tag in step.scenario.tags if tag.startswith("TC")), "N/A")
        logging.error(f"Step failed in test case {test_case_id}: {context.exception}")
        screenshot_name = f"{test_case_id}_{step.name.replace(' ', '_')}.png"
        capture_screenshot(context, screenshot_name)

def after_scenario(context, scenario):
    test_case_id = next((tag for tag in scenario.tags if tag.startswith("TC")), "N/A")

    steps_info = []
    for step in scenario.steps:
        step_info = {
            "step_name": step.name,
            "status": step.status.name,
            "duration": "{:.0f}s".format(step.duration) if step.duration else "None",
            "start_time": step.start_time.strftime('%H:%M:%S') if hasattr(step, 'start_time') else "N/A",
            "end_time": step.end_time.strftime('%H:%M:%S') if hasattr(step, 'end_time') else "N/A"
        }
        steps_info.append(step_info)

    input_values = print_top_row(test_case_id)
    logging.info(f"Test case {test_case_id} passed with input values: {input_values}")

    scenario_info = {
        "test_case_id": test_case_id,
        "test_case_name": scenario.name,
        "status": scenario.status.name,
        "duration": "{:.0f}s".format(scenario.duration) if scenario.duration else "None",
        "start_time": context.start_time.strftime('%H:%M'),
        "end_time": datetime.now().strftime('%H:%M'),
        "steps": steps_info,
        "input_values": input_values
    }

    scenarios.append(scenario_info)
    logging.info(f"After scenario hook executed for {test_case_id}.")
    try:
        reg.close_driver()
    except:
        pass

def capture_screenshot(context, file_name, file_location='/home/administrator/Desktop/'):
    os.makedirs(file_location, exist_ok=True)
    file_path = os.path.join(file_location, file_name)
    
    if hasattr(context, 'driver') and context.driver:
        success = context.driver.get_screenshot_as_file(file_path)
        if success:
            logging.info(f"Screenshot saved at: {file_path}")
        else:
            logging.warning("Failed to capture screenshot.")
    else:
        logging.warning("No driver found in context. Cannot capture screenshot.")

def after_all(context):
    end_time = datetime.now()
    duration = end_time - context.start_time
    today_date = datetime.now().strftime('%Y-%m-%d')

    passed_scenarios = [s for s in scenarios if s['status'].lower() == 'passed']
    failed_scenarios = [s for s in scenarios if s['status'].lower() == 'failed']
    skipped_scenarios = [s for s in scenarios if s['status'].lower() == 'skipped']

    report_file = os.path.join(os.getcwd(), f"Udhyam{today_date}.html")

    logging.info("Writing report to HTML file.")

    with open(report_file, "w") as f:
        f.write("<html><head>")
        f.write(f"<title>QA-Automation - {today_date}</title>")
        f.write("""
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f4f4f4;
                color: #333;
            }
            h1, h2 {
                text-align: center;
                color: #4CAF50;
            }
            .summary {
                background-color: #e0e0e0;
                padding: 10px;
                margin-bottom: 20px;
                border-radius: 5px;
            }
            .summary h2 {
                margin-top: 0;
            }
            .summary p {
                margin: 5px 0;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }
            th, td {
                border: 1px solid #ccc;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            tr:hover {
                background-color: #f1f1f1;
            }
            .passed {
                color: #4CAF50;
                font-weight: bold;
            }
            .failed {
                color: #F44336;
                font-weight: bold;
            }
            .skipped {
                color: #000000;
                font-weight: bold;
            }
            .center {
                text-align: center;
            }
            .test-case-link {
                text-decoration: none;
                color: #4CAF50;
            }
        </style>
        """)
        f.write("</head><body>")

        f.write("<div class='center'>")
        f.write(f"<h1>Udhyam QA-Automation Report - {today_date}</h1>")
        f.write("</div>")

        f.write(f"<p>Started at: {context.start_time.strftime('%H:%M')}</p>")
        f.write(f"<p>Ended at: {end_time.strftime('%H:%M')}</p>")
        f.write(f"<p>Total duration: {str(duration).split('.')[0]}</p>")

        f.write("<div class='summary'>")
        f.write("<h2>Test Summary</h2>")
        f.write(f"<p>Total Scenarios: {len(scenarios)}</p>")
        f.write(f"<p class='passed'>Passed: {len(passed_scenarios)}</p>")
        f.write(f"<p class='failed'>Failed: {len(failed_scenarios)}</p>")
        f.write("</div>")

        f.write("<table>")
        f.write("<thead><tr><th>Test Case ID</th><th>Test Case Name</th><th>Input Values</th><th>Step Name</th><th>Status</th><th>Duration</th><th>Start Time</th><th>End Time</th></tr></thead>")
        f.write("<tbody>")

        for scenario in scenarios:
            scenario_status_class = (
                "failed" if scenario['status'].lower() == "failed" else 
                "skipped" if scenario['status'].lower() == "skipped" else 
                "passed"
            )
            f.write("<tr>")
            f.write(f"<td rowspan='{len(scenario['steps']) + 1}' class='{scenario_status_class}'>{scenario['test_case_id']}</td>")
            f.write(f"<td rowspan='{len(scenario['steps']) + 1}'>{scenario['test_case_name']}</td>")
            f.write(f"<td rowspan='{len(scenario['steps']) + 1}'>{scenario['input_values']}</td>")
            f.write("</tr>")

            for step in scenario['steps']:
                step_status_class = (
                    "failed" if step['status'].lower() == "failed" else 
                    "skipped" if step['status'].lower() == "skipped" else 
                    "passed"
                )
                f.write("<tr>")
                f.write(f"<td>{step['step_name']}</td>")
                f.write(f"<td class='{step_status_class}'>{step['status']}</td>")
                f.write(f"<td>{step['duration']}</td>")
                f.write(f"<td>{step['start_time']}</td>")
                f.write(f"<td>{step['end_time']}</td>")
                f.write("</tr>")

        f.write("</tbody></table>")
        f.write("<p>Regards,</p>")
        f.write("<p>K.Nirmal</p>")
        f.write("</body></html>")

    logging.info(f"Report generation completed. Report saved as: {report_file}")

def format_input_data(input_values):
    formatted_values = []
    for item in input_values:
        key, value = item.split(':', 1)
        formatted_values.append(f"<strong>{key}:</strong> {value}")
    return '<br><br>'.join(formatted_values)

def print_top_row(test_case_id, file_path='Udhyam.xlsx', sheet_name='Registration'):
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        top_row = df.iloc[0]
        headers = test_case_headers.get(test_case_id, [])
        input_values = [f'{header}:{top_row[header]}' for header in headers if header in top_row.index]
        formatted_output = format_input_data(input_values)
        logging.info(f"Extracted top row data for test case {test_case_id}: {formatted_output}")
        return formatted_output
    except Exception as e:
        logging.error(f"Error in print_top_row for test case {test_case_id}: {e}")
        return "Error retrieving input values"
