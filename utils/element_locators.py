from selenium.webdriver.common.by import By

lendez_username_input = (By.ID, 'Username')
lendez_password_input = (By.ID, 'Password')


lendez_login_button = (By.CSS_SELECTOR, '.formsubmit[value="Login"]')

New_registation = (By.XPATH, '/html/body/div/div[3]/div/div[5]/div[2]/div/div[3]/div[1]/div/div[2]/div[2]/div/a/div/b')
mobile_number_feild = (By.ID, 'MobileNumber')
udyam_password_input = (By.ID, 'password')

agreements_next = (By.ID, 'next')

tc_iframe = (By.ID, 'iframeterms')
loan_intrest = (By.ID, 'ProductSelectionDetails_Interest')
Apporve_loan = (By.ID, 'ApprovalModelSubmitbtn')


vcip_vcip = (By.XPATH, '/html/body/div/div[3]/div/div[5]/div[2]/div/div[3]/div[5]/div/div[2]/div[2]/div/a/div/b')
vcip_Approved_limit = (By.XPATH, '//*[@id="rdIncomeTypeboth"]')
vcip_EBV_status = (By.XPATH, '//*[@id="rdebvstatusboth"]')
vcip_Sign_Status = (By.XPATH, '//*[@id="rdLoanstatusboth"]')
vcip_search_box = (By.XPATH, '/html/body/div/div[3]/div/div[5]/div[2]/div/div[3]/div/div[2]/div/div/div[2]/label/input')
vcip_view = (By.XPATH, '//*[@id="responsive-datatable"]/tbody/tr/td[9]/a')
vcip_Accepted = (By.ID, 'ApprovalStatus')
vcip_Submit = (By.ID, 'SubmitID')
vcip_notes = (By.ID, 'ApproveNotestxt')
vcip_add_comment = (By.ID, 'btnApproveStatusSubmit')

vcip_select_days = (By.XPATH, '//*[@id="dddaterange"]')



udyam_consent = (By.ID, 'terms2')
submit_number = (By.ID, 'LoginSubmit')

progress_bar = (By.ID, 'loader')

progress_bar1 = (By.XPATH, '//*[@id="globalProgressPopup"]/img')






submit_login_otp = (By.XPATH, '//*[@id="otpForm"]/div[4]/button')

OTP_1 = (By.ID, 'otp-1')

OTP_2 = (By.ID, "otp-2")
OTP_3 = (By.ID, "otp-3")
OTP_4 = (By.ID, "otp-4")
OTP_5 = (By.ID, "otp-5")
OTP_6 = (By.ID, "otp-6")
resend_otp = (By.ID, "resendOtpLink")
verify_otp = (By.ID, "verifyOtp")

password_input = (By.ID, "password")
confirm_password = (By.ID, "confirmPassword")
create_password = (By.ID, "createPassword")


first_name = (By.ID, "FirstName")
last_name = (By.ID, "LastName")
Dob_feild = (By.ID, "DateOfBirth")
email_feild = (By.ID, "Email")
address_line1 = (By.ID, "AddressLine1")
address_line2 = (By.ID, "AddressLine2")
pincode = (By.ID, "Pincode")
residence_city = (By.ID, "City")


Pan_Number = (By.ID, "PANNumber")
Create_account = (By.ID, "create-account")
Business_name = (By.ID, "BusinessName")
Retailer_id = (By.ID, "RetailerId")
Business_estb_date = (By.ID, "BusinessEstDate")
Business_type = (By.ID, "Businesstype")
Business_mobile = (By.ID, "BusinessMobileNumber")
Business_industry = (By.ID, "BusinessIndustry")
Business_online = (By.ID, "BusinessOnline")
Business_website = (By.ID, "BusinessWebsite")
Upload_submit = (By.ID, "submitButton")
submit_ebv = (By.ID, "ebvButton")

Required_amount = (By.ID, "RequiredLoanAmount")
Repayment_tenure = (By.ID, "RepaymentTenure")
Loan_purpose = (By.ID, "LoanPurpose")

Verifiy_acccount = (By.XPATH, '//*[@id="bankVerificationForm"]/div[2]/button')

Confirm_ebv = (By.XPATH, '//*[@id="verificationModal"]/div/div/div[3]/button')
One_money_otp = (By.ID, 'otp_input')

ver_iframe = (By.ID,'verificationIframe')

Proprietorship = (By.ID, "1")
Individual = (By.ID, "2")
Business_clssifincation = (By.ID, "BusinessClassification")
Avg_mothly_profit = (By.ID, "AverageMonthlyProfit")
Avg_mothly_turnover = (By.ID, 'AverageMonthlyTurnover')
Business_transaction_mode  = (By.ID, '1')
Business_description = (By.ID, 'BusinessDesctiption')
Business_upiid = (By.ID, 'BusinessUPIIDs_0_')
IFSC_Code = (By.ID, 'BankAccounts_0__BankIFSCCode')
Account_type  = (By.ID, 'accounttype')
Account_active_month = (By.ID, 'BankAccounts_0__ActiveSinceMonth')

