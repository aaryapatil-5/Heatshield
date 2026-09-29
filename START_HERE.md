# HeatShield AI — Start Here

## Windows

1. Open a terminal in this folder.
2. Run `run_backend.bat` and keep it running.
3. Open a second terminal and run `run_frontend.bat`.
4. Open the Vite URL shown in the terminal, usually `http://localhost:5173`.
5. FastAPI docs are at `http://localhost:8000/docs`.

## Manual

Backend:

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Frontend:

```powershell
cd frontend
npm install
npm run dev
```

## Demo mode

The application works without an API key. Demo Mode is deterministic and explicitly labelled as simulated.

## Live mode

Click the mode button in the dashboard. Live Mode uses Open-Meteo for current and five-day weather when the network is reachable. If it fails, the backend automatically falls back to demo data.
