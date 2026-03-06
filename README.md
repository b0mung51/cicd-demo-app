# CMPE 195 — CI/CD Demo App

A small Python/Flask app used in the **CI/CD & Deployment** class activity.

## What's in this repo

```
app.py              Flask web app with / and /health endpoints
src/calculator.py   Simple module with add, subtract, multiply, divide
tests/
  test_calculator.py  Unit tests for the calculator module
  test_app.py         Integration tests for the Flask routes
requirements.txt    All dependencies (flask, pytest, flake8, black, gunicorn)
Procfile            Tells Render how to start the app
```

## Activity 1: Set Up CI

### 1. Fork this repo

```bash
git clone <repo-url>
cd cicd-demo-app
```

### 2. Run the tests locally first

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

pytest tests/ -v
```

All 10 tests should pass.

### 3. Run the linter locally

```bash
black --check src/ tests/
flake8 src/ tests/ --max-line-length=120
```

Both should exit cleanly (no output = no errors).

### 4. Create the CI workflow

```bash
mkdir -p .github/workflows
```

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install flake8 black
      - name: Check formatting
        run: black --check src/ tests/
      - name: Lint
        run: flake8 src/ tests/ --max-line-length=120

  test:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/ -v
```

### 5. Push to a branch and open a PR

```bash
git checkout -b setup-ci
git add .github/workflows/ci.yml
git commit -m "Add CI workflow"
git push -u origin setup-ci
```

Open a PR on GitHub, then click the **Actions** tab to watch the pipeline run.

### 6. Turn on branch protection

GitHub → **Settings → Branches → Add rule**

- Branch name pattern: `main`
- Require status checks to pass before merging
- Require pull request reviews (at least 1)
- Require branches to be up to date

---

## Activity 2: Deploy Your App

Pick one path based on your project type:

| Project Type | Deploy Target |
|---|---|
| Static front-end (HTML/CSS/JS) | GitHub Pages |
| Full-stack app (backend + DB) | Render |

Both deploy automatically via GitHub Actions on every push to `main`.

---

### Path A — GitHub Pages (static front-ends)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: './build'
      - uses: actions/deploy-pages@v4
```

---

### Path B — Render (full-stack / this demo app)

**Step 1** — Connect your repo on [render.com](https://render.com), then copy your **Service ID** and **API Key** from the Render dashboard.

**Step 2** — Add them as GitHub secrets:

> GitHub → Repository Settings → Secrets and variables → Actions

```
RENDER_SERVICE_ID = srv-abc123...
RENDER_API_KEY    = rnd_abc123...
```

**Step 3** — Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Render

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - name: Trigger Render deploy
        run: |
          curl -X POST \
            "https://api.render.com/v1/services/${{ secrets.RENDER_SERVICE_ID }}/deploys" \
            -H "Authorization: Bearer ${{ secrets.RENDER_API_KEY }}" \
            -H "Content-Type: application/json"
```

> Deploy only runs **after tests pass** (`needs: test` references the job in `ci.yml`).

**Step 4** — Configure the service on Render:

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `gunicorn app:app`

Hit your live URL then `/health` — you should get `{"status": "healthy"}`.

---

## Run locally

```bash
python app.py
# → http://localhost:5000
# → http://localhost:5000/health
# → http://localhost:5000/calculate/add/3/4
```
