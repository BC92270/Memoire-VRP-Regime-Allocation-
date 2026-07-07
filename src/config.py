from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"
OUTPUT_CHARTS_DIR = PROJECT_ROOT / "outputs" / "charts"

for directory in [
    DATA_RAW_DIR,
    DATA_PROCESSED_DIR,
    OUTPUT_TABLES_DIR,
    OUTPUT_CHARTS_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)


START_DATE = "2005-01-01"
END_DATE = None

# MVP design:
# US should work immediately.
# Europe depends on Yahoo availability for VSTOXX. If it fails, we will plug a manual source later.
MARKET_CONFIGS = {
    "US": {
        "equity_candidates": ["SPY", "^GSPC"],
        "vol_candidates": ["^VIX"],
        "bond_candidates": ["AGG", "IEF", "BND"],
    },
    "EU": {
        "equity_candidates": ["^STOXX50E", "FEZ"],
        "vol_candidates": ["^V2TX", "V2TX.DE", "VSTOXX.DE", "^VSTOXX"],
        "manual_vol_csv": DATA_RAW_DIR / "vstoxx.csv",
        "bond_candidates": ["IEAG.AS", "EUNA.DE", "AGGH.L", "BNDX", "AGG", "IEF"],
    },
}

RV_WINDOW_DAYS = 21
TRADING_DAYS_PER_YEAR = 252
PERIODS_PER_YEAR_MONTHLY = 12

BASE_TRANSACTION_COST_BPS = 10