import pandas as pd

df_peer = pd.read_csv("extracted/peer_benchmark.csv")
print("PEER BENCHMARK:")
print(df_peer.to_string())

df_forensic = pd.read_csv("extracted/forensic_screening_results.csv")
print("\nFORENSIC SCREENING FOR BATA:")
print(df_forensic[df_forensic["Company"].str.lower() == "bata"].to_string())
