# Copyright (c) 2025, Laxman Tandon and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document

class FailedTallyMigrationRecord(Document):
	pass

@frappe.whitelist()
def retry_failed_voucher(failed_record_id):
	'''
        Method to create missing Voucher
	'''
	docname = None
	if frappe.db.exists('Failed Tally Migration Record', failed_record_id):
		doc = frappe.get_doc('Failed Tally Migration Record', failed_record_id)
		payload = json.loads(doc.payload)
		voucher = frappe.get_doc(payload)
		voucher.save()
		try:
			voucher.submit()
		except Exception as e:
			frappe.log_error(
				title="{0} submisison".format(voucher.doctype),
				message=str(e),
				reference_doctype=voucher.doctype,
				reference_name=voucher.name,
			)
		docname = voucher.name
		return docname