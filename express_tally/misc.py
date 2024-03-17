from __future__ import unicode_literals

import frappe
import json


@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_pending_orders(doctype, txt, searchfield, start, page_len, filters):

	item_code = filters.get('item_code')
	company = filters.get('company')
	supplier = filters.get('supplier')
	status = filters.get('status')
	values = {'status':status, 'item_code': item_code, 'company': company, 'supplier': supplier, 'txt': txt }
	return frappe.db.sql("""
		SELECT 
			res.name,
			res.supplier,
			res.item_code,
			SUM(CASE WHEN res.parenttype='Purchase Order' THEN res.qty ELSE res.qty * -1 END) AS pending_qty
			FROM
				(
				SELECT
					so.name, so.transaction_date, so.supplier, soi.parenttype, soi.item_name, soi.item_code, soi.qty
				FROM `tabPurchase Order Item` soi
						LEFT JOIN `tabItem` i on i.name = soi.item_code
						LEFT JOIN `tabPurchase Order` so ON so.name = soi.parent
				WHERE so.docstatus = 1 AND so.status = %(status)s AND soi.item_code = %(item_code)s AND so.supplier = %(supplier)s AND so.company = %(company)s
				UNION ALL
				SELECT
					sii.purchase_order, si.posting_date, si.supplier, sii.parenttype, sii.item_name, sii.item_code, sii.qty
				FROM `tabPurchase Invoice Item` sii
					LEFT JOIN `tabItem` i on i.name = sii.item_code
					LEFT JOIN `tabPurchase Invoice` si ON si.name = sii.parent
				WHERE si.docstatus IN (1, 0) and sii.item_code = %(item_code)s AND si.supplier = %(supplier)s AND si.company = %(company)s
				)
			AS res
		GROUP BY res.name, res.supplier, res.item_code
		HAVING (SUM(CASE WHEN res.parenttype='Purchase Order' THEN res.qty ELSE res.qty * -1 END)) > 0
		ORDER BY res.supplier, res.item_code
	""", values=values, as_dict=0)

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_items_of_etpl_group(doctype, txt, searchfield, start, page_len, filters):

	etpl_product_group = filters.get('etpl_product_group')
	disabled = filters.get('disabled')
	values = { 'etpl_product_group': etpl_product_group, 'txt': '%'+txt+'%', 'disabled': disabled }
	return frappe.db.sql("""
		SELECT 
			i.name,
			i.item_name,
			g.etpl_product_group
		FROM 	`tabItem` i,
				`tabItem Group` g
		WHERE
		i.item_group = g.name
		AND g.etpl_product_group = %(etpl_product_group)s
		AND i.disabled = %(disabled)s
		AND (i.item_name like %(txt)s OR i.item_code like %(txt)s)
		LIMIT 10
	""", values=values, as_dict=0)


@frappe.whitelist()
def get_party_credit_limit_html(party):

	values = { 'party': party}
	credit_limit = frappe.db.sql("""
		SELECT
			gl.posting_date,
			DATE_ADD(gl.posting_date, INTERVAL epg.credit_days DAY) dueon,
			SUM(CASE WHEN (DATE_ADD(gl.posting_date, INTERVAL epg.credit_days DAY)) < CURDATE()	THEN (gl.debit - gl.credit) ELSE 0 END) overdue,
			ccl.credit_limit,
			epg.credit_days,
			si.etpl_product_group AS `group`,
			(Sum(gl.debit) - SUM(gl.credit)) due,
			MAX(DATEDIFF(CURDATE(), DATE_ADD(gl.posting_date, INTERVAL epg.credit_days DAY))) due_days
		FROM `tabGL Entry` gl
		LEFT JOIN `tabSales Invoice` si ON si.name = gl.against_voucher
		LEFT JOIN `tabCustomer Credit Limit` ccl ON ccl.parent = si.customer_name
		LEFT JOIN `tabETPL Product Group` epg ON epg.name = si.etpl_product_group
		WHERE `party` = %(party)s AND is_cancelled = 0
		GROUP BY `group`
		ORDER BY si.posting_date ASC
	""", values=values, as_dict=1)	

	html = """
	<div class="tax-break-up" style="overflow-x: auto;">
	<table class="table table-bordered table-hover">
		<tr>
			<th>Credit Limit</th>
			<th>ETPL Group</th>
			<th class='text-right' >Outstanding</th>
			<th class='text-right' >Overdue</th>
			<th class='text-right' >Due Days</th>
		</tr>
		{% for d in credit_limit %}
		<tr>
			<td>{% if loop.index == 1 %} {{ d['credit_limit'] }} {% endif %}</td>
			<td>{{ d['group'] }}</td>
			<td class='text-right' >{{ d['due'] }}</td>
			<td class='text-right' >{{ d['overdue'] }}</td>
			<td class='text-right' >{% if 'due_days' in d %} {{ d['due_days'] }} {% endif %}</td>
		</tr>
		{% endfor %}
		<tr>
			<th></th>
			<th>Total</th>
			<th class='text-right' >{{ credit_limit | sum(attribute='due') }}</th>
			<th class='text-right' ></th>
		</tr>
	</table>
	"""

	return frappe.render_template(html, dict(credit_limit=credit_limit))

