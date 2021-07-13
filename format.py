from pathlib import Path
import subprocess

SOURCE_DIRECTORY = Path("./source")
for path in SOURCE_DIRECTORY.rglob("*.nim"):
    subprocess.run(f"nimpretty {str(path)}")
