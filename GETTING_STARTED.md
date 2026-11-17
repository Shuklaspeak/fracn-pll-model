# Getting started (one-time setup on your Mac)

## 1. Open Terminal and go to the repo
```bash
cd ~/Documents/Claude/Projects/"DTC in PLLs"/fracn-pll-model
```

## 2. Check Python
```bash
python3 --version        # want 3.9 or newer
```

## 3. Virtual environment (a private Python just for this project)
```bash
python3 -m venv .venv
source .venv/bin/activate      # prompt now starts with (.venv)
pip install -r requirements.txt
```
Every new Terminal window: `cd` to the repo, then `source .venv/bin/activate` again.

## 4. Run the tests and plots (always from the repo root)
```bash
pytest -v
python scripts/bode.py
python scripts/sweep_icp.py
```
Run a single test: `pytest -v -k oracle`

## 5. Python survival kit
- `print(x)` anywhere to see a value. Engineering units: `print(f"{C1*1e12:.2f} pF")`
- `np.abs`, `np.angle`, `np.degrees`, `np.radians`, `np.sqrt`, `np.tan`, `np.log10`, `np.logspace`
- `1j` is the imaginary unit; `**` is power (`^` is XOR!)
- numpy arrays work element-wise
- Indentation is syntax: 4 spaces, consistent within a block
- Error messages: read the LAST line first, then the line number it points to

## 6. Editing text files
Use VS Code (or vim). **Not TextEdit** — it silently converts `.md` to `.rtf`, which GitHub can't render.
In vim: `Esc` then `:wq` to save and quit, `:q!` to quit without saving.

## 7. GitHub (one time)
1. Make an account at github.com.
2. Create a new empty repo named `fracn-pll-model` (no README — we already have one).
3. In Terminal, in the repo folder:
```bash
git init
git add .
git commit -m "Integer-N CP PLL loop model"
git branch -M main
git remote add origin https://github.com/<your-username>/fracn-pll-model.git
git push -u origin main
```
GitHub will ask you to sign in; follow its prompt (a personal access token or the GitHub CLI).