@frappe.whitelist()
def get_pending_order_qty(item_code, company, supplier, purchase_order):
	values = { 'item_code': item_code, 'company': company, 'supplier': supplier, 'purchase_order': purchase_order }
	return frappe.db.sql("""
		SELECT 
			res.name,
			res.supplier,
			res.item_code,
			SUM(CASE WHEN res.parenttype='Purchase Order' THEN res.qty ELSE res.qty * -1 END) AS pending_qty
			FROM
				(
				SELECT
					so.name, so.transaction_date, so.supplier, soi.parenttype, soi.item_name, soi.item_code, soi.qty
				FROM `tabPurchase Order Item` soi
						LEFT JOIN `tabItem` i on i.name = soi.item_code
						LEFT JOIN `tabPurchase Order` so ON so.name = soi.parent
				WHERE so.docstatus = 1 AND soi.item_code = %(item_code)s AND so.supplier = %(supplier)s AND so.company = %(company)s
				UNION ALL
				SELECT
					sii.purchase_order, si.posting_date, si.supplier, sii.parenttype, sii.item_name, sii.item_code, sii.qty
				FROM `tabPurchase Invoice Item` sii
					LEFT JOIN `tabItem` i on i.name = sii.item_code
					LEFT JOIN `tabPurchase Invoice` si ON si.name = sii.parent
				WHERE si.docstatus IN (1, 0) and sii.item_code = %(item_code)s AND si.supplier = %(supplier)s AND si.company = %(company)s
				)
			AS res
		GROUP BY res.name, res.supplier, res.item_code
		HAVING res.name = %(purchase_order)s AND (SUM(CASE WHEN res.parenttype='Purchase Order' THEN res.qty ELSE res.qty * -1 END)) > 0
		ORDER BY res.supplier, res.item_code
	""", values=values, as_dict=1)

@frappe.whitelist()
def etpl_get_warehouse_batch(filters):
	conditions = ""
	for field in ["item_code", "warehouse","company"]:
		if filters.get(field):
			conditions += " and {0} = {1}".format(field, frappe.db.escape(filters.get(field)))

	return frappe.db.sql(
		"""
		select item_code, batch_no, warehouse, posting_date, sum(actual_qty) as actual_qty
		from `tabStock Ledger Entry`
		where is_cancelled = 0 and docstatus < 2 and ifnull(batch_no, '') != '' %s
		group by batch_no, item_code, warehouse
		order by item_code, warehouse"""
		% conditions,
		as_dict=1,
	)


# @frappe.whitelist()
# def etpl_tail_unit(item_code, qty, unit):
# 	conversion = 0
# 	conversion_unit = ""
# 	item = frappe.get_doc("Item", item_code)
# 	for u in item.uoms:
# 		if u == unit:
# 			conversion = u.conversion_factor
# 			conversion_unit = u.uom
	
# 	tail_unit = (qty - (qty % conversion)) / conversion