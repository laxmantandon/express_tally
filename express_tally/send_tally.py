
from __future__ import unicode_literals
import frappe, json

@frappe.whitelist()
def customer():

    payload = json.loads(frappe.request.data)
    customers = frappe.db.get_all(
        'Customer',
        fields=['name', 'customer_name', 'company', 'customer_primary_address', 'gst_category', 'modified', 'tax_id', 'email_id', 'mobile_no','pan', 'first_name', 'is_synced'],
        filters={ 
            # 'modified' : ['>', payload['date']],
            'company': payload['company'],
            'is_synced': ['!=', 'Yes']
            },
        limit=100
        )
    if customers:
        for customer in customers:
            primary_address = customer['customer_primary_address']

            if primary_address:
                address = frappe.get_doc('Address', primary_address)

                if address:
                    customer['taddress'] = address
                else:
                    customer['taddress'] = {}

    return customers

@frappe.whitelist()
def supplier():

    payload = json.loads(frappe.request.data)
    suppliers = frappe.db.get_all(
        'Supplier',
        fields=['name', 'supplier_name', 'company', 'gst_category', 'modified', 'is_synced'],
        filters={ 
            # 'modified' : ['>', payload['date']],
            'company': payload['company'],
            'is_synced': ['!=', 'Yes']
            },
        limit=100
        )
    if suppliers:
        for supplier in suppliers:
            supplier_name = supplier['name']

            if supplier_name:
                
                if frappe.db.exists('Address', supplier_name + '-Billing'):
                    address = frappe.get_doc('Address', supplier_name + '-Billing')
                    supplier['taddress'] = address
                else:
                    supplier['taddress'] = {}

            # get contact details of suppliers

            parent = frappe.db.sql("""
                SELECT 
                    parent
                FROM `tabDynamic Link`
                WHERE parenttype = 'Contact' AND link_doctype = 'Supplier' AND link_name = %s
            """, supplier_name, as_dict=1)

            #supplier['p'] = parent
            if len(parent) > 0:
                contact = frappe.get_doc('Contact', parent[0]['parent'])
                supplier['email_id'] = contact.email_id
                supplier['mobile_no'] = contact.mobile_no
                supplier['first_name'] = contact.first_name

    return suppliers


@frappe.whitelist()
def purchase():

    payload = json.loads(frappe.request.data)

    branch = payload['branch']
    converted_branch = branch.split(",")

    purchase_invoices = frappe.db.get_all(
        'Purchase Invoice',
        fields=[
            'name', 'posting_date', 'docstatus', 'company', 'base_grand_total', 'base_net_total',
            'base_rounded_total', 'rounding_adjustment', 'modified', 'is_return', 'supplier', 'supplier_name', 'bill_no',
            'amended_from', 'supplier_name_in_tally', 'branch'
            ],
        filters={ 
            # 'modified' : ['>', payload['date']],
            'company': payload['company'],
            'branch': ["in", converted_branch],
            'is_synced': ['!=', 'Yes']
            },
        limit=100
        )

    if purchase_invoices:
        for purchase_invoice in purchase_invoices:
            purchase_invoice_no = purchase_invoice['name']

            if purchase_invoice_no:
                pi_no = frappe.get_doc('Purchase Invoice', purchase_invoice_no).as_json()

                pi_no = json.loads(pi_no)

                items = pi_no.get("items")
                for item in items:

                    if item.get("pr_detail"):
                        serial_and_batch_bundle  = frappe.db.get_value("Purchase Receipt Item", item.get("pr_detail"), "serial_and_batch_bundle")

                    if item.get("batch_no"):
                        item["batches"] = [
                            {
                                "batch_no": item.get("batch_no"),
                                "warehouse": item.get("warehouse"),
                                "qty": item.get("qty")
                            }
                        ]
                    else:
                        serial_and_batch_bundle  = item.get("serial_and_batch_bundle")
                        if serial_and_batch_bundle:
                            bundle = frappe.get_doc("Serial and Batch Bundle", serial_and_batch_bundle).as_json()
                            bundle = json.loads(bundle)
                            item["batches"] = bundle.get("entries")
                        else:
                            item["batches"] = [
                                {
                                    "batch_no": "Primary Batch",
                                    "warehouse": item.get("warehouse"),
                                    "qty": item.get("qty")
                                }
                            ]

                if pi_no:
                    purchase_invoice['tpurchaseinvoice'] = pi_no
                else:
                    purchase_invoice['tpurchaseinvoice'] = {}


    return purchase_invoices


