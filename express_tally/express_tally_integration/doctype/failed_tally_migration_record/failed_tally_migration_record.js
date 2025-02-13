// Copyright (c) 2025, Laxman Tandon and contributors
// For license information, please see license.txt

frappe.ui.form.on("Failed Tally Migration Record", {
    refresh(frm) {
        frm.disable_save();
        frm.disable_form();
        if (!frm.is_new()) {
            handle_custom_button(frm);
        }
    }
});

function handle_custom_button(frm) {
    if (frm.doc.voucher_type && !frm.doc.reference_document) {
        frm.add_custom_button('Retry', () => {
            frappe.confirm('Are you sure you want to proceed?',
                () => {
                    create_failed_record(frm);
                }, () => {
                    console.log("Skipped");
                }
            );
        });
    }
}

function create_failed_record(frm) {
    frappe.call({
        method: 'express_tally.express_tally_integration.doctype.failed_tally_migration_record.failed_tally_migration_record.retry_failed_voucher',
        args: {
            failed_record_id: frm.doc.name
        },
        freeze: true,
        callback: (r) => {
            console.log(r.message);
        }
    });
}