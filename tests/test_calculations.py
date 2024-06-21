import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds

# Parametrized test for the add function
@pytest.mark.parametrize("num1, num2, expected", [
    (2, 2, 4),
    (8, 2, 10),
    (12, 2, 14),
    (14, 2, 16)])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected 

# Simple test for the subtract function
def test_subtract():
    assert subtract(5, 3) == 2

# Simple test for the multiply function
def test_multiply():
    assert multiply(5, 3) == 15

# Simple test for the divide function
def test_divide():
    assert divide(5, 3) == 1.6666666666666667

# Test initializing a BankAccount with a specific amount
def test_bank_set_initial_amount():
    bank_account = BankAccount(50)
    assert bank_account.balance == 50

# Test initializing a BankAccount with the default amount (zero)
def test_bank_default_amount():
    bank_account = BankAccount()
    assert bank_account.balance == 0

# Fixture to create a bank account with a default balance of 50
@pytest.fixture
def bank_account():
    return BankAccount(50)

# Test withdrawing an amount from the bank account
def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30

# Test withdrawing an amount from the bank account
def test_withdraw2(bank_account):
    bank_account.withdraw(60)
    assert bank_account.balance == 30

# Test withdrawing an amount that leaves a balance of 10
def test_withdraw_not_enough(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(60)

# Test depositing an amount into the bank account
def test_deposit(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80

# Test collecting interest on the bank account
def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55

# Fixture to create a bank account with a zero balance
@pytest.fixture
def zero_bank_account():
    print("creating empty bank account")
    return BankAccount()

# Parametrized test for multiple bank transactions
@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000)])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

# Test withdrawing an amount that exceeds the balance and raises an InsufficientFunds exception
def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)