Account_active_year = (By.ID, 'BankAccounts_0__ActiveSinceYear')
Account_number = (By.NAME, 'BankAccounts[0].AccountNumber')
Confirm_account = (By.NAME, 'BankAccounts[0].ConfirmAccountNumber')
submit_button = (By.ID, 'form-submit')



Upload_bank_statement  = (By.ID, 'fileInput')
Upload_itr   = (By.ID, 'ITRFiling_File')
Upload_gst1 = (By.ID, 'GSTReports[0].File')

Upload_gst2 = (By.ID, 'GSTReports[2].File')

Upload_gst3 = (By.ID, 'GSTReports[4].File')
Upload_gst4  = (By.ID, 'GSTReports[6].File')
Upload_gst5  = (By.ID, 'GSTReports[8].File')
Upload_gst6  = (By.ID, 'GSTReports[10].File')

Upload_gst3b = (By.ID, 'GSTReports[1].File')
Upload_gst3b2 = (By.ID, 'GSTReports[3].File')
Upload_gst3b3 = (By.ID, 'GSTReports[5].File')
Upload_gst3b4 = (By.ID, 'GSTReports[7].File')
Upload_gst3b5 = (By.ID, 'GSTReports[9].File')
Upload_gst3b6 = (By.ID, 'GSTReports[11].File')

upload_pan = (By.ID, 'PANCard_File')
proof_of_identity = (By.ID, 'identityProofSelect')
upload_id_proof = (By.ID, 'IdentityProof_File')


upload_poa_front = (By.ID, 'ProofOfAddress_Front_File')
upload_poa_back = (By.ID, 'ProofOfAddress_Back_File')

submit_documents = (By.XPATH, '//*[@id="uploadForm"]/div[4]/button')

upload_business_photo = (By.ID, 'BusinessPhoto_File')

upload_business_doc_front = (By.ID, 'BusinessRegistrationFront_File')
upload_business_doc_back = (By.ID, 'BusinessRegistrationBack_File')

upload_business_address_proof = (By.ID, 'ProofOfAddress_File')

select_address_type = (By.ID, 'proofOfAddressSelect')


being_verified = (By.XPATH, '/html/body/main/div[2]/div/div/div/div/div[1]/div/h5')






pending_verification_queue = (By.XPATH, '/html/body/div/div[3]/div/div[5]/div[2]/div/div[3]/div[2]/div/div[2]/div[2]/div/a/div/b')
loan_type_all = (By.ID, 'rdAll')


product_msme = (By.ID, 'rdmsme')
emp_type_both = (By.ID, 'rdEmpTypeboth')
income_type_both = (By.ID, 'rdIncomeTypeboth')
ebv_status_both = (By.ID, 'rdebvstatusboth')
verification_lauch_queue = (By.ID, 'Launchqueue')
ver_page_end = (By.ID, 'year')

approve_status_dropdown = (By.ID, 'ApprovalStatus')
submit_approve = (By.ID, 'SubmitID')
click_yes_approve = (By.ID, 'AcceptReqProccedBtn')
approve_search_box = (By.XPATH, '//*[@id="responsive-datatable_filter"]/label/input')
approve_select_customer = (By.XPATH, '//*[@id="responsive-datatable"]/tbody/tr/td[1]')

login_edit_button = (By.XPATH, '//*[@id="responsive-datatable"]/tbody/tr/td[4]/a')
pendings_open_select_customer = (By.XPATH, '//*[@id="responsive-datatable"]/tbody/tr/td[7]/a')
pendings_ok = (By.XPATH, '//*[@id="globalPopup"]/div[2]/div/a')

approve_amount = (By.ID, 'ProductSelectionDetails_Amount')
approve_tenure = (By.ID, 'ProductSelectionDetails_Tenure')



pendings_Selfie = (By.ID, 'selfieID')



Proceed_button = (By.ID, 'Proceed')
Start_button = (By.ID, 'startButton')
Capture_button = (By.ID, 'captureButton')

vkyc_loaded = (By.ID, 'waitingDivID')



vkyc_second_tab = (By.ID, 'v-pills-second-tab')
kyc_document_dropdown = (By.ID, 'kycDocument')
capture_kyc_front = (By.ID, 'captureKYCFrontButton')
capture_kyc_back = (By.ID, 'captureKYCBackButton')

