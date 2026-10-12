# Adaptive AI Traffic Controller

A local interactive Foundation of AI demo built with Python and Streamlit.

## Features
- Four-way intersection visualization with animated-looking car markers and live traffic signals
- State-based AI heuristic: prioritizes the approach with the largest queue
- Interactive controls to advance simulation, inject traffic, and reset
- Live queue, throughput, and waiting metrics
- Charts and recent simulation history

## Requirements
Python 3.10 or newer is recommended.

## Run on Windows
1. Extract the ZIP.
2. Open the extracted `adaptive_ai_traffic_controller` folder.
3. In File Explorer's address bar, type `cmd` and press Enter.
4. Run:

```bat
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

If `py` is unavailable, use `python` instead.
Streamlit opens a browser tab, usually at `http://localhost:8501`.

## Run on macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Demo in 60 seconds
1. Run `streamlit run app.py`.
2. Click **Run one AI step** 5–10 times.
3. Point out that the controller observes the queue sizes and selects the busiest approach.
4. Click **Add traffic** and show that the signal decision changes as queues change.
5. Explain the performance indicators: vehicles served, average queue length, and cumulative waiting.
6. Reset before another demo.

## AI mapping
- Environment: four-way intersection
- Agent: traffic controller
- State/percepts: queue length in each direction
- Action: choose the green direction
- Decision policy: largest-queue-first heuristic with deterministic tie-breaking
- Performance: throughput, queue length and cumulative waiting

## Notes
This is an educational simulation using a simple heuristic, not a trained ML model and not suitable for controlling real traffic. Signal transitions and vehicle flow are abstracted for demonstration.
