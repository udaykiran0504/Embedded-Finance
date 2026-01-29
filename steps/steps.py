from behave import given,then,Then,when,When
from utils.db import DATABASE
from Declarations import Registration
import logging



logging.basicConfig(filename='application.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

db_obj = DATABASE()

reg_obj = Registration()



excel_data = reg_obj.read_excel_file()
max_retries = 10
@given('The Customer is on embeded registation page')
def click_flexpay_icon(context):
    reg_obj.Embeded_reister()
    reg_obj.new_login()
    reg_obj.update_insertion()

@given('Complete Customer')
def click_flexpay_icon(context):
    reg_obj.Embeded_reister()
    reg_obj.update_insertion()



@then('Agent Verifies the Customer')
def check_register_login_page(context):
    reg_obj.verify_customer()
    reg_obj.update_customer_ckyc()

@Then('Customer login to the account and completes vkyc')
def check_record_insertion(context):
    reg_obj.customer_vkyc()

@Then('The Customer logs in and complete esign')
def check_record_insertion(context):
    reg_obj.complete_esing()
    reg_obj.update_esgin()
    reg_obj.vcip()

@Then('The Customer logs in and complete esign with -4')
def check_record_insertion(context):
    reg_obj.complete_esing()
    reg_obj.update_esgin_neg()
    reg_obj.vcip()


@Then('The Customer completes emandate')
def complete_customer_esign(self):
    reg_obj.login_customer2()
    reg_obj.emandate()
    

@Then('Agent performs Pendings open')
def complete_customer_esign(self):
    reg_obj.pendings_open()

@Then('Agent performs Pendings open to confirm esign')
def complete_customer_esign(self):
    reg_obj.pendings_open_eign()



@Then('Customer should have a active loan')
def complete_customer_esign(self):
    reg_obj.validate_mpin()







