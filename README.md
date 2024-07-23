# Submission Dashboard

## Setup Environment

!pip install -q streamlit
!npm install localtunnel
!pip install pipreqs
pip freeze -> requirements.txt

## Run steamlit app
!streamlit run dashboard.py &>/content/logs.txt & npx localtunnel --port 8501 & curl ipv4.icanhazip.com
