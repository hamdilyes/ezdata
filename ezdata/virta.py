from datetime import datetime, timezone
import requests
# __API_URI_PROD__ = "https://api.virta.global/customer"
# __API_URI_TEST__ = "https://api.test.virta.global/customer"

__API_URI_PROD__ = "https://api.virta.fi"
__API_URI_TEST__ = "https://api.test.virta-ev.com"

__VERSION__ = "v4"

ENTITY_MAP = {
    "prod": __API_URI_PROD__,
    "test": __API_URI_TEST__,
}


def status(token=None, entity="prod"):

    url = __build_url("stations/status", entity=entity)
    headers = {"authorization": "Bearer {}".format(token)}
    url += "?latMin=0.526487&latMax=23.869931&longMin=-81.390376&longMax=-48.850960&privilegedStations=0&includePoi=1"
    payload = {}

    # response = requests.request("GET", url, data=payload)
    response = requests.get(url, headers=headers, data=payload)

    date_str = response.headers["Date"]
    date_t = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %Z").astimezone(
        timezone.utc
    )
    # print(dt.isoformat())

    status_target_lst = []
    if response.status_code == requests.codes.ok:

        status_target_lst = response.json()
        for idx, status in enumerate(status_target_lst):

            print("- ", idx, status)
        #     status_target_lst.append(status)
    else:
        print(
            "Station status GET request: {}, URL: {}, Status: {}, JSON: {}".format(
                response.headers, response.url, response.status_code, response.json()
            )
        )

    return date_t, status_target_lst


def __build_url(endpoint, entity="test"):
    url = "/".join([ENTITY_MAP[entity], __VERSION__, endpoint])
    print("Build URL:", url)

    return url


if __name__ == "__main__":
    print("Ilyes")
    status()
