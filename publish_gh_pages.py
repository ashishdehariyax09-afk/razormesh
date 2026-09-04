"""
RazorMesh One-Command GitHub Pages Deployment Script
Publishes static assets from frontend/ to gh-pages branch cleanly.
"""
import subprocess
import shutil
import sys
from pathlib import Path

def main():
    root = Path(__file__).resolve().parent
    temp_dir = root.parent / "razormesh_gh_pages_build"
    
    print("[1/4] Preparing static site build directory...")
    if temp_dir.exists():
        shutil.rmtree(temp_dir, ignore_errors=True)
    temp_dir.mkdir(parents=True, exist_ok=True)

    # Copy HTML, CSS, JS and .nojekyll
    shutil.copy(root / "frontend" / "index.html", temp_dir / "index.html")
    (temp_dir / "static" / "css").mkdir(parents=True, exist_ok=True)
    (temp_dir / "static" / "js").mkdir(parents=True, exist_ok=True)
    shutil.copy(root / "frontend" / "css" / "style.css", temp_dir / "static" / "css" / "style.css")
    shutil.copy(root / "frontend" / "js" / "app.js", temp_dir / "static" / "js" / "app.js")
    (temp_dir / ".nojekyll").touch()

    print("[2/4] Initializing temporary git environment...")
    subprocess.run(["git", "init"], cwd=temp_dir, check=True)
    subprocess.run(["git", "branch", "-M", "gh-pages"], cwd=temp_dir, check=True)
    subprocess.run(["git", "add", "."], cwd=temp_dir, check=True)
    subprocess.run(["git", "commit", "-m", "deploy: publish static frontend to GitHub Pages"], cwd=temp_dir, check=True)
    
    print("[3/4] Pushing to origin gh-pages...")
    remote_url = "https://github.com/ashishdehariyax09-afk/razormesh.git"
    subprocess.run(["git", "remote", "add", "origin", remote_url], cwd=temp_dir, check=True)
    res = subprocess.run(["git", "push", "-u", "origin", "gh-pages", "--force"], cwd=temp_dir)

    print("[4/4] Cleaning up temporary build directory...")
    shutil.rmtree(temp_dir, ignore_errors=True)

    if res.returncode == 0:
        print("\n[SUCCESS] Deployed to GitHub Pages!")
        print("Live URL: https://ashishdehariyax09-afk.github.io/razormesh/")
    else:
        print("\n[FAILED] Deployment failed during git push.")
        sys.exit(res.returncode)

if __name__ == "__main__":
    main()
