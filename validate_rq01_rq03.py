"""
Validação dos campos RQ01–RQ03 em amostra de 5 repositórios.
Consulta a API GraphQL e compara com os valores do CSV.
"""
import csv
from src.github import graphql_request

SAMPLE = [
    "codecrafters-io/build-your-own-x",
    "sindresorhus/awesome",
    "freeCodeCamp/freeCodeCamp",
    "donnemartin/system-design-primer",
    "jwasham/coding-interview-university",
]

QUERY = """
query ValidateRepos {
  r0: repository(owner: "codecrafters-io", name: "build-your-own-x") {
    createdAt
    pullRequests(states: MERGED) { totalCount }
    releases { totalCount }
  }
  r1: repository(owner: "sindresorhus", name: "awesome") {
    createdAt
    pullRequests(states: MERGED) { totalCount }
    releases { totalCount }
  }
  r2: repository(owner: "freeCodeCamp", name: "freeCodeCamp") {
    createdAt
    pullRequests(states: MERGED) { totalCount }
    releases { totalCount }
  }
  r3: repository(owner: "donnemartin", name: "system-design-primer") {
    createdAt
    pullRequests(states: MERGED) { totalCount }
    releases { totalCount }
  }
  r4: repository(owner: "jwasham", name: "coding-interview-university") {
    createdAt
    pullRequests(states: MERGED) { totalCount }
    releases { totalCount }
  }
  rateLimit { cost remaining }
}
"""

# Carrega CSV
csv_data = {}
with open("data/repositories.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row["name"] in SAMPLE:
            csv_data[row["name"]] = row

# Consulta API
result = graphql_request(QUERY)
data = result["data"]

api_data = {
    SAMPLE[0]: data["r0"],
    SAMPLE[1]: data["r1"],
    SAMPLE[2]: data["r2"],
    SAMPLE[3]: data["r3"],
    SAMPLE[4]: data["r4"],
}

print(f"{'Repositório':<48} {'Campo':<15} {'CSV':>8}  {'API':>8}  {'OK?'}")
print("-" * 90)

all_ok = True
for name in SAMPLE:
    csv_row = csv_data.get(name, {})
    api_row = api_data[name]

    checks = [
        ("created_at", csv_row.get("created_at", "")[:10], api_row["createdAt"][:10]),
        ("merged_prs",  csv_row.get("merged_prs", ""),      str(api_row["pullRequests"]["totalCount"])),
        ("releases",    csv_row.get("releases", ""),         str(api_row["releases"]["totalCount"])),
    ]

    for field, csv_val, api_val in checks:
        ok = "OK" if str(csv_val) == str(api_val) else "DIVERGE"
        if ok != "OK":
            all_ok = False
        print(f"{name:<48} {field:<15} {csv_val:>8}  {api_val:>8}  {ok}")

print()
print("rateLimit cost:", data["rateLimit"]["cost"])
print("Resultado:", "TODOS OK" if all_ok else "HA DIVERGENCIAS")