vkyc_thrid_tab = (By.ID, 'v-pills-three-tab')
address_proof_dropdown = (By.ID, 'AddressProof')
capture_address_front = (By.ID, 'captureAddressProofFrontButton')
capture_address_back = (By.ID, 'captureAddressProofBackButton')

vkyc_fourth_tab = (By.ID, 'v-pills-four-tab')
capture_pan_button = (By.ID, 'capturePanButton')



pendings_open = (By.XPATH, '/html/body/div/div[3]/div/div[5]/div[2]/div/div[3]/div[4]/div/div[2]/div[2]/div/a/div/b')

installment_loan = (By.ID, 'rdinstallmentloan')


vkyc_fifth_tab = (By.ID, 'v-pills-five-tab')
capture_bussiness_name_board = (By.ID, 'captureBNBButton')
vkyc_sixth_tab = (By.ID, 'v-pills-six-tab')
  

capture_bussiness_name = (By.ID, 'captureBPButton')
stop_button = (By.ID, 'stopButton')
save_button = (By.ID, 'saveButton')

vkyc_loader = (By.XPATH, '//*[@id="loader"]/div')
share_link = (By.ID, 'sendDownloadLink')

vkyc_mitc_loaded = (By.XPATH, '/html/body/div[1]/div[7]/div/div/div/div/div[1]/h2')


vkyc_continue = (By.ID, 'ContinueBtn')




vkyc_queue = (By.XPATH, '/html/body/div/div[3]/div/div[5]/div[2]/div/div[3]/div[3]/div/div[2]/div[2]/div/a/div/b')
launch_queue = (By.ID, 'Launchqueue')


vkyc_search_box = (By.XPATH, '//*[@id="responsive-datatable_filter"]/label/input')
vkyc_click_join = (By.XPATH, '//*[@id="responsive-datatable"]/tbody/tr[1]/td[7]/a')
vkyc_iframe = (By.XPATH, '/html/body/div/div[3]/div/div[5]/div[2]/div/iframe')
vkyc_select_language = (By.XPATH, '/html/body/div[1]/div/div[1]/div/div/div/div[2]/div/div/div[3]/div[2]/section[1]/div[2]/select')
vkyc_confirm_identity = (By.XPATH, '//*[@id="example-vertical-p-1"]/p')
vkyc_save_next = (By.XPATH, '//*[@id="example-vertical"]/div[3]/ul/li[1]/a')
vkyc_live_check = (By.XPATH, '//*[@id="example-vertical-p-3"]/p')

vkyc_location_photo_page = (By.XPATH, '//*[@id="example-vertical-p-4"]/p')

vkyc_id_number_id = (By.ID, 'IDNumber')
we_are_connecting = (By.ID, 'waitingDivID')


vkyc_image_clear3 = (By.XPATH, '/html/body/div[14]/div[2]/div/div[2]/div/div[2]/div[3]/input')


read_consent_page = (By.XPATH, '//*[@id="example-vertical-p-2"]/p')


vkyc_capture_image = (By.XPATH, '//*[@id="example-vertical-p-4"]/div[2]/div[2]/div/div/div[1]/div/button')
vkyc_approv_consent = (By.ID, 'disclaimer')
vkyc_approv_consent1 = (By.XPATH, '/html/body/div[14]/div[1]/div/div[3]/div[1]/input')


vkyc_save_image = (By.XPATH, '//*[@id="imagePopUp"]/div[1]/div/div[3]/div[2]/button[2]')
vkyc_save_image_buss = (By.XPATH, '//*[@id="vkycBusinessDetails"]/div/div/div[2]/div/div[2]/div[5]/button[2]')


vkyc_pan_card = (By.XPATH, '//*[@id="example-vertical-p-5"]/p')
vkyc_pan_card_capture = (By.XPATH, '//*[@id="example-vertical-p-5"]/div[2]/div[2]/div/div/div[1]/div/button')
vkyc_original = (By.XPATH, '//*[@id="approveDocumentDisclaimer"]')
vkyc_image_clear2 = (By.XPATH, '/html/body/div[5]/div/div/div[2]/div/div[2]/div[5]/input')
vkyc_image_clear = (By.XPATH, '//*[@id="approveImageDisclaimer"]')
vkyc_save_image_vkyc = (By.XPATH, '//*[@id="vkycPopUp"]/div/div/div[2]/div/div[2]/div[7]/button[2]')
vkyc_kyc_document = (By.XPATH, '//*[@id="example-vertical-p-6"]/p')
vkyc_select_type = (By.ID, '22238Select')
Accept_EsignID = (By.ID, 'AcceptEsignID')
Save_Changes = (By.ID, 'SaveDocDetails')
udhyam_number = (By.XPATH, '//*[@id="BusinessUDYAMNumber"]')



