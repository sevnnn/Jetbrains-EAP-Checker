import requests
from datetime import datetime, timedelta

API_URL_TO_SPRINTF = "https://data.services.jetbrains.com/products?code=%s&release.type=eap&fields=name,releases"
JETBRAINS_APPS_MAP = {
    "Integrated Development Environments (IDEs)": [
        "IIU",
        "CL",
        "DG",
        "DS",
        "GO",
        "PS",
        "PY",
        "RM",
        "WS",
    ],
    ".NET and Visual Studio": [
        "RSU",
        "RD",
    ],
    "Toolbox": [
        "TBA",
    ],
    "Remote development": [
        "GW",
    ],
}


def get_eap_status(app_code: str) -> dict[str, int]:
    json_response = requests.get(API_URL_TO_SPRINTF % app_code).json()[0]

    try:
        last_release = json_response["releases"][0]
    except IndexError:
        return {json_response["name"]: 0}

    last_release_expire_date = datetime.strptime(
        last_release["date"], "%Y-%m-%d"
    ) + timedelta(days=30)

    if last_release_expire_date.date() < datetime.now().date():
        return {json_response["name"]: 0}

    return {
        json_response["name"]: (
            last_release_expire_date.date() - datetime.now().date()
        ).days
    }


def pretty_print_eap_statuses(eap_statuses: dict[str, int], title: str) -> None:
    max_key_length = len(max(eap_statuses.keys(), key=len))
    print(title)
    for app_name, days_left in eap_statuses.items():
        padding_spaces = " " * (max_key_length - len(app_name))
        print(
            " | ".join(
                [
                    "   " + app_name + padding_spaces,
                    "Not available"
                    if days_left == 0
                    else f"Available for {days_left} more days",
                ]
            )
        )
    print()


def main() -> None:
    for category, app_codes in JETBRAINS_APPS_MAP.items():
        category_statuses = {}
        for code in app_codes:
            category_statuses |= get_eap_status(code)
        pretty_print_eap_statuses(category_statuses, category)

    print("Download here:")
    print("   https://www.jetbrains.com/resources/eap")


if __name__ == "__main__":
    main()
