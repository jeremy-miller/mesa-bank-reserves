import mesa


class Person(mesa.Agent):
    def __init__(self, unique_id, model, pos, bank, rich_threshold):
        super().__init__(unique_id, model)
        self.pos = pos
        self.bank = bank
        self.savings = 0
        self.loan_amount = 0
        self.wallet = self.random.randint(1, rich_threshold + 1)
        self.wealth = 0  # savings - loan_amount
        self.customer = 0  # person to trade with

    def step(self):
        self._move()
        self._trade()
        self._balance_books()
        self.bank.balance_bank()

    def _move(self):
        next_moves = self.model.grid.get_neighborhood(self.pos, True, True)
        next_move = self.random.choice(next_moves)
        self.model.grid.move_agent(self, next_move)

    def _trade(self):
        if self.savings > 0 or self.wallet > 0 or self.bank.available_loan_amount > 0:
            customers_at_my_cell = self.model.grid.get_cell_list_contents([self.pos])
            if len(customers_at_my_cell) > 1:  # list includes self
                customer = self
                while customer == self:
                    # select a random customer that's not self
                    customer = self.random.choice(customers_at_my_cell)
                if self.random.randint(0, 1) == 1:  # 50% chance of trading with customer
                    if self.random.randint(0, 1) == 1:  # 50% chance of trading $5
                        customer.wallet += 5
                        self.wallet -= 5
                    else:  # 50% chance of trading $2
                        customer.wallet += 2
                        self.wallet -= 2

    def _balance_books(self):
        if self.wallet < 0:
            if self.savings >= -self.wallet:
                # check if savings can cover negative wallet balance
                self._withdraw_from_savings(-self.wallet)
            else:
                # savings can't completely cover negative wallet balance
                if self.savings > 0:
                    # withdraw all savings to reduce negative wallet balance
                    self._withdraw_from_savings(self.savings)
                available_loan_amount = self.bank.available_loan_amount
                if available_loan_amount >= -self.wallet:
                    # bank can loan enough to cover negative wallet balance
                    self._take_out_loan(-self.wallet)
                else:
                    # take out loan to cover some of my negative wallet balance
                    self._take_out_loan(available_loan_amount)
        else:
            self._deposit_to_savings(self.wallet)

        if self.loan_amount > 0 and self.savings > 0:
            if self.savings >= self.loan_amount:
                # payoff full loan with savings
                self._withdraw_from_savings(self.loan_amount)
                self._repay_loan(self.loan_amount)
            else:
                # payoff part of loan with savings
                self._withdraw_from_savings(self.savings)
                self._repay_loan(self.wallet)

        self.wealth = self.savings - self.loan_amount

    def _withdraw_from_savings(self, amount):
        self.savings -= amount
        self.wallet += amount
        self.bank.deposits_total -= amount

    def _deposit_to_savings(self, amount):
        self.wallet -= amount
        self.savings += amount
        self.bank.deposits_total += amount

    def _take_out_loan(self, amount):
        self.loan_amount += amount
        self.wallet += amount
        self.bank.available_loan_amount -= amount
        self.bank.loan_total += amount

    def _repay_loan(self, amount):
        self.loan_amount -= amount
        self.wallet -= amount
        self.bank.available_loan_amount += amount
        self.bank.loan_total -= amount
