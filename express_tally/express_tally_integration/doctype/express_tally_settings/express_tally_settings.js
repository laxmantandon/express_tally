// Copyright (c) 2025, Laxman Tandon and contributors
// For license information, please see license.txt

frappe.ui.form.on("Express Tally Settings", {
    refresh(frm) {
        set_filters(frm);
    }
});

function set_filters(frm) {
    frm.set_query('default_account', () => {
        return {
            filters: {
                is_group: 1
            }
        }
    })
}
