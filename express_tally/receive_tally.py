from __future__ import unicode_literals

import frappe
import json
from frappe.utils import getdate

@frappe.whitelist()
def customer_group():
    payload = json.loads(frappe.request.data)
    groups = payload['data']

    tally_response = []

    for group in groups:
        group_exists = frappe.db.exists(
            group['doctype'], group['customer_group_name'])
        if not group_exists:
            try:
                doc = frappe.get_doc(group)
                doc.insert()
                tally_response.append(
                    {'name': group['customer_group_name'], 'tally_object': 'Group', 'message': 'Success'})
            except Exception as e:
                tally_response.append(
                    {'name': group['customer_group_name'], 'tally_object': 'Group', 'message': str(e)})
        else:
            tally_response.append(
                    {'name': group['customer_group_name'], 'tally_object': 'Group', 'message': 'Already Exists'})

    return {"status": True, 'data': tally_response}


@frappe.whitelist()
def supplier_group():
    payload = json.loads(frappe.request.data)
    groups = payload['data']

    tally_response = []

    for group in groups:
        group_exists = frappe.db.exists(
            group['doctype'], group['supplier_group_name'])
        if not group_exists:
            try:
                doc = frappe.get_doc(group)
                doc.insert()
                tally_response.append(
                    {'name': group['supplier_group_name'], 'tally_object': 'Group', 'message': 'Success'})
            except Exception as e:
                tally_response.append(
                    {'name': group['supplier_group_name'], 'tally_object': 'Group', 'message': str(e)})
        else:
            tally_response.append(
                    {'name': group['supplier_group_name'], 'tally_object': 'Group', 'message': 'Already Exists'})

    return {"status": True, 'data': tally_response}


@frappe.whitelist()
def item_group():
    payload = json.loads(frappe.request.data)
    stockgroups = payload['data']

    tally_response = []

    for stockgroup in stockgroups:
        group_exists = frappe.db.exists(
            stockgroup['doctype'], stockgroup['item_group_name'])
        if not group_exists:
            try:
                doc = frappe.get_doc(stockgroup)
                doc.insert()
                tally_response.append(
                    {'name': stockgroup['item_group_name'], 'tally_object': 'Stock Group', 'message': 'Success'})
            except Exception as e:
                tally_response.append(
                    {'name': stockgroup['item_group_name'], 'tally_object': 'Stock Group', 'message': str(e)})
        else:
            tally_response.append(
                    {'name': stockgroup['item_group_name'], 'tally_object': 'Stock Group', 'message': 'Already Exists'})

    return {"status": True, 'data': tally_response}


@frappe.whitelist()
def warehouse():
    payload = json.loads(frappe.request.data)
    warehouses = payload['data']

    tally_response = []

    for warehouse in warehouses:
        is_exists = frappe.db.exists(
            warehouse['doctype'], warehouse['warehouse_name'])
        if not is_exists:
            try:
                doc = frappe.get_doc(warehouse)
                doc.insert()
                tally_response.append(
                    {'name': warehouse['warehouse_name'], 'tally_object': 'Godown', 'message': 'Success'})
            except Exception as e:
                tally_response.append(
                    {'name': warehouse['item_group_name'], 'tally_object': 'Godown', 'message': str(e)})
        else:
            tally_response.append(
                    {'name': warehouse['warehouse_name'], 'tally_object': 'Godown', 'message': 'Already Exists'})

    return {"status": True, 'data': tally_response}


@frappe.whitelist()
def customer():
    payload = json.loads(frappe.request.data)
    customers = payload['data']

    tally_response = []

    for customer in customers:
        is_exists = frappe.db.exists(
            customer['doctype'], customer['customer_name'])
        if not is_exists:
            try:
                # create_account(customer)

                doc = frappe.get_doc(customer)
                doc.insert()

                create_contact(customer)
                create_address(customer)


                tally_response.append(
                    {'name': customer['customer_name'], 'tally_object': 'Ledger', 'message': 'Success'})
            except Exception as e:
                tally_response.append(
                    {'name': customer['customer_name'], 'tally_object': 'Ledger', 'message': str(e)})
        else:
            tally_response.append(
                    {'name': customer['customer_name'], 'tally_object': 'Ledger', 'message': 'Already Exists'})

    return {"status": True, 'data': tally_response}


