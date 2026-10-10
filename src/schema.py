from pydantic import BaseModel, Field, ValidationError


class Measurement(BaseModel):
    strain: str
    replicate: int = Field(ge=1, le=3)     # between 1 and 3
    time_h: float = Field(ge=0, le=48)     # between 0 and 48 hours
    od600: float = Field(ge=0, le=5)       # cloudiness, never negative


# Check every row: good ones go in one list, bad ones in another
def validate_rows(table):
    good_rows = []
    bad_rows = []

    for row in table.to_dict(orient="records"):
        try:
            measurement = Measurement(**row)
            good_rows.append(measurement)
        except ValidationError:
            bad_rows.append(row)

    return good_rows, bad_rows