@frappe.whitelist()
def sales():

    payload = json.loads(frappe.request.data)

    branch = payload['branch']
    converted_branch = branch.split(",")
    
    sales_invoices = frappe.db.get_all(
        'Sales Invoice',
        fields=[
            'name', 'posting_date', 'docstatus', 'company', 'base_grand_total', 'base_net_total',
            'base_rounded_total', 'rounding_adjustment', 'modified', 'is_return', 'customer', 'customer_name',
            'supplier_name_in_tally', 'amended_from', 'branch'
            ],
    
        filters={ 
            # 'posting_date' : ['>=', payload['date']],
            'posting_date' : ['>=', '2023-01-01'],
            'company': payload['company'],
            'branch': ["in", converted_branch],
            'docstatus': ["in", ["1", "2"]],
            'is_synced': ['!=', 'Yes'],
            },
        limit=100
        )
    if sales_invoices:
        for sales_invoice in sales_invoices:
            sales_invoice_no = sales_invoice['name']

            if sales_invoice_no:
                pi_no = frappe.get_doc('Sales Invoice', sales_invoice_no).as_json()
                pi_no = json.loads(pi_no)

                items = pi_no.get("items")
                for item in items:

                    if item.get("dn_detail"):
                        serial_and_batch_bundle  = frappe.db.get_value("Delivery Note Item", item.get("dn_detail"), "serial_and_batch_bundle")

                    if item.get("batch_no"):
                        item["batches"] = [
                            {
                                "batch_no": item.get("batch_no"),
                                "warehouse": item.get("warehouse"),
                                "qty": item.get("qty")
                            }
                        ]
                    else:
                        serial_and_batch_bundle  = item.get("serial_and_batch_bundle")
                        if serial_and_batch_bundle:
                            bundle = frappe.get_doc("Serial and Batch Bundle", serial_and_batch_bundle).as_json()
                            bundle = json.loads(bundle)
                            item["batches"] = bundle.get("entries")
                        else:
                            item["batches"] = [
                                {
                                    "batch_no": "Primary Batch",
                                    "warehouse": item.get("warehouse"),
                                    "qty": item.get("qty")
                                }
                            ]

                cust = frappe.get_doc("Customer", pi_no.get("customer"))
                credit_limit = 0
                if len(cust.credit_limits) > 0:
                    credit_limit = cust.credit_limits[0].credit_limit
                sales_invoice['credit_limit'] = credit_limit

                if pi_no:
                    sales_invoice['tsalesinvoice'] = pi_no
                else:
                    sales_invoice['tsalesinvoice'] = {}

    return sales_invoices



@frappe.whitelist()
def payments():

    payload = json.loads(frappe.request.data)

    branch = payload['branch']
    converted_branch = branch.split(",")

    payments = frappe.db.get_all(
        'Payment Entry',
        fields=[
            'name', 'posting_date', 'docstatus', 'company', 'party', 'party_name',
            'paid_to', 'paid_amount', 'remarks', 'payment_type', 'paid_from', 'amended_from', 'naming_series',
            'reference_no', 'reference_date', 'party_bank_account', 'branch'
            ],
        filters={ 
            # 'modified' : ['>', payload['date']],
            'company': payload['company'],
            'branch': ["in", converted_branch],
            'docstatus': ["in", ["1", "2"]],
            'is_synced': ['!=', 'Yes']
            # 'is_synced': ['!=', 'Yes']
            },
        limit=100
        )
    if payments:
        for payment in payments:
            payment_no = payment['name']

            if payment_no:
                pi_no = frappe.get_doc('Payment Entry', payment_no)

                if pi_no:

                    payment['treferences'] = pi_no
                    
                else:
                    payment['treferences'] = {}