@frappe.whitelist()
def customer_opening():
    payload = json.loads(frappe.request.data)
    bills = payload['data']

    tally_response = []
    for b in bills:
        for bill in b['bills']:
            try:
                req = {
                    "remarks": bill['bill_name'],
                    "customer": bill['customer'],
                    "customer_name": bill['customer'],
                    "company": bill['company'],
                    "currency": "INR",
                    "set_posting_time": True,
                    "price_list_currency": "INR",
                    "posting_date": bill['posting_date'],
                    "due_date": bill['due_date'],
                    "debit_to": bill['debit_to'], #"Test 3 Customer - ETPL",
                    "party_account_currency": "INR",
                    "is_opening": 'Yes',
                    "is_return": bill['is_return'],
                    "grand_total": bill['amount'],
                    "against_income_account": bill['against_income_account'],#"Temporary Opening - ETPL",
                    "doctype": "Sales Invoice",
                    "items": [
                        {
                        "item_name": "Opening Invoice Item",
                        "description": "Opening Invoice Item",
                        "qty": 1 if bill['is_return'] == 0 else -1,
                        "stock_uom": "Nos",
                        "uom": "Nos",
                        "conversion_factor": 1,
                        "stock_qty": 1 if bill['is_return'] == 0 else -1,
                        "rate": abs(bill['amount']),
                        "amount": bill['amount'],
                        "income_account": bill['against_income_account'],
                        "doctype": "Sales Invoice Item"
                        }
                    ],
                    "payment_schedule": [
                        {
                        "due_date": bill['due_date'],
                        "invoice_portion": 100,
                        "payment_amount": bill['amount'],
                        "outstanding": bill['amount'],
                        "paid_amount": 0,
                        "base_payment_amount": bill['amount'],
                        "doctype": "Payment Schedule"
                        }
                    ],
                }

                doc = frappe.get_doc(req)
                doc.flags.ignore_mandatory = True
                doc.insert()
                doc.submit()
                tally_response.append(
                        {'name': bill['customer'], 'tally_object': 'Ledger', 'message': 'Success'})
            except Exception as e:
                tally_response.append(
                        {'name': bill['customer'], 'tally_object': 'Ledger', 'message': str(e)})

    return {"status": True, 'data': tally_response}    

@frappe.whitelist()
def supplier_opening():
    payload = json.loads(frappe.request.data)
    bills = payload['data']

    tally_response = []
    for b in bills:
        for bill in b['bills']:
            try:
                req = {
                    "remarks": bill['bill_name'],
                    "supplier": bill['supplier'],
                    "supplier_name": bill['supplier'],
                    "company": bill['company'],
                    "currency": "INR",
                    "set_posting_time": True,
                    "price_list_currency": "INR",
                    "posting_date": bill['posting_date'],
                    "due_date": bill['due_date'],
                    "credit_to": bill['credit_to'], #"Test 3 Customer - ETPL",
                    "party_account_currency": "INR",
                    "is_opening": 'Yes',
                    "is_return": bill['is_return'],
                    "grand_total": bill['amount'],
                    "against_expense_account": bill['against_expense_account'],#"Temporary Opening - ETPL",
                    "doctype": "Purchase Invoice",
                    "items": [
                        {
                        "item_name": "Opening Invoice Item",
                        "description": "Opening Invoice Item",
                        "qty": 1 if bill['is_return'] == 0 else -1,
                        "stock_uom": "Nos",
                        "uom": "Nos",
                        "conversion_factor": 1,
                        "stock_qty": 1 if bill['is_return'] == 0 else -1,
                        "rate": abs(bill['amount']),
                        "amount": bill['amount'],
                        "expense_account": bill['against_expense_account'],
                        "doctype": "Purchase Invoice Item"
                        }
                    ],
                    # "payment_schedule": [
                    #     {
                    #     "due_date": bill['due_date'],
                    #     "invoice_portion": 100,
                    #     "payment_amount": bill['amount'],
                    #     "outstanding": bill['amount'],
                    #     "paid_amount": 0,
                    #     "base_payment_amount": bill['amount'],
                    #     "doctype": "Payment Schedule"
                    #     }
                    # ],
                }

                doc = frappe.get_doc(req)
                doc.flags.ignore_mandatory = True
                doc.insert()
                # doc.submit()
                tally_response.append(
                        {'name': bill['supplier'], 'tally_object': 'Ledger', 'message': 'Success'})
            except Exception as e:
                tally_response.append(
                        {'name': bill['supplier'], 'tally_object': 'Ledger', 'message': str(e)})

    return {"status": True, 'data': tally_response}    


