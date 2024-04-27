## Qoala


![image](https://github.com/safvanhuzain/Qoala/assets/92985225/908e8141-8a71-487e-8f4d-9f27be6a9c67)<br>
<b>insurance technology company</b>
<h2>* Introduction:</h2>
Customizing ERPNext involves adding functionalities tailored to specific business needs. This documentation outlines the process of adding a custom app and a custom function within the app.<br>
<h2>Step 1: Creating a Custom App:</h2>
  
  Navigate to the Frappe Bench directory using the terminal.<br>
  Run the following command to create a new app<br>
  `bench new-app <app_name>`<br>
  <h2>Step 2:Defining the Custom Function:</h2>
  <h3>ERPNext Batch Invoice Submission</h3>
    1) Transactional submission and rollback mechanism for invoices.<br>
      &nbsp;&nbsp;&nbsp; # Within custom app directory, locate the custom_app folder.<br>
        &nbsp;&nbsp;&nbsp; # Created a new Python file for custom function, e.g., crud_events.py<br>
        &nbsp;&nbsp;&nbsp; # Defined custom function within this file e.g., <b>generate_batch_wise_sales_invoice</b><br>
        &nbsp;&nbsp;&nbsp; #  This function will create and submit the Batch-wise sales invoices from a third party App with a unique identifier.<br>
        &nbsp;&nbsp;&nbsp; # If any of the invoice failed while submitting. All of the invoices group by unique identifier will revert back to Draft State<br>
     
    
    NB: Based on the frappe frame work design we cannot revert back to sumitted invoice without cancel & Amend. So here if any of the invoices from the same batch failed.
    
    it will automatically cancel and amend to draft states. But after cancelling the documentb it will create a new series from the reference series.
    
    for eg., if the invoice is cancelled with the series 001. then if we amended from 001 it will create new series like 001-1.
    
    so we will not lost any series. As per tax law this series can be accepted.
    
<div>
  2) Custom field addition in the ERPNext invoice doctype.<br>
    &nbsp;&nbsp;&nbsp; # Added custom fields for <b>unique identifier, is_rolled_back, custom_default_price_list</b><br>
    &nbsp;&nbsp;&nbsp; # Added custom field via <b>Customize Form</b> Doctype. Exported those fields to <b>Qoala</b> App<br>
    &nbsp;&nbsp;&nbsp; # So if we install this app to any erpnext instance no need to create these fields again it will sync when we migrate the app.<br>
 3) Cron job script.<br>
    &nbsp;&nbsp;&nbsp; # I  used Scheduler Events for running tasks periodically in the background using the scheduler_events hook.<br>
    &nbsp;&nbsp;&nbsp; # It will check the custom functions that added in the path in hooks under scheduler_events every one hour.<br>
    &nbsp;&nbsp;&nbsp; # Here the custom function <b>cancel_sales_invoices</b> check for is_rolled_back Draft invoices and it will delete.<br>
  4) Error handling and logging code.<br>
    &nbsp;&nbsp;&nbsp; # Have included the exceptional handling in all root functions.<br>
    &nbsp;&nbsp;&nbsp; # Based on the framework if we trying to logging to frappe with token/user credentials it will check by itself. there is an inbuilt code for that. you can check the below reference 
  https://frappeframework.com/docs/user/en/api/rest
  </div>
  <h2>4. Conclusion:</h2>
By following these steps, you have successfully added a custom app and function within ERPNext, allowing for tailored functionalities to meet specific business requirements.

#### License

MIT
