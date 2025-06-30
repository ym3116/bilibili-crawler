# convert Unix timestamp into readable date
# add after_policy(boolean) column to indicate if video was published after 2023-09-01
# add year_month column to count videos per month
import pandas as pd
from pathlib import Path

# Paths
RAW_PATH = Path("data/raw/bilibili_video_info.csv")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Load data
df = pd.read_csv(RAW_PATH)

# Convert timestamp to datetime
df["pub_datetime"] = pd.to_datetime(df["pubdate"], unit="s")

# Label whether video was published after 2023-09-01 policy
policy_cutoff = pd.Timestamp("2023-09-01")
df["after_policy"] = df["pub_datetime"] >= policy_cutoff

# Add monthly column
df["year_month"] = df["pub_datetime"].dt.to_period("M").astype(str)

# Save processed version
df.to_parquet(PROCESSED_DIR / "processed_videos.parquet", index=False)
#df.to_csv("data/processed/processed_videos.csv", index=False)
print("✅ Data processed and saved.")