@frappe.whitelist()
def supplier():
    payload = json.loads(frappe.request.data)
    suppliers = payload['data']

    tally_response = []

    for supplier in suppliers:
        is_exists = frappe.db.exists(
            supplier['doctype'], supplier['supplier_name'])
        if not is_exists:
            try:
                # create_account(supplier)

                doc = frappe.get_doc(supplier)
                doc.insert()

                create_contact(supplier)
                create_address(supplier)

                tally_response.append(
                    {'name': supplier['supplier_name'], 'tally_object': 'Ledger', 'message': 'Success'})
            except Exception as e:
                tally_response.append(
                    {'name': supplier['supplier_name'], 'tally_object': 'Ledger', 'message': str(e)})
        else:
            tally_response.append(
                    {'name': supplier['supplier_name'], 'tally_object': 'Ledger', 'message': 'Already Exists'})

    return {"status": True, 'data': tally_response}    


def create_account(customer):
    try:
        doctype = customer['doctype']
        cus_name = customer['customer_name'] if doctype == 'Customer' else customer['supplier_name']
        parent_account = 'Accounts Receivable - W' if doctype == 'Customer' else 'Accounts Payable - W'
        account_type = 'Receivable' if doctype == 'Customer' else 'Payable'

        req = {
            "company": customer['company'],
            "account_name": cus_name,
            "account_currency": "INR",
            "doctype": "Account",
            "parent_account": parent_account,
            "account_type": account_type
        }

        # print(req)
        doc = frappe.get_doc(req)
        doc.insert()

        # return {'name': customer['customer_name'], 'tally_object': 'Ledger_Contact', 'message': 'Success'}
        print('Success- Account')
    except Exception as e:
        print(str(e))
        # return {'name': customer['customer_name'], 'tally_object': 'Ledger_Contact', 'message': str(e)}


def create_contact(customer):
    try:
        doctype = customer['doctype']
        cus_name = customer['customer_name'] if doctype == 'Customer' else customer['supplier_name']

        req = {
            "name": customer['ledgercontact'],
            "first_name": customer['ledgercontact'],
            "email_id": customer['email']  if 'email' in customer else "",
            "status": "Passive",
            "phone": customer['ledgermobile'] if 'ledgermobile' in customer else "",
            "mobile_no": customer['ledgermobile'] if 'ledgermobile' in customer else "",
            "is_primary_contact": 1,
            "is_billing_contact": 1,
            "doctype": "Contact",
            "email_ids": [
                {
                    "parent": customer['ledgercontact'],
                    "parentfield": "email_ids",
                    "parenttype": "Contact",
                    "email_id": customer['email'] if 'email' in customer else "a@b.com",
                    "is_primary": 1,
                    "doctype": "Contact Email"
                }
            ],
            "phone_nos": [
                {
                    "parent": customer['ledgercontact'],
                    "parentfield": "phone_nos",
                    "parenttype": "Contact",
                    "phone": customer['ledgermobile'] if 'ledgermobile' in customer else "9999999999",
                    "is_primary_phone": 1,
                    "is_primary_mobile_no": 1,
                    "doctype": "Contact Phone"
                }
            ],
            "links": [
                {
                    "parent": customer['ledgercontact'],
                    "parentfield": "links",
                    "parenttype": "Contact",
                    "link_doctype": doctype,
                    "link_name": cus_name,
                    "link_title": cus_name,
                    "doctype": "Dynamic Link"
                }
            ],
        }

        # print(req)
        doc = frappe.get_doc(req)
        doc.insert()

        # return {'name': customer['customer_name'], 'tally_object': 'Ledger_Contact', 'message': 'Success'}
        print('Success- Contact')
    except Exception as e:
        print(str(e))
        # return {'name': customer['customer_name'], 'tally_object': 'Ledger_Contact', 'message': str(e)}


