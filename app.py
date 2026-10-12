import random
import time
from collections import deque
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

st.set_page_config(page_title="Adaptive AI Traffic Controller", page_icon="🚦", layout="wide")

# ---------- Styling ----------
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #081426 0%, #102b3f 55%, #143b46 100%); color: #edf6ff; }
[data-testid="stSidebar"] { background: #0b1728; }
h1, h2, h3, p, label { color: #edf6ff !important; }
.hero { padding: 1.2rem 1.5rem; border: 1px solid #2c5369; border-radius: 18px;
        background: linear-gradient(120deg, rgba(18,48,69,.95), rgba(18,74,79,.72));
        box-shadow: 0 12px 40px rgba(0,0,0,.2); margin-bottom: 1rem; }
.pill { display:inline-block; padding:.3rem .7rem; border-radius:999px; background:#164e63;
        border:1px solid #2dd4bf; color:#ccfbf1; font-size:.85rem; margin-right:.35rem; }
.metric-card { padding:.8rem 1rem; border:1px solid #29485d; border-radius:14px;
               background:rgba(10,26,43,.75); }
div.stButton > button { border-radius: 12px; border: 1px solid #2dd4bf; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div><span class="pill">FOUNDATION OF AI</span><span class="pill">INTELLIGENT AGENT</span><span class="pill">LIVE SIMULATION</span></div>
  <h1 style="margin:.55rem 0 .2rem 0;">🚦 Adaptive AI Traffic Controller</h1>
  <p style="margin:0;color:#c8dce9!important;">A four-way intersection where an AI agent observes queue lengths and adapts signal timing to reduce waiting.</p>
</div>
""", unsafe_allow_html=True)

if "queues" not in st.session_state:
    st.session_state.queues = {"North": 5, "East": 2, "South": 4, "West": 1}
if "green" not in st.session_state:
    st.session_state.green = "North"
if "elapsed" not in st.session_state:
    st.session_state.elapsed = 0
if "total_wait" not in st.session_state:
    st.session_state.total_wait = 0
if "served" not in st.session_state:
    st.session_state.served = 0
if "history" not in st.session_state:
    st.session_state.history = []
if "last_action" not in st.session_state:
    st.session_state.last_action = "Initial state"
if "running" not in st.session_state:
    st.session_state.running = False

SIDES = ["North", "East", "South", "West"]
COLORS = {"North":"#38bdf8", "East":"#f59e0b", "South":"#a78bfa", "West":"#34d399"}

def choose_signal(queues, current):
    """Simple state-based policy: select the largest queue; break ties by fixed order."""
    max_q = max(queues.values())
    candidates = [s for s in SIDES if queues[s] == max_q]
    if current in candidates and len(candidates) > 1:
        return current
    return candidates[0]

def step_simulation(arrival_rate):
    q = st.session_state.queues
    # Vehicles arrive stochastically at each approach.
    for side in SIDES:
        if random.random() < arrival_rate / 100:
            q[side] = min(24, q[side] + random.randint(1, 3))
    current = st.session_state.green
    # Green direction serves vehicles; red directions accrue waiting.
    if q[current] > 0:
        departed = min(q[current], random.randint(1, 3))
        q[current] -= departed
        st.session_state.served += departed
    for side in SIDES:
        if side != current and q[side] > 0:
            st.session_state.total_wait += q[side]
    st.session_state.elapsed += 1
    next_signal = choose_signal(q, current)
    st.session_state.last_action = f"Observed queues → selected {next_signal} (largest queue: {q[next_signal]} vehicles)"
    st.session_state.green = next_signal
    st.session_state.history.append({
        "Step": st.session_state.elapsed,
        "North": q["North"], "East": q["East"], "South": q["South"], "West": q["West"],
        "Green": next_signal, "Vehicles served": st.session_state.served,
        "Cumulative waiting (vehicle-steps)": st.session_state.total_wait
    })
    st.session_state.history = st.session_state.history[-80:]

def reset_simulation():
    st.session_state.queues = {"North": 5, "East": 2, "South": 4, "West": 1}
    st.session_state.green = "North"
    st.session_state.elapsed = 0
    st.session_state.total_wait = 0
    st.session_state.served = 0
    st.session_state.history = []
    st.session_state.last_action = "Simulation reset"
    st.session_state.running = False

with st.sidebar:
    st.header("⚙️ Simulation controls")
    arrival_rate = st.slider("Traffic arrival probability (%)", 5, 90, 35, 5)
    st.caption("Higher values create busier roads.")
    if st.button("▶️ Run one AI step", use_container_width=True):
        step_simulation(arrival_rate)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚗 Add traffic", use_container_width=True):
            side = random.choice(SIDES)
            st.session_state.queues[side] = min(24, st.session_state.queues[side] + random.randint(3, 6))
            st.session_state.last_action = f"Manual traffic injected on {side}"
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            reset_simulation()
    st.markdown("---")
    st.markdown("**Try this demo**")
    st.markdown("1. Click **Run one AI step** several times.\\n2. Watch the green signal follow the busiest queue.\\n3. Add traffic to create a new bottleneck.\\n4. Compare queues and vehicles served.")

q = st.session_state.queues
green = st.session_state.green
avg_queue = sum(q.values()) / 4
c1, c2, c3, c4 = st.columns(4)
c1.metric("🟢 Active green", green)
c2.metric("🚙 Vehicles waiting", sum(q.values()))
c3.metric("✅ Vehicles served", st.session_state.served)
c4.metric("⏱️ Simulation steps", st.session_state.elapsed)

left, right = st.columns([1.25, 1])
with left:
    st.subheader("Intersection — live view")
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor("#0b1728")
    ax.set_facecolor("#183044")
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.axis("off")
    # roads
    road = "#374151"
    ax.add_patch(Rectangle((36, 0), 28, 100, color=road))
    ax.add_patch(Rectangle((0, 36), 100, 28, color=road))
    # road markings
    for y in range(2, 100, 10):
        ax.plot([49,49], [y,y+5], color="#f8fafc", lw=1.4, alpha=.75)
        ax.plot([51,51], [y,y+5], color="#f8fafc", lw=1.4, alpha=.75)
    for x in range(2, 100, 10):
        ax.plot([x,x+5], [49,49], color="#f8fafc", lw=1.4, alpha=.75)
        ax.plot([x,x+5], [51,51], color="#f8fafc", lw=1.4, alpha=.75)
    # center intersection
    ax.add_patch(Rectangle((36,36),28,28,color="#475569"))
    # signal boxes and queues; cars are small rounded-looking rectangles
    placements = {
        "North": {"xy":(43,67), "dx":7, "dy":3.5, "vertical":True, "signal":(68,74)},
        "South": {"xy":(43,19), "dx":7, "dy":3.5, "vertical":True, "signal":(68,23)},
        "West": {"xy":(7,43), "dx":3.5, "dy":7, "vertical":False, "signal":(24,68)},
        "East": {"xy":(67,43), "dx":3.5, "dy":7, "vertical":False, "signal":(74,68)},
    }
    for side, p in placements.items():
        active = side == green
        sx, sy = p["signal"]
        ax.add_patch(Circle((sx,sy), 4.3, color="#111827", ec="#94a3b8", lw=1.2, zorder=5))
        ax.add_patch(Circle((sx,sy), 2.2, color=("#22c55e" if active else "#ef4444"), zorder=6))
        ax.text(sx, sy-7, "GREEN" if active else "RED", color=("#86efac" if active else "#fca5a5"),
                fontsize=8, ha="center", weight="bold")
        count = q[side]
        for i in range(min(count, 12)):
            if side == "North":
                x, y = 42 + (i % 2)*8, 88 - (i//2)*5
                w,h=5,3
            elif side == "South":
                x, y = 42 + (i % 2)*8, 8 + (i//2)*5
                w,h=5,3
            elif side == "West":
                x, y = 8 + (i//2)*5, 42 + (i%2)*8
                w,h=3,5
            else:
                x, y = 88 - (i//2)*5, 42 + (i%2)*8
                w,h=3,5
            ax.add_patch(Rectangle((x,y),w,h,color=COLORS[side], ec="#e2e8f0", lw=.5, zorder=4))
        label_xy = {"North":(50,96),"South":(50,3),"West":(4,50),"East":(96,50)}[side]
        ax.text(*label_xy, f"{side}: {count}", color="#f8fafc", fontsize=9, ha="center", weight="bold")
    ax.text(50, 50, "AI", color="white", fontsize=15, weight="bold", ha="center", va="center",
            bbox=dict(boxstyle="round,pad=.35", facecolor="#0f766e", edgecolor="#99f6e4"))
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    st.caption("Colored cars represent waiting vehicles (up to 12 drawn per road). The green signal marks the approach selected by the AI.")

with right:
    st.subheader("🧠 Agent decision")
    st.markdown(f"""
    <div class="metric-card">
      <div style="font-size:.85rem;color:#93c5fd;">CURRENT OBSERVATION</div>
      <h3 style="margin:.25rem 0;">N {q['North']} · E {q['East']} · S {q['South']} · W {q['West']}</h3>
      <div style="color:#cbd5e1;">The agent compares the queue length on all four approaches.</div>
      <hr style="border-color:#29485d"/>
      <div style="font-size:.85rem;color:#5eead4;">ACTION</div>
      <h3 style="margin:.25rem 0;">Give green to {green}</h3>
      <div style="color:#cbd5e1;">{st.session_state.last_action}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("#### Queue lengths")
    for side in SIDES:
        st.write(f"**{side}** — {q[side]} vehicles")
        st.progress(min(q[side] / 24, 1.0), text=f"{q[side]} / 24")
    st.markdown("#### Performance indicators")
    st.metric("Average queue length", f"{avg_queue:.1f} vehicles")
    st.metric("Cumulative waiting", f"{st.session_state.total_wait} vehicle-steps")
    st.info("This is a teaching simulation, not a certified real-world traffic-control system.")

st.markdown("---")
st.subheader("📈 Performance over time")
if st.session_state.history:
    import pandas as pd
    hist = pd.DataFrame(st.session_state.history)
    chart_col, table_col = st.columns([1.1, 1])
    with chart_col:
        st.line_chart(hist.set_index("Step")[["North","East","South","West"]], height=260)
        st.caption("Queue lengths change as vehicles arrive and the active green direction serves traffic.")
    with table_col:
        st.line_chart(hist.set_index("Step")[["Vehicles served","Cumulative waiting (vehicle-steps)"]], height=260)
        st.dataframe(hist.tail(8), use_container_width=True, hide_index=True)
else:
    st.caption("Run a few steps to generate live queue and performance charts.")

with st.expander("🧩 How this demonstrates AI"):
    st.markdown("""
    - **Environment:** A simulated four-way intersection.
    - **Agent:** The adaptive traffic controller.
    - **Percepts/state:** Queue lengths on North, East, South and West.
    - **Actions:** Select which approach receives the green signal.
    - **Policy:** Give priority to the approach with the largest queue (a simple state-based heuristic).
    - **Performance measures:** Vehicles served, average queue length and cumulative waiting.

    This is a simplified heuristic controller, not a trained machine-learning model. A real deployment would require safety constraints, pedestrian phases, sensor validation, fairness controls and extensive testing.
    """)
