from flask import Flask, render_template, request
from dataclasses import dataclass

app = Flask(__name__)
YEAR = 12


@dataclass
class InvestmentParameters:
    initial_deposit: float = 0.0
    monthly_deposit: float = 0.0
    saving_months: int = 0
    interest_rate: float = 0.0


def interest_rate_formula(params: InvestmentParameters) -> tuple:
    interest_rate: float = params.interest_rate / 100
    initial_deposit: float = params.initial_deposit
    monthly_deposit: float = params.monthly_deposit
    saving_months: int = params.saving_months
    total_deposit: float = initial_deposit
    total_profit: float = 0.0
    total_tax: float = 0.0

    for _ in range(saving_months):
        profit: float = initial_deposit * interest_rate / YEAR
        tax: float = profit * 0.19
        profit -= tax
        initial_deposit += profit + monthly_deposit
        total_profit += profit
        total_tax += tax
        total_deposit += monthly_deposit

    return total_profit, total_tax, initial_deposit, total_deposit


@dataclass
class ExpenseParameters:
    bills: float = 0.0
    rent: float = 0.0
    loan: float = 0.0
    food: float = 0.0
    transport: float = 0.0
    health: float = 0.0
    education: float = 0.0
    entertainment: float = 0.0
    income: float = 0.0
    months: float = 0.0


def expenses(params: ExpenseParameters) -> tuple:
    bills_result: float = params.bills * params.months / YEAR
    rent_result: float = params.rent * params.months / YEAR
    loan_result: float = params.loan * params.months / YEAR
    food_result: float = params.food * params.months / YEAR
    transport_result: float = params.transport * params.months / YEAR
    health_result: float = params.health * params.months / YEAR
    education_result: float = params.education * params.months / YEAR
    entertainment_result: float = params.entertainment * params.months / YEAR
    income_result: float = params.income * params.months / YEAR

    total_expenses: float = (
        bills_result
        + rent_result
        + loan_result
        + food_result
        + transport_result
        + health_result
        + education_result
        + entertainment_result
    )
    difference: float = income_result - total_expenses

    return (
        bills_result,
        rent_result,
        loan_result,
        food_result,
        transport_result,
        health_result,
        education_result,
        entertainment_result,
        income_result,
        difference,
    )


@dataclass
class PropertyParameters:
    property_cost: float = 0.0
    monthly_loan_payment: float = 0.0
    loan_term_months: int = 0
    rent: float = 0.0
    taxes: float = 0.0
    insurance: float = 0.0
    management_costs: float = 0.0
    maintenance_costs: float = 0.0


def property_formula(params: PropertyParameters) -> tuple:
    investment_return_time: int = 0
    current_return: float = 0.0
    loan_under_year: float = params.monthly_loan_payment * params.loan_term_months

    annual_difference: float = (
        params.rent
        - (
            params.taxes
            + params.insurance
            + params.maintenance_costs
            + params.management_costs
        )
    ) * YEAR

    if params.loan_term_months > 12:
        annual_difference_incl_loan: float = (
            params.rent
            - (
                params.taxes
                + params.insurance
                + params.maintenance_costs
                + params.management_costs
                + params.monthly_loan_payment
            )
        ) * YEAR
    else:
        annual_difference_incl_loan: float = (
            params.rent
            - (
                params.taxes
                + params.insurance
                + params.maintenance_costs
                + params.management_costs
            )
        ) * YEAR - loan_under_year

    annual_profit: float = params.rent * YEAR
    annual_costs: float = (
        params.taxes
        + params.insurance
        + params.maintenance_costs
        + params.management_costs
        + params.monthly_loan_payment
    ) * YEAR

    loan_term_remaining: int = params.loan_term_months

    while params.property_cost > current_return and investment_return_time <= 999:
        if loan_term_remaining > 0:
            monthly_profit: float = params.rent - (
                params.taxes
                + params.insurance
                + params.maintenance_costs
                + params.management_costs
                + params.monthly_loan_payment
            )
            loan_term_remaining -= 1
        else:
            monthly_profit: float = params.rent - (
                params.taxes
                + params.insurance
                + params.maintenance_costs
                + params.management_costs
            )
        current_return += monthly_profit
        investment_return_time += 1

    if investment_return_time > 999:
        investment_return_time = float("nan")

    return (
        annual_difference,
        annual_difference_incl_loan,
        annual_profit,
        annual_costs,
        investment_return_time,
    )


@app.route("/")
def home() -> str:
    return render_template("index.html")


