import frappe
from frappe import _
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def after_install():
	create_custom_fields(get_sales_invoice_custom_fields(), ignore_validate=True)
	create_custom_fields(get_purchase_invoice_custom_fields(), ignore_validate=True)
	create_custom_fields(get_journal_entry_custom_fields(), ignore_validate=True)

def after_migrate():
	after_install()

def before_uninstall():
	delete_custom_fields(get_sales_invoice_custom_fields())
	delete_custom_fields(get_purchase_invoice_custom_fields())
	delete_custom_fields(get_journal_entry_custom_fields())

def delete_custom_fields(custom_fields: dict):
	'''
		Method to Delete custom fields
		args:
			custom_fields: a dict like `{'Sales Invoice': [{fieldname: 'tally_masterid', ...}]}`
	'''
	for doctype, fields in custom_fields.items():
		frappe.db.delete(
			"Custom Field",
			{
				"fieldname": ("in", [field["fieldname"] for field in fields]),
				"dt": doctype,
			},
		)
		frappe.clear_cache(doctype=doctype)

def get_sales_invoice_custom_fields():
	'''
        Express Tally specific custom fields in Sales Invoice
    '''
	return {
		"Sales Invoice": [
			{
				"fieldname": "tally_masterid",
				"fieldtype": "Data",
				"label": "Tally Master ID",
				"insert_after": "customer",
				"read_only": 1,
				"no_copy": 1
			},
			{
				"fieldname": "tally_voucherno",
				"fieldtype": "Data",
				"label": "Tally Voucher No",
				"insert_after": "tally_masterid",
				"read_only": 1,
				"no_copy": 1
			}
		]
	}

def get_purchase_invoice_custom_fields():
	'''
        Express Tally specific custom fields in Purchase Invoice
    '''
	return {
		"Purchase Invoice": [
			{
				"fieldname": "tally_masterid",
				"fieldtype": "Data",
				"label": "Tally Master ID",
				"insert_after": "supplier_name",
				"read_only": 1,
				"no_copy": 1
			},
			{
				"fieldname": "tally_voucherno",
				"fieldtype": "Data",
				"label": "Tally Voucher No",
				"insert_after": "tally_masterid",
				"read_only": 1,
				"no_copy": 1
			}
		]
	}

def get_journal_entry_custom_fields():
	'''
        Express Tally specific custom fields in Journal Entry
    '''
	return {
		"Journal Entry": [
			{
				"fieldname": "tally_masterid",
				"fieldtype": "Data",
				"label": "Tally Master ID",
				"insert_after": "posting_date",
				"read_only": 1,
				"no_copy": 1
			},
			{
				"fieldname": "tally_voucherno",
				"fieldtype": "Data",
				"label": "Tally Voucher No",
				"insert_after": "tally_masterid",
				"read_only": 1,
				"no_copy": 1
			}
		]
	}