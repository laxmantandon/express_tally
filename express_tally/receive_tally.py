from __future__ import unicode_literals

import frappe, json


@frappe.whitelist()
def customer_group():
    payload = json.loads(frappe.request.data)
    groups = payload['data']

    tally_response = []

    for group in groups:
        group_exists = frappe.db.exists(group['doctype'], group['customer_group_name'])
        if not group_exists:
            try:
                doc = frappe.get_doc(group)
                doc.insert()
                tally_response.append({'name': group['customer_group_name'], 'tally_object': 'Group', 'message': 'Success'})
            except Exception as e:
                tally_response.append({'name': group['customer_group_name'], 'tally_object': 'Group', 'message': str(e)})
        else:
            try:
                frappe.db.set_value(group['doctype'], group['customer_group_name'], {
                    "customer_group_name": group['customer_group_name'],
                    "is_group": group['is_group'],
                    "parent_customer_group": group['parent_customer_group'],
                })

                tally_response.append({'name': group['customer_group_name'], 'tally_object': 'Group', 'message': 'Success'})
            except Exception as e:
                tally_response.append({'name': group['customer_group_name'], 'tally_object': 'Group', 'message': str(e)})

    return {"status" : True, 'data': tally_response}

@frappe.whitelist()
def supplier_group():
    payload = json.loads(frappe.request.data)
    groups = payload['data']

    tally_response = []

    for group in groups:
        group_exists = frappe.db.exists(group['doctype'], group['supplier_group_name'])
        if not group_exists:
            try:
                doc = frappe.get_doc(group)
                doc.insert()
                tally_response.append({'name': group['supplier_group_name'], 'tally_object': 'Group', 'message': 'Success'})
            except Exception as e:
                tally_response.append({'name': group['supplier_group_name'], 'tally_object': 'Group', 'message': str(e)})
        else:
            try:
                frappe.db.set_value(group['doctype'], group['supplier_group_name'], {
                    "supplier_group_name": group['suppiler_group_name'],
                    "is_group": group['is_group'],
                    "parent_supplier_group": group['parent_supplier_group'],
                })

                tally_response.append({'name': group['supplier_group_name'], 'tally_object': 'Group', 'message': 'Success'})
            except Exception as e:
                tally_response.append({'name': group['supplier_group_name'], 'tally_object': 'Group', 'message': str(e)})

    return {"status" : True, 'data': tally_response}


@frappe.whitelist()
def item_group():
    payload = json.loads(frappe.request.data)
    stockgroups = payload['data']

    tally_response = []

    for stockgroup in stockgroups:
        group_exists = frappe.db.exists(stockgroup['doctype'], stockgroup['item_group_name'])
        if not group_exists:
            try:
                doc = frappe.get_doc(stockgroup)
                doc.insert()
                tally_response.append({'name': stockgroup['item_group_name'], 'tally_object': 'Stock Group', 'message': 'Success'})
            except Exception as e:
                tally_response.append({'name': stockgroup['item_group_name'], 'tally_object': 'Stock Group', 'message': str(e)})
        else:
            try:
                frappe.db.set_value(stockgroup['doctype'], stockgroup['item_group_name'], {
                    "item_group_name": stockgroup['item_group_name'],
                    "is_group": stockgroup['is_group'],
                    "parent_item_group": stockgroup['parent_item_group'],
                })

                tally_response.append({'name': stockgroup['item_group_name'], 'tally_object': 'Stock Group', 'message': 'Success'})
            except Exception as e:
                tally_response.append({'name': stockgroup['item_group_name'], 'tally_object': 'Stock Group', 'message': str(e)})

    return {"status" : True, 'data': tally_response}



@frappe.whitelist()
def customer():
    payload = json.loads(frappe.request.data)
    customers = payload['data']

    tally_response = []

    for customer in customers:
        group_exists = frappe.db.exists(customer['doctype'], customer['item_group_name'])
        if not group_exists:
            try:
                doc = frappe.get_doc(customer)
                doc.insert()
                tally_response.append({'name': customer['item_group_name'], 'tally_object': 'Stock Group', 'message': 'Success'})
            except Exception as e:
                tally_response.append({'name': customer['item_group_name'], 'tally_object': 'Stock Group', 'message': str(e)})
        else:
            try:
                frappe.db.set_value(customer['doctype'], customer['item_group_name'], {
                    "item_group_name": customer['item_group_name'],
                    "is_group": customer['is_group'],
                    "parent_item_group": customer['parent_item_group'],
                })

                tally_response.append({'name': customer['item_group_name'], 'tally_object': 'Stock Group', 'message': 'Success'})
            except Exception as e:
                tally_response.append({'name': customer['item_group_name'], 'tally_object': 'Stock Group', 'message': str(e)})

    return {"status" : True, 'data': tally_response}


