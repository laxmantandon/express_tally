import frappe

def autoname(doc, method):
    '''
        Method which trigger on autoname event of Sales Invoice, Purchase Invoice and Journal Entry
    '''
    set_docname_as_tally = frappe.db.get_single_value('Express Tally Settings', 'set_docname_as_tally')
    transaction_types = ['Sales Invoice', 'Purchase Invoice', 'Journal Entry']
    if set_docname_as_tally and doc.get('tally_voucherno'):
        if doc.doctype in transaction_types:
            doc.name = doc.tally_voucherno