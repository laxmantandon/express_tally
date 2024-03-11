
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
            'is_synced': ['!=', 'Yes'],
            'branch': payload['branch']
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
            'is_synced': ['!=', 'Yes'],
            'branch': payload['branch']
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
    purchase_invoices = frappe.db.get_all(
        'Purchase Invoice',
        fields=[
            'name', 'posting_date', 'docstatus', 'company', 'base_grand_total', 'base_net_total', 'bill_no', 'bill_date',
            'base_rounded_total', 'rounding_adjustment', 'modified', 'is_return', 'supplier', 'supplier_name'
            ],
        filters={ 
            # 'modified' : ['>', payload['date']],
            'company': payload['company'],
            'docstatus': 1,
            'is_synced': ['!=', 'Yes'],
            'branch': payload['branch']
            },
        limit=100
        )
    if purchase_invoices:
        for purchase_invoice in purchase_invoices:
            purchase_invoice_no = purchase_invoice['name']

            if purchase_invoice_no:
                pi_no = frappe.get_doc('Purchase Invoice', purchase_invoice_no)

                if pi_no:
                    purchase_invoice['tpurchaseinvoice'] = pi_no
                else:
                    purchase_invoice['tpurchaseinvoice'] = {}

    return purchase_invoices


@frappe.whitelist()
def sales():

    payload = json.loads(frappe.request.data)
    sales_invoices = frappe.db.get_all(
        'Sales Invoice',
        fields=[
            'name', 'posting_date', 'docstatus', 'company', 'base_grand_total', 'base_net_total',
            'base_rounded_total', 'rounding_adjustment', 'modified', 'is_return', 'customer', 'customer_name'
            ],
        filters={ 
            'posting_date' : ['>=', payload['date']],
            'company': payload['company'],
            'docstatus': 1,
            'is_synced': ['!=', 'Yes'],
            'branch': payload['branch']
            },
        limit=100
        )
    if sales_invoices:
        for sales_invoice in sales_invoices:
            sales_invoice_no = sales_invoice['name']

            if sales_invoice_no:
                pi_no = frappe.get_doc('Sales Invoice', sales_invoice_no)

                if pi_no:
                    sales_invoice['tsalesinvoice'] = pi_no
                else:
                    sales_invoice['tsalesinvoice'] = {}

    return sales_invoices



@frappe.whitelist()
def payments():

    payload = json.loads(frappe.request.data)
    payments = frappe.db.get_all(
        'Payment Entry',
        fields=[
            'name', 'posting_date', 'docstatus', 'company', 'party', 'party_name',
            'paid_to', 'paid_amount', 'remarks', 'payment_type', 'paid_from'
            ],
        filters={ 
            # 'modified' : ['>', payload['date']],
            'company': payload['company'],
            'docstatus': 1,
            'is_synced': ['!=', 'Yes'],
            'branch': payload['branch']
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

    return payments

@frappe.whitelist()
def journal():

    payload = json.loads(frappe.request.data)
    payments = frappe.db.get_all(
        'Journal Entry',
        fields=[
            'name', 'posting_date', 'docstatus', 'company',
            'voucher_type', 'branch', 'mspl_voucher_type', 'cheque_no', 'cheque_date', 'user_remark', 'amended_from'
            ],
        filters={ 
            # 'modified' : ['>', payload['date']],
            'company': payload['company'],
            'docstatus': 1,
            'is_synced': ['!=', 'Yes'],
            'branch': payload['branch'],
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

    # frappe.db.commit()


@frappe.whitelist()
def update_tally_flag(doc, method):
        
    if doc:
        if method == 'on_cancel' and doc.is_synced == 'No':
            pass
        else:
            frappe.db.set_value(
                doc.doctype,
                doc.name,
                {
                    "is_synced": 'No',
                    "sync_message": ""
                }
            )

            doc.reload()
