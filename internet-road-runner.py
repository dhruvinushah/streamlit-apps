import streamlit as st
import plotly.graph_objects as go
import time

# Page configuration
st.set_page_config(page_title="Ad-Free Internet Speed Test", layout="centered")

# Gradient background CSS
page_bg = """<style>
.stApp {
  background: linear-gradient(135deg, #667eea, #764ba2, #89f7fe);
  color: white;
}
div.block-container {
    padding-top: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
    padding-bottom: 2rem;
}
</style>"""
st.markdown(page_bg, unsafe_allow_html=True)

st.title("🚀 Ad-Free Internet Speed Test")
st.write("This app tests your internet speed without ads and shows live gauges for download and upload speeds.")

# Hold state for test results
if 'results' not in st.session_state:
    st.session_state['results'] = None

# Button to start test
if st.button('Start Test'):
    with st.spinner('Testing... This may take a while.'):
        try:
            import speedtest
        except Exception as e:
            st.error(f"speedtest module not found: {e}. Please install via `pip install speedtest-cli`.")
        else:
            try:
                stt = speedtest.Speedtest()
                # Get best server based on ping
                stt.get_best_server()
                # Perform download and upload tests
                dl = stt.download()
                ul = stt.upload()
                ping = stt.results.ping
                # Convert from bits/s to Mb/s
                dl_mbps = dl / 1e6
                ul_mbps = ul / 1e6
                # Retrieve results dictionary for further details
                results_dict = stt.results.dict()
                # Store to session
                st.session_state['results'] = {
                    'download': dl_mbps,
                    'upload': ul_mbps,
                    'ping': ping,
                    'client': results_dict.get('client', {}),
                    'server': results_dict.get('server', {}),
                }
            except Exception as e:
                st.error(f"Error running speedtest: {e}")

# If results available, display
if st.session_state['results']:
    res = st.session_state['results']
    dl_val = res['download']
    ul_val = res['upload']
    ping_val = res['ping']
    # Gauge for download
    fig_dl = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = dl_val,
        title = {'text': "Download (Mb/s)"},
        gauge = {'axis': {'range': [None, max(dl_val*1.5, 100)]},
                 'bar': {'color': "#3333ff"}}
    ))
    # Gauge for upload
    fig_ul = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = ul_val,
        title = {'text': "Upload (Mb/s)"},
        gauge = {'axis': {'range': [None, max(ul_val*1.5, 100)]},
                 'bar': {'color': "#ff5733"}}
    ))
    st.plotly_chart(fig_dl, use_container_width=True)
    st.plotly_chart(fig_ul, use_container_width=True)
    st.write(f"**Ping:** {ping_val:.2f} ms")
    # Show additional details
    st.subheader("Client info")
    client = res['client']
    if client:
        st.write(f"ISP: {client.get('isp', 'N/A')}")
        st.write(f"IP: {client.get('ip', 'N/A')}")
        st.write(f"Latitude: {client.get('lat', 'N/A')}")
        st.write(f"Longitude: {client.get('lon', 'N/A')}")
        st.write(f"Country: {client.get('country', 'N/A')}")
    st.subheader("Server info")
    server = res['server']
    if server:
        st.write(f"Host: {server.get('host', 'N/A')}")
        st.write(f"Sponsor: {server.get('sponsor', 'N/A')}")
        st.write(f"Country: {server.get('country', 'N/A')}")
        st.write(f"Latency: {server.get('latency', 'N/A')} ms")
    # Additional metrics: download/upload in bytes
    st.write("---")
    st.subheader("Raw Results")
    st.json(res)

# Footer
st.markdown("---")
st.write("Built with ❤️ using Streamlit and speedtest-cli.")
