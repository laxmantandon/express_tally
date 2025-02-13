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
                doc.disabled = 0
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
                # doc.submit()
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
                doc.disabled = 0
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
            "gstin": customer['gstin'] if 'gstin' in customer else "",
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
                tally_response.append(
                    {'name': voucher_data['tally_masterid'], 'docname': doc.name, 'tally_object': 'voucher', 'message': 'Success'})
            except Exception as e:
                tally_response.append(
                    {'name': voucher_data['tally_masterid'], 'tally_object': 'voucher', 'message': str(e)})
 
    return {"status": True, 'data': tally_response}

def create_sales_invoice(data):
    '''
        Method to create Sales Invoices
    '''
    has_data = frappe.db.exists('Sales Invoice', { 'tally_masterid': data.get('tally_masterid') })
    tally_settings = frappe.get_single('Express Tally Settings')
    disable_invoice_rounding = tally_settings.disable_invoice_rounding
    submit_vouchers = tally_settings.submit_vouchers
    tds_keyword = tally_settings.tds_keyword
    tds_account = tally_settings.tds_account
    create_missing_item = tally_settings.create_missing_item
    item_group = tally_settings.item_group
    default_uom = tally_settings.default_uom
    if not has_data:
        try:
            items = []
            taxes = []
            taxes_and_charges = data.get('taxes') or []
            for row in taxes_and_charges:
                if row.get('description'):
                    description = get_formatted_value(row.get('description'))
                    if 'GST' in description:
                        gst_details = get_gst_details(description)
                        if gst_details:
                            row['rate'] = gst_details.get('tax_rate')
                            row['account_head'] = gst_details.get('gst_account_head')
                            taxes.append(row)
                    elif tds_keyword and description == tds_keyword:
                        row['charge_type'] = 'Actual'
                        row['account_head'] = tds_account
                        row['rate'] = 0
                        taxes.append(row)
                    else:
                        # Setting Items
                        item_details = get_item_details(description)
                        if not item_details:
                            item_details = {}
                            # Create Missing Items
                            if create_missing_item:
                                item_code = create_item(description, item_group, default_uom)
                                item_details['item'] = item_code
                                item_details['uom'] = default_uom
                                item_details['stock_uom'] = default_uom
                        if item_details:
                            items.append({
                                'item_code': item_details.get('item'),
                                'stock_uom': item_details.get('uom'),
                                'uom': item_details.get('uom'),
                                'conversion_factor': 1,
                                'qty': 1,
                                'rate': float(row.get('base_tax_amount')),
                                'amount': float(row.get('base_tax_amount')),
                                'base_amount': float(row.get('base_tax_amount')),
                                'base_price_list_rate': float(row.get('base_tax_amount')),
                                'price_list_rate': float(row.get('base_tax_amount'))
                            })
            data['items'] = items
            data['taxes'] = taxes
            doc = frappe.get_doc(data)
            doc.customer = get_formatted_value(data.get('customer'))
            doc.disable_rounded_total = disable_invoice_rounding
            doc.insert()
            if submit_vouchers:
                doc.submit()
            response = {'name': data['tally_masterid'], 'docname': doc.name, 'tally_object': 'voucher', 'message': 'Success'}
        except Exception as e:
            create_failed_record(data, str(e))
            response = {'name': data['tally_masterid'], 'tally_object': 'voucher', 'message': str(e)}
    else:
        response = {'name': data['tally_masterid'], 'docname': has_data, 'tally_object': 'voucher', 'message': 'Already Exists'}
    return response

