import logging

from requests import get

from ..models import Assets, AssetsValues


logger = logging.getLogger(__name__)


def get_history_values():
    values = AssetsValues.objects.all().order_by("-created_dt")

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


def insert_assets():
    companies = get_all_companies()
    for company in companies:
        try:
            asset = Assets.objects.create(
                name = company["nm_empresa"],
                ticker = company["cd_acao"]
            )
            asset.save()

        except Exception:
            logger.error(
                "Something went when trying to insert a company. Maybe the company is already in database.")
