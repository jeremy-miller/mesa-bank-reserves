import mesa


class Bank(mesa.Agent):
    def __init__(self, unique_id, model, reserve_percent):
        super().__init__(unique_id, model)
        self.reserve_percent = reserve_percent
        self.loan_total = 0
        self.deposits_total = 0
        self.reserves = self._calculate_reserves()
        self.available_loan_amount = 0

    def balance_bank(self):
        self.reserves = self._calculate_reserves()
        self.available_loan_amount = self.deposits_total - (self.reserves + self.loan_total)

    def _calculate_reserves(self):
        return (self.reserve_percent / 100) * self.deposits_total
