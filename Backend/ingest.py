import sys
import os
import pandas as pd

from vectorstore import ingest_excel

def main():
    if len(sys.argv) != 2:
        print(" Usage: python ingest.py <excel_file.xlsx>")
        sys.exit(1)

    excel_path = sys.argv[1]

    #  Validate file
    if not os.path.exists(excel_path):
        print(f"File not found: {excel_path}")
        sys.exit(1)

    if not excel_path.lower().endswith(".xlsx"):
        print(" Only .xlsx files are supported")
        sys.exit(1)

    try:
        print(f"📥 Loading Excel file: {excel_path}")
        df = pd.read_excel(excel_path, dtype=str)  #  FORCE STRING

        if df.empty:
            print(" Excel file is empty")
            sys.exit(1)

        # Normalize column names ONLY (not values)
        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
            .str.lower()
            .str.replace(".", "", regex=False)
        )

        # Required columns
        required_cols = {"alarm no", "alarm description"}
        missing = required_cols - set(df.columns)
        if missing:
            print(f" Missing required columns: {missing}")
            sys.exit(1)

        # 🔎 Validate alarm codes (NO modification)
        print("🔎 Validating alarm codes...")
        bad_codes = []

        for val in df["alarm no"]:
            if not isinstance(val, str):
                bad_codes.append(val)
                continue
            val = val.strip().upper()
            if not val:
                bad_codes.append(val)
            # STRICT: prefix + digits (AL4024, ST4024, etc.)
            elif not any(c.isdigit() for c in val):
                bad_codes.append(val)

        if bad_codes:
            print("Invalid alarm codes found (prefix will NOT be guessed):")
            for b in bad_codes[:10]:
                print("   →", b)
            sys.exit(1)

        print(f" Rows loaded   : {len(df)}")
        print(f" Columns found : {list(df.columns)}")

        ingest_excel(df)

        print(" Excel data successfully ingested into ChromaDB")
        print(" Alarm prefixes preserved exactly as in Excel")

    except Exception as e:
        print(" Ingestion failed")
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
