
import streamlit as st
import plotly.graph_objects as go

# Page configuration
st.set_page_config(page_title="Internet Speed Test", layout="centered")

# Sleek, dark theme CSS
page_bg = """
<style>
.stApp {
  background-color: #0E1117;
  color: #fafafa;
}
div.block-container {
    padding-top: 2rem;
    padding-left: 2rem;
    padding-right: 2rem;
    padding-bottom: 2rem;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

st.title("🚀 Ad-Free Internet Speed Test")
st.write("This app tests your internet speed without ads and shows live gauges for download and upload speeds.")

# State to hold results between runs
if 'results' not in st.session_state:
    st.session_state['results'] = None

if st.button('Start Test'):
    with st.spinner('Testing... This may take a while.'):
        try:
            import speedtest
        except Exception as e:
            st.error(f"speedtest module not found: {e}. Please install via `pip install speedtest-cli`.")
        else:
            try:
                stt = speedtest.Speedtest()
                stt.get_best_server()
                dl = stt.download()
                ul = stt.upload()
                ping = stt.results.ping
                dl_mbps = dl / 1e6
                ul_mbps = ul / 1e6
                results_dict = stt.results.dict()
                st.session_state['results'] = {
                    'download': dl_mbps,
                    'upload': ul_mbps,
                    'ping': ping,
                    'client': results_dict.get('client', {}),
                    'server': results_dict.get('server', {}),
                }
            except Exception as e:
                st.error(f"Error running speedtest: {e}")

if st.session_state['results']:
    res = st.session_state['results']
    dl_val = res['download']
    ul_val = res['upload']
    ping_val = res['ping']

    fig_dl = go.Figure(go.Indicator(
        mode="gauge+number",
        value=dl_val,
        title={'text': "Download speed (Mb/s)"},
        gauge={'axis': {'range': [None, max(dl_val*1.5, 100)]}, 'bar': {'color': "#00c2f0"}}
    ))
    fig_ul = go.Figure(go.Indicator(
        mode="gauge+number",
        value=ul_val,
        title={'text': "Upload speed (Mb/s)"},
        gauge={'axis': {'range': [None, max(ul_val*1.5, 100)]}, 'bar': {'color': "#ff7f50"}}
    ))

    st.plotly_chart(fig_dl, use_container_width=True)
    st.write("*Download speed tells you how fast you can get stuff from the internet, like videos or games. Bigger numbers mean things load quicker!")
    st.plotly_chart(fig_ul, use_container_width=True)
    st.write("*Upload speed tells you how fast you can send stuff to the internet, like photos or messages. Bigger numbers mean things send quicker!")
    st.write(f"**Ping:** {ping_val:.2f} ms")
    st.write("*Ping measures how quickly a signal goes to the server and back, like the echo time in a canyon. Smaller numbers mean less delay, which is great for games!")

    st.subheader("Client info (you)")
    client = res['client']
    if client:
        st.write(f"IP (your internet address): {client.get('ip', 'N/A')}")
        st.write("*Your IP address is like your computer's house number on the internet. It helps other computers know where to send information.")
        st.write(f"ISP (your internet helper): {client.get('isp', 'N/A')}")
        st.write("*Your ISP is the company that gives you internet, like your internet helper provider.")
        st.write(f"Country: {client.get('country', 'N/A')}")

    st.subheader("Server info (tester)")
    server = res['server']
    if server:
        st.write(f"Host: {server.get('host', 'N/A')}")
        st.write("*Host is the computer we use to test your speed. It's like picking a referee for a game.")
        st.write(f"Sponsor: {server.get('sponsor', 'N/A')}")
        st.write("*Sponsor tells who lets us use this testing computer.")
        st.write(f"Country: {server.get('country', 'N/A')}")
        st.write(f"Latency (ms): {server.get('latency', 'N/A')}")
        st.write("*Latency is another word for ping specific to the server. Smaller values are better!")

    st.write('---')
    st.subheader('Raw Results')
    st.json(res)

st.markdown('---')
st.write('Built with ❤️ using Streamlit and speedtest-cli.')
