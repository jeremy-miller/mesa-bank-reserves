import mesa

from bank_reserves.model import BankReserves
from bank_reserves.person import Person

GRID_WIDTH = 20
GRID_HEIGHT = 20
CANVAS_WIDTH = 500
CANVAS_HEIGHT = 500

RICH_COLOR = "#2ca02c"
MIDDLE_CLASS_COLOR = "#1f77b4"
POOR_COLOR = "#d62728"


def person_portrayal(agent):
    if not agent or not isinstance(agent, Person):
        return

    portrayal = {
        "Shape": "circle",
        "r": 0.5,
        "Layer": 0,
        "Filled": True,
    }

    color = MIDDLE_CLASS_COLOR
    if agent.savings > agent.model.rich_threshold:
        color = RICH_COLOR
    if agent.savings < 10 and agent.loan_amount < 10:
        color = MIDDLE_CLASS_COLOR
    if agent.loan_amount > 10:
        color = POOR_COLOR
    portrayal["Color"] = color

    return portrayal


canvas_element = mesa.visualization.CanvasGrid(
    person_portrayal, GRID_WIDTH, GRID_HEIGHT, CANVAS_WIDTH, CANVAS_HEIGHT
)

line_chart = mesa.visualization.ChartModule(
    [
        {"Label": "Rich", "Color": RICH_COLOR},
        {"Label": "Middle Class", "Color": MIDDLE_CLASS_COLOR},
        {"Label": "Poor", "Color": POOR_COLOR},
    ]
)

model_bar = mesa.visualization.BarChartModule(
    [
        {"Label": "Rich", "Color": RICH_COLOR},
        {"Label": "Middle Class", "Color": MIDDLE_CLASS_COLOR},
        {"Label": "Poor", "Color": POOR_COLOR},
    ]
)

agent_bar = mesa.visualization.BarChartModule(
    [{"Label": "Wealth", "Color": MIDDLE_CLASS_COLOR}],
    scope="agent",
    sorting="ascending",
    sort_by="Wealth",
)

pie_chart = mesa.visualization.PieChartModule(
    [
        {"Label": "Rich", "Color": RICH_COLOR},
        {"Label": "Middle Class", "Color": MIDDLE_CLASS_COLOR},
        {"Label": "Poor", "Color": POOR_COLOR},
    ]
)


model_params = {
    "width": GRID_WIDTH,
    "height": GRID_HEIGHT,
    "initial_people": mesa.visualization.Slider(
        "People", 25, 1, 200, description="Initial Number of People"
    ),
    "rich_threshold": mesa.visualization.Slider(
        "Rich Threshold",
        10,
        1,
        20,
        description="Max Initial Wallet Amount",
    ),
    "bank_reserve_percent": mesa.visualization.Slider(
        "Reserves",
        50,
        1,
        100,
        description="Percent of deposits the bank has to hold in reserve",
    ),
}

server = mesa.visualization.ModularServer(
    BankReserves,
    [canvas_element, line_chart, model_bar, agent_bar, pie_chart],
    "Bank Reserves Model",
    model_params=model_params,
)
