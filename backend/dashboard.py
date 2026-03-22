import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="PhishGuard Admin Console", page_icon="🛡️")
st.title("🛡️ AI PhishGuard: Real-Time Monitoring")

# Mock data for the demo
if 'scan_count' not in st.session_state:
    st.session_state.scan_count = 0

col1, col2 = st.columns(2)
col1.metric("Total Scans", st.session_state.scan_count)
col2.metric("Threats Blocked", int(st.session_state.scan_count * 0.3))

st.write("### Recent Activity Log")
# In a real app, you'd pull this from a database
st.table(pd.DataFrame({
    'Timestamp': [time.strftime("%H:%M:%S")],
    'URL': ["https://secure-login-verify.com"],
    'Status': ["🔴 PHISHING"]
}))

if st.button("Refresh Stats"):
    st.session_state.scan_count += 1
    st.rerun()