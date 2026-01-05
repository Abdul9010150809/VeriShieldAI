import streamlit as st
import requests
import time

# TITLE AND CONFIG
st.set_page_config(page_title="VeriShield AI Defense", page_icon="🛡️", layout="wide")

st.title("🛡️ VeriShield AI: Sovereign Identity Defense")
st.markdown("### Agentic Fraud Prevention System")

# SIDEBAR - CONTROLS
st.sidebar.header("⚙️ Simulation Settings")
simulation_mode = st.sidebar.checkbox("Enable Deepfake Simulation", value=True)
st.sidebar.info("Connects to Agentic Core running on Port 8000")

# MAIN LAYOUT - TWO COLUMNS
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("💳 Transaction Terminal")
    user_id = st.text_input("User Identity", "Abdul_Student")
    amount = st.number_input("Transaction Amount ($)", min_value=1, value=500)
    
    st.markdown("**🎥 Biometric Verification**")
    
    # 1. REAL CAMERA INPUT
    camera_image = st.camera_input("Take a Snapshot to Verify")
    
    verify_btn = st.button("🛡️ Verify & Approve Transaction", type="primary")

    if verify_btn and camera_image is None:
        st.warning("⚠️ Please take a photo first!")

with col2:
    st.subheader("🧠 Agentic Brain Logs")
    log_container = st.empty()
    
    if verify_btn:
        # 1. SHOW LOADING ANIMATION
        with st.status("Agents Analyzing...", expanded=True) as status:
            st.write("💰 Finance Agent: Checking banking patterns...")
            time.sleep(1) # Fake delay for effect
            
            st.write("👁️ Vision Agent: Scanning for Deepfake artifacts...")
            time.sleep(1)
            
            st.write("🗣️ Challenge Bot: Verifying Liveness...")
            time.sleep(1)
            
            # 2. CALL THE REAL BACKEND API
            # 2. CALL THE REAL BACKEND API WITH FILE
            try:
                # Prepare the file for upload
                files = {"image_file": ("camera_capture.jpg", camera_image, "image/jpeg")}
                data = {"user_id": user_id, "amount": amount}
                
                response = requests.post(
                    "http://127.0.0.1:8000/verify", 
                    data=data,  # Send text data
                    files=files # Send image file
                )
                # 3. DISPLAY RESULT
                if response.status_code == 200:
                    status.update(label="✅ Access Granted", state="complete", expanded=False)
                    st.success("## TRANSACTION APPROVED")
                    st.json(response.json())
                else:
                    status.update(label="🚨 Access Denied", state="error", expanded=False)
                    st.error(f"## {response.json()['detail']}")
                    st.warning("Account Frozen due to Security Threat.")
            
            except Exception as e:
                st.error(f"❌ Connection Error: Is the Backend Running? \n\nError: {e}")

# FOOTER
st.markdown("---")
st.caption("VeriShield AI | RGUKT RKV | Agentic Security Protocol")