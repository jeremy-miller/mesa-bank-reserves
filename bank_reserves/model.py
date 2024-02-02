import mesa

from bank_reserves.bank import Bank
from bank_reserves.person import Person

LOAN_THRESHOLD = 10


def get_num_rich_people(model):
    rich_people = [
        person for person in model.schedule.agents if person.savings > model.rich_threshold
    ]
    return len(rich_people)


def get_num_middle_class_people(model):
    middle_class_people = [
        person
        for person in model.schedule.agents
        if person.loan_amount < LOAN_THRESHOLD and person.savings < model.rich_threshold
    ]
    return len(middle_class_people)


def get_num_poor_people(model):
    rich_people = [
        person for person in model.schedule.agents if person.loan_amount > LOAN_THRESHOLD
    ]
    return len(rich_people)


def get_total_savings(model):
    savings_amounts = [person.savings for person in model.schedule.agents]
    return sum(savings_amounts)


def get_total_wallet_sum(model):
    wallet_amounts = [person.wallet for person in model.schedule.agents]
    return sum(wallet_amounts)


def get_total_money(model):
    total_savings = get_total_savings(model)
    total_wallet_sum = get_total_wallet_sum(model)
    return total_savings + total_wallet_sum


def get_total_loans(model):
    loan_amounts = [person.loan_amount for person in model.schedule.agents]
    return sum(loan_amounts)


class BankReserves(mesa.Model):
    def __init__(
        self,
        width=20,
        height=20,
        initial_people=2,
        rich_threshold=10,
        bank_reserve_percent=50,
    ):
        super().__init__()
        self.width = width
        self.height = height
        self.initial_people = initial_people
        self.rich_threshold = rich_threshold
        self.bank_reserve_percent = bank_reserve_percent
        self.schedule = mesa.time.RandomActivation(self)
        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=True)
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Rich": get_num_rich_people,
                "Middle Class": get_num_middle_class_people,
                "Poor": get_num_poor_people,
                "Savings": get_total_savings,
                "Wallet Sum": get_total_wallet_sum,
                "Money": get_total_money,
                "Loans": get_total_loans,
            },
            agent_reporters={"Wealth": "wealth"},
        )
        self._initialize_agents()
        self.datacollector.collect(self)

    def _initialize_agents(self):
        self.bank = Bank(self.next_id(), self, self.bank_reserve_percent)

        for _ in range(self.initial_people):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            # all people share same bank in this simulation
            person = Person(self.next_id(), self, (x, y), self.bank, self.rich_threshold)
            self.grid.place_agent(person, (x, y))
            self.schedule.add(person)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
