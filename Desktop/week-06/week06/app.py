from dash import Dash, dcc, html, dash_table, Input, Output
import pandas as pd
import plotly.express as px
import os
import webbrowser

# CSV in the same folder as app.py
CSV_PATH = "gyroscope_clean.csv"

# Check if the file exists
if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"CSV file not found: {CSV_PATH}. Please make sure it's in the same folder as app.py.")

df = pd.read_csv(CSV_PATH)

# Convert timestamp if necessary
if "timestamp" not in df.columns and "timestamp_ms" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp_ms"], unit="ms", errors="coerce")

AXES = [c for c in ["x", "y", "z"] if c in df.columns]
idx_col = "timestamp"

app = Dash(__name__)
app.title = "SIT225 – Gyroscope Dashboard"

app.layout = html.Div([
    html.H2("Gyroscope Dashboard"),
    html.Div([
        dcc.Dropdown(
            id="chart-type",
            options=[
                {"label":"Line","value":"line"},
                {"label":"Scatter","value":"scatter"},
                {"label":"Distribution","value":"hist"}
            ],
            value="line",
            clearable=False
        ),
        dcc.Dropdown(
            id="vars",
            options=[{"label":v.upper(),"value":v} for v in AXES],
            value=AXES,
            multi=True
        ),
        dcc.Input(
            id="n-samples",
            type="number",
            value=min(1000, len(df)),
            min=50,
            step=50
        ),
    ], style={"display":"grid","gridTemplateColumns":"1fr 1fr 1fr","gap":"12px"}),
    html.Div([
        html.Button("◀ Previous", id="prev", n_clicks=0),
        html.Button("Next ▶", id="next", n_clicks=0),
        html.Div(id="page-info")
    ], style={"marginTop":8, "display":"flex","gap":"8px"}),
    dcc.Graph(id="graph"),
    html.H4("Summary (current view)"),
    dash_table.DataTable(
        id="summary",
        style_table={"overflowX":"auto"},
        style_cell={"textAlign":"center","padding":"6px"}
    )
])

@app.callback(
    Output("graph","figure"),
    Output("summary","data"),
    Output("summary","columns"),
    Output("page-info","children"),
    Input("chart-type","value"),
    Input("vars","value"),
    Input("n-samples","value"),
    Input("prev","n_clicks"),
    Input("next","n_clicks"),
)
def update(chart_type, vars_selected, n_samples, n_prev, n_next):
    vars_selected = vars_selected or AXES
    n_samples = int(n_samples) if (n_samples and n_samples > 0) else len(df)

    page = (n_next or 0) - (n_prev or 0)
    total_pages = max((len(df)-1) // max(n_samples,1), 0)
    page = max(0, min(page, total_pages))

    start = page * n_samples
    end = min(start + n_samples, len(df))
    view = df.iloc[start:end].copy()

    if chart_type == "hist":
        long = view[vars_selected].melt(var_name="axis", value_name="value")
        fig = px.histogram(long, x="value", color="axis", barmode="overlay", nbins=50)
    else:
        long = view[[idx_col] + vars_selected].melt(id_vars=idx_col, var_name="axis", value_name="value")
        fig = px.scatter(long, x=idx_col, y="value", color="axis") if chart_type=="scatter" \
            else px.line(long, x=idx_col, y="value", color="axis")

    stats = view[vars_selected].agg(["count","mean","std","min","max"]).round(3).reset_index().rename(columns={"index":"metric"})
    cols = [{"name":"metric","id":"metric"}] + [{"name":v.upper(),"id":v} for v in vars_selected]
    page_text = f"Page {page+1} of {total_pages+1}  |  Rows {start}–{end-1} / {len(df)}"

    return fig, stats.to_dict("records"), cols, page_text

if __name__ == "__main__":
    # Open browser automatically
    webbrowser.open("http://127.0.0.1:8050/")
    app.run(debug=True, use_reloader=False)