def create_address(customer):
    try:
        address1 = customer['address1'] if 'address1' in customer else ""
        address2 = customer['address2'] if 'address2' in customer else ""
        address3 = customer['address3'] if 'address3' in customer else ""
        address4 = customer['address4'] if 'address4' in customer else ""
        doctype = customer['doctype']
        cus_name = customer['customer_name'] if doctype == 'Customer' else customer['supplier_name']

        req = {
            "name": cus_name+"-Billing",
            "address_title": cus_name,
            "address_type": "Billing",
            "address_line1": address1 + " " + address2,
            "address_line2": address3 + " " + address4,
            "city": customer['city'] if 'city' in customer else "",
            "state": customer['state'] if 'state' in customer else "",
            "country": customer['country'] if 'country' in customer else "",
            "pincode": customer['pincode'] if 'pincode' in customer else "",
            # "phone": customer['customer_name'],
            "gstin": customer['partygstin'] if 'partygstin' in customer else "",
            "gst_state": customer['state'] if 'state' in customer else "",
            "gst_state_number": customer['state_code'] if 'state_code' in customer else "",
            "tax_category": customer['tax_category'] if 'tax_category' in customer else "",
            "is_primary_address": 1,
            "is_shipping_address": 1,
            "doctype": "Address",
            "links": [
                {
                    "parent": cus_name+"-Billing",
                    "parentfield": "links",
                    "parenttype": "Address",
                    "link_doctype": doctype,
                    "link_name": cus_name,
                    "link_title": cus_name,
                    "doctype": "Dynamic Link"
                }
            ]
        }
        # print(req)
        doc = frappe.get_doc(req)
        doc.insert()

        print('Success- Address') # return {'name': customer['customer_name'], 'tally_object': 'Ledger_Address', 'message': 'Success'}
    except Exception as e:
        print(str(e))
        # return {'name': customer['customer_name'], 'tally_object': 'Ledger_Address', 'message': str(e)}




@frappe.whitelist()
def uom():
    payload = json.loads(frappe.request.data)
    uoms = payload['data']

    tally_response = []

    for uom in uoms:
        uom_exists = frappe.db.exists(
            uom['doctype'], uom['uom_name'])
        if not uom_exists:
            try:
                doc = frappe.get_doc(uom)
                doc.insert()
                tally_response.append(
                    {'name': uom['uom_name'], 'tally_object': 'Unit', 'message': 'Success'})
            except Exception as e:
                tally_response.append(
                    {'name': uom['uom_name'], 'tally_object': 'Unit', 'message': str(e)})
        else:
            tally_response.append(
                    {'name': uom['uom_name'], 'tally_object': 'Unit', 'message': 'Already Exists'})

    return {"status": True, 'data': tally_response}



@frappe.whitelist()
def item():
    payload = json.loads(frappe.request.data)
    items = payload['data']

    tally_response = []

    for item in items:
        create_hsn(item)
        item_exists = frappe.db.exists(
            'Item', item['item_name'])
        if not item_exists:
            try:
                doc = frappe.get_doc(item)
                doc.insert()
                tally_response.append(
                    {'name': item['item_name'], 'tally_object': 'Stock Item', 'message': 'Success'})
            except Exception as e:
                tally_response.append(
                    {'name': item['item_name'], 'tally_object': 'Stock Item', 'message': str(e)})
        else:
            tally_response.append(
                    {'name': item['item_name'], 'tally_object': 'Stock Item', 'message': 'Already Exists'})

    return {"status": True, 'data': tally_response}

def create_hsn(item):
    if 'gst_hsn_code' in item:
        if not frappe.db.exists('GST HSN Code', item['gst_hsn_code']):

            req = {
                "hsn_code": item['gst_hsn_code'],
                "doctype": "GST HSN Code"
            }

            doc = frappe.get_doc(req)
            doc.insert()

@frappe.whitelist()
def voucher():
    payload = json.loads(frappe.request.data)
    vouchers_data = payload['data']
    
    tally_response = []

    for voucher_data in vouchers_data:
        from_date = frappe.db.get_single_value('Express Tally Settings', 'from_date')
        to_date = frappe.db.get_single_value('Express Tally Settings', 'to_date')
        if from_date and to_date and voucher_data.get('posting_date'):
            if not (getdate(from_date) <= getdate(voucher_data.get('posting_date')) and getdate(voucher_data.get('posting_date')) <= getdate(to_date)):
                tally_response.append(
                    {'name': voucher_data['tally_masterid'], 'tally_object': 'voucher', 'message': 'Date out of range'})
                continue
        if voucher_data['doctype'] == 'Sales Invoice':
            response = create_sales_invoice(voucher_data)
            tally_response.append(response)
        elif voucher_data['doctype'] == 'Purchase Invoice':
            response = create_purchase_invoice(voucher_data)
            tally_response.append(response)
        elif voucher_data['doctype'] == 'Journal Entry':
            response = create_journal_entry(voucher_data)
            tally_response.append(response)
        else:
            try:
                doc = frappe.get_doc(voucher_data)
                doc.insert()
                doc.submit()
                tally_response.append(
                    {'name': voucher_data['tally_masterid'], 'docname': doc.name, 'tally_object': 'voucher', 'message': 'Success'})
            except Exception as e:
                tally_response.append(
                    {'name': voucher_data['tally_masterid'], 'tally_object': 'voucher', 'message': str(e)})
 
    for tal in tally_response:
        if tal.get('message') not in ['Success', 'Already Exists']:
            print("row : ", tal)
    return {"status": True, 'data': tally_response}

