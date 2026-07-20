import pandas as pd
import json

print("Peer Benchmark:")
try:
    df_peer = pd.read_csv("extracted/peer_benchmark.csv")
    print(df_peer.to_string())
except Exception as e:
    print(e)

print("\nForensic Screening Results:")
try:
    df_forensic = pd.read_csv("extracted/forensic_screening_results.csv")
    print(df_forensic.to_string())
except Exception as e:
    print(e)

print("\nRatio Analysis:")
try:
    df_ratios = pd.read_csv("extracted/ratio_analysis.csv")
    print(df_ratios.to_string())
except Exception as e:
    print(e)
