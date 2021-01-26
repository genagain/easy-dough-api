from app.models import User, Bank, Account, SpendingPlanPart, Transaction

from app import create_app, db

app = create_app()

with app.app_context():

    user = User.create(
            firstname="John",
            lastname="Doe",
            email="john@test.com",
            password="test_password"
            )

    spending_plan_parts_data = [
            {
                'category': 'Discretionary Spending',
                'label': 'Spending Money',
                'search_term': '*',
                'expected_amount': '100000'
            },
            {
                'category': 'Fixed Costs',
                'label': 'Rent',
                'search_term': 'Property Management',
                'expected_amount': '100000'
            },
            {
                'category': 'Fixed Costs',
                'label': 'Internet',
                'search_term': 'COMCAST',
                'expected_amount': '4000'
            },
            {
                'category': 'Fixed Costs',
                'label': 'Electric',
                'search_term': 'EVERSOURCE ELECTRIC',
                'expected_amount': '4000'
            },
            {
                'category': 'Fixed Costs',
                'label': 'Gas',
                'search_term': 'EVERSOURCE GAS',
                'expected_amount': '2000'
            },
            {
                'category': 'Fixed Costs',
                'label': 'Cellphone',
                'search_term': 'VERIZON',
                'expected_amount': '5000'
            },
            {
                'category': 'Fixed Costs',
                'label': 'Groceries',
                'search_term': 'WHOLEFDS',
                'expected_amount': '40000'
            },
            {
                'category': 'Savings',
                'label': 'Emergency Fund',
                'search_term': 'Direct Deposit',
                'expected_amount': '50000'
            }
    ]

    for spending_part_datum in spending_plan_parts_data:
        category = spending_part_datum['category']
        label = spending_part_datum['label']
        search_term = spending_part_datum['search_term']
        expected_amount = spending_part_datum['expected_amount']

        spending_plan_part = SpendingPlanPart(
                category=category,
                label=label,
                search_term=search_term,
                expected_amount=expected_amount,
                user=user
                )
        db.session.add(spending_plan_part)

    db.session.commit()

    bank_logo = "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"

    bank = Bank(name='Ally Bank', logo=bank_logo, access_token='fake access token', user=user)
    db.session.add(bank)
    db.session.commit()

    accounts_data = [
        {
          'plaid_account_id': 'fake account id',
          'name': 'Interest Checking Account',
          'type': 'Checking'
        },
        {
          'plaid_account_id': 'another fake account id',
          'name': 'Interest Savings Account',
          'type': 'Savings'
        },
        {
          'plaid_account_id': 'yet another fake account id',
          'name': 'Ally Cashback Card',
          'type': 'Credit card'
        },
    ]

    for account_datum in accounts_data:
        plaid_account_id = account_datum['plaid_account_id']
        name = account_datum['name']
        type = account_datum['type']

        account = Account(plaid_account_id=plaid_account_id, name=name, type=type, bank=bank)
        db.session.add(bank)

    db.session.commit()

    transactions_data = [
      {
        'date': '2021-01-01',
        'description': 'Postmates',
        'amount': 30,
        'account_id': 'yet another fake account id'
      },
      {
        'date': '2021-01-02',
        'description': 'WHOLEFDS',
        'amount': 83.80,
        'account_id': 'fake account id'
      },
      {
        'date': '2021-01-04',
        'description': 'COMCAST',
        'amount': 40,
        'account_id': 'fake account id'
      },
      {
        'date': '2021-01-04',
        'description': 'EVERSOURCE ELECTRIC',
        'amount': 38.30,
        'account_id': 'fake account id'
      },
      {
        'date': '2021-01-04',
        'description': 'EVERSOURCE GAS',
        'amount': 18.09,
        'account_id': 'fake account id'
      },
      {
        'date': '2021-01-07',
        'description': 'Blue Bottle',
        'amount': 7.50,
        'account_id': 'yet another fake account id'
      },
      {
        'date': '2021-01-08',
        'description': 'VERIZON',
        'amount': 50,
        'account_id': 'fake account id'
      },
      {
        'date': '2021-01-01',
        'description': 'PROPERTY MANAGEMENT',
        'amount': 1000,
        'account_id': 'fake account id'
      }
    ]

    accounts_by_id = dict(list(map(lambda account: [account.plaid_account_id, account], bank.accounts)))
    discretionary_spending = SpendingPlanPart.query.filter_by(category="Discretionary Spending", user=user).first()

    for transaction_datum in transactions_data:
        date = transaction_datum['date']
        description = transaction_datum['description']
        amount = float(transaction_datum['amount']) * 100
        account = accounts_by_id[transaction_datum['account_id']]
        transaction = Transaction(
              date=date,
              description=description,
              amount=amount,
              account=account,
              spending_plan_part=discretionary_spending
        )
        db.session.add(transaction)
        db.session.commit()

    user.categorize_transactions('2021-01-01', '2021-01-23')
