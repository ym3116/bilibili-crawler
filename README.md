# bilibili-crawler
## Setup Notes

This project requires a local copy of Chrome for Testing and Chromedriver.
To download them:

- [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/)
- [Chromedriver](https://sites.google.com/chromium.org/driver/)

Place the files under root and name them `chrome-mac-arm64/` and `chromedriver-mac-arm64/` accordingly.

## Craw Data

```bash
    python crawler/main.py 
```  
it saves bilibili_video_info.csv in data/raw

## 🛠 Data Processing

```bash
python analysis/process_video_data.py
```


## 📁 Project Structure

```

bilibili-crawler/
├── README.md                      # Project documentation
├── .gitignore                     # Git ignore rules
├── venv/                          # Python virtual environment (excluded from Git)
│
├── crawler/                       # 🔧 Core crawling scripts
│   ├── main.py                    # Main execution entry for crawling
│   ├── config.py                  # Configuration (paths, keywords, max pages, etc.)
│   ├── crawler.py                 # Crawling logic for fetching video data
│   ├── html\_checker.py            # Utility to validate video charging status
│   └── test\_on\_single\_video.py    # Script for testing on one specific BV ID
│
├── data/                          # 📦 Dataset storage
│   ├── raw/                       # Original, unprocessed data (e.g., video info CSV)
│   │   ├── bilibili\_video\_info.csv
│   │   ├── bv\_list.txt
│   │   └── raw\_test\_output.json
│   └── processed/                 # Cleaned or manually labeled data
│       
│
├── analysis/                      # 📊 Future regression or statistical scripts (WIP)
├── notebooks/                     # 🧪 Jupyter notebooks for exploratory analysis (WIP)
├── results/                       # 📈 Generated plots, tables, and final outputs
├── src/                           # 🧩 Shared analysis utilities and processing functions (WIP)
│
├── chrome-mac-arm64/              # Chrome for Testing (used by Selenium)
├── chromedriver-mac-arm64/        # ChromeDriver binary for macOS
└── **pycache**/                   # Python bytecode cache (auto-generated)

```