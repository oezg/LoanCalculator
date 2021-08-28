import math
import argparse


def error_message():
    print("Incorrect parameters")


def calculate_overpayment(periods, payment, principal):
    overpayment = periods * payment - principal
    print("Overpayment =", overpayment)


def calculate_periods(payment, principal, interest):
    periods = math.ceil(math.log(payment/(payment-interest*principal), 1+interest))
    if periods // 12 == 0:
        if periods == 1:
            print("\nIt will take 1 month to repay the loan!")
        else:
            print("\nIt will take {0} months to repay the loan!".format(periods))
    elif periods // 12 == 1:
        if periods % 12 == 0:
            print("\nIt will take 1 year to repay this loan!")
        elif periods % 12 == 1:
            print("\nIt will take 1 year and 1 month to repay this loan!")
        else:
            print("\nIt will take 1 year and {0} months to repay this loan!".format(periods % 12))
    else:
        if periods % 12 == 0:
            print("\nIt will take {0} years to repay this loan!".format(periods // 12))
        elif periods % 12 == 1:
            print("\nIt will take {0} years and 1 month to repay this loan!".format(periods // 12))
        else:
            print("\nIt will take {0} years and {1} months to repay this loan!".format(periods // 12, periods % 12))
    calculate_overpayment(periods=periods, payment=payment, principal=principal)


def calculate_payment(periods, principal, interest):
    payment = math.ceil(principal * (interest * (1 + interest) ** periods) / ((1 + interest) ** periods - 1))
    print("Your monthly payment = {}!".format(payment))
    calculate_overpayment(periods=periods, payment=payment, principal=principal)


def calculate_principal(periods, payment, interest):
    principal = math.ceil(payment / ((interest * (interest + 1) ** periods) / ((1 + interest) ** periods - 1)))
    print("Your loan principal = {}!".format(principal))
    calculate_overpayment(periods=periods, payment=payment, principal=principal)


def calculate_differentiated(n, p, i):
    d = []
    for m in range(n):
        d.append(math.ceil(p / n + i * (p - p * m / n)))
        print("Month {0}: payment is {1}".format(m+1, d[m]))
    print()
    overpayment = sum(d) - p
    print("Overpayment =", overpayment)


parser = argparse.ArgumentParser(description="This program calculates the differentiated payment of a loan")

parser.add_argument("--type", choices=["annuity", "diff"])
parser.add_argument("--payment")
parser.add_argument("--principal")
parser.add_argument("--periods")
parser.add_argument("--interest")

args = parser.parse_args()

if args.type == "diff" and args.principal and args.periods and args.interest and not args.payment:
    principal = int(args.principal)
    periods = int(args.periods)
    interest = float(args.interest) / 1200
    if principal > 0 and periods > 0 and interest >= 0:
        calculate_differentiated(n=periods, p=principal, i=interest)
    else:
        error_message()

elif args.type == "annuity" and args.interest:
    interest = float(args.interest) / 1200
    if interest < 0:
        error_message()

    # we look for the number of periods
    elif args.payment and args.principal and not args.periods:
        payment = float(args.payment)
        principal = int(args.principal)
        if payment > 0 and principal > 0:
            calculate_periods(payment=payment, principal=principal, interest=interest)
        else:
            error_message()

    # we look for the amount of monthly payments
    elif args.periods and args.principal and not args.payment:
        periods = int(args.periods)
        principal = int(args.principal)
        if periods > 0 and principal > 0:
            calculate_payment(periods=periods, principal=principal, interest=interest)
        else:
            error_message()

    # we look for the principal amount
    elif args.payment and args.periods and not args.principal:
        payment = float(args.payment)
        periods = int(args.periods)
        if payment > 0 and periods > 0:
            calculate_principal(periods=periods, payment=payment, interest=interest)
        else:
            error_message()
    else:
        error_message()
else:
    error_message()
