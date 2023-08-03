<div align="center">

<h1>Tally To ERPNext Data Migration Tool</h1>

This Application helps synchronizing data from tally to erpnext

</div>



## Introduction

Using this application will help you to migrate your tally data, masters and transactions both using frappe rest apis.

## Key Features

- Migrate Masters (Account, Customer, Suppliers, Contact and Address)
- Migrates Transactions (Purchase Invoice, Sales Invoice, Payment Entry, Journal Entry)

## Installation

Once you've [set up a Frappe site](https://frappeframework.com/docs/v14/user/en/installation/), installing Express Tally Integration is simple:


1. Download the app using the Bench CLI.

    ```bash
    bench get-app --branch [branch name] https://github.com/laxmantandon/express_tally.git
    ```

2. Install the app on your site.

    ```bash
    bench --site [site name] install-app express_tally
    ```

## Planned Features

- Sync Alternate (Multiple Units)
- Sync Price Lists

## Contributing

- [Issue Guidelines](https://github.com/frappe/erpnext/wiki/Issue-Guidelines)
- [Pull Request Requirements](https://github.com/frappe/erpnext/wiki/Contribution-Guidelines)

## License

[GNU General Public License (v3)]