back_to_list = (By.XPATH, '/html/body/div[1]/div[3]/div/div[5]/div[2]/div/div[2]/div[1]/div/ol/li/button')



vkyc_capture_front = (By.XPATH, '//*[@id="example-vertical-p-6"]/div[3]/div[2]/div/div/div[1]/div/button')
vkyc_id_number = (By.XPATH, '/html/body/div[13]/div[2]/div/div[2]/div/div[2]/div[1]/div[2]/div/input')
vkyc_save_image_2 = (By.XPATH, '//*[@id="imagePopUp"]/div[2]/div/div[2]/div/div[2]/div[4]/button[2]')
vkyc_address_proof = (By.XPATH, '//*[@id="example-vertical-p-7"]/p')
vkyc_choose_type_2 = (By.ID, '22234Select')

vkyc_capture_front_2 = (By.XPATH, '//*[@id="example-vertical-p-7"]/div[3]/div[4]/div/div/div[1]/div/button')
vkyc_location_yes = (By.XPATH, '//*[@id="addressProofDetailsYes"]')
vkyc_disclaimer = (By.XPATH, '/html/body/div[12]/div/div/div[2]/div/div[2]/div[4]/input')
vkyc_save_image_3 = (By.XPATH, '//*[@id="vkycAdressPopUp"]/div/div/div[2]/div/div[2]/div[6]/button[2]')
vkyc_close = (By.XPATH, '//*[@id="partialModal"]/div/div/div[1]/button')
vkyc_close_2 = (By.XPATH, '//*[@id="myKFCModal"]/div/div/div[1]/button')
vkyc_self_declaration = (By.XPATH, '//*[@id="selfdeclarationcheckbox"]')
vkyc_finish = (By.XPATH, '//*[@id="example-vertical"]/div[3]/ul/li[2]/a')


businees_photo_capture = (By.XPATH, '//*[@id="example-vertical-p-8"]/div[2]/div[3]/div/div/div[1]/div/button')

businees_photo = (By.XPATH, '//*[@id="example-vertical-p-9"]/div[2]/div[3]/div/div/div[1]/div/button')

esign_button = (By.ID, 'eSignOptionSelected')

esign_yes = (By.ID, 'btn-clickonyes')
esign_no = (By.ID, 'btn-clickonno')

esign_edit_number = (By.ID, 'phone-number-display')



esign_verify = (By.ID, 'btn-verify')
esign_agree = (By.XPATH, '//*[@id="consentAgr"]/div[3]/div/div/button')

esign_agree_proceed = (By.XPATH, '//*[@id="Agreementsec"]/div[4]/div/div/button')
zoop_proceed = (By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div/div[2]/div/div[3]/div/button')

zoop_proceed2 = (By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div/div[2]/div/div[3]/div/div/button')
nsdl_page = (By.XPATH, '/html/body/div[2]/div/div/div[1]/header/div[1]/nav/div/div')




mandate_proceed = (By.ID, 'proceedToEmandate')
emandate_frame = (By.XPATH, '/html/body/div[2]/iframe[1]')

savings_account = (By.XPATH, '//*[@id="emandate-options"]/div[2]')
select_Account_type = (By.XPATH, '//*[@id="emandate-inner"]/div/div[5]/div/select')
authenticate = (By.ID, 'redesign-v15-cta')
Sucess_button = (By.XPATH, '/html/body/form/button[1]')
# mandate_proceed = (By.ID, 'proceedToEmandate')



language = (By.XPATH, '//*[@id="preferredLanguage"]/div/div')
english_lang = (By.ID, 'english-language')
Proceed_button_new = (By.XPATH,'//*[@id="Proceedbtn"]')
details_consent = (By.XPATH,'/html/body/div[1]/div[1]/div[1]/div/div/div/div[3]/div/label')
share_details = (By.ID, 'btnProceed_EMFin')
connect_partner = (By.XPATH,'//*[@id="contactPartner"]/div/div/div[2]/div[4]/img')
details_fetched = (By.ID, 'proceedToAccountCreation')
review_deatils = (By.XPATH,'//*[@id="emFinReviewDetailsContainer"]/div/div/div/div/div/div[1]/div[1]/h3')
edit_option = (By.ID,'editEmFinCustomerDetails')
personal_details = (By.XPATH,'//*[@id="whizardForm"]/div[2]/div[1]')
dob_input_field = (By.XPATH,'//*[@id="DOB"]')
gender_drop = (By.ID,'GenderID')
net_income = (By.ID,'NetIncomeAmount')
ifsc_new = (By.ID,'IFSC')
account_no =(By.ID,'AccountNumber')
confirm_account_no = (By.ID,'ConfirmAccountNumber')
customer_zip_code = (By.ID,'CustomerZipCode')
driving_lic = (By.ID,'DrivingLicense')




