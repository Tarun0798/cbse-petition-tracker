import pandas as pd
import matplotlib.pyplot as plt

# Changed to look for the local file in your folder instead of downloading from the web
CSV_URL = "petition_data.csv" 

print("Connecting to GitHub data stream...")
try:
    # 1. Download and preview the raw data file
    df = pd.read_csv(CSV_URL)
    print("\n[SUCCESS] Connection secure. Data packet fetched successfully!")
    print(f"Total entries found in cloud log: {len(df)} rows.")
    print("\n--- SAMPLE DATA PREVIEW ---")
    print(df.tail(3)) # Displays the last 3 rows of data
    print("---------------------------\n")
    
    if len(df) < 2:
        print("[!] STOPPING: Your CSV file needs at least 2 or 3 rows of data to calculate growth loops and draw a line.")
        input("\nPress Enter to close this diagnostic window...")
        exit()

    # 2. Process Timeline Math
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df_hourly = df.set_index("Timestamp").resample("1H").last().reset_index()
    df_hourly["Hourly Growth"] = df_hourly["Total Signatures"].diff().fillna(0)

    # 3. Compile layout
    print("Compiling charts and generating rendering window...")
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))

    ax1.plot(df["Timestamp"], df["Total Signatures"], color="#E53935", linewidth=2)
    ax1.set_title("CBSE Petition: Cumulative Growth Curve", fontweight="bold")
    ax1.grid(True, linestyle=":", alpha=0.5)

    ax2.bar(df["Timestamp"], df["Interval Growth"], color="#1E88E5", width=0.003)
    ax2.set_title("Micro Velocity Pulse (Signatures Added Every 5 Mins)")
    ax2.grid(True, linestyle=":", alpha=0.5)

    ax3.bar(df_hourly["Timestamp"], df_hourly["Hourly Growth"], color="#4CAF50", width=0.03)
    ax3.set_title("Macro Velocity Pulse (Signatures Added Per Hour)")
    ax3.grid(True, linestyle=":", alpha=0.5)

    plt.tight_layout()
    print("[SUCCESS] Window initialized. Opening display interface now...")
    plt.show()

except Exception as e:
    print("\n[ERROR] The script encountered a critical processing block:")
    print(f"Details: {e}")
    input("\nPress Enter to close this diagnostic window...")
