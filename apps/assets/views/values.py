import logging

from requests import get
from django.contrib.auth.models import User

from emails.views import send_email
from emails.template import template
from ..models import AssetsValues, AssetsConfig

logger = logging.getLogger(__name__)


def insert_history_value(asset, user):
    price = get_price(asset.ticker)
    if price:
        value = int(str(price["vl_fechamento"]).replace('.', ""))

        history_value = AssetsValues.objects.create(
            asset_id=asset,
            user_id=user,
            value=value
        )

        history_value.save()

        return history_value


def get_history_values(request):
    user = User.objects.get(pk=request.user.id)

    values = AssetsValues.objects.filter(user_id=user.id).order_by("-created_dt")

    for value in values:
        value.value = f"{(value.value)/100:.2f}"

    return values


def get_all_companies():
    try:
        companies = get(
            url="https://api-cotacao-b3.labdo.it/api/empresa"
        )

        return companies.json()
    except Exception:
        logger.exception(
            "Something went wrong when trying to get all companies")
        return []


def get_price(ticker):
    try:
        prices = get(
            url=f"https://api-cotacao-b3.labdo.it/api/cotacao/cd_acao/{ticker}"
        )

        last_price = prices.json()[0]

        return last_price
    except Exception:
        logger.exception(
            f"Something went wrong when trying to get price from {ticker}")
        return {}


def check_price(asset_config: AssetsConfig):
    history_value = insert_history_value(
        asset_config.asset_id, asset_config.user_id)

    if asset_config.min_value >= history_value.value:
        new_template = template.replace("{%OPORTUNITY%}", "Buy Opportunity").replace(
            "{%TICKER%}", asset_config.asset_id.ticker).replace("{%TEXT%}", f"This is the momment to buy a {asset_config.asset_id.ticker}. It's value is {history_value.value}")

        send_email(asset_config.user_id.email, "Buy Opportunity", new_template)

    if history_value.value >= asset_config.max_value:
        new_template = template.replace("{%OPORTUNITY%}", "Sell Opportunity").replace(
            "{%TICKER%}", asset_config.asset_id.ticker).replace("{%TEXT%}", f"This is the momment to sell a {asset_config.asset_id.ticker}. It's value is {history_value.value}")

        send_email(asset_config.user_id.email, "Sell Opportunity", new_template)
