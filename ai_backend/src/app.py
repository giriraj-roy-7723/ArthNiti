from fastapi import FastAPI
from src.routes import (
    population,
    competitor,
    market_price,
    supply_chain,
    logistics,
    advisory,
    report,
)

app = FastAPI(
    title="Rural Business Intelligence API",
    description="FastAPI backend for hyper-local micro-enterprise feasibility analysis.",
    version="1.0.0",
)

# Individual Module Routes
app.include_router(population.router, prefix="/api/v1/population", tags=["Population"])

app.include_router(
    competitor.router, prefix="/api/v1/competitors", tags=["Competitors"]
)
app.include_router(
    market_price.router, prefix="/api/v1/market-price", tags=["Market Price"]
)
app.include_router(
    supply_chain.router, prefix="/api/v1/supply-chain", tags=["Supply Chain"]
)
app.include_router(
    logistics.router, prefix="/api/v1/logistics", tags=["Logistics & Freight"]
)
app.include_router(
    advisory.router, prefix="/api/v1/advisory", tags=["Seasonal Advisory & Risks"]
)

# The Master Orchestrator Route
app.include_router(
    report.router, prefix="/api/v1/report", tags=["Master Report Generation"]
)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Rural Business Intelligence API. Visit /docs for the Swagger UI."
    }
