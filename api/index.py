from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
import asyncio
from datetime import datetime

app = FastAPI(
    title="Global GDP Comparison API",
    description="Real-time global GDP and economic data powered by World Bank Open Data",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

WB_BASE_URL = "https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"

COUNTRIES = [
    {"iso": "WLD", "name": "World"},
    {"iso": "USA", "name": "United States"},
    {"iso": "CHN", "name": "China"},
    {"iso": "JPN", "name": "Japan"},
    {"iso": "DEU", "name": "Germany"},
    {"iso": "GBR", "name": "United Kingdom"},
    {"iso": "IND", "name": "India"},
    {"iso": "FRA", "name": "France"},
    {"iso": "ITA", "name": "Italy"},
    {"iso": "CAN", "name": "Canada"},
    {"iso": "KOR", "name": "South Korea"},
]

INDICATORS = {
    "gdp":                  {"id": "NY.GDP.MKTP.CD",    "name": "GDP (Current US$)",                    "unit": "Current US$"},
    "gdp_growth":           {"id": "NY.GDP.MKTP.KD.ZG", "name": "GDP Growth Rate (Annual %)",           "unit": "Annual %"},
    "gdp_per_capita":       {"id": "NY.GDP.PCAP.CD",    "name": "GDP Per Capita (Current US$)",         "unit": "Current US$"},
    "gdp_per_capita_growth":{"id": "NY.GDP.PCAP.KD.ZG", "name": "GDP Per Capita Growth (Annual %)",    "unit": "Annual %"},
    "gni":                  {"id": "NY.GNP.MKTP.CD",    "name": "GNI (Current US$)",                    "unit": "Current US$"},
    "gdp_ppp":              {"id": "NY.GDP.MKTP.PP.CD", "name": "GDP PPP (Current International $)",    "unit": "Current International $"},
    "industry":             {"id": "NV.IND.TOTL.ZS",    "name": "Industry Value Added (% of GDP)",      "unit": "% of GDP"},
    "services":             {"id": "NV.SRV.TOTL.ZS",    "name": "Services Value Added (% of GDP)",      "unit": "% of GDP"},
}


async def fetch_wb_country(client: httpx.AsyncClient, iso: str, country_name: str, indicator_id: str, limit: int):
    url = WB_BASE_URL.format(country=iso, indicator=indicator_id)
    params = {
        "format": "json",
        "mrv": limit,
        "per_page": limit,
    }
    try:
        res = await client.get(url, params=params, timeout=15)
        data = res.json()
    except Exception:
        return None

    if not data or len(data) < 2:
        return None

    records = data[1] or []
    entries = [
        {
            "country": country_name,
            "iso_code": iso,
            "year": str(r["date"]),
            "value": r["value"],
        }
        for r in records
        if r.get("value") is not None
    ]
    return entries[0] if entries else None


async def fetch_indicator_all_countries(indicator_id: str, limit: int):
    async with httpx.AsyncClient() as client:
        tasks = [
            fetch_wb_country(client, c["iso"], c["name"], indicator_id, limit)
            for c in COUNTRIES
        ]
        results = await asyncio.gather(*tasks)
    return [r for r in results if r is not None]


async def fetch_wb_world_summary(indicator_id: str, limit: int):
    url = WB_BASE_URL.format(country="WLD", indicator=indicator_id)
    params = {
        "format": "json",
        "mrv": limit,
        "per_page": limit,
    }
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(url, params=params, timeout=15)
            data = res.json()
        except Exception:
            return []

    if not data or len(data) < 2:
        return []

    records = data[1] or []
    return [
        {"year": str(r["date"]), "value": r["value"]}
        for r in records
        if r.get("value") is not None
    ]


@app.get("/")
def root():
    return {
        "api": "Global GDP Comparison API",
        "version": "1.0.0",
        "description": "Global GDP and economic indicators — compare the world's top economies using World Bank data",
        "endpoints": [
            "/summary",
            "/gdp",
            "/gdp-growth",
            "/gdp-per-capita",
            "/gdp-per-capita-growth",
            "/gni",
            "/ppp",
            "/industry",
            "/services",
        ],
        "countries": [c["name"] for c in COUNTRIES],
        "source": "World Bank Open Data (data.worldbank.org)",
        "updated_at": datetime.utcnow().isoformat() + "Z",
    }


@app.get("/summary")
async def summary(limit: int = Query(default=1, ge=1, le=30)):
    """Get latest GDP and economic indicator values for the World aggregate."""
    result = {}
    for key, meta in INDICATORS.items():
        data = await fetch_wb_world_summary(meta["id"], limit=limit)
        result[key] = {
            "name": meta["name"],
            "unit": meta["unit"],
            "data": data,
        }
    return {
        "country": "World",
        "iso_code": "WLD",
        "source": "World Bank Open Data",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "indicators": result,
    }


@app.get("/gdp")
async def gdp(limit: int = Query(default=10, ge=1, le=60)):
    """GDP (current US$) for top global economies."""
    data = await fetch_indicator_all_countries(INDICATORS["gdp"]["id"], limit)
    return {
        "indicator": INDICATORS["gdp"]["name"],
        "unit": INDICATORS["gdp"]["unit"],
        "frequency": "Annual",
        "source": "World Bank",
        "data": data,
    }


@app.get("/gdp-growth")
async def gdp_growth(limit: int = Query(default=10, ge=1, le=60)):
    """GDP growth rate (annual %) for top global economies."""
    data = await fetch_indicator_all_countries(INDICATORS["gdp_growth"]["id"], limit)
    return {
        "indicator": INDICATORS["gdp_growth"]["name"],
        "unit": INDICATORS["gdp_growth"]["unit"],
        "frequency": "Annual",
        "source": "World Bank",
        "data": data,
    }


@app.get("/gdp-per-capita")
async def gdp_per_capita(limit: int = Query(default=10, ge=1, le=60)):
    """GDP per capita (current US$) for top global economies."""
    data = await fetch_indicator_all_countries(INDICATORS["gdp_per_capita"]["id"], limit)
    return {
        "indicator": INDICATORS["gdp_per_capita"]["name"],
        "unit": INDICATORS["gdp_per_capita"]["unit"],
        "frequency": "Annual",
        "source": "World Bank",
        "data": data,
    }


@app.get("/gdp-per-capita-growth")
async def gdp_per_capita_growth(limit: int = Query(default=10, ge=1, le=60)):
    """GDP per capita growth (annual %) for top global economies."""
    data = await fetch_indicator_all_countries(INDICATORS["gdp_per_capita_growth"]["id"], limit)
    return {
        "indicator": INDICATORS["gdp_per_capita_growth"]["name"],
        "unit": INDICATORS["gdp_per_capita_growth"]["unit"],
        "frequency": "Annual",
        "source": "World Bank",
        "data": data,
    }


@app.get("/gni")
async def gni(limit: int = Query(default=10, ge=1, le=60)):
    """GNI (current US$) for top global economies."""
    data = await fetch_indicator_all_countries(INDICATORS["gni"]["id"], limit)
    return {
        "indicator": INDICATORS["gni"]["name"],
        "unit": INDICATORS["gni"]["unit"],
        "frequency": "Annual",
        "source": "World Bank",
        "data": data,
    }


@app.get("/ppp")
async def ppp(limit: int = Query(default=10, ge=1, le=60)):
    """GDP PPP (current international $) for top global economies."""
    data = await fetch_indicator_all_countries(INDICATORS["gdp_ppp"]["id"], limit)
    return {
        "indicator": INDICATORS["gdp_ppp"]["name"],
        "unit": INDICATORS["gdp_ppp"]["unit"],
        "frequency": "Annual",
        "source": "World Bank",
        "data": data,
    }


@app.get("/industry")
async def industry(limit: int = Query(default=10, ge=1, le=60)):
    """Industry value added (% of GDP) for top global economies."""
    data = await fetch_indicator_all_countries(INDICATORS["industry"]["id"], limit)
    return {
        "indicator": INDICATORS["industry"]["name"],
        "unit": INDICATORS["industry"]["unit"],
        "frequency": "Annual",
        "source": "World Bank",
        "data": data,
    }


@app.get("/services")
async def services(limit: int = Query(default=10, ge=1, le=60)):
    """Services value added (% of GDP) for top global economies."""
    data = await fetch_indicator_all_countries(INDICATORS["services"]["id"], limit)
    return {
        "indicator": INDICATORS["services"]["name"],
        "unit": INDICATORS["services"]["unit"],
        "frequency": "Annual",
        "source": "World Bank",
        "data": data,
    }
