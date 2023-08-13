<div align="left">

<h1>Tally To ERPNext Data Migration Tool</h1>

This tool helps migration of data from Tally Prime (Masters and transactions) to ERPNext using frappe rest apis.
- Migrate Masters (Account, Customer, Suppliers, Contact and Address)
- Migrate Transactions (Purchase Invoice, Sales Invoice, Payment Entry, Journal Entry)

</div>

## Prerequisite
* TDL Files https://github.com/laxmantandon/tally_migration_tdl.git
* Tally Prime
* ERPNext Active Site 

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


## Steps to Configure
* Configure TDL Files in tally
  - follow instruction on this repo https://github.com/laxmantandon/tally_migration_tdl.git

* Generate Authentication Keys
  Create a user with appropriate permission and generate api key and secret
  ![image](https://github.com/laxmantandon/express_tally/assets/24727535/73558d52-d260-4a38-b0a1-8c2ef307a50b)

* Setting up Auth Keys in Tally Prime
  - From Gateway of Tally -> F1 -> Addon Features -> F6
  Set *Enable ERPNext Integration* to Yes and specify auth keys and other parameters
  
  ![image](https://github.com/laxmantandon/express_tally/assets/24727535/5039845f-6a04-49e2-b45c-4a55933630f7)

* Migrating Data from Tally to ERPNext
  - From Gateway of Tally go to Display -> ERPNext -> Migrate to ERPNext
  
  ![image](https://github.com/laxmantandon/express_tally/assets/24727535/d7029c93-1a44-450b-b2f1-ef3655eb28ce)

* Observe result in ERPNext

![image](https://github.com/laxmantandon/express_tally/assets/24727535/f1b46186-89d0-42fb-9136-1df767adbdb7)

## Errors and Exception Handling 
* From Gateway of Tally goto -> ERPNext -> Migration -> Exception (select object type )
  - You can check for exceptions here and make necessary changes in data
  - Check Error Log List in ERPNext for errors
  - Alternatively you check tally event log for more info
    
![image](https://github.com/laxmantandon/express_tally/assets/24727535/726a60b0-7291-4a82-a453-af3eb1d8a2fc)


## Planned Features

- Sync Alternate (Multiple Units)
- Sync Price Lists

## Contributing

- [Issue Guidelines](https://github.com/frappe/erpnext/wiki/Issue-Guidelines)
- [Pull Request Requirements](https://github.com/frappe/erpnext/wiki/Contribution-Guidelines)

## License

[GNU General Public License (v3)]
