print("Dollars and sense")


class Mortage:
    def __init__(self):
        self.start_balance = 180_000
        self.mortgage_interest = 0.0275
        self.monthly_payment = 851.44 + 402.73
        self.earnings_interest = 0.060

    def dont_pay_off(self, lump_sum):
        brokerage_value = lump_sum
        balance = self.start_balance

        month = 0
        yr = 0
        total_interest_paid = 0.0
        while balance > 0:
            interest = balance * self.mortgage_interest / 12.0
            total_interest_paid += interest
            principle_payment = self.monthly_payment - interest
            balance -= principle_payment

            brokerage_value *= (1 + self.earnings_interest / 12.0)

            month += 1
            yr = month // 12
            # print(f"year: {yr}, month: {month}, balance: {balance}, brokerage value:{brokerage_value}")

        # Don't pay off the mortgage, just pay normal monthly payments and
        # invest the lump sum in a brokerage account
        print("Don't pay off, invest lump sum")
        print(f"year: {yr}, month: {month - 12 * yr}, brokerage value:{brokerage_value}")
        print(f"Total interest_paid: {total_interest_paid}, brokerage_gain:{brokerage_value - lump_sum}")
        print(f"Value: paid of house + {brokerage_value - total_interest_paid}")

    def pay_off(self, lump_sum):
        brokerage_value = lump_sum
        balance = self.start_balance

        # Pay off mortgage
        reduced_balance = balance - brokerage_value
        brokerage_value = 0.0

        month = 0
        yr = 0
        total_interest_paid = 0.0
        while balance > 0:
            # Run unreduced balance so simulation continues for same amount of time
            interest = balance * self.mortgage_interest / 12.0
            principle_payment = self.monthly_payment - interest
            balance -= principle_payment

            if reduced_balance > 0.0:
                # continue to pay down
                actual_interest = reduced_balance * self.mortgage_interest / 12.0
                principle_payment = self.monthly_payment - actual_interest
                total_interest_paid += actual_interest
                reduced_balance -= principle_payment
            else:
                # Apply mortgage to brokerage account
                brokerage_value += self.monthly_payment

            brokerage_value *= (1 + self.earnings_interest / 12.0)

            month += 1
            yr = month // 12
            # print(f"year: {yr}, month: {month}, balance: {balance}, brokerage value:{brokerage_value}")

        # Use the lump sum to pay down the mortgage and after it is paid off
        # put the monthly payment into the brokerage account
        print("\nPay off, invest mortgage ofter its paid")
        print(f"year: {yr}, month: {month - 12 * yr}, brokerage value:{brokerage_value}")
        print(f"Total interest_paid: {total_interest_paid}, brokerage_gain:{brokerage_value - lump_sum}")
        print(f"Value: paid of house + {brokerage_value - total_interest_paid}")


    def use_brokerage_to_pay_mortgage(self, lump_sum):
        brokerage_value = lump_sum
        balance = self.start_balance
        reduced_monthly_payment = 1254.17
        reduced_monthly_payment = 1000.00

        month = 0
        yr = 0
        total_interest_paid = 0.0
        while balance > 0:
            interest = balance * self.mortgage_interest / 12.0
            total_interest_paid += interest
            principle_payment = self.monthly_payment - interest
            balance -= principle_payment

            if brokerage_value < 0.0:
                print(f"Ran out of money to pay mortgage yr:{yr}, mo:{month}")
            else:
                # Pay mortgage from brokerage
                brokerage_value -= self.monthly_payment

            brokerage_value += reduced_monthly_payment
            brokerage_value *= (1 + self.earnings_interest / 12.0)

            month += 1
            yr = month // 12
            # print(f"year: {yr}, month: {month}, balance: {balance}, brokerage value:{brokerage_value}")

        # don't pay off the mortgage, invest the lump sum in a brokerage account
        # and use the brokerage account to help reduce monthly payments.
        # NOTE: the savings in monthly payments don't earn any interest!
        # NOTE: if the reduced monthly is the same as the monthly, this degenerates to the don't payoff case
        saved_monthly = (self.monthly_payment - reduced_monthly_payment) * month
        print("\nDon't pay off, use brokerage to pay mortgage and reduced monthly goes to brokerage")
        print(f"month goes from {self.monthly_payment} down to {reduced_monthly_payment}")
        print(f"year: {yr}, month: {month - 12 * yr}, brokerage value:{brokerage_value}")
        print(f"Total interest_paid: {total_interest_paid}, brokerage_gain:{brokerage_value - lump_sum}")
        value = brokerage_value - total_interest_paid + saved_monthly
        print(f"Value: paid of house + {value}")


if __name__ == "__main__":
    m = Mortage()
    m.dont_pay_off(70000)
    m.pay_off(70000)
    m.use_brokerage_to_pay_mortgage(70000)