def create_purchase_invoice(data):
    '''
        Method to create Purchase Invoices
    '''
    has_data = frappe.db.exists('Purchase Invoice', { 'tally_masterid': data.get('tally_masterid') })
    tally_settings = frappe.get_single('Express Tally Settings')
    submit_vouchers = tally_settings.submit_vouchers
    create_missing_item = tally_settings.create_missing_item
    item_group = tally_settings.item_group
    default_uom = tally_settings.default_uom
    tds_payable_keyword = tally_settings.tds_payable_keyword
    tds_payable_account = tally_settings.tds_payable_account
    disable_invoice_rounding = tally_settings.disable_invoice_rounding
    if not has_data:
        try:
            items = []
            taxes = []
            taxes_and_charges = data.get('taxes') or []
            for row in taxes_and_charges:
                if row.get('description'):
                    description = get_formatted_value(row.get('description'))
                    if 'GST' in description:
                        # Fetching GST Details and adding as taxes
                        gst_details = get_gst_details(description)
                        if gst_details:
                            row['charge_type'] = 'On Net Total'
                            row['row_id'] = ''
                            row['rate'] = gst_details.get('tax_rate')
                            row['account_head'] = gst_details.get('gst_account_head')
                            taxes.append(row)
                    elif tds_payable_keyword and description == tds_payable_keyword:
                        # Checking for TDS and if any will add to taxes
                        row['charge_type'] = 'Actual'
                        row['account_head'] = tds_payable_account
                        row['rate'] = 0
                        tax_amount = float(row.get('tax_amount')) or 0
                        if tax_amount > 0:
                            row['tax_amount'] = - tax_amount
                            row['base_tax_amount'] = - tax_amount
                            row['tax_amount_after_discount_amount'] = - tax_amount
                            row['base_tax_amount_after_discount_amount'] = - tax_amount
                        taxes.append(row)
                    else:
                        # Setting Items
                        item_details = get_item_details(description)
                        if not item_details:
                            item_details = {}
                            # Create Missing Items
                            if create_missing_item:
                                item_code = create_item(description, item_group, default_uom)
                                item_details['item'] = item_code
                                item_details['uom'] = default_uom
                                item_details['stock_uom'] = default_uom
                        if item_details:
                            items.append({
                                'item_code': item_details.get('item'),
                                'stock_uom': item_details.get('uom'),
                                'uom': item_details.get('uom'),
                                'conversion_factor': 1,
                                'qty': 1,
                                'rate': float(row.get('base_tax_amount')),
                                'amount': float(row.get('base_tax_amount')),
                                'base_amount': float(row.get('base_tax_amount')),
                                'base_price_list_rate': float(row.get('base_tax_amount')),
                                'price_list_rate': float(row.get('base_tax_amount'))
                            })
            if len(items) > 1:
                for tax_row in taxes:
                    tax_row['charge_type'] = 'Actual'
            data['items'] = items
            data['taxes'] = taxes
            doc = frappe.get_doc(data)
            doc.supplier = get_formatted_value(data.get('supplier'))
            doc.disable_rounded_total = disable_invoice_rounding
            doc.insert()
            if submit_vouchers:
                doc.submit()
            response = {'name': data['tally_masterid'], 'docname': doc.name, 'tally_object': 'voucher', 'message': 'Success'}
        except Exception as e:
            create_failed_record(data, str(e))
            response = {'name': data.get('tally_masterid'), 'tally_voucherno':data.get('tally_voucherno'), 'posting_date':data.get('posting_date'), 'tally_object': 'voucher', 'message': str(e)}
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
    submit_vouchers = tally_settings.submit_vouchers
    payroll_payable_account = tally_settings.payroll_payable_account
    salary_account = tally_settings.salary_account
    default_account = tally_settings.default_account
    abbr_len = -1 * (len(company_abbr) + 3)
    if not has_data:
        try:
            for row in data.get('accounts'):
                if row.get('account'):
                    row['user_remark'] = row.get('account')
                    # if payroll_payable_account and payroll_payable_keyword:
                    #     if payroll_payable_keyword in row.get('account'):
                    #         row['account'] = payroll_payable_account
                    # if salary_account and salary_account_keyword:
                    #     if salary_account_keyword in row.get('account'):
                    #         row['account'] = salary_account
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
            if submit_vouchers:
                doc.submit()
            response = {'name': data['tally_masterid'], 'docname': doc.name, 'tally_object': 'voucher', 'message': 'Success'}
        except Exception as e:
            create_failed_record(data, str(e))
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

def get_gst_details(gst_keyword):
    '''
        Method to get tax head account from Express Tally Settings
    '''
    gst_details = None
    if frappe.db.exists('GST Mapping', { 'parenttype':'Express Tally Settings', 'gst_keyword':gst_keyword, 'parentfield':'gst_mappings' }):
        gst_details = frappe.db.get_value('GST Mapping', { 'parenttype':'Express Tally Settings', 'gst_keyword':gst_keyword, 'parentfield':'gst_mappings' }, ['gst_account_head', 'tax_rate'], as_dict=1)
    return gst_details

def get_item_details(item_keyword):
    '''
        Method to get tax head account from Express Tally Settings
    '''
    item_details = None
    if frappe.db.exists('Item Mapping', { 'parenttype':'Express Tally Settings', 'item_keyword':item_keyword, 'parentfield':'item_mappings' }):
        item_details = frappe.db.get_value('Item Mapping', { 'parenttype':'Express Tally Settings', 'item_keyword':item_keyword, 'parentfield':'item_mappings' }, ['item', 'uom'], as_dict=1)
    return item_details

def get_formatted_value(value):
    '''
        Method to remove unicode values
    '''
    return value.replace("\r", "").replace("\n", "")

def create_item(item_name, item_group, uom):
    '''
        Method to create Item
    '''
    item = frappe.db.exists('Item', item_name)
    if not item:
        doc = frappe.new_doc('Item')
        doc.item_code = item_name
        doc.item_name = item_name
        doc.item_group = item_group
        doc.stock_uom = uom
        doc.is_stock_item = 0
        doc.insert()
        return doc.name
    return item

def create_failed_record(data, message):
    '''
        Method to create Failed Migration Records
    '''
    tally_masterid = data.get('tally_masterid', '')
    tally_voucher_no = data.get('tally_voucherno', '')
    posting_date = data.get('posting_date', '')
    voucher_type = data.get('doctype')
    if not frappe.db.exists('Failed Tally Migration Record', { 'tally_masterid':tally_masterid, 'voucher_type':voucher_type, 'exception':message }):
        doc = frappe.new_doc('Failed Tally Migration Record')
        doc.tally_masterid = tally_masterid
        doc.tally_voucher_no = tally_voucher_no
        doc.posting_date = posting_date
        doc.voucher_type = voucher_type
        doc.payload = frappe.as_json(data)
        doc.exception = message
        doc.insert()