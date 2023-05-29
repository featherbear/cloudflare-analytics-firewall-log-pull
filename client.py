import http.client
import json


headers = {
    'X-AUTH-EMAIL': "<EMAIL>",
    'Content-Type': "application/json",
    'Authorization': "Bearer <TOKEN>"
}
zone = "<ZONEID>"

####

f = open("output.json", "a+")
state = open("state.txt", "a+")
count = open("count.txt", "a+")

def saveState(newState: str):
    if not newState:
        return
    state.truncate(0)
    state.write(newState)


count.seek(0)
c = int(count.read())


def updateCount():
    global c
    count.truncate(0)
    count.write(str(c := c + 10000))


conn = http.client.HTTPSConnection("api.cloudflare.com")


def generatePayload(since: str = None):
    extra = [{"rayName_gt": since}] if since else []
    # https://developers.cloudflare.com/analytics/graphql-api/tutorials/querying-firewall-events/
    # https://developers.cloudflare.com/analytics/graphql-api/sampling/#access-to-raw-data
    return json.dumps(
        {
            "query": """
                query ActivityLogQuery(
                    $zoneTag: string
                    $activityFilter: ZoneFirewallEventsAdaptiveFilter_InputObject!
                    $limit: uint64!
                ) {
                    viewer {
                        zones(filter: { zoneTag: $zoneTag }) {
                            activity: firewallEventsAdaptive(
                                filter: $activityFilter,
                                limit: $limit

                                orderBy: [rayName_ASC]
                            ) {
                                time: datetime
                                
                                ip: clientIP
                                method: clientRequestHTTPMethodName
                                host: clientRequestHTTPHost
                                proto: clientRequestHTTPProtocol
                                path: clientRequestPath
                                query: clientRequestQuery
                                userAgent
                                # 				__typename
                                rayName
                            }
                        }
                    }
                }
            """,
            "operationName": "ActivityLogQuery",
            "variables": {
                "zoneTag": zone,
                "limit": 10000,
                "activityFilter": {
                    "AND": [
                        {
                            "datetime_geq": "2023-04-18T08:27:18.740Z"
                        }, *extra
                    ]
                }
            }
        }

    )

def fetch(since: str = None):
    conn.request("POST", "/client/v4/graphql", generatePayload(since), headers)
    body = json.loads(conn.getresponse().read())
    data = body["data"]["viewer"]["zones"][0]["activity"]
    f.write(json.dumps(data) + ",")
    if len(data) == 0:
        print("DONE")
        return
    return data[-1]["rayName"]


state.seek(0)
last = state.read()

while True:
    saveState(last)
    last = fetch(last)
    if not last:
        break
    updateCount()
    print(last, c)
