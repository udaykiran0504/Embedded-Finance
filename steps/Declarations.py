import time
from utils.db import DATABASE 
import logging
from utils.element_locators import *
import requests
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException,NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
import pandas as pd
import os

max_retries = 10
db_obj = DATABASE()
class Registration:


    def read_element_text_by_locator(self, locator):
        element = self.driver.find_element(*locator) 
        return element.text  



    def update_insertion(self):
        excel_data = self.read_excel_file()
        for row in excel_data:
            cust = db_obj.get_customer_id(row['Valid_Email'])
            db_obj.update_insertion_time(cust)
            logging.info(f'Insertion time updated for customerid {cust}')
            


    def delete_second_row(self,file_path='Udhyam.xlsx', sheet_name='Registration'): 
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        df = df.drop(index=0)
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
        logging.info(f"Deleted second row from {sheet_name} in {file_path}")


            
   
    def build_url(self):
        base_url = "http://qa-2-fponline.finextqa.xyz/EmFin/NewApplication"
        partner_id = "225"
        excel_data = self.read_excel_file()
        phn_no = excel_data[0]['Phone_Number_New']
        final_url = f"{base_url}?MobileNo={phn_no}&PartnerID={partner_id}"
        self.last_phn_no = phn_no
        self.last_partner_id = partner_id
        self.last_final_url= final_url
        logging.info(f" embeded  url was genearted {final_url}")
        return final_url
    
    def get_recent_final_url(self):
        if hasattr(self, "last_phn_no") and hasattr(self,"last_partner_id"):
            resume_base_url = "http://qa-2-fponline.finextqa.xyz/EmFin/ResumeApplication"
            resume_url = (
                f"{resume_base_url}"
                f"?MobileNo={self.last_phn_no}"
                f"&partnerid={self.last_partner_id}"
            )
            logging.info(f"Returning recently used relogin URL: {resume_url}")
            return resume_url
        else:
            raise Exception("No relogin URL found. Please call relogin_url() first.")

 
    def enter_dob_js(self, dob):
        """
        Optimized JS injection to set DOB and trigger validation.
        """
        js_code = f"""
        let e = document.getElementById('DOB');
        e.value = '{dob}';
        e.dispatchEvent(new Event('input', {{ bubbles: true }}));
        e.dispatchEvent(new Event('change', {{ bubbles: true }}));
        e.dispatchEvent(new Event('blur', {{ bubbles: true }}));
        """
        self.driver.execute_script(js_code)
        logging.info(f"DOB set to {dob} via optimized JS.")

    



    def scroll_until_found(self, element_locator, start_x, start_y, end_x, end_y, max_swipes=10):
        self.wait_for_invisibility(progress_bar)
        for attempt in range(max_swipes):
            try:
                element = self.driver.find_element(*element_locator)
                if element.is_displayed():
                    return element
            except :
                pass

            actions = ActionChains(self.driver)
            actions.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
            actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(2)
            actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

        raise Exception(f"Element {element_locator} not found after {max_swipes} swipes")

    def clear_text_box(self, locator,wait_time=30):
        text_box  = WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located(locator))
        text_box.clear()




    def capture_screenshot(self, file_name, file_location='/home/administrator/Desktop/Screenshots'):
        os.makedirs(file_location, exist_ok=True)
        file_path = os.path.join(file_location, file_name)
        success = self.driver.get_screenshot_as_file(file_path)
        if success:
            logging.info(f"Screenshot saved at: {file_path}")
            pass
        else:
            logging.info("Failed to capture screenshot.")
            pass
        return success
    
    def wait_for_dropdown_to_have_minimum_options(self, locator, min_options=2, timeout=200, poll_frequency=0.5):
        end_time = time.time() + timeout
        while time.time() < end_time:
            try:
                dropdown = Select(self.driver.find_element(*locator))
                options = dropdown.options

                if len(options) >= min_options:
                    logging.info(f"Dropdown has {len(options)} options. Proceeding.")
                    return True
            except NoSuchElementException:
                pass

            time.sleep(poll_frequency)

        logging.warning(f"Dropdown did not have at least {min_options} options within {timeout} seconds.")
        return False
    
    def enter_dob(self, dob_value):
        dob_element = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(Dob_feild)
            )
        self.driver.execute_script(
            "arguments[0].removeAttribute('readonly')",
            dob_element
            )
        dob_element.clear()
        dob_element.send_keys(dob_value)


    def is_element_disabled(self, locator,wait_time=30):
        element = WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located(locator))
        return not element.is_enabled()


    def select_dropdown_by_index(self, dropdown_locator, index):
        dropdown_element =  self. driver.find_element(*dropdown_locator)
        select = Select(dropdown_element)
        select.select_by_index(index)
        logging.info(f'Successfully selected item at index {index}')

    def select_dropdown_value(self, dropdown_locator, visible_text):
        dropdown_element = self.driver.find_element(*dropdown_locator)
        select = Select(dropdown_element)
        select.select_by_value(visible_text)
        logging.info(f'Successfully selected: {visible_text}')

    def wait_for_and_accept_alert(self, wait_time=30):
        start_time = time.time()
        WebDriverWait(self.driver, wait_time).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        alert_text = alert.text 
        alert.accept()  
        duration = time.time() - start_time
        logging.info("Accepted alert with text '{}', after {:.2f} seconds".format(alert_text, duration))
        return alert_text

    def wait_for_visibility(self, locator, wait_time=30):
        start_time = time.time()
        WebDriverWait(self.driver, wait_time).until(EC.presence_of_element_located(locator))
        duration = time.time() - start_time
        logging.info("Waited for element '{}' to appear in : {:.2f} seconds".format(self.get_locator_variable_name(locator), duration))
        return duration

    def interact_with_progress(self, locator, wait_time=30):
        start_time = time.time()
        element = WebDriverWait(self.driver, wait_time).until(EC.element_to_be_clickable(locator))
        self.wait_for_invisibility(progress_bar)
        time.sleep(2)
        element.click()
        duration = time.time() - start_time
        logging.info("Interacted with element '{}' in : {:.2f} seconds".format(self.get_locator_variable_name(locator), duration))
        return duration

    def visibility_and_click(self, locator, wait_time=30):
        start_time = time.time()
        element = WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located(locator))
        element.click()
        duration = time.time() - start_time
        logging.info("Interacted with element '{}' in : {:.2f} seconds".format(self.get_locator_variable_name(locator), duration))
        return duration

    def wait_and_clickable(self, locator, wait_time=30):
        start_time = time.time()
        WebDriverWait(self.driver, wait_time).until(EC.element_to_be_clickable(locator))
        duration = time.time() - start_time
        logging.info("Interacted with element '{}' in : {:.2f} seconds".format(self.get_locator_variable_name(locator), duration))
        return duration

    def wait_and_click(self, locator, wait_time=30):
        start_time = time.time()
        element = WebDriverWait(self.driver, wait_time).until(EC.element_to_be_clickable(locator))
        element.click()
        duration = time.time() - start_time
        logging.info("Interacted with element '{}' in : {:.2f} seconds".format(self.get_locator_variable_name(locator), duration))
        return duration
    

    def scroll_into_view(self, locator, wait_time=30):
        start_time = time.time()
        element = WebDriverWait(self.driver, wait_time).until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});",element)
        time.sleep(0.5)
        duration = time.time() - start_time
        logging.info("Scrolled to element '{}' in : {:.2f} seconds".format(self.get_locator_variable_name(locator), duration))
        return duration

    def wait_for_invisibility(self, locator, wait_time=300):
        start_time = time.time()
        WebDriverWait(self.driver, wait_time).until(EC.invisibility_of_element(locator))
        duration = time.time() - start_time
        return duration

    def wait_send_keys(self, locator, keys, wait_time=30):
        start_time = time.time()
        element = WebDriverWait(self.driver, wait_time).until(EC.element_to_be_clickable(locator))
        element.send_keys(keys)
        duration = time.time() - start_time
        logging.info("Sent keys to element '{}' in : {:.2f} seconds".format(self.get_locator_variable_name(locator), duration))
        return duration
    
    def progress_send_keys(self, locator, keys, wait_time=30):
        start_time = time.time()
        element = WebDriverWait(self.driver, wait_time).until(EC.presence_of_element_located(locator))

        self.wait_for_invisibility(progress_bar)


        element.send_keys(keys)
        

        self.wait_for_invisibility(progress_bar)
        duration = time.time() - start_time
        logging.info("Sent keys to element '{}' in : {:.2f} seconds".format(self.get_locator_variable_name(locator), duration))
        return duration

    def get_locator_variable_name(self, locator):
        for name, value in globals().items():
            if value == locator:
                return name
        return str(locator)

    def read_excel_file(self, sheet_name='Registration'):
        file_path = 'Udhyam.xlsx'
        df = pd.read_excel(file_path, sheet_name=sheet_name, dtype=str, engine='openpyxl', nrows=1)
        return df.to_dict(orient='records')


    def scroll_to_element(self, locator):
        self.wait_for_invisibility(progress_bar)
        element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)


    def validate_ml_pan_details(self,stpl,loch,ers,stpl_band,lev,score):
        excel_data = self.read_excel_file()
        for row in excel_data:
            customerid = db_obj.get_customerid_customerphone(row['Phone_Number_New'])
            db_obj.insert_six_variables(customerid)

            db_obj.update_stpl_cibil(stpl)
            db_obj.update_loch_cibil(loch)
            db_obj.update_ers_cibil(ers)
            db_obj.update_stpl_band_cibil(stpl_band)
            db_obj.update_levrage_score_cibil(lev)

            db_obj.update_ml_model(customerid)
            db_obj.insert_ml_model(customerid,score)


    def Embeded_reister(self):
        excel_data = self.read_excel_file()
        for row in excel_data:
            chrome_service = Service(ChromeDriverManager().install())
            chrome_options = Options()
            # chrome_options.add_argument("--headless=new") 
            chrome_options.add_experimental_option("detach", True)
            chrome_options.add_argument("--incognito")
            chrome_options.add_argument("--force-device-scale-factor=0.80")
            chrome_options.add_argument("--guest")
            self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
            self.driver.maximize_window()
            
            self.driver.get(self.build_url())


            self.wait_for_visibility(language)

            self.wait_and_click(english_lang)
            #self.wait_for_visibility(progress_bar)
            self.wait_for_invisibility(progress_bar)

            self.driver.switch_to.default_content()

            self.wait_for_invisibility(progress_bar)

            time.sleep(2)


            self.wait_for_visibility(OTP_1)

            ver_code = db_obj.get_verification_code(row['Phone_Number_New'])
            otp = db_obj.aes_decrypt(ver_code)

            self.wait_send_keys(OTP_1,otp[0])
            self.wait_send_keys(OTP_2,otp[1])
            self.wait_send_keys(OTP_3,otp[2])
            self.wait_send_keys(OTP_4,otp[3])
            self.wait_send_keys(OTP_5,otp[4])
            self.wait_send_keys(OTP_6,otp[5])

            self.wait_and_click(Proceed_button_new)
            self.wait_for_invisibility(progress_bar)

            self.wait_for_visibility(details_consent)
            self.wait_and_click(share_details)
            self.wait_for_invisibility(progress_bar)
            self.wait_for_visibility(connect_partner)
            time.sleep(2)
            self.wait_for_visibility(details_fetched)
            self.wait_and_click(details_fetched)
            self.wait_for_invisibility(progress_bar)
            self.wait_for_visibility(review_deatils)
            self.wait_and_click(edit_option)
            time.sleep(2)
            self.wait_for_visibility(personal_details)
            self.clear_text_box(first_name)
            self.clear_text_box(last_name)
            self.wait_send_keys(first_name,row['First_Name'])
            self.wait_send_keys(last_name,row['Last_Name'])
            self.enter_dob_js(row['DOB'])
            time.sleep(2)
            self.select_dropdown_value(gender_drop,'Male')
            self.clear_text_box(Pan_Number)
            self.wait_send_keys(Pan_Number,row['PAN_Number'])
            self.clear_text_box(driving_lic)
            db_obj.update_dl()
            self.wait_send_keys(driving_lic,'JH4619440257018')
            self.clear_text_box(address_line1)
            self.clear_text_box(address_line2)
            self.clear_text_box(customer_zip_code)
            self.wait_send_keys(address_line1,row['Address'])
            self.wait_send_keys(address_line2,row['Business_Address'])
            self.wait_send_keys(customer_zip_code,row['Pincode'])
            self.clear_text_box(email_feild)
            self.wait_send_keys(email_feild,row['Valid_Email'])
            time.sleep(4)
            self.clear_text_box(net_income)
            self.wait_send_keys(net_income,'55000')
            self.clear_text_box(ifsc_new)
            self.clear_text_box(account_no)
            self.clear_text_box(confirm_account_no)
            self.wait_send_keys(ifsc_new,row['IFSC_Code'])
            time.sleep(2)
            self.wait_send_keys(account_no,row['Account_Number'])
            self.wait_send_keys(confirm_account_no,row['Confirm_Account'])
            self.wait_for_invisibility(progress_bar)
            customerid = db_obj.get_customerid_customerphone(row['Phone_Number_New'])
            db_obj.insert_six_variables(customerid)
            db_obj.update_ml_model(customerid)
            db_obj.insert_ml_model(customerid,980)
            db_obj.insert_six_variables(customerid)
            self.wait_for_invisibility(progress_bar)
            self.scroll_into_view(Account_creation)
            self.wait_and_click(Account_creation)
            self.wait_for_invisibility(progress_bar)
            #time.sleep(3)
            self.wait_for_visibility(Congrtualtions_cibil)
            print("Displayed:",Congrtualtions_cibil)
            self.wait_for_visibility(progress_bar)
            self.wait_for_invisibility(progress_bar)
            self.wait_for_visibility(cibil_button)
            time.sleep(2)
            self.visibility_and_click(cibil_button)
            self.driver.quit()



            # self.wait_for_visibility(cibil_button)
            # self.wait_and_click(cibil_button)
            # self.wait_for_invisibility(progress_bar)
            # time.sleep(2)
            # self.wait_for_invisibility(progress_bar)

            # self.interact_with_progress(submit_button)
            # self.wait_for_invisibility(progress_bar)


            # self.wait_and_click(Verifiy_acccount)
            # self.wait_and_click(Confirm_ebv)


            # self.wait_for_visibility(ver_iframe)


            # ver_iframe1 = self.driver.find_element(By.ID, 'verificationIframe')
            # self.driver.switch_to.frame(ver_iframe1)



            # time.sleep(4)

            # self.driver.switch_to.default_content()
            # self.complete_ebv()

            # self.driver.quit()

    def new_login(self):
        excel_data = self.read_excel_file()
        for row in excel_data:
            chrome_service = Service(ChromeDriverManager().install())
            prefs = {
                "profile.default_content_setting_values.media_stream_mic": 1,
                "profile.default_content_setting_values.media_stream_camera": 1,
                "profile.default_content_setting_values.notifications": 1,
                "profile.default_content_setting_values.geolocation": 1
            }
            chrome_options = Options()
            # chrome_options.add_argument("--headless=new") 
            chrome_options.add_experimental_option("detach", True)
            chrome_options.add_experimental_option("prefs", prefs)
            chrome_options.add_argument("--use-fake-ui-for-media-stream")
            chrome_options.add_argument("--force-device-scale-factor=0.80")
            chrome_options.add_argument("--guest")
            self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
            self.driver.maximize_window()

            url = self.get_recent_final_url()
            self.driver.get(url)
            self.wait_for_visibility(language)

            self.wait_and_click(english_lang)
            #self.wait_for_visibility(progress_bar)
            self.wait_for_invisibility(progress_bar)

            self.driver.switch_to.default_content()

            self.wait_for_invisibility(progress_bar)

            time.sleep(2)


            self.wait_for_visibility(OTP_1)

            ver_code = db_obj.get_verification_code(row['Phone_Number_New'])
            otp = db_obj.aes_decrypt(ver_code)

            self.wait_send_keys(OTP_1,otp[0])
            self.wait_send_keys(OTP_2,otp[1])
            self.wait_send_keys(OTP_3,otp[2])
            self.wait_send_keys(OTP_4,otp[3])
            self.wait_send_keys(OTP_5,otp[4])
            self.wait_send_keys(OTP_6,otp[5])

            self.wait_and_click(Proceed_button_new)
            self.wait_for_invisibility(progress_bar) 
            #time.sleep(300)           

            self.wait_for_visibility(cibil_button)
            self.wait_and_click(cibil_button)
            self.wait_for_invisibility(progress_bar)
            time.sleep(2)
            self.wait_for_invisibility(progress_bar)
            self.interact_with_progress(submit_button)
            self.wait_for_invisibility(progress_bar)
            self.wait_and_click(Verifiy_acccount)
            self.wait_and_click(Confirm_ebv)
            self.wait_for_visibility(ver_iframe)
            ver_iframe1 = self.driver.find_element(By.ID, 'verificationIframe')
            self.driver.switch_to.frame(ver_iframe1)
            time.sleep(4)
            self.driver.switch_to.default_content()
            self.complete_ebv()
            self.driver.quit()

    def logout_relogin(self):
        excel_data = self.read_excel_file()
        for row in excel_data:
            chrome_service = Service(ChromeDriverManager().install())
            prefs = {
                "profile.default_content_setting_values.media_stream_mic": 1,
                "profile.default_content_setting_values.media_stream_camera": 1,
                "profile.default_content_setting_values.notifications": 1,
                "profile.default_content_setting_values.geolocation": 1
            }
            chrome_options = Options()
            # chrome_options.add_argument("--headless=new") 
            chrome_options.add_experimental_option("detach", True)
            chrome_options.add_experimental_option("prefs", prefs)
            chrome_options.add_argument("--use-fake-ui-for-media-stream")
            chrome_options.add_argument("--force-device-scale-factor=0.80")
            chrome_options.add_argument("--guest")
            self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
            self.driver.maximize_window()

            url = self.get_recent_final_url()
            self.driver.get(url)
            self.wait_for_visibility(language)

            self.wait_and_click(english_lang)
            #self.wait_for_visibility(progress_bar)
            self.wait_for_invisibility(progress_bar)

            self.driver.switch_to.default_content()

            self.wait_for_invisibility(progress_bar)

            time.sleep(2)


            self.wait_for_visibility(OTP_1)

            ver_code = db_obj.get_verification_code(row['Phone_Number_New'])
            otp = db_obj.aes_decrypt(ver_code)

            self.wait_send_keys(OTP_1,otp[0])
            self.wait_send_keys(OTP_2,otp[1])
            self.wait_send_keys(OTP_3,otp[2])
            self.wait_send_keys(OTP_4,otp[3])
            self.wait_send_keys(OTP_5,otp[4])
            self.wait_send_keys(OTP_6,otp[5])

            self.wait_and_click(Proceed_button_new)
            #self.wait_for_invisibility(progress_bar)  

            
        
    def complete_ebv(self):
        excel_data = self.read_excel_file()
        self.wait_for_invisibility(progress_bar)
        
        for row in excel_data:
            email = row['Valid_Email']
            cust = db_obj.get_customer_id(email)
            request_code = db_obj.get_ebv_request_code(cust)
            logging.info(f"Request Code for {cust} : {request_code}.")
            self.update_canarafi(cust, request_code)

            for attempt in range(10):
                try:
                    status = db_obj.get_customer_status(cust)
                    assert status == 160
                    break  
                except Exception as e:
                    logging.warning(f"Attempt {attempt + 1} failed for customer {cust}: {e}")
                    time.sleep(2)
            else:
                raise Exception(f"Status check failed after 10 attempts for customer {cust}")



    def update_canarafi(self, customer_id, request_code, html_content_file='steps/ebv.txt'):
        url = "https://stageapi.finextqa.xyz/api/EBV/SaveEBVReport"

        try:
            with open(html_content_file, 'r') as file:
                html_content = file.read().strip()
        except FileNotFoundError:
            logging.info(f"Error: The file {html_content_file} was not found.")
            return

        payload = {
            "HtmlContent": html_content,
            "YodleeStatusText": "SYNC",
            "NoOfTransactions": 50,
            "CustomerIdentifier": customer_id,
            "AccountNumberInput": "109309990",
            "RoutingNumberInput": "999988181",
            "InstitutionName": "DAG",
            "FirstNameInput": "Sashank",
            "LastNameInput": "R",
            "IsLoginValid": True,
            "RequestStatus": 2,
            "AccountNumberFound": "2093",
            "NameFound": "AMIT GROVER",
            "CurrentBalanceFound": 10310.16,
            "AvailableBalanceFound": 10310.16,
            "BankType": "CURRENT",
            "TotalDeposits": 0.0,
            "TotalWithdrawals": 0.0,
            "TransactionsFromDate": "2025-03-26 06:33:00.0000000",
            "TransactionsToDate": "2025-05-26 06:33:00.0000000",
            "RequestCode": request_code,
            "PageID": "SYNC",
            "canarifistatus": 80
        }

        headers = {
            'Content-Type': 'application/json',
            'accesstoken' : 'eyJhbGciOiJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzA0L3htbGRzaWctbW9yZSNobWFjLXNoYTI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE3Mzk3OTI5MjUsImV4cCI6MjA4NTM5MjkzMCwiaXNzIjoiRmxleFNhbGFyeVdlYiIsImF1ZCI6ImVidmludGVybmFsIiwiQWNjZXNzIjoiIiwiUGFydG5lcklEIjoiMSJ9.g90nmEB8jfcRlv29eIzFT3dMsn_17X2dXv-Kg-HLCkg'
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            logging.info("Request sent successfully.")
        except requests.exceptions.HTTPError as http_err:
            logging.info(f"HTTP error occurred: {http_err}")
            logging.info("Status Code:", response.status_code)
        except Exception as err:
            logging.info(f"Other error occurred: {err}")
            raise


    def vcip(self):
        excel_data = self.read_excel_file()
        for row in excel_data:
            chrome_service = Service(ChromeDriverManager().install())
            chrome_options = Options()
            # chrome_options.add_argument("--headless=new") 
            chrome_options.add_experimental_option("detach", True)
            chrome_options.add_argument("--incognito")
            chrome_options.add_argument("--force-device-scale-factor=0.80")
            chrome_options.add_argument("--guest")            

            self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

            self.driver.maximize_window()
            self.driver.get('https://finextqa.xyz/Admin/Lendez#x')

            self.wait_send_keys(lendez_username_input, 'Uday')
            self.wait_send_keys(lendez_password_input, 'Password@123')

            self.wait_and_click(lendez_login_button)
            self.wait_for_invisibility(progress_bar1)

            for i in range(20):
                try:
                    self.wait_and_click(vcip_vcip)
                    break
                except:
                    time.sleep(1)

            self.wait_for_invisibility(progress_bar1)
            time.sleep(2)

            self.wait_and_click(vcip_Approved_limit)
            self.wait_and_click(vcip_EBV_status)
            self.wait_and_click(installment_loan)
            self.wait_and_click(vcip_Sign_Status)
            self.select_dropdown_by_index(vcip_select_days,1)

            self.wait_and_click(launch_queue)

            self.wait_for_visibility(vcip_search_box)
            phone_number_cust = row['Phone_Number_New']
            cust = db_obj.get_customerid_customerphone(phone_number_cust)
            self.wait_send_keys(vcip_search_box,cust)
            self.wait_for_invisibility(progress_bar1)

            self.wait_and_click(vcip_view)

            self.wait_for_invisibility(progress_bar1)
            time.sleep(10)

            element = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable((By.ID,'ApprovalStatus')))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

            self.select_dropdown_value(vcip_Accepted,'Approve')
            submit_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(vcip_Submit))
            self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_element)
            try:
                self.wait_for_invisibility(progress_bar1)
                self.wait_and_click(submit_element)
            except ElementClickInterceptedException:
                logging.warning("ElementClickInterceptedException: Using JavaScript to click the Submit button.")
                self.driver.execute_script("arguments[0].click();", submit_element)

            self.wait_send_keys(vcip_notes,"Accepted the customer")
            self.wait_and_click(vcip_add_comment)

            self.wait_for_invisibility(progress_bar1)
            self.wait_for_visibility(vcip_search_box)
            self.driver.quit()


    def verify_customer(self):
        excel_data = self.read_excel_file()
        for row in excel_data:
            chrome_service = Service(ChromeDriverManager().install())
            chrome_options = Options()
            # chrome_options.add_argument("--headless=new") 
            chrome_options.add_experimental_option("detach", True)
            chrome_options.add_argument("--incognito")
            chrome_options.add_argument("--force-device-scale-factor=0.80")
            chrome_options.add_argument("--guest")
            self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
            self.driver.maximize_window()
            self.driver.get('https://finextqa.xyz/admin/lendez/#x')


            self.wait_send_keys(lendez_username_input, 'Uday')
            self.wait_send_keys(lendez_password_input, 'Password@123')

            self.wait_and_click(lendez_login_button)
            self.wait_for_invisibility(progress_bar1)

            time.sleep(2)

            self.wait_for_visibility(pending_verification_queue)
            self.wait_for_invisibility(progress_bar1)

            self.wait_and_click(pending_verification_queue)
            self.wait_for_invisibility(progress_bar1)
            time.sleep(2)

            self.wait_and_click(product_msme)
            self.wait_and_click(emp_type_both)
            #self.wait_and_click(income_type_both)
            self.wait_and_click(ebv_status_both)
            self.wait_and_click(verification_lauch_queue)

            self.wait_for_invisibility(progress_bar)

            cust = db_obj.get_customer_id(row['Valid_Email'])

            self.wait_send_keys(approve_search_box,cust)
            self.wait_and_click(approve_select_customer)

            self.wait_for_invisibility(progress_bar1)
            self.scroll_to_element(ver_page_end)
            
            self.select_dropdown_value(approve_status_dropdown,'Accepted')
            self.wait_for_visibility(progress_bar1)
            self.wait_for_invisibility(progress_bar1)

            # self.wait_send_keys(approve_amount,row['Approve_amount'])
            self.wait_send_keys(approve_amount,'100000')
            self.wait_for_invisibility(progress_bar1)
            time.sleep(1)

            self.select_dropdown_value(approve_tenure,'24')
            self.select_dropdown_by_index(loan_intrest,3)
            self.wait_for_invisibility(progress_bar)

            time.sleep(2)

            self.scroll_to_element(ver_page_end)
            self.wait_for_visibility(ver_page_end)
            self.wait_for_invisibility(progress_bar1)
            time.sleep(2)

            self.wait_and_click(submit_approve)
            self.wait_and_click(Apporve_loan)
            
            self.wait_for_visibility(approve_search_box)

            self.driver.quit()


    def update_customer_ckyc(self):
        excel_data = self.read_excel_file()
        for row in excel_data:
            customer_id = db_obj.get_customer_id(row['Valid_Email'])
            ckyc_id = db_obj.get_ckyc_id(customer_id)
            db_obj.update_ckyc_status(ckyc_id)
            db_obj.update_search_download(ckyc_id)


    def login_customer(self):
        excel_data = self.read_excel_file()
        for row in excel_data:
            chrome_service = Service(ChromeDriverManager().install())
            chrome_options = Options()
            # chrome_options.add_argument("--headless=new") 
            chrome_options.add_experimental_option("detach", True)
            chrome_options.add_argument("--incognito")

            chrome_options.add_argument("--guest")
            self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
            self.driver.maximize_window()
            self.driver.get(self.build_url())

            # self.wait_for_visibility(mobile_number_feild)
            # self.wait_send_keys(mobile_number_feild,row['Phone_Number_New'])

            # self.wait_and_click(udyam_consent)
            

            # self.interact_with_progress(submit_number)
            # self.wait_for_invisibility(progress_bar)

            # self.wait_send_keys(lendez_password_input,row['Password'])
            # self.wait_and_click(submit_number)
            # self.wait_for_invisibility(progress_bar)



    def login_customer2(self):
        excel_data = self.read_excel_file()
        for row in excel_data:
            chrome_service = Service(ChromeDriverManager().install())
            chrome_options = Options()
            # chrome_options.add_argument("--headless=new") 
            chrome_options.add_experimental_option("detach", True)
            chrome_options.add_argument("--incognito")

            chrome_options.add_argument("--guest")
            self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
            self.driver.maximize_window()
            self.driver.get('https://msme.finextqa.xyz/#x')

            self.wait_for_visibility(mobile_number_feild)
            self.wait_send_keys(mobile_number_feild,row['Phone_Number_New'])

            self.wait_and_click(udyam_consent)
            

            self.interact_with_progress(submit_number)
            self.wait_for_invisibility(progress_bar)

            self.wait_send_keys(udyam_password_input,row['Password'])
            self.wait_and_click(submit_number)
            self.wait_for_invisibility(progress_bar)




    def handle_interaction_and_alert(self):
        while True:
            try:
                self.wait_for_visibility(vkyc_select_language)
                self.select_dropdown_by_index(vkyc_select_language, 1)
                self.wait_and_click(vkyc_save_next)
                try:
                    WebDriverWait(self.driver, 2).until(EC.alert_is_present())
                    time.sleep(3)
                    alert = self.driver.switch_to.alert
                    alert.accept()
                except:
                    time.sleep(1)
                    logging.info("No alert present.")
                    break 
            except Exception as e:
                logging.error(f"An error occurred: {str(e)}")
                break

    def customer_vkyc(self):
        excel_data = self.read_excel_file()
        for row in excel_data:
            chrome_service = Service(ChromeDriverManager().install())
            prefs = {
                "profile.default_content_setting_values.media_stream_mic": 1,
                "profile.default_content_setting_values.media_stream_camera": 1,
                "profile.default_content_setting_values.notifications": 1,
                "profile.default_content_setting_values.geolocation": 1
            }
            chrome_options = Options()
            # chrome_options.add_argument("--headless=new") 
            chrome_options.add_experimental_option("detach", True)
            chrome_options.add_experimental_option("prefs", prefs)
            chrome_options.add_argument("--use-fake-ui-for-media-stream")
            chrome_options.add_argument("--force-device-scale-factor=0.80")
            chrome_options.add_argument("--guest")
            self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
            self.driver.maximize_window()

            self.driver.get('https://msme.finextqa.xyz/#x')

            self.wait_for_visibility(mobile_number_feild)
            self.wait_send_keys(mobile_number_feild,row['Phone_Number_New'])

            self.interact_with_progress(udyam_consent)
            

            self.interact_with_progress(submit_number)
            self.wait_for_invisibility(progress_bar)

            self.wait_send_keys(udyam_password_input,row['Password'])
            self.wait_and_click(submit_number)
            self.wait_for_invisibility(progress_bar1)

            try:
                self.login_mfa()
            except:
                pass


            self.wait_and_click(Proceed_button)
            self.wait_for_invisibility(progress_bar1)

            self.wait_for_visibility(vkyc_mitc_loaded)
            self.wait_for_invisibility(progress_bar1)

            
            self.scroll_to_element(vkyc_continue)
            
            

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.wait_for_invisibility(progress_bar1)
            time.sleep(5)

            self.wait_and_click(vkyc_continue)
            self.wait_for_invisibility(progress_bar1)

            iframe_vkyc = (By.XPATH,'/html/body/div[1]/div[7]/div[1]/iframe')
            self.wait_for_visibility(iframe_vkyc,wait_time=300)

            Iframe4 = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable(iframe_vkyc))

            self.driver.switch_to.frame(Iframe4)

            self.wait_for_visibility(we_are_connecting)
            self.driver.execute_script("window.open('https://finextqa.xyz/admin/lendez/#x');")

            tabs = self.driver.window_handles
            self.driver.switch_to.window(tabs[1])


            self.wait_send_keys(lendez_username_input, 'Uday')
            self.wait_send_keys(lendez_password_input, 'Password@123')

            self.wait_and_click(lendez_login_button)
            self.wait_for_invisibility(progress_bar1)


            for i in range(20):
                try:
                    self.wait_and_click(vkyc_queue)
                    break
                except:
                    time.sleep(1)

            self.wait_for_invisibility(progress_bar1)

            time.sleep(2)
            self.wait_and_click(product_msme)
            #self.wait_and_click(loan_type_all)
            self.wait_and_click(launch_queue)
            self.wait_for_invisibility(progress_bar1)

            customerid = db_obj.get_customer_id(row['Valid_Email'])
   
            self.wait_send_keys(vkyc_search_box,customerid)

            #self.wait_send_keys(vkyc_search_box,'1988972')

            self.wait_and_click(vkyc_click_join)
            Iframe = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable(vkyc_iframe))
            self.driver.switch_to.frame(Iframe)

            self.wait_for_visibility(vkyc_select_language)
            self.wait_for_visibility(vkyc_save_next)



            tabs = self.driver.window_handles
            self.driver.switch_to.window(tabs[0])
            

            try:

                WebDriverWait(self.driver, 10).until(EC.alert_is_present())
                alert = self.driver.switch_to.alert
                alert.accept()
            except:
                pass


            tabs = self.driver.window_handles
            logging.info(tabs)
            self.driver.switch_to.window(tabs[1])

            title = self.driver.title
            logging.info(f"Current tab title: {title}")

            Iframe = WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable(vkyc_iframe))
            self.driver.switch_to.frame(Iframe)

            self.wait_for_visibility(vkyc_select_language)




            try:
                WebDriverWait(self.driver, 2).until(EC.alert_is_present())
                alert = self.driver.switch_to.alert
                alert.accept()
            except Exception as e:
                logging.info("Exception occured {}".format(e))
                pass

            self.handle_interaction_and_alert()

            for i in range(20):
                try:
                    patner_cust = db_obj.get_patner_customerid(customerid)
                    taskdetails_id = db_obj.get_taskdetails_id(patner_cust)
                    partner_location = db_obj.get_partner_location(taskdetails_id)
                    logging.info(f"Found records Customer_Id: {customerid}, patner_cust_id: {patner_cust}, taskdetails_id: {taskdetails_id}, partner_location_id: {partner_location}")

                    assert patner_cust is not None
                    assert taskdetails_id is not None
                    assert partner_location is not None

                    logging.info(f"Took : {i}")
                    break
                except AssertionError:
                    logging.info(f"All records not found: {i}")
                    time.sleep(1)

            self.wait_for_visibility(vkyc_confirm_identity)

            self.wait_and_click(vkyc_save_next)
            self.wait_for_visibility(read_consent_page)
            self.wait_and_click(vkyc_save_next)
            self.wait_for_visibility(vkyc_live_check)
            self.wait_and_click(vkyc_save_next)
            self.wait_for_visibility(vkyc_location_photo_page)
            time.sleep(2)
            self.wait_and_click(vkyc_capture_image)
            self.wait_and_click(vkyc_approv_consent)
            self.wait_and_click(vkyc_save_image)
            self.wait_and_click(vkyc_save_next)
            self.wait_and_click(vkyc_pan_card_capture)
            self.wait_and_click(vkyc_original)
            self.wait_and_click(vkyc_image_clear)
            self.wait_and_click(vkyc_save_image_vkyc)
            self.wait_and_click(vkyc_save_next)
            self.select_dropdown_by_index(vkyc_select_type,1)
            self.wait_and_click(vkyc_capture_front)

            self.wait_send_keys(vkyc_id_number_id,row['PAN_Number'])
            time.sleep(2)

            self.wait_and_click(vkyc_image_clear3)
            self.wait_and_click(vkyc_save_image_2)
            self.wait_and_click(vkyc_save_next)

            self.select_dropdown_by_index(vkyc_choose_type_2,1)
            self.wait_and_click(vkyc_capture_front_2)
            time.sleep(1)
            self.driver.find_element(By.ID,'addressProofDetailsYes').click()
            time.sleep(2)

            self.driver.find_element(By.XPATH,'/html/body/div[12]/div/div/div[2]/div/div[2]/div[4]/input').click()
            self.driver.find_element(By.XPATH,'/html/body/div[12]/div/div/div[2]/div/div[2]/div[5]/input').click()

            self.driver.find_element(By.XPATH, '//*[@id="vkycAdressPopUp"]/div/div/div[2]/div/div[2]/div[6]/button[2]').click()


            self.wait_and_click(vkyc_save_next)

            self.wait_and_click(businees_photo_capture)
            time.sleep(4)
            self.driver.find_element(By.XPATH,'/html/body/div[9]/div/div/div[2]/div/div[2]/div[3]/input').click()
            self.driver.find_element(By.XPATH,'/html/body/div[9]/div/div/div[2]/div/div[2]/div[4]/input').click()



            self.wait_and_click(vkyc_save_image_buss)
            self.wait_and_click(vkyc_save_next)


            self.wait_and_click(businees_photo)
            self.wait_and_click(vkyc_approv_consent1)
            self.wait_and_click(vkyc_save_image)
            self.wait_and_click(vkyc_save_next)

            self.wait_and_click(vkyc_close)
            self.wait_and_click(vkyc_save_next)

            self.wait_and_click(vkyc_close_2)
            self.wait_and_click(vkyc_save_next)

            self.wait_and_click(vkyc_save_next)

            time.sleep(1)
            self.wait_and_click(vkyc_self_declaration)
            time.sleep(1)
            self.wait_and_click(vkyc_save_next)

            self.wait_and_click(vkyc_finish)

            try:
                start_time = time.time()
                WebDriverWait(self.driver, 5).until(EC.alert_is_present())
                alert = self.driver.switch_to.alert
                alert.accept()
                duration = time.time() - start_time
                logging.info("Interacted with alert in : {:.2f} ".format(duration))
                self.driver.quit()

            except Exception as e:
                logging.error(f"Exception: {e}")
                
            self.driver.quit()



    def update_esgin(self):
        excel_data = self.read_excel_file()
        for row in excel_data:
            cust = db_obj.get_customer_id(row['Valid_Email'])
            db_obj.update_esign_status(cust)
            logging.info(f"Updated e-sign status for customer ID: {cust}.")


    def update_esgin_neg(self):
        excel_data = self.read_excel_file()
        for row in excel_data:
            cust = db_obj.get_customer_id(row['Valid_Email'])
            db_obj.update_esign_negative(cust)
            logging.info(f"Updated e-sign status for customer ID: {cust}.")


    def pendings_open(self):
        excel_data = self.read_excel_file()
        for row in excel_data:
            chrome_service = Service(ChromeDriverManager().install())
            chrome_options = Options()
            # chrome_options.add_argument("--headless=new") 
            chrome_options.add_experimental_option("detach", True)
            chrome_options.add_argument("--incognito")

            chrome_options.add_argument("--guest")
            self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
            self.driver.maximize_window()
            self.driver.get('https://finextqa.xyz/admin/lendez/#x')


            self.wait_send_keys(lendez_username_input, 'Uday')
            self.wait_send_keys(lendez_password_input, 'Password@123')

            self.wait_and_click(lendez_login_button)
            self.wait_for_invisibility(progress_bar1)

            self.wait_and_click(pendings_open)

            time.sleep(2)


            self.wait_and_click(product_msme)

            self.wait_and_click(installment_loan)

            self.wait_and_click(verification_lauch_queue)


            cust = db_obj.get_customerid_customerphone(row['Phone_Number_New'])

            self.wait_send_keys(approve_search_box,cust)

            self.wait_and_click(pendings_open_select_customer)
            time.sleep(2)

            self.wait_for_invisibility(progress_bar1)

            self.wait_for_visibility(pendings_Selfie)

            self.scroll_to_element(ver_page_end)


            self.select_dropdown_value(approve_status_dropdown,'Approved')

            self.wait_for_invisibility(progress_bar1)

            self.scroll_to_element(submit_approve)
            self.wait_for_invisibility(progress_bar1)
            time.sleep(2)

            self.wait_and_click(submit_approve)

            self.wait_and_click(pendings_ok)

            self.wait_for_visibility(approve_search_box)

            self.driver.quit()



    def pendings_open_eign(self):
        excel_data = self.read_excel_file()
        for row in excel_data:
            chrome_service = Service(ChromeDriverManager().install())
            chrome_options = Options()
            # chrome_options.add_argument("--headless=new") 
            chrome_options.add_experimental_option("detach", True)
            chrome_options.add_argument("--incognito")

            chrome_options.add_argument("--guest")
            self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
            self.driver.maximize_window()
            self.driver.get('https://finextqa.xyz/admin/lendez/#x')


            self.wait_send_keys(lendez_username_input, 'Uday')
            self.wait_send_keys(lendez_password_input, 'Password@123')

            self.wait_and_click(lendez_login_button)
            self.wait_for_invisibility(progress_bar1)

            self.wait_and_click(pendings_open)

            time.sleep(2)


            self.wait_and_click(product_msme)

            self.wait_and_click(installment_loan)

            self.wait_and_click(verification_lauch_queue)


            cust = db_obj.get_customerid_customerphone(row['Phone_Number_New'])

            self.wait_send_keys(approve_search_box,cust)

            self.wait_and_click(pendings_open_select_customer)
            time.sleep(2)


            self.wait_for_invisibility(progress_bar1)

            self.wait_for_visibility(pendings_Selfie)

            self.scroll_to_element(ver_page_end)


            self.select_dropdown_value(approve_status_dropdown,'Approved')

            self.wait_for_invisibility(progress_bar1)
            

            self.scroll_to_element(submit_approve)
            

            self.wait_for_invisibility(progress_bar1)
            time.sleep(2)
            # self.wait_and_click(Accept_EsignID)

            self.wait_for_invisibility(progress_bar1)
            self.scroll_to_element(back_to_list)  # Should scroll it into view
            time.sleep(2)  # Let rendering complete

            # Ensure clickable
            self.wait_and_click(back_to_list)

            self.wait_and_click(Save_Changes)

            self.wait_for_visibility(approve_search_box)

            self.driver.quit()

    def login_mfa(self):
        self.wait_for_invisibility(progress_bar)
        self.wait_for_visibility(OTP_1,wait_time=5)
        excel_data = self.read_excel_file()
        for row in excel_data:
            phone = row['Phone_Number_New']
            cust = db_obj.get_customerid_customerphone(phone)
            ver_code = db_obj.get_login_otp(cust)
            otp = db_obj.aes_decrypt(ver_code)

            self.wait_send_keys(OTP_1,otp[0])
            self.wait_send_keys(OTP_2,otp[1])
            self.wait_send_keys(OTP_3,otp[2])
            self.wait_send_keys(OTP_4,otp[3])
            self.wait_send_keys(OTP_5,otp[4])
            self.wait_send_keys(OTP_6,otp[5])

            self.wait_and_click(submit_login_otp)

    def complete_esing(self):
        self.customer_login()
        self.interact_with_progress(esign_button)
        self.wait_and_click(esign_yes)

        self.interact_with_progress(esign_agree)
        self.interact_with_progress(esign_agree_proceed)
        self.interact_with_progress(zoop_proceed)
        self.wait_and_click(zoop_proceed2)
        self.wait_for_visibility(nsdl_page)

        self.update_esgin()
        self.driver.quit()

    def customer_login(self):
        excel_data = self.read_excel_file()
        for row in excel_data:
            chrome_service = Service(ChromeDriverManager().install())

            chrome_options = Options()
            # chrome_options.add_argument("--headless=new") 
            chrome_options.add_experimental_option("detach", True)
            self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
            self.driver.maximize_window()

            self.driver.get('https://msme.finextqa.xyz/#x')

            self.wait_for_visibility(mobile_number_feild)
            self.wait_send_keys(mobile_number_feild,'7948910351')
            #self.wait_send_keys(mobile_number_feild,row['Phone_Number_New'])

            self.interact_with_progress(udyam_consent)
            

            self.interact_with_progress(submit_number)
            self.wait_for_invisibility(progress_bar)

            self.wait_send_keys(udyam_password_input,row['Password'])
            self.wait_and_click(submit_number)
            self.wait_for_invisibility(progress_bar1)

            try:
                self.login_mfa()
            except:
                pass

    def emandate(self):
        self.interact_with_progress(mandate_proceed)
        iframe = self.driver.find_element(By.XPATH, '/html/body/div[2]/iframe[1]')
        self.driver.switch_to.frame(iframe)

        self.wait_and_click(savings_account)
        self.select_dropdown_by_index(select_Account_type,1)

        original_window = self.driver.current_window_handle
        existing_windows = self.driver.window_handles

        self.wait_and_click(authenticate)

        WebDriverWait(self.driver, 30).until(
            lambda d: len(d.window_handles) > len(existing_windows)
        )

        new_window = [window for window in self.driver.window_handles if window not in existing_windows][0]
        self.driver.switch_to.window(new_window)

        self.driver.save_screenshot("before_click.png")


        self.wait_and_click(Sucess_button)
        time.sleep(2)

        # Optional: switch back to the original window
        self.driver.switch_to.window(original_window)

        self.driver.quit()



    def validate_mpin(self):
        self.login_customer2()

    