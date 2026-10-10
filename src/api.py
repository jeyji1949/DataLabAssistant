from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.storage import load_from_sqlite
from src.analysis import peak_od, max_growth_rate, fastest_strain


DB_PATH = Path(__file__).resolve().parent.parent / "data" / "clean" / "lab.db"

app = FastAPI(title="Lab Data Assistant API")


class StrainSummary(BaseModel):
    strain: str
    peak_od: float
    max_growth_rate: float


# Helper: read the clean table, or explain what is missing
def get_table():
    if not DB_PATH.exists():
        raise HTTPException(
            status_code=503,
            detail="Database not found. Run the pipeline first.",
        )
    return load_from_sqlite(DB_PATH)


@app.get("/strains")
def list_strains():
    table = get_table()
    strains = sorted(table["strain"].unique())
    return {"strains": strains}


@app.get("/strains/{strain}/summary", response_model=StrainSummary)
def strain_summary(strain: str):
    table = get_table()

    if strain not in table["strain"].values:
        raise HTTPException(status_code=404, detail="Unknown strain")

    return StrainSummary(
        strain=strain,
        peak_od=round(peak_od(table, strain), 3),
        max_growth_rate=round(max_growth_rate(table, strain), 3),
    )


@app.get("/fastest-strain")
def get_fastest_strain():
    table = get_table()
    return {"fastest_strain": str(fastest_strain(table))}