## draft entries 

    draft_payments = frappe.db.get_all(
        'Payment Entry',
        fields=[
            'name', 'posting_date', 'docstatus', 'company', 'party', 'party_name',
            'paid_to', 'paid_amount', 'remarks', 'payment_type', 'paid_from', 'amended_from', 'naming_series',
            'reference_no', 'reference_date', 'party_bank_account', 'branch'
            ],
        filters={ 
            'company': payload['company'],
            'branch': ["in", converted_branch],
            'docstatus': "0",
            'party': ["like", "XYZ%"],
            'payment_type': "Receive",
            'is_synced': ['!=', 'Yes']
            # 'is_synced': ['!=', 'Yes']
            },
        limit=100
        )
    
    if draft_payments:
        for payment in draft_payments:
            payment_no = payment['name']

            if payment_no:
                pi_no = frappe.get_doc('Payment Entry', payment_no)

                if pi_no:
                    payment['treferences'] = pi_no
                else:
                    payment['treferences'] = {}


    payments.extend(draft_payments)

    return payments

@frappe.whitelist()
def stock_journals():

    payload = json.loads(frappe.request.data)

    branch = payload['branch']
    converted_branch = branch.split(",")

    stock_jvs = frappe.db.get_all(
        'Stock Entry',
        fields=[
            'name', 'posting_date', 'docstatus', 'company',
            'branch', 'amended_from', 'naming_series', 'remarks', 'total_amount', 'to_warehouse', 'from_warehouse'
            ],
        filters={ 
            # 'modified' : ['>', payload['date']],
            'company': payload['company'],
            'branch': ["in", converted_branch],
            'docstatus': ["in", ["1", "2"]],
            'is_synced': ['!=', 'Yes'],
            # 'is_synced': ['!=', 'Yes']
            },
        limit=100
        )
    if stock_jvs:
        for sjv in stock_jvs:
            pi_no = frappe.get_doc('Stock Entry', sjv.get("name"))
            if pi_no:
                sjv['tstockjournal'] = pi_no
            else:
                sjv['tstockjournal'] = {}

    return stock_jvs

@frappe.whitelist()
def journal():

    payload = json.loads(frappe.request.data)

    branch = payload['branch']
    converted_branch = branch.split(",")

    payments = frappe.db.get_all(
        'Journal Entry',
        fields=[
            'name', 'posting_date', 'docstatus', 'company',
            'custom_branch', 'voucher_type', 'cheque_no', 'cheque_date', 'user_remark', 'amended_from'
            ],
        filters={ 
            'company': payload['company'],
            'custom_branch': ["in", converted_branch],
            'docstatus': ["in", ["1", "2"]],
            'is_synced': ['!=', 'Yes'],
            'is_opening': 'No'
            },
        limit=100
        )
    if payments:
        for payment in payments:
            payment_no = payment['name']

            if payment_no:
                pi_no = frappe.get_doc('Journal Entry', payment_no)

                if pi_no:
                    payment['treferences'] = pi_no
                else:
                    payment['treferences'] = {}

    return payments

@frappe.whitelist()
def customer_update():
    # print(frappe.request.data)
    _json = json.loads(frappe.request.data)
    doctype = _json['request_type']
    doc_data = _json['data']
    
    for doc in doc_data:
        frappe.db.set_value(
            doctype,
            doc['docname'],
            {
                "is_synced": 'Yes',
                "sync_message": "Success"
            }
        )

    frappe.db.commit()


@frappe.whitelist()
def update_tally_flag(doc, method):

    if doc:
        frappe.db.set_value(
            doc.doctype,
            doc.name,
            {
                "is_synced": 'No',
                "sync_message": ""
            }
        )

        doc.reload()

        # frappe.db.commit()