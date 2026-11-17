import os
import streamlit as st
import requests
import pandas as pd

TRACK_URL = os.getenv("TRACK_SERVICE_URL", "http://127.0.0.1:8001")
LISTENER_URL = os.getenv("LISTENER_SERVICE_URL", "http://127.0.0.1:8002")
STREAM_URL = os.getenv("STREAM_SERVICE_URL", "http://127.0.0.1:8003")

def api(method, url, **kwargs):
    try:
        r = requests.request(method, url, timeout=5, **kwargs)
        if r.status_code in (200, 201):
            return r.json(), None
        return None, r.json().get("detail", f"Error {r.status_code}")
    except requests.RequestException as e:
        return None, str(e)

st.set_page_config(page_title="Music App", layout="wide")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Tracks", "Listeners", "Stream Player"])

if page == "Dashboard":
    st.title("System Dashboard")
    status, err = api("GET", f"{STREAM_URL}/services/status")
    if err:
        st.error(f"Could not load status: {err}")
    else:
        cols = st.columns(3)
        for i, (svc, stat) in enumerate(status.items()):
            color = "green" if stat == "healthy" else "red"
            cols[i%3].markdown(f"### {svc}\n**Status:** :{color}[{stat}]")
            
elif page == "Tracks":
    st.title("Track Catalog")
    tracks, err = api("GET", f"{TRACK_URL}/tracks")
    if err:
        st.error(err)
    elif tracks:
        st.dataframe(pd.DataFrame(tracks))
    
    st.subheader("Add a Track")
    with st.form("add_track"):
        title = st.text_input("Title")
        artist = st.text_input("Artist")
        is_premium = st.checkbox("Premium Only?")
        if st.form_submit_button("Add"):
            res, e = api("POST", f"{TRACK_URL}/tracks", json={"title": title, "artist": artist, "is_premium_only": is_premium})
            if e:
                st.error(e)
            else:
                st.success("Added successfully! Refresh to see.")

elif page == "Listeners":
    st.title("Listeners")
    listeners, err = api("GET", f"{LISTENER_URL}/listeners")
    if err:
        st.error(err)
    elif listeners:
        st.dataframe(pd.DataFrame(listeners))
        
    st.subheader("Add a Listener")
    with st.form("add_listener"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        active = st.checkbox("Active Account", value=True)
        premium = st.checkbox("Premium Subscription")
        if st.form_submit_button("Add"):
            res, e = api("POST", f"{LISTENER_URL}/listeners", json={"name": name, "email": email, "active": active, "is_premium": premium})
            if e:
                st.error(e)
            else:
                st.success("Added successfully! Refresh to see.")

elif page == "Stream Player":
    st.title("Stream a Track")
    
    tracks, _ = api("GET", f"{TRACK_URL}/tracks")
    listeners, _ = api("GET", f"{LISTENER_URL}/listeners")
    
    if tracks and listeners:
        with st.form("stream_form"):
            listener_opt = {l["id"]: f"{l['name']} {'(Premium)' if l['is_premium'] else '(Free)'}" for l in listeners}
            track_opt = {t["id"]: f"{t['title']} by {t['artist']} {'[PREMIUM]' if t['is_premium_only'] else ''}" for t in tracks}
            
            l_id = st.selectbox("Select Listener", options=list(listener_opt.keys()), format_func=lambda x: listener_opt[x])
            t_id = st.selectbox("Select Track", options=list(track_opt.keys()), format_func=lambda x: track_opt[x])
            
            if st.form_submit_button("Play"):
                res, err = api("POST", f"{STREAM_URL}/stream", json={"listener_id": l_id, "track_id": t_id})
                if err:
                    st.error(f"Failed to play: {err}")
                else:
                    st.success(f"Now playing: {res['track']} for {res['listener']}!")
    
    st.subheader("Recent Streams")
    streams, err = api("GET", f"{STREAM_URL}/streams")
    if err:
        st.error(err)
    elif streams:
        st.dataframe(pd.DataFrame(streams))
