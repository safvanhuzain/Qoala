import frappe
from frappe.utils import today
from erpnext.setup.utils import get_exchange_rate


# Submit Batch-wise Sales Invoices via API
@frappe.whitelist()
def generate_batch_wise_sales_invoice(data, is_rolled_back=False):
	result = {}
	submitted_invoice_list = []
	try:
		if data:
			for d in data:
				sales_invoice = frappe.new_doc("Sales Invoice")
				sales_invoice.customer = d['customer']
				sales_invoice.custom_unique_identifier = d['custom_unique_identifier']
				sales_invoice.company = d['company']
				date = d.get('date', today())
				company = extract_company_details(d['company'])
				sales_invoice.posting_date = date
				sales_invoice.currency = company.default_currency
				sales_invoice.conversion_rate = get_exchange_rate(d['currency'], company.default_currency, date)
				sales_invoice.selling_price_list = company.custom_default_price_list
				sales_invoice.price_list_currency = frappe.db.get_value("Price List", company.custom_default_price_list, "currency")
				sales_invoice.append("items", {
					"item_code": d['item_code'],
					"qty": d['qty'],
					"rate": d['rate'],
					"income_account": company.default_income_account,
					"cost_center": company.cost_center,
				})
				sales_invoice.save()
				sales_invoice.submit()
				submitted_invoice_list.append(sales_invoice.name)

	except Exception:
		frappe.log_error(title="Error while submitting Sales invoice", message=frappe.get_traceback())
		result['error'] = "Error while submitting Sales Invoice. Please reach out the erp support team"
		is_rolled_back = True

	if is_rolled_back:
		for d in data:
			failed_invoices = frappe.db.get_all("Sales Invoice", filters={"custom_unique_identifier": d['unique_identifier']}, fields=['name'])
			details = cancel_sales_invoices(failed_invoices)
			if "error" in details:
				result['error'] = details['error']
			if "invoices" in details:
				result['invoices'] = f"Error encountered while submitting sales invoices. Pending invoices have been reverted back to draft status. Please find the details of the invoices for your reference: {details['invoices']}."
	else:
		result['success'] = f"Successfully submitted sales invoices {submitted_invoice_list}."
	return result
		

# Fetch Company Details
def extract_company_details(company):
	data =  frappe.db.get_value("Company", company, ["default_currency", "default_income_account", "custom_default_price_list", "cost_center"], as_dict=True)
	return data


# Revert back the submitted invoices to Draft
def cancel_sales_invoices(data):
	result = {}
	draft_invoice_list = []
	try:
		for d in data:
			sales_invoice = frappe.get_doc("Sales Invoice", d.name)
			sales_invoice.cancel()
			new_si = frappe.copy_doc(sales_invoice) 
			new_si.amended_from = sales_invoice.name 
			new_si.status = "Draft"
			new_si.custom_is_rolled_back = 1
			new_si.insert()
			draft_invoice_list.append(new_si.name)
	except Exception:
		frappe.log_error(title="Error while cancelling Sales invoice", message=frappe.get_traceback())
		result['error'] = "Error while cancelling the sales Invoice. Please reach out to the support Team"

	if draft_invoice_list:
		result['invoices'] = draft_invoice_list
	return result


# Background Job: It will delete all batchwise reverted Sales invoices on hourly basis.
def delete_failed_transactions():
	try:
		invoice = frappe.qb.DocType("Sales Invoice")
		query = (
			frappe.qb.from_(invoice)
			.select(
				invoice.name
			)
			.where(
				invoice.status == 0
				& invoice.custom_is_rolled_back == 1
			)
		)
		query = query.run(as_dict=1)
		for d in query:
			doc = frappe.get_doc("Sales Invoice", d.name)
			doc.delete()
	except Exception:
		frappe.log_error(title="Error while deleting sales invoices", message=frappe.get_traceback())
