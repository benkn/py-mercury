# PyMercury

This project (aka Mercury) is used to collect transactions for checking accounts, savings accounts, and credit cards. It consumes transactions using Plaid and writes them to Google Sheets. It also deduplicates transactions so only new transactions are appended into the Google sheet.

## Getting Started

To get this all working, there were some setup tasks that anyone replicating this workflow would need to follow:

### 1. Sign up for Plaid.

I signed up and stuck with the free tier. I used the Sandbox to build the core functionality, and switched to Development for my personal use. Production has costs attributed to it, but Development allows me 100 items (bank accounts, credit cards). Since I only care about transactions and not identity, this should be good enough.

To work with some banks, like Chase, Bank of America, and CitiBank, you will need production access and to complete a security questionnaire. This process takes some time to complete.

### 2. Configure a Google Sheets Service Account.

I followed [this guide](https://javascript.plainenglish.io/how-to-use-node-js-with-google-sheets-c256c26e10fc) on how to get the service account from Google and how to read/write to a Sheet. A real kicker is the sheet has to be shared to the service account as an Editor. **You will need the service account name and certificate for Mercury's [.env.tmpl](./.env.tmpl).**

The [structure of the rows](./etl/to_column_format.py) uses these columns:

```
Date	Description	Amount	✅	Category	Sub Category	Account	Raw Category	Transaction ID
```

The ✅ column is useful for confirming new transactions.

I use a sheet called **This_Month** and manually copy the sheet to a month-named sheet at the start of every month. (See the [configuration](./config/config.py)).

### 3. Use Plaid Quickstart Project to Get Access Tokens

My budget app uses access tokens to get transactions from Plaid for different financial institutions. To get the access token, rather than implementing the code myself, I used their [example project](https://plaid.com/docs/quickstart/#quickstart-setup).

> Prerequisite to using this app at all is getting production access in Plaid and [getting OAuth access to institutions](https://dashboard.plaid.com/settings/compliance/us-oauth-institutions). This step can take weeks to complete.

1. Clone the quickstart project as per their instructions, and install dependencies for the **node** and **frontend** folders.
2. In the **node** project, update the **.env** file:
   - Set the `PLAID_CLIENT_ID` and `PLAID_SECRET`
   - Switch the `PLAID_ENV` to production
   - Update the `PLAID_REDIRECT_URI` to https://localhost:3000/
   - Update `PLAID_PRODUCTS` to just transactions
3. Configure `https://localhost:3000/` as a redirect URI in [the Plaid Dashboard](https://dashboard.plaid.com/developers/api)
4. Follow [their instructions for running locally with SSL](https://github.com/plaid/quickstart/blob/master/README.md#testing-oauth)
5. Run the **frontend** and **node** projects with `npm start` in each directory
6. Open `https://localhost:3000/` in your web browser
7. After configuring a financial institution, the item id and access token will display in the browser. Copy these credentials.

## Configuring PyMercury

Once the prerequisites are complete, you should have production credentials (key + token). Remember, the token is private! Do not commit it.

1. Initialize the project by running `make init`
2. Then run `source ./.venv/bin/activate`
3. Copy **[.env.tmpl](./.env.tmpl)** to **.env**
4. Replace all `<>` variables with your own from the earlier steps.
5. Duplicate the **[accounts.tmpl.py](./config/accounts.tmpl.py)** to **config/accounts.py**. Enter the details from your financial institutions as you onboard them.
6. Duplicate the [custom_etls.example.py](./etl/custom_etls.example.py) to **etl/custom_etls.py**.
7. There are two mechanisms for updating (ETL) the transactions:
   - The [Category Lookups](./etl/custom_categories.py) have a key-value reference to Plaid categories. Feel free to edit them to replace any instance of a Plaid category to a custom value.
   - The [Custom Rules](./etl/custom_etls.example.py) power logic based on the description of the transaction to override the name, category or sub-category. Whenever a transaction name `starts_with`, `ends_with`, or `includes` the filter text, regardless of lower case or upper case, then the transformation is applied.
8. _Lastly_ (I know it's a lot...), the **[config.py](./config/config.py)** manages all of these custom settings, as well as setting the date range for fetching transactions. There are controls for ignoring transactions which are too large, which is helpful if it is holiday/birthday time and you don't want to spoil any surpises :)

## Running PyMercury

After all the configuration is complete, run with `make`. You should see the results in the sheet.

## FAQ

### How to run for previous months

You can run Mercury to collect transactions from earlier time periods, such as earlier months, and write to a separate sheet by update the **[config.py](./config/config.[y])**.

1. Update the `start_date` and `end_date`
2. Update the `spreadsheetTabName`
3. Run with `npm start`

### How to run more easily

You can create a Shortcut on MacOS to run Mercury with the click of a button:

1. Create a new Shortcut
2. Choose a **Run Shell Script** action
3. Set the script as:

```sh
cd ~/ws/py-mercury && \
./.venv/bin/python3 main.py
```

4. Add shortcut to the Dock or Desktop

### How to prevent committing secrets

The secrets for PyMercury are in either accounts.py or .env. Both of these files are ignored by git via **[.gitignore](./.gitignore)**.

The personal details of your custom rules are also ignored by git.

### Why is the category "Maybe..."

Plaid categorizes transactions and includes a degree of confidence in the categorization. If the confidence is low, Mercury will prepend "Maybe..." to the category to indicate deeper review is necessary. Edit the category manually in Google Sheets, and optionally add a Custom Rule if the merchant frequently has this issue.

### Does Mercury support Apple Card

No, Apple Card does not work with Plaid and so it is not available with Mercury. Instead, I manually enter the transaction details and skip setting a Transaction ID.

### How to split a transaction

Because Mercury distinguishes transactions by transaction ID, you can duplicate rows in the **This_Month** sheet to split a transaction and leave the transaction IDs on both rows.

## Reference

- [Plaid Category Hierarchy CSV](https://plaid.com/documents/transactions-personal-finance-category-taxonomy.csv)
