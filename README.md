# Global GDP Comparison API

Compare GDP and economic indicators across the world's top economies — powered by World Bank Open Data.

**Live API:** https://global-gdp-api.vercel.app
**RapidAPI:** [Subscribe on RapidAPI](#)

---

## Endpoints

| Endpoint | Description | Default Limit | Max Limit |
|---|---|---|---|
| `GET /` | API info and available endpoints | — | — |
| `GET /summary` | Latest GDP & economic indicators for World aggregate | 1 | 30 |
| `GET /gdp` | GDP (current US$) for top economies | 10 | 60 |
| `GET /gdp-growth` | GDP growth rate (annual %) | 10 | 60 |
| `GET /gdp-per-capita` | GDP per capita (current US$) | 10 | 60 |
| `GET /gdp-per-capita-growth` | GDP per capita growth (annual %) | 10 | 60 |
| `GET /gni` | GNI (current US$) | 10 | 60 |
| `GET /ppp` | GDP PPP (current international $) | 10 | 60 |
| `GET /industry` | Industry value added (% of GDP) | 10 | 60 |
| `GET /services` | Services value added (% of GDP) | 10 | 60 |

### Query Parameters

All endpoints (except `/` and `/summary`) accept:

| Parameter | Type | Description |
|---|---|---|
| `limit` | integer | Number of years to return (default: 10, max: 60) |

`/summary` accepts `limit` with default 1, max 30.

### Countries Covered

World (WLD), United States, China, Japan, Germany, United Kingdom, India, France, Italy, Canada, South Korea

---

## Example Response

**`GET /gdp?limit=1`**

```json
{
  "indicator": "GDP (Current US$)",
  "unit": "Current US$",
  "frequency": "Annual",
  "source": "World Bank",
  "data": [
    {"country": "World",          "iso_code": "WLD", "year": "2023", "value": 105435519764452.0},
    {"country": "United States",  "iso_code": "USA", "year": "2023", "value": 27357567000000.0},
    {"country": "China",          "iso_code": "CHN", "year": "2023", "value": 17794782000000.0}
  ]
}
```

---

## Data Source

**World Bank Open Data** — [data.worldbank.org](https://data.worldbank.org)

| Indicator | World Bank Code |
|---|---|
| GDP (current US$) | NY.GDP.MKTP.CD |
| GDP growth (annual %) | NY.GDP.MKTP.KD.ZG |
| GDP per capita (current US$) | NY.GDP.PCAP.CD |
| GDP per capita growth (annual %) | NY.GDP.PCAP.KD.ZG |
| GNI (current US$) | NY.GNP.MKTP.CD |
| GDP PPP (current international $) | NY.GDP.MKTP.PP.CD |
| Industry value added (% of GDP) | NV.IND.TOTL.ZS |
| Services value added (% of GDP) | NV.SRV.TOTL.ZS |

---

## Pricing

| Plan | Requests | Price |
|---|---|---|
| BASIC | 500,000 req/mo | Free |
| PRO | Unlimited | $9/mo |
| ULTRA | Unlimited | $29/mo |

---

## Tech Stack

- **Framework:** FastAPI
- **Deployment:** Vercel
- **Data:** World Bank Open Data API

---

*By **GlobalData Store***
