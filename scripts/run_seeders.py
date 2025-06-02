import subprocess
import os
from utils.db import has_already_run, mark_seed_as_run

SEED_SCRIPTS = [
    "scripts/load_locations_from_users.py",
    "scripts/load_interests.py",
    "scripts/load_advertisers.py",
    "scripts/load_users.py",
    "scripts/load_user_interests.py",
    "scripts/load_campaigns.py",
    "scripts/load_campaign_targets.py",
    "scripts/load_ad_events.py",
]

def run_seeds():
    for script_path in SEED_SCRIPTS:
        script_name = os.path.basename(script_path)

        if has_already_run(script_name):
            print(f"⏭️ Skipping {script_name} (already ran)")
            continue

        print(f"\n🔧 Running: {script_name}")
        try:
            subprocess.run(["python", script_path], check=True)
            mark_seed_as_run(script_name)
            print("✅ Success")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed: {script_name}")
            print(e)
            break

if __name__ == "__main__":
    run_seeds()
