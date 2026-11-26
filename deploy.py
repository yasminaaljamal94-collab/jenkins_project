"""Simple local deployment script for the Jenkins lab.

Copies the application into a versioned release folder, points a
'current' marker at it, and runs a smoke test against the deployed copy.
"""
import os
import shutil
import subprocess
import sys
from datetime import datetime

FILES_TO_DEPLOY = ["app.py", "requirements.txt"]


def deploy(target_root):
    release = datetime.now().strftime("release_%Y%m%d_%H%M%S")
    release_dir = os.path.join(target_root, release)
    os.makedirs(release_dir, exist_ok=True)

    for name in FILES_TO_DEPLOY:
        shutil.copy2(name, release_dir)
        print(f"Copied {name} -> {release_dir}")

    with open(os.path.join(target_root, "CURRENT"), "w") as marker:
        marker.write(release + "\n")

    # Smoke test: run the deployed app and check its output.
    result = subprocess.run(
        [sys.executable, "app.py"],
        cwd=release_dir,
        capture_output=True,
        text=True,
        check=True,
    )
    output = result.stdout.strip()
    print(f"Smoke test output: {output}")
    if output != "Hello, World from Yasmina Eljamal!":
        raise SystemExit("Smoke test failed")

    print(f"Deployment successful: {release_dir}")
    return release_dir


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "deploy_target"
    deploy(target)
