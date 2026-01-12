DROP TABLE IF EXISTS cards;
CREATE TABLE IF NOT EXISTS cards (
    "year",
    series,
    "set",
    "number",
    "name",
    team,
    features,
    "count",
    parallels,
    normalized,
    PRIMARY KEY ("year", series, "set", "number", "name") ON CONFLICT REPLACE
)