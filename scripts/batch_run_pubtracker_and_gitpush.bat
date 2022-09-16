C:
cd C:\Users\gpelle20\Desktop\open_science_metrics_tools
C:\Users\gpelle20\Desktop\open_science_metrics_tools\venv\Scripts\activate.bat && python C:\Users\gpelle20\Desktop\open_science_metrics_tools\scripts\open_access_publication_tracker.py
git fetch origin
git checkout origin/main
git add --all
git commit -m "ran tracker"
git push origin HEAD:main
