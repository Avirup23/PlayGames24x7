import sys
sys.path.append('../')
import os
import glob
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from algo_minscore import mscore  # your custom function

OUTPUT_FILE = "EloData.csv"

def process_csv(csv_path):
    """Process a single CSV and return a DataFrame of results."""
    try:
        parts = os.path.basename(csv_path).split('.')
        if len(parts) < 4:
            return None
        p1, p2 = parts[1], parts[3]
        if p1 == p2:
            return None

        df = pd.read_csv(csv_path, usecols=['init.hand1', 'init.hand2', 'wcj', 'winner', 'score1', 'score2'])
        if df.empty:
            return None

        if len(df) > 5000:
            df = df.sample(n=5000, random_state=42)

        rows = []
        for h1, h2, w, winner, s1, s2 in zip(df['init.hand1'], df['init.hand2'], df['wcj'], df['winner'], df['score1'], df['score2']):
            try:
                hand1 = [int(x) for x in str(h1).split()]
                hand2 = [int(x) for x in str(h2).split()]
                rows.append({
                    'Winner': winner,
                    'Player1': p1,
                    'Player2': p2,
                    'Init.Score1': mscore(hand1, w),
                    'Init.Score2': mscore(hand2, w),
                    'Final.Score1': s1,
                    'Final.Score2': s2
                })
            except Exception:
                continue

        if not rows:
            return None
        return pd.DataFrame(rows)

    except Exception as e:
        print(f"⚠️ Error processing {csv_path}: {e}")
        return None


def append_to_csv(df, output_file, header_written):
    """Append a DataFrame to the CSV file safely."""
    df.to_csv(output_file, mode='a', header=not header_written, index=False)


def main():
    csv_files = glob.glob('Paper Data/*.csv')
    if not csv_files:
        print("⚠️ No CSV files found in 'Paper Data/'.")
        return

    # If output file exists, remove to start fresh
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)

    header_written = False

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(process_csv, csv): csv for csv in csv_files}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing CSVs"):
            df = future.result()
            if df is not None and not df.empty:
                append_to_csv(df, OUTPUT_FILE, header_written)
                header_written = True

    print("✅ All files processed. Output saved to EloData.csv")


if __name__ == "__main__":
    main()