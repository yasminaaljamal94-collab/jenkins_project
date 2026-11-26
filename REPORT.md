# Lab 10 Report – Jenkins for DevOps Automation (CI/CD)

**Name:** Yasmina Eljamal  **AUB username:** yie08  **Student ID:** 202406430

## 1. Project
| File | Purpose |
|---|---|
| `app.py` | `greet(name)` returns `"Hello, {name} from Yasmina Eljamal!"` |
| `tests/test_app.py` | unittest checking `greet("World")` |
| `requirements.txt` | flake8, pytest, coverage, bandit |
| `pytest.ini` | puts the project root on the import path so `from app import greet` works |
| `.coveragerc` | coverage settings (measures app.py, minimum 80%) |
| `deploy.py` | local deployment script |
| `Jenkinsfile_Yasmina_Eljamal` | the pipeline |

## 2. Changes made to the original Jenkinsfile

1. **Coverage stage (new).** Runs the test suite under coverage.py:
   `coverage run -m pytest && coverage report && coverage xml && coverage html`.
   The report is printed in the console log, and `coverage.xml` plus the `htmlcov/` HTML report are archived as build artifacts. `.coveragerc` sets `fail_under = 80`, so the stage fails if coverage drops below 80%. The `if __name__ == "__main__":` block is excluded since it is not library code.
2. **Security Scan stage (new).** Runs bandit on the application source (`app.py`, `deploy.py`). A full report is written to `bandit-report.txt` and archived; a second run with `-ll` fails the build on any **medium or high** severity issue. Low-severity notes (the `subprocess` import used by the deploy smoke test) are reported but do not fail the build.
3. **Deploy stage (implemented).** Replaced the `echo` placeholder with `python deploy.py deploy_target`, which:
   - copies `app.py` and `requirements.txt` into a timestamped release folder (`deploy_target/release_YYYYMMDD_HHMMSS`),
   - writes the release name to `deploy_target/CURRENT`,
   - runs the deployed app as a smoke test and fails if the output is not `Hello, World from Yasmina Eljamal!`.
4. **Windows / Linux support.** The original file used `sh "source ..."`, which fails on Windows agents (no `sh`) and on many Linux agents (`/bin/sh` has no `source`). A helper `run(unixCmd, winCmd)` uses `isUnix()` to call `sh` with `. venv/bin/activate` on Linux/macOS or `bat` with `call venv\Scripts\activate.bat` on Windows.
5. **Small fixes.** Added `pytest`, `coverage` and `bandit` to `requirements.txt` (the original only had flake8, so the Test stage could not run), added `pytest.ini` so the tests can import `app`, made the test expect the personalised greeting, and added `success`/`failure` messages in `post` (keeping `cleanWs()` in `always`).

## 3. Pipeline stages
| Stage | Command | Pass condition |
|---|---|---|
| Setup | create venv, `pip install -r requirements.txt` | install succeeds |
| Lint | `flake8 app.py` | no style errors |
| Test | `pytest -v` | all tests pass |
| Coverage | `coverage run -m pytest`, `coverage report/xml/html` | coverage ≥ 80% |
| Security Scan | `bandit app.py deploy.py -ll` | no medium/high issues |
| Deploy | `python deploy.py deploy_target` | files copied and smoke test passes |

## 4. Output of the Jenkins build

The `Python-CI-CD` job ("Pipeline script from SCM": Git, branch `*/main`, Script Path `Jenkinsfile_Yasmina_Eljamal`) was run on Jenkins 2.580.3 (Windows, Java 21, Python 3.12).
**Build #1 result: `Finished: SUCCESS`** (about 2 minutes). Full log: [`jenkins_build_1_console.txt`](jenkins_build_1_console.txt).

| Stage | Result | Key output |
|---|---|---|
| Checkout SCM | ✅ | cloned `main` @ `73cc7c7` |
| Setup | ✅ | venv created; flake8 7.5.0, pytest 9.2.0, coverage 7.17.5, bandit 1.9.4 installed |
| Lint | ✅ | `flake8 app.py`: no errors |
| Test | ✅ | `tests/test_app.py::TestApp::test_greet PASSED` (1 passed) |
| Coverage | ✅ | `app.py` 100% coverage; `coverage.xml` + `htmlcov/` archived |
| Security Scan | ✅ | bandit: no medium/high issues (2 low); `bandit-report.txt` archived |
| Deploy | ✅ | release folder created, smoke test printed `Hello, World from Yasmina Eljamal!` |

Coverage stage:
```
Name     Stmts   Miss  Cover   Missing
--------------------------------------
app.py       2      0   100%
--------------------------------------
TOTAL        2      0   100%
Wrote XML report to coverage.xml
Wrote HTML report to htmlcov\index.html
```

Security Scan stage:
```
Test results:
        No issues identified.
Run metrics:
        Total issues (by severity):
                Low: 2   Medium: 0   High: 0
```

Deploy stage:
```
Deploying application...
Copied app.py -> deploy_target\release_20261126_223923
Copied requirements.txt -> deploy_target\release_20261126_223923
Smoke test output: Hello, World from Yasmina Eljamal!
Deployment successful: deploy_target\release_20261126_223923
...
Pipeline finished: all stages passed.
Finished: SUCCESS
```