def create_sales_invoice(data):
    '''
        Method to create Sales Invoices
    '''
    has_data = frappe.db.exists('Sales Invoice', { 'tally_masterid': data.get('tally_masterid') })
    if not has_data:
        try:
            doc = frappe.get_doc(data)
            doc.insert()
            doc.submit()
            response = {'name': data['tally_masterid'], 'docname': doc.name, 'tally_object': 'voucher', 'message': 'Success'}
        except Exception as e:
            response = {'name': data['tally_masterid'], 'tally_object': 'voucher', 'message': str(e)}
    else:
        response = {'name': data['tally_masterid'], 'docname': has_data, 'tally_object': 'voucher', 'message': 'Already Exists'}
    return response

def create_purchase_invoice(data):
    '''
        Method to create Purchase Invoices
    '''
    has_data = frappe.db.exists('Purchase Invoice', { 'tally_masterid': data.get('tally_masterid') })
    if not has_data:
        try:
            doc = frappe.get_doc(data)
            doc.insert()
            doc.submit()
            response = {'name': data['tally_masterid'], 'docname': doc.name, 'tally_object': 'voucher', 'message': 'Success'}
        except Exception as e:
            response = {'name': data['tally_masterid'], 'tally_object': 'voucher', 'message': str(e)}
    else:
        response = {'name': data['tally_masterid'], 'docname': has_data, 'tally_object': 'voucher', 'message': 'Already Exists'}
    return response

def create_journal_entry(data):
    '''
        Method to create Journal Entry
    '''
    tally_settings = frappe.get_single('Express Tally Settings')
    has_data = frappe.db.exists('Journal Entry', { 'tally_masterid': data.get('tally_masterid') })
    company_abbr = tally_settings.company_abbr
    payroll_payable_account = tally_settings.payroll_payable_account
    payroll_payable_keyword = tally_settings.payroll_payable_keyword
    salary_account = tally_settings.salary_account
    salary_account_keyword = tally_settings.salary_account_keyword
    default_account = tally_settings.default_account
    abbr_len = -1 * (len(company_abbr) + 3)
    if not has_data:
        try:
            for row in data.get('accounts'):
                if row.get('account'):
                    row['user_remark'] = row.get('account')
                    if payroll_payable_account and payroll_payable_keyword:
                        if payroll_payable_keyword in row.get('account'):
                            row['account'] = payroll_payable_account
                    if salary_account and salary_account_keyword:
                        if salary_account_keyword in row.get('account'):
                            row['account'] = salary_account
                    if not frappe.db.exists('Account', row.get('account')):
                        account_name = row.get('account')[:abbr_len]
                        if frappe.db.exists('Customer', account_name):
                            row['account'] = get_party_account('Customer', account_name)
                            row['party_type'] = 'Customer'
                            row['party'] = account_name
                        elif frappe.db.exists('Supplier', account_name):
                            row['account'] = get_party_account('Supplier', account_name)
                            row['party_type'] = 'Supplier'
                            row['party'] = account_name
                        else:
                            create_coa(default_account, account_name)
            doc = frappe.get_doc(data)
            doc.insert()
            doc.submit()
            response = {'name': data['tally_masterid'], 'docname': doc.name, 'tally_object': 'voucher', 'message': 'Success'}
        except Exception as e:
            response = {'name': data['tally_masterid'], 'tally_object': 'voucher', 'message': str(e)}
    else:
        response = {'name': data['tally_masterid'], 'docname': has_data, 'tally_object': 'voucher', 'message': 'Already Exists'}
    return response

def create_coa(parent, account_name):
    '''
        Method to create Account
    '''
    if frappe.db.exists('Account', parent) and not frappe.db.exists('Account', account_name):
        account_doc = frappe.new_doc('Account')
        account_doc.parent_account = parent
        account_doc.account_name = account_name
        account_doc.insert()

def get_party_account(party_type, party):
    '''
        Method to get Customer Account
    '''
    account = None
    if frappe.db.exists('Party Account', { 'parenttype':party_type, 'parent':party, 'parentfield':'accounts' }):
        account = frappe.db.get_value('Party Account', { 'parenttype':party_type, 'parent':party, 'parentfield':'accounts' }, 'account')
    return account