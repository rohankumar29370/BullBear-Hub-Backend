from app.services.user_dao import get_all, create_user,delete_user
from app.services.portfolio_dao import get_portfolio_by_user, create_new
from app.services.investment_dao import get_investment_by_portfolio,purchase,sell
from termcolor import colored

def print_main_menu():
    print("Welcome to the Investment Management System")
    print("1. Users Menu")
    print("2. Portfolio Menu")
    print("3. Market Menu")
    print("0. Exit")

def print_user_menu():
    return ("""
    __________________
    USER MENU
    __________________
    1. View all users
    2. Add User
    3. Delete User
    0. Return to Main Menu
    __________________
    """)

def print_portfolio_menu():
    return ("""
    __________________
    PORTFOLIO MENU
    __________________
    1. View portfolio by user
    2. Add Portfolio
    0. Return to Main Menu
    __________________
    """)

def print_market_menu():
    return ("""
    __________________
    MARKET MENU
    __________________
    1. View investments by portfolio
    2. Purchase
    3. Sell
    0. Return to Main Menu
    __________________
    """)

def user_prompt():
    while(True):
        user_input = input(print_user_menu())
        if user_input == '1':
            users= get_all()
            if len(users) == 0:
                print(colored("No users found", 'red'))
            for user in users:
                print (colored(user, 'blue'))
        elif user_input == '2':
            username_input = input("Enter username: ")
            password_input = input("Enter password: ")
            balance_input = input("Enter balance: ")
            balance_input = float(balance_input)
            try:
                create_user(username_input, password_input, balance_input)
                print(colored(f"User {username_input} created successfully", 'green'))
            except Exception as e:
                print(colored(f"Error: {e}", 'red'))
        elif user_input == '3':
            user_id_input = input("Enter user ID to delete: ")
            try:
                delete_user(user_id_input)
                print(colored(f"User {user_id_input} deleted successfully", 'green'))
            except Exception as e:
                print(colored(f"Error: {e}", 'red'))
        elif user_input == '0':
            break 
        else:
            print(colored("Invalid input, please try again.", 'red'))

def portfolio_prompt():
    while(True):
        user_input = input(print_portfolio_menu())
        if user_input == '1':
            userid_input = input("Enter user ID to view portfolios: ")
            try:
                userid_input = int(userid_input)
                portfolios= get_portfolio_by_user(userid_input)
                if len(portfolios) == 0:
                    print(colored(f"No portfolios found for user ID {userid_input}", 'red'))
                for portfolio in portfolios:
                    print (colored(portfolio, 'blue'))
            except Exception as e:
                print(colored(f"Failed to get portfolios: {e}", 'red'))
        elif user_input == '2':
            userid_input = input("Enter user ID to add portfolio: ")
            name_input= input("Enter portfolio name: ")
            strategy_input= input("Enter portfolio strategy: ")
            try:
                 userid_input= int(userid_input)
                 create_new(name_input, strategy_input, userid_input)
                 print(colored(f"Portfolio {name_input} created successfully", 'green'))
            except Exception as e:
                print(colored(f"Failed to create portfolio: {e}", 'red'))
        elif user_input == '0':
            break
        else:
            print(colored("Invalid input, please try again.", 'red'))

def market_prompt(): 
    while(True):
        user_input = input(print_market_menu())
        if user_input == '1':
            portfolio_id_input = input("Enter portfolio ID to view investments: ")
            try:
                portfolio_id = int(portfolio_id_input)
                investments= get_investment_by_portfolio(portfolio_id)
                if len(investments) == 0:
                    print(colored(f"No investments found for portfolio ID {portfolio_id}", 'red'))
                for investment in investments:
                    print (colored(investment, 'blue'))
            except Exception as e:
                print(colored(f"Failed to get investments: {e}", 'red'))
        elif user_input == '2':
            portid_input = input("Enter Portfolio Id: ")
            ticker_input = input("Enter Ticker: ")
            price_input = input("Enter Price: ")
            qty_input = input("Enter Quantity: ")
            try:
                portid_input = int(portid_input)
                price_input = float(price_input)
                qty_input = int(qty_input)
                purchase(portid_input, ticker_input, price_input, qty_input)
                print(colored(f"Purchased {qty_input} of {ticker_input} at {price_input}", 'green'))
            except Exception as e:
                print(colored(f"Failed to purchase: {e}", 'red'))
        elif user_input == '3':
            investment_id_input = input("Enter Investment Id: ")
            qty_input = input("Enter Quantity: ")
            sale_price_input = input("Enter Sale Price: ")
            try:
                investment_id_input = int(investment_id_input)
                qty_input = int(qty_input)
                sale_price_input = float(sale_price_input)
                sell(investment_id_input, qty_input, sale_price_input)
                print(colored(f"Sold {qty_input} of investment ID {investment_id_input} at {sale_price_input}", 'green'))
            except Exception as e:
                print(colored(f"Failed to sell: {e}", 'red'))


        elif user_input == '0':
            break
        else:
            print(colored("Invalid input, please try again.", 'red'))



def run():
    while(True):
        user_input = input(print_main_menu())
        if user_input == '1':
            user_prompt()
        if user_input == '2':
            portfolio_prompt()
        if user_input == '3':
            market_prompt()  
        elif user_input == '0':
            break
        else:
            print(colored("Invalid input, please try again.", 'red'))
run()