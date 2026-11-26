# Lab 10 Report – Jenkins for DevOps Automation (CI/CD)

**Name:** Yasmina Eljamal  **AUB username:** yie08  **Student ID:** 202406430

## 1. Project
| File | Purpose |
|---|---|
| `app.py` | `greet(name)` returns `"Hello, {name} from Yasmina Eljamal!"` |
| `tests/test_app.py` | unittest checking `greet("World")` |
| `requirements.txt` | flake8, pytest, coverage, bandit |
| `pytest.ini` | puts the project root on the import path so `from app import greet` works |
| `.coveragerc` | coverage settings (excludes venv/tests, minimum 80%) |
| `deploy.py` | local deployment script |
| `Jenkinsfile_Yasmina_Eljamal` | the pipeline |

## 2. Changes made to the original Jenkinsfile

1. **Coverage stage (new).** Runs the test suite under coverage.py:
   `coverage run -m pytest && coverage report && coverage xml && coverage html`.
   The report is printed in the console log, and `coverage.xml` plus the `htmlcov/` HTML report are archived as build artifacts. `.coveragerc` sets `fail_under = 80`, so the stage fails if coverage drops below 80%. The `if __name__ == "__main__":` block is excluded since it is not library code.
2. **Security Scan stage (new).** Runs bandit on the source (excluding `venv` and `tests`). A full report is written to `bandit-report.txt` and archived; a second run with `-ll` fails the build on any **medium or high** severity issue. Low-severity notes (the `subprocess` import used by the deploy smoke test) are reported but do not fail the build.
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
| Security Scan | `bandit -r . -x ./venv,./tests -ll` | no medium/high issues |
| Deploy | `python deploy.py deploy_target` | files copied and smoke test passes |

## 4. Output of the pipeline

The same commands the pipeline runs were executed on the project before pushing, with these results:

- **Lint:** flake8 – no errors.
- **Test:** `tests/test_app.py::TestApp::test_greet PASSED` – 1 passed.
- **Coverage:**
  ```
  Name     Stmts   Miss  Cover   Missing
  --------------------------------------
  app.py       2      0   100%
  --------------------------------------
  TOTAL        2      0   100%
  ```
- **Security Scan:** bandit – "No issues identified" at medium/high severity (2 low-severity notes on the `subprocess` use in `deploy.py`).
- **Deploy:**
  ```
  Copied app.py -> deploy_target/release_...
  Copied requirements.txt -> deploy_target/release_...
  Smoke test output: Hello, World from Yasmina Eljamal!
  Deployment successful: deploy_target/release_...
  ```

**Jenkins build `Python-CI-CD`:**

<!-- Add screenshots here: (1) the stage view with all six stages green, (2) the end of the Console Output showing "Finished: SUCCESS". -->

![Stage view](screenshots/stage_view.png)

![Console output](screenshots/console_output.png)