@app.route("/interest_rate", methods=["GET", "POST"])
def interest_rate() -> str:
    results: dict = {}
    if request.method == "POST":
        initial_deposit = request.form.get("initial_deposit")
        monthly_deposit = request.form.get("monthly_deposit")
        saving_years = request.form.get("saving_years")
        saving_months = request.form.get("saving_months")
        interest_rate = request.form.get("interest_rate")
        try:
            investment_params: InvestmentParameters = InvestmentParameters(
                initial_deposit=float(initial_deposit or 0),
                monthly_deposit=float(monthly_deposit or 0),
                saving_months=int(
                    saving_months or int(float(saving_years or 0) * YEAR)
                ),
                interest_rate=float(interest_rate or 0),
            )
        except ValueError:
            results["error"] = "Provided values must be numbers."
            return render_template("interest_rate.html", results=results)
        (
            total_profit,
            total_tax,
            final_sum,
            total_deposit,
        ) = interest_rate_formula(investment_params)
        results = {
            "initial_deposit": round(investment_params.initial_deposit),
            "monthly_deposit": round(investment_params.monthly_deposit),
            "saving_years": round(float(saving_years or 0)),
            "saving_months": round(investment_params.saving_months),
            "interest_rate": round(investment_params.interest_rate),
            "total_deposit": round(total_deposit),
            "total_profit": round(total_profit, 2),
            "total_tax": round(total_tax, 2),
            "final_sum": round(final_sum, 2),
        }
    return render_template("interest_rate.html", results=results)


@app.route("/total", methods=["GET", "POST"])
def total() -> str:
    results: dict = {}
    if request.method == "POST":
        bills = request.form.get("bills")
        rent = request.form.get("rent")
        loan = request.form.get("loan")
        food = request.form.get("food")
        transport = request.form.get("transport")
        health = request.form.get("health")
        education = request.form.get("education")
        entertainment = request.form.get("entertainment")
        income = request.form.get("income")
        years = request.form.get("years")
        months = request.form.get("months")
        try:
            expense_params: ExpenseParameters = ExpenseParameters(
                bills=float(bills or 0),
                rent=float(rent or 0),
                loan=float(loan or 0),
                food=float(food or 0),
                transport=float(transport or 0),
                health=float(health or 0),
                education=float(education or 0),
                entertainment=float(entertainment or 0),
                income=float(income or 0),
                months=float(months or (float(years or 0) * YEAR)),
            )
        except ValueError:
            results["error"] = "Provided values must be numbers."
            return render_template("total.html", results=results)
        (
            bills_result,
            rent_result,
            loan_result,
            food_result,
            transport_result,
            health_result,
            education_result,
            entertainment_result,
            income_result,
            difference,
        ) = expenses(expense_params)
        results = {
            "bills": round(expense_params.bills),
            "rent": round(expense_params.rent),
            "loan": round(expense_params.loan),
            "food": round(expense_params.food),
            "transport": round(expense_params.transport),
            "health": round(expense_params.health),
            "education": round(expense_params.education),
            "entertainment": round(expense_params.entertainment),
            "income": round(expense_params.income),
            "years": round(float(years or 0)),
            "months": round(expense_params.months),
            "bills_result": round(bills_result, 2),
            "rent_result": round(rent_result, 2),
            "loan_result": round(loan_result, 2),
            "food_result": round(food_result, 2),
            "transport_result": round(transport_result, 2),
            "health_result": round(health_result, 2),
            "education_result": round(education_result, 2),
            "entertainment_result": round(entertainment_result, 2),
            "income_result": round(income_result, 2),
            "difference": round(difference, 2),
        }
    return render_template("total.html", results=results)


@app.route("/property", methods=["GET", "POST"])
def property() -> str:
    results: dict = {}
    if request.method == "POST":
        property_cost = request.form.get("property_cost")
        monthly_loan_payment = request.form.get("monthly_loan_payment")
        loan_term_months = request.form.get("loan_term_months")
        rental_income = request.form.get("rental_income")
        taxes = request.form.get("taxes")
        insurance = request.form.get("insurance")
        management_costs = request.form.get("management_costs")
        maintenance_costs = request.form.get("maintenance_costs")
        try:
            property_params: PropertyParameters = PropertyParameters(
                property_cost=float(property_cost or 0),
                monthly_loan_payment=float(monthly_loan_payment or 0),
                loan_term_months=int(loan_term_months or 0),
                rent=float(rental_income or 0),
                taxes=float(taxes or 0),
                insurance=float(insurance or 0),
                management_costs=float(management_costs or 0),
                maintenance_costs=float(maintenance_costs or 0),
            )
        except ValueError:
            results["error"] = "Provided values must be numbers."
            return render_template("property.html", results=results)
        (
            annual_difference,
            annual_difference_incl_loan,
            annual_profit,
            annual_costs,
            investment_return_time,
        ) = property_formula(property_params)
        results = {
            "property_cost": round(property_params.property_cost),
            "monthly_loan_payment": round(property_params.monthly_loan_payment),
            "loan_term_months": round(property_params.loan_term_months),
            "rental_income": round(property_params.rent),
            "taxes": round(property_params.taxes),
            "insurance": round(property_params.insurance),
            "management_costs": round(property_params.management_costs),
            "maintenance_costs": round(property_params.maintenance_costs),
            "annual_difference": round(annual_difference),
            "annual_difference_incl_loan": round(annual_difference_incl_loan),
            "annual_profit": round(annual_profit),
            "annual_costs": round(annual_costs),
            "investment_return_time": (
                round(investment_return_time, 2)
                if not investment_return_time != investment_return_time
                else "N/A"
            ),
        }
        return render_template("property.html", results=results)
    return render_template("property.html", results=None)


if __name__ == "__main__":
    app.run(debug=True)
