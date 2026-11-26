# Lab 10 – Jenkins CI/CD Pipeline for Python

Yasmina Eljamal (yie08) – EECE435L

A small Python app with a Jenkins pipeline (`Jenkinsfile_Yasmina_Eljamal`) that runs:
**Setup → Lint → Test → Coverage → Security Scan → Deploy**.

See [REPORT.md](REPORT.md) for the changes made and the pipeline output.

## Jenkins job setup
1. New Item → **Pipeline** → name `Python-CI-CD`.
2. Pipeline → Definition: **Pipeline script from SCM**, SCM: **Git**, Repository URL: this repo, Branch: `*/main`.
3. **Script Path: `Jenkinsfile_Yasmina_Eljamal`** (the file is not named plain `Jenkinsfile`).
4. Save → Build Now.

## Run locally
```
python -m venv venv
venv\Scripts\activate        # Windows  (source venv/bin/activate on Linux/macOS)
pip install -r requirements.txt
flake8 app.py
pytest -v
coverage run -m pytest && coverage report
bandit -r . -x ./venv,./tests -ll
python deploy.py
```
