import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Used Car Fair Price Range", layout="wide")

st.title("Used Car Fair Price Range")
st.caption("Quantile-based fair pricing (Q25 / Q50 / Q75) using a FastAPI backend.")

def api_health() -> bool:
    try:
        r = requests.get(f"{API_URL}/health", timeout=3)
        return r.status_code == 200
    except Exception:
        return False

def format_gbp(x: int) -> str:
    return f"£{x:,}"

with st.sidebar:
    st.header("Vehicle Details")

    with st.form("predict_form"):
        car_model = st.text_input("Model", value="Clio", help="Examples: Clio, A3, A1, Q3")
        year = st.number_input("Year", min_value=1990, max_value=2026, value=2018, step=1)
        km = st.number_input("Mileage (km)", min_value=0, value=85000, step=1000)

        fuel = st.selectbox("Fuel", ["Petrol", "Diesel", "Hybrid", "Electric"], index=0)
        transmission = st.selectbox("Transmission", ["Manual", "Automatic", "Semi-Auto"], index=0)

        tax = st.number_input("Tax", min_value=0, value=150, step=10)
        mpg = st.number_input("MPG", min_value=0.0, value=55.4, step=0.1, format="%.1f")
        engine_size = st.number_input("Engine Size (L)", min_value=0.0, value=1.2, step=0.1, format="%.1f")

        show_payload = st.checkbox("Show request payload", value=False)
        submitted = st.form_submit_button("Predict Price Range")

status_ok = api_health()
st.sidebar.markdown(
    f"**API status:** {'🟢 Online' if status_ok else '🔴 Offline'}  \n"
    f"**API URL:** `{API_URL}`"
)

if "result" not in st.session_state:
    st.session_state.result = None
if "last_payload" not in st.session_state:
    st.session_state.last_payload = None

col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("Result")

    if submitted:
        if not status_ok:
            st.error("FastAPI is not reachable. Start the API first and try again.")
        elif not car_model.strip():
            st.error("Model cannot be empty.")
        else:
            payload = {
                "car_model": car_model.strip(),
                "year": int(year),
                "km": int(km),
                "fuel": fuel,
                "transmission": transmission,
                "tax": int(tax),
                "mpg": float(mpg),
                "engineSize": float(engine_size),
            }

            with st.spinner("Requesting prediction..."):
                try:
                    r = requests.post(f"{API_URL}/predict", json=payload, timeout=20)
                    if r.status_code != 200:
                        st.error(f"API Error {r.status_code}")
                        st.code(r.text)
                        st.session_state.result = None
                        st.session_state.last_payload = payload
                    else:
                        data = r.json()
                        st.session_state.result = data.get("price_range")
                        st.session_state.last_payload = payload
                except requests.exceptions.Timeout:
                    st.error("Request timed out. The API may be busy or not responding.")
                    st.session_state.result = None
                    st.session_state.last_payload = payload
                except requests.exceptions.ConnectionError:
                    st.error("Connection error. FastAPI may not be running.")
                    st.session_state.result = None
                    st.session_state.last_payload = payload
                except Exception as e:
                    st.error(f"Unexpected error: {e}")
                    st.session_state.result = None
                    st.session_state.last_payload = payload

    pr = st.session_state.result
    if pr:
        min_v = int(pr["min"])
        rec_v = int(pr["recommended"])
        max_v = int(pr["max"])
        currency = pr.get("currency", "GBP")

        m1, m2, m3 = st.columns(3)
        m1.metric("Min (Q25)", format_gbp(min_v))
        m2.metric("Recommended (Q50)", format_gbp(rec_v))
        m3.metric("Max (Q75)", format_gbp(max_v))

        st.caption(f"Currency: {currency}")

        st.divider()
        st.markdown(
            "**How to read this range**\n"
            "- **Min (Q25):** More conservative pricing (faster sale)\n"
            "- **Recommended (Q50):** Median fair price\n"
            "- **Max (Q75):** More optimistic pricing"
        )

        spread = max_v - min_v
        st.info(f"Range width: {format_gbp(spread)}")

        if show_payload and st.session_state.last_payload:
            st.divider()
            st.subheader("Request payload")
            st.code(st.session_state.last_payload, language="json")
    else:
        st.write("Submit the form to get a price range.")

with col_right:
    st.subheader("Quick Examples")

    st.write("Use these example inputs in the sidebar:")

    ex1 = {
        "car_model": "Clio",
        "year": 2018,
        "km": 85000,
        "fuel": "Petrol",
        "transmission": "Manual",
        "tax": 150,
        "mpg": 55.4,
        "engineSize": 1.2,
    }

    ex2 = {
        "car_model": "A3",
        "year": 2012,
        "km": 165000,
        "fuel": "Diesel",
        "transmission": "Manual",
        "tax": 30,
        "mpg": 65.0,
        "engineSize": 1.6,
    }

    st.code(ex1, language="json")
    st.code(ex2, language="json")

    st.divider()
    st.subheader("API Links")
    st.write(f"Swagger UI: {API_URL}/docs")
    st.write(f"Health: {API_URL}/health")
