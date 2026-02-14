import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ================= CONFIG =================
st.set_page_config(
    page_title="Dashboard Kuesioner",
    layout="wide"
)

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    .main {
        background-color: #fff6fb;
    }
    h1, h2, h3 {
        color: #b565a7;
    }
</style>
""", unsafe_allow_html=True)

# ================= LOAD DATA =================
df = pd.read_excel("data_kuesioner.xlsx")
questions = [f"Q{i}" for i in range(1,18)]

score_map = {
    "SS":6, "S":5, "CS":4,
    "CTS":3, "TS":2, "STS":1
}
color_map = {
    "SS":"#f9afdf",   # soft pink
    "S":"#f6a3d9",
    "CS":"#ffccf1",   # lavender
    "CTS":"#ffd6cc",  # peach
    "TS":"#ffc5f4",
    "STS":"#ff6fc8"
}

# ================= SIDEBAR =================
st.sidebar.title("🌸 Filter Dashboard")

selected_questions = st.sidebar.multiselect(
    "Pilih Pertanyaan",
    questions,
    default=questions
)

filtered_df = df[selected_questions]
filtered_answers = filtered_df.stack()

# ================= HEADER =================
st.title("🌸 Dashboard Analisis Kuesioner")
st.markdown("Visualisasi data kuesioner")

# ================= KPI =================
score_df = filtered_df.replace(score_map)
avg_total = score_df.mean().mean()

total_responden = len(df)
total_jawaban = len(filtered_answers)
skala_terbanyak = filtered_answers.value_counts().idxmax()

c1, c2, c3, c4 = st.columns(4)

c1.metric("Responden", total_responden)
c2.metric("Total Jawaban", total_jawaban)
c3.metric("Skala Dominan", skala_terbanyak)
c4.metric("Rata-rata Skor", f"{avg_total:.2f}")

st.divider()

# ================= GAUGE =================
st.subheader("💗 Tingkat Kepuasan")

fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=avg_total,
    gauge={
        'axis': {'range': [1,6]},
        'bar': {'color': "#ff85a2"},
        'steps': [
            {'range': [1,3], 'color': "#ffd6d6"},
            {'range': [3,4], 'color': "#ffe6f0"},
            {'range': [4,6], 'color': "#ffcce0"}
        ]
    }
))

st.plotly_chart(fig_gauge, use_container_width=True)

# ================= DISTRIBUSI =================
st.subheader("Distribusi Jawaban")

count_scale = filtered_answers.value_counts().reset_index()
count_scale.columns = ["Skala","Jumlah"]

col1, col2 = st.columns(2)

with col1:
    fig_bar = px.bar(
        count_scale,
        x="Skala",
        y="Jumlah",
        color="Skala",
        color_discrete_map=color_map
    )
    fig_bar.update_layout(plot_bgcolor="#fff6fb")
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    fig_pie = px.pie(
        count_scale,
        names="Skala",
        values="Jumlah",
        color="Skala",
        color_discrete_map=color_map
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ================= STACKED BAR =================
st.subheader("Distribusi per Pertanyaan")

stacked = filtered_df.apply(pd.Series.value_counts).fillna(0)
stacked = stacked.T

fig_stack = px.bar(
    stacked,
    barmode="stack",
    color_discrete_map=color_map
)
fig_stack.update_layout(plot_bgcolor="#fff6fb")

st.plotly_chart(fig_stack, use_container_width=True)

# ================= RATA-RATA =================
st.subheader("Rata-rata Skor")

avg_score = score_df.mean().reset_index()
avg_score.columns = ["Pertanyaan","Rata-rata"]

fig_avg = px.bar(
    avg_score,
    x="Pertanyaan",
    y="Rata-rata",
    color="Rata-rata",
    color_continuous_scale="RdPu"
)

st.plotly_chart(fig_avg, use_container_width=True)

# ================= HEATMAP =================
st.subheader("Heatmap Jawaban")

heatmap_data = filtered_df.apply(pd.Series.value_counts).fillna(0)

fig_heatmap = px.imshow(
    heatmap_data,
    text_auto=True,
    color_continuous_scale="RdPu"
)

st.plotly_chart(fig_heatmap, use_container_width=True)
