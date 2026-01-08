import pyodbc
import pandas as pd
import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from base64 import b64encode
from base64 import b64decode
import os

class DATABASE:

    def __init__(self):
        self.server_ip = '18.61.141.153'
        self.database = 'VivifiQA_2'
        self.username = 'udaykiran.mummina'
        self.password = 'Hello@123'
        self.connection_string = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={self.server_ip};DATABASE={self.database};UID={self.username};PWD={self.password};Encrypt=yes;TrustServerCertificate=yes"

    def establish_connection(self):
        return pyodbc.connect(self.connection_string)

    def execute_query(self, query, params=None):
        conn = self.establish_connection()
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        if query.lower().startswith('select'):
            result = cursor.fetchone()
            if result is not None:
                result = result[0]
            else:
                raise
        else:
            result = None
            conn.commit()
        cursor.close()
        conn.close()
        return result


    def get_verification_code(self, Phone_number, max_retries=3, retry_delay=1):
        retry_count = 0
        while retry_count < max_retries:
            try:
                conn = self.establish_connection()
                cursor = conn.cursor()
                query = (
                    "SELECT VerificationCode FROM VBTLog WHERE PhoneNumber = ? and isverified = 0 ORDER BY InsertedDate DESC"
                )
                cursor.execute(query, Phone_number)
                row = cursor.fetchone()
                verification_code = row[0] if row else None
                if verification_code is not None:
                    return verification_code
                else:
                    retry_count += 1
                    time.sleep(retry_delay)
            finally:
                cursor.close()
                conn.close()
        return 
    

    def get_customerphone_customerid(self,customerid):
        query = "SELECT PhoneNumber from CustomerPhone where customerid = ? order by 1 desc"
        return self.execute_query(query, (customerid,))
    

    def get_customer_status(self, customer_id):
        query = "SELECT CustomerStatusCodeID FROM customer WHERE CustomerID = ? order by 1 desc"
        return self.execute_query(query, (customer_id,))


    def get_verification_staus(self, customer_id):
        query = "SELECT VerificationStatus from customer where customerid = ? order by 1 desc"
        return self.execute_query(query, (customer_id,))
    
    def get_application_staus(self, customer_id):
        query = "SELECT ApplicationStatus from customer where customerid = ? order by 1 desc"
        return self.execute_query(query, (customer_id,))
    
    def get_agent_staus(self, customer_id):
        query = "SELECT agentstatus from customer where customerid =  ? order by 1 desc"
        return self.execute_query(query, (customer_id,))

    def get_document_id(self, ltdocumenttypeid,customer_id ):
        query = "SELECT CustomerDocumentid from CustomerDocument WHERE LTDocumentTypeid = ? and status =0 and CustomerID = ? order by 1 desc"
        return self.execute_query(query, (ltdocumenttypeid, customer_id,))

    def get_customer_id(self,email):
        query = "SELECT CustomerId FROM customer WHERE Email = ? order by 1 desc"
        return self.execute_query(query, (email,))


    def get_insert_date_appflownavigation(self,device_name):
        query = "select inserteddate from AppFlowNavigation WHERE devicename= ? order by 1 desc"
        return self.execute_query(query, (device_name,))


    def get_insert_date_deviceregistration(self,Model_name):
        query = "select inserteddate from deviceregistration WHERE model= ? order by 1 desc"
        return self.execute_query(query, (Model_name,))

    def get_customerid_appflownavigation(self,device_name):
        query = "select CustomerID  from AppFlowNavigation where AppFlowNavigationID= ? order by 1 desc"
        return self.execute_query(query, (device_name,))

    def get_appflow_navigationid(self,device_name):
        query = "select AppFlowNavigationID  from AppFlowNavigation where devicename= ? order by 1 desc"
        return self.execute_query(query, (device_name,))

    def get_flowid_appflownavigation(self,device_name):
        query = "select flowid  from AppFlowNavigation where CustomerID= ? order by 1 desc"
        return self.execute_query(query, (device_name,))

    def get_customer_conset(self,customerid):
        query = "SELECT CustomerConsentid from CustomerConsent where customerid = ? order by 1 desc"
        return self.execute_query(query, (customerid,))


    def get_deviceregistration_customerid(self,DeviceRegistrationid):
        query = "SELECT DeviceRegistrationid from DeviceRegistration where customerid = ? order by 1 desc"
        return self.execute_query(query, (DeviceRegistrationid,))

    def get_currentpageid_customerappnavigation(self,DeviceRegistrationid):
        query = "SELECT CurrentPageID from CustomerAppNavigation where customerid = ? order by InsertedDate DESC"
        return self.execute_query(query, (DeviceRegistrationid,))

    def get_customerconsentid(self, customer_id, consent_type_id):
        query = "SELECT CustomerConsentid FROM CustomerConsent WHERE LTConsentTypeID = ? AND customerid = ? order by 1 desc"
        return self.execute_query(query, (consent_type_id, customer_id,))

    def get_Apicommunication_logid(self, customer_id):
        query = "SELECT APICommunicationLogid FROM APICommunicationLog where customerid = ? order by 1 desc"
        return self.execute_query(query, (customer_id,))
    
    def get_customer_loginid(self, customer_id,):
        query = "SELECT customerloginid from CustomerLogin where CustomerID = ?"
        return self.execute_query(query, (customer_id,))


    def get_firstname_custome(self, customer_id,):
        query = "SELECT firstname from customer WHERE CustomerID = ?"
        return self.execute_query(query, (customer_id,))

    def get_lastname_customer(self, customer_id,):
        query = "SELECT lastname from customer WHERE CustomerID = ?"
        return self.execute_query(query, (customer_id,))

    def get_email_customer(self, customer_id,):
        query = "SELECT email from customer WHERE CustomerID = ? order by 1 desc"
        return self.execute_query(query, (customer_id,))


    def get_pandetailsid_pan(self, panid,):
        query = "SELECT PanDetailsid from PanDetails where panid = ? order by 1 desc"
        return self.execute_query(query,panid )
    
    def get_pannumber_customeridentiry(self, customer_id,):
        query = "SELECT pannumber from CustomerIdentity WHERE CustomerID = ? order by 1 desc"
        return self.execute_query(query, (customer_id,))

    def get_form60_status(self, customer_id,):
        query = "SELECT FormSixtyRequeststatus from FormSixtyRequest WHERE customerid = ? and status = 0 order by 1 desc"
        return self.execute_query(query, (customer_id,))

    def get_status_form60(self, customer_id,):
        query = "SELECT Status from FormSixtyRequest WHERE customerid = ? order by 1 desc"
        return self.execute_query(query, (customer_id,))


    def get_employername_customerincome(self, customer_id,):
        query = "SELECT employername from CustomerIncome where CustomerID =  ? order by 1 desc"
        return self.execute_query(query, (customer_id,))

    def get_salarydate_customerincome(self, customer_id,):
        query = "SELECT DateOfMonth1 from CustomerIncome where CustomerID = ? order by 1 desc"
        return self.execute_query(query, (customer_id,))

    def get_salary_customerincome(self, customer_id,):
        query = "SELECT NetIncomeAmount from CustomerIncome where CustomerID = ? order by 1 desc"
        return self.execute_query(query, (customer_id,))


    def get_employment_type(self, customer_id,):
        query = "SELECT LTSourceOfIncomeid from CustomerIncome where CustomerID = ? order by 1 desc"
        return self.execute_query(query, (customer_id,))
    
    def get_ifsc_customerbank(self, customer_id,):
        query = "select ifsc from customerBank where customerid = ? order by 1 desc"
        return self.execute_query(query, (customer_id,))
    
    def get_accountnumber_customerbank(self, customer_id,):
        query = "select accountnumber from customerBank where customerid =? order by 1 desc"
        return self.execute_query(query, (customer_id,))


    def get_customer_eligibilityid(self, customer_id,):
        query = "SELECT CustomerEligibilityid from CustomerEligibility where customerid = ? order by 1 desc"
        return self.execute_query(query, (customer_id,))

    def get_cibil_detailsid(self, customer_id,):
        query = "SELECT CustomerCibilStatusDetailid from CustomerCibilStatusDetail where customerid =  ? order by 1 desc"
        return self.execute_query(query, (customer_id,))


    def get_product_eligibilityid(self, customer_id,):
        query = "SELECT CustomerProductEligibilityid from CustomerProductEligibility where customerid =  ? order by 1 desc"
        return self.execute_query(query, (customer_id,))

    def get_apitype_apicommunication(self, customer_id,):
        query = "SELECT apitype from APICommunicationLog where CustomerID = ? order by requestdatetime DESC"
        return self.execute_query(query, (customer_id,))

    def get_new_address(self, customer_id,):
        query = "SELECT addressline1 from customeraddress where customerid = ? and status = 0"
        return self.execute_query(query, (customer_id,))

    def update_pan_n(self, customer_id,):
        query = "update pandetails set panstatus = 'N' where panid = ?"
        return self.execute_query(query, (customer_id,))

    def get_reject_reason(self, customer_id,):
        query = "SELECT  Rejectionreasondetail from RejectionReasonLog where customerid = ? order by 1 desc"
        return self.execute_query(query, (customer_id,))

    def get_nmi_reason(self, customer_id,):
        query = "SELECT Nmireasondetail from NmiVerificationLog where customerid = ? and status = 0"
        return self.execute_query(query, (customer_id,))


    def update_customer_suspicious(self, customer_id,):
        query = """MERGE INTO SuspiciousDetails AS target
                USING (SELECT ? AS CustomerID) AS source
                ON target.CustomerID = source.CustomerID
                WHEN NOT MATCHED THEN
                    INSERT (CustomerID, riskscore, risklog, Status, InsertedBy, InsertedDate, Requeststatus)
                    VALUES (source.CustomerID, 30, 'Log:;Score:', 0, 'sql', GETDATE(), 1);"""
        return self.execute_query(query, (customer_id,))
    

    
    def update_insertion_time(self, customer_id):
        query = "update customer set VerificationStatusChangeDate=Dateadd(MINUTE,-10,VerificationStatusChangeDate) where customerid=?"
        self.execute_query(query, (customer_id,))

    def get_partner_location(self, TaskDetailID):
        query = "select TaskDetailLocationID from pikfi.dbo.TaskDetailLocation where TaskDetailID = ?"
        return self.execute_query(query,(TaskDetailID,))

    def insert_loc_document(self, locid):
        query = """
        Declare @locid int = ?,
                @Customerid int
        insert into LOCDocument
        select @locid
        ,DocumentType
        ,DocumentFileName
        ,LendingProductDocumentSetupID
        ,DocumentVersion
        ,OutletID
        ,LOCStatementID
        ,GETDATE()
        ,SignedDevice
        ,SignedIP
        ,SignedChannel
        ,SignedBrowser
        ,SignedBrowserAgent
        ,DocumentFilePath
        ,IsMailSent
        ,IsActive
        ,'Manual'
        ,GETDATE()
        ,NULL
        ,NULL
        ,DocumentContent
        ,IsDocumentAgreed
        ,DocumentFilePathTeller
        ,ElectronicallySignedAgreement
        ,@Customerid
        ,IsElectronicallySigned
        ,AzureFilePath,EsignPageNumber ,Documentsource,SignType,ProviderFileVersion,ProviderFileDirectoryPath from locdocument  where locid = 517065 and DocumentType = 'FLEXAGREEMENTWITHESIGN'
        """
        self.execute_query(query, (locid,))


    def insert_retailor_id(self, reatilid):
        query = """
            insert into RetailerData (RetailerID,RetailerName,RetailerBalance,RetailerRiskBin,
            CustomerID,IsActive,InsertedBy,InsertedDate,UpdatedBy,UpdatedDate)
            values(?,'gtUFSA',7015,'B4',NULL,1,'qa',getdate(),Null,Null)
        """
        self.execute_query(query, (reatilid,))




    def get_customerid_customerphone(self,customerid):
        query = "SELECT customerid from CustomerPhone where PhoneNumber = ? order by 1 desc"
        return self.execute_query(query, (customerid,))
    
    def get_patner_customerid(self, Customerid):
        query = "select PartnerCustomerID from pikfi.dbo.PartnerCustomer where customerid= ?"
        return self.execute_query(query,(Customerid,))

    def get_taskdetails_id(self, PartnerCustomerID):
        query = "select TaskDetailID from pikfi.dbo.TaskDetails where PartnerCustomerID= ?"
        return self.execute_query(query,(PartnerCustomerID,))

    def get_opentok_id(self, groupname):
        query = "SELECT OpenTokSessionDeatilid from pikfi.dbo.OpenTokSessionDeatils where groupname = ?"
        return self.execute_query(query,(groupname,))

    def update_esign_negative(self, customer_id):
        query = "UPDATE AAdhaarAPIesign SET esignstatus=-4 WHERE customerid= ?"
        self.execute_query(query, (customer_id,))


    def get_loc_id(self, customer_id):
        query = "SELECT locid FROM LOC WHERE CustomerID = ? ORDER by LOCOpenDate DESC"
        return self.execute_query(query, (customer_id,))



    def update_ckyc_status(self, ckyc_id):
        query = "update CustomerCKYCData set status = 0 where CustomerCKYCDataID = ?"
        self.execute_query(query, (ckyc_id,))



    def get_ckyc_id(self, customer_id):
        query = "SELECT CustomerCKYCDataid from CustomerCKYCData WHERE customerid = ? ORDER by 1 DESC"
        return self.execute_query(query, (customer_id,))



    def update_search_download(self, ckyc_id):
        query = "update CustomerCKYCData set CKYCNumber = '544548033713', search=1, download=1, status=0 where CustomerCKYCDataID= ?"
        self.execute_query(query, (ckyc_id,))


    def update_document_source(self, customer_id):
        query = "update CustomerDocument set DocumentSource = 5 WHERE CustomerID =   ?"
        self.execute_query(query, (customer_id,))

    def update_emandate_confirmed(self, customer_id):
        query = "UPDATE RazorpayTransaction SET TransactionStatus = 'confirmed' WHERE CustomerID = ?"
        self.execute_query(query, (customer_id,))


    def update_emandate_authorized(self, customer_id):
        query = "UPDATE RazorpayTransaction SET TransactionStatus = 'authorized' WHERE CustomerID = ?"
        self.execute_query(query, (customer_id,))


    def get_outstanding_due(self, customer_id):
        query = "SELECT CurrentLOCPrincipal FROM LOC WHERE CustomerID = ? order by 1 desc"
        return self.execute_query(query, (customer_id,))

    def get_ebv_request_code(self, customer_id):
        query = "SELECT requestcode from CanariFi where customerid = ? order by 1 DESC"
        return self.execute_query(query, (customer_id,))

    def get_product_type(self, customer_id):
        query = "SELECT ltproducttypeid from customertrafficsplit where customerid = ? order by 1 DESC"
        return self.execute_query(query, (customer_id,))



    def get_vkyc_status(self, customer_id):
        query = "SELECT vkycstatus from CustomerVKYCQueue where customerid  = ? and status = 0"
        return self.execute_query(query, (customer_id,))

    def aes_encrypt(self, plaintext, key="LoPwUjWnZr9o8w!z"):
        key = key.encode('utf-8')
        iv = b'\x00' * 16 
        backend = default_backend()
        
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(plaintext.encode('utf-8')) + padder.finalize()

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()

        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return b64encode(ciphertext).decode('utf-8')

    def update_esign_status(self, customer_id):
        query = "UPDATE AAdhaarAPIesign SET esignstatus=4 WHERE customerid= ?"
        self.execute_query(query, (customer_id,))

    def get_withdrawl_limit(self, customer_id):
        query = "SELECT AvailableCredit FROM LOC WHERE CustomerID = ?"
        return self.execute_query(query, (customer_id,))
    


    def get_document_type(self, customer_id,LTDocumentTypeid):
        query = "SELECT CustomerDocumentID from customerdocument where customerid=? and documentsource = 7 and LTDocumentTypeid = ? order by 1 desc"
        return self.execute_query(query, (customer_id,LTDocumentTypeid))
    
    def get_vkyc_videoid(self,customer_id):
        query = "SELECT CustomerDocumentid from customerdocument where customerid = ? and LTDocumentTypeid = 60 order by 1 DESC"
        return self.execute_query(query, (customer_id,))


    def get_upload_pikfi(self, customer_id):
        # Format customer_id to ensure it matches %"1173200"% pattern
        formatted_customer_id = f'%"{customer_id}"%'  # Add both % and double quotes around the customer_id
        print(f'customerid is {formatted_customer_id}')  # Debug statement
        query = "SELECT uploadid FROM pikfi.dbo.Uploads WHERE path LIKE ?"
        return self.execute_query(query, (formatted_customer_id,))


    def aes_decrypt(self, ciphertext, key="LoPwUjWnZr9o8w!z"):
        key = key.encode('utf-8')
        ciphertext = b64decode(ciphertext)
        backend = default_backend()
        iv = b'\x00' * 16
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        decryptor = cipher.decryptor()
        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
        return unpadded_data.decode('utf-8')

    def get_limit_customereligibility(self,cutomer_id):
        query = 'SELECT eligibleamount from CustomerEligibility WHERE CustomerID = ? order by CustomerEligibilityID DESC'
        return self.execute_query(query,(cutomer_id,))

    def get_login_otp(self,cutomer_id):
        query = 'SELECT SECURITYcode from otpverificationlog WHERE CustomerID = ? and status=0 order by 1 DESC'
        return self.execute_query(query,(cutomer_id,))


    def update_ers_cibil(self, CIBILKeyValue):
        query = "update CIBILDatabase.dbo.CIBILQAData1 set CIBILKeyValue = ? where CIBILKeyName = 'ERSScore' and UnderwritinType = 'Full'"
        self.execute_query(query, (CIBILKeyValue,))


    def update_stpl_band_cibil(self, CIBILKeyValue):
        query = "update CIBILDatabase.dbo.CIBILQAData1 set CIBILKeyValue = ? where CIBILKeyName = 'STPLBand' and UnderwritinType = 'Full'"
        self.execute_query(query, (CIBILKeyValue,))


    def update_levrage_score_cibil(self, CIBILKeyValue):
        query = "update CIBILDatabase.dbo.CIBILQAData1 set CIBILKeyValue = ? where CIBILKeyName = 'LeverageScore' and UnderwritinType = 'Full'"
        self.execute_query(query, (CIBILKeyValue,))

    def get_phone_customerid(self,customerid):
        query = "SELECT PhoneNumber from CustomerPhone where customerid = ? order by 1 desc"
        return self.execute_query(query, (customerid,))
    

    def update_loch_cibil(self, CIBILKeyValue):
        query = "update CIBILDatabase.dbo.CIBILQAData1 set CIBILKeyValue = ? where CIBILKeyName = 'LengthOfCreditHistory' and UnderwritinType = 'Full'"
        self.execute_query(query, (CIBILKeyValue,))


    def update_stpl_cibil(self, CIBILKeyValue):
        query = "update CIBILDatabase.dbo.CIBILQAData1 set CIBILKeyValue = ? where CIBILKeyName = 'ExcludingSTPLOTP' and UnderwritinType = 'Full'"
        self.execute_query(query, (CIBILKeyValue,))

    def get_risk_configid(self,cutomer_id):
        query = 'select creditriskrateconfigid from Customereligibility where customerid = ? ORDER by 1 DESC'
        return self.execute_query(query,(cutomer_id,))

    def update_ml_model(self, customer_id):
        query = "Update MLModelResult set Status = 2 where customerid = ? and ModelType = 3 and Status = 0;"
        self.execute_query(query, (customer_id,))

    def insert_ml_model(self, customer_id,score):
        query = "insert into MLModelResult (CustomerID, Score, ModelType, Status, CommunicationLogID, InsertedBy, InsertedDate, Bin) values (?, ?, 3, 0, 0, 'Vivifi', GETDATE(), 10);"
        self.execute_query(query, (customer_id,score))
  






    def insert_six_variables(self, customer_id):
        query = """
            declare @customerid int = ?
            declare @CIBILRequestApplicationID int ,@CIBILRequestApplicantid int , @CIBILResponseApplicationDataid int , @CIBILResponseApplicantid int , @ScoreSegmentID int

                insert into CIBILDATABASE.DBO.CIBILRequestApplication
                values(15297.50,0,5,'reference','CIBIL',getdate())

            set @CIBILRequestApplicationID = @@IDENTITY
            select * from CIBILDATABASE.DBO.CIBILRequestApplication where CIBILRequestApplicationID = @CIBILRequestApplicationID 

                insert into CIBILDATABASE.DBO.CIBILRequestApplicant
                values ('BNibD wY','ITsRU',NULL,'Main',@CIBILRequestApplicationID,@customerid,'1996-05-01 00:00:00.0000000','Male','CIBIL',getdate())

            set @CIBILRequestApplicantid = @@IDENTITY
            select * from CIBILDATABASE.DBO.CIBILRequestApplicant where CIBILRequestApplicantid = @CIBILRequestApplicantid

                insert into CIBILDATABASE.DBO.CIBILResponseApplicationData
                select Amount,@CIBILRequestApplicantid,BranchReferenceNo,BusinessUnitId,CIBILPDFReport,CenterReferenceNo   ,CibilBureauFlag    ,ConsumerConsentForUIDAIAuthentication  ,DSTuNtcFlag    ,EnvironmentType    ,EnvironmentTypeId  ,GSTStateCode   ,IDVMemberCode  ,IDVPDFReport   ,IDVerificationFlag ,Income ,InputValReasonCodes    ,IsMFTUEF   ,MFIBureauFlag  ,MFIMemberCode  ,MFIPDFReport   ,Milestone  ,NTCProductType ,Purpose    ,RepaymentPeriodInMonths    ,SkipCPVPoliciesQDEFlag ,SkipCibilBureauFlag    ,SkipCreditRiskPoliciesFlag ,SkipDSTuIDVisionFlag   ,SkipDSTuNtcFlag    ,SkipDocVerificationFlag    ,SkipDsCrifIndFlag  ,SkipDsEverifyFlag  ,SkipEkycFlag   ,SkipIDVerificationFlag ,SkipIndiaInputQueueDdeFlag ,SkipIndiaInputQueueQdeFlag ,SkipMFICIRPuller   ,SkipMultiBureauFlag    ,SkipPreQDEFlag ,SkipQDEResultsQ    ,SkipQDEValidationQ ,SkipReferQueue ,SkipTuVerificationFlag ,SkipVelocityCheckFlag  ,SolutionSetId  ,[Start],[User],    InsertedBy  ,'2025-05-01'    ,MileStones
                ,@CIBILRequestApplicationID
                from CIBILDATABASE.DBO.CIBILResponseApplicationData where CIBILResponseApplicationDataID = 11055

            set @CIBILResponseApplicationDataid = @@identity
            select * from CIBILDATABASE.DBO.CIBILResponseApplicationData where CIBILResponseApplicationDataID = @CIBILResponseApplicationDataid

                insert into CIBILDATABASE.DBO.CIBILResponseApplicant (ApplicantFirstName,ApplicantLastName,ApplicantMiddleName,ApplicantType,CIBILResponseApplicationDataID,DateOfBirth,Gender,Insertedate,CustomerID)
                select ApplicantFirstName,ApplicantLastName,ApplicantMiddleName,ApplicantType,@CIBILResponseApplicationDataID,DateOfBirth,Gender,Insertedate,@CustomerID from CIBILDATABASE.DBO.CIBILResponseApplicant where CIBILResponseApplicantID= 20

            set @CIBILResponseApplicantid = @@identity 
            select * from CIBILDATABASE.DBO.CIBILResponseApplicant where CIBILResponseApplicantid = @CIBILResponseApplicantid

                insert into CIBILDatabase.dbo.CreditReport_ScoreSegment
                select @CIBILResponseApplicantid,10,'000-1',22,10,getdate(),'CIBILTUERS',NULL,getdate(),NULL,0,NULL,0,NULL,0,NULL,0,NULL,0,NULL,0

            set @ScoreSegmentID = @@identity	
            select * from CIBILDatabase.dbo.CreditReport_ScoreSegment where ScoreSegmentID = @ScoreSegmentID
                """
        self.execute_query(query, (customer_id,))




# db = DATABASE()

# print(db.get_customerid_customerphone('7832360114'))
