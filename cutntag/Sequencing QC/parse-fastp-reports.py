import argparse
from pathlib import Path
import json
import pandas as pd

def extract_fields(json_files):
    records = []
    for f in json_files:
        with open(f) as jf:
            data = json.load(jf)
            record = {
                "sample": f.stem,  # file name without extension
                "prefilter_reads": data["summary"]["before_filtering"]["total_reads"],
                "postfilter_reads": data["summary"]["after_filtering"]["total_reads"],
                "prefilter_read_length": data["summary"]["before_filtering"]["read1_mean_length"],
                "corrected_reads": data.get("filtering_result", {}).get("corrected_reads", None),
                "low_qual_reads": data.get("filtering_result", {}).get("low_quality_reads", None),
                "too_many_N_reads": data.get("filtering_result", {}).get("too_many_N_reads", None),
                "low_complexity_reads": data.get("filtering_result", {}).get("low_complexity_reads", None),
                "too_short_reads": data.get("filtering_result", {}).get("too_short_reads", None),
                "adapter_trimmed": data["adapter_cutting"]["adapter_trimmed_reads"],
                "duplication_rate": data.get("duplication", {}).get("rate", None),
            }
            record["filter_pass_rate"] = record["postfilter_reads"]/record["prefilter_reads"]
            records.append(record)
    df = pd.DataFrame(records).set_index("sample")
    return df

def main():
    parser = argparse.ArgumentParser(description="Summarize all fastp runs")
    parser.add_argument("json_dir", help="Directory containing .json fastp reports")
    
    args = parser.parse_args()
    fastp_path=Path(args.json_dir)
    json_files = list(fastp_path.rglob("*.json"))

    df = extract_fields(json_files).sort_index()
    df.to_csv("fastp_summary_table.csv")

if __name__ == "__main__":
    main()