<<<<<<< HEAD
#!/usr/bin/env python

import os
import subprocess
from pyngrok import ngrok

# Ensure NGROK_AUTHTOKEN is set
authtoken = os.getenv("NGROK_AUTHTOKEN")
if not authtoken:
    raise ValueError("NGROK_AUTHTOKEN environment variable is not set")

# Set your ngrok authtoken
ngrok.set_auth_token(authtoken)

# Start ngrok tunnel
public_url = ngrok.connect(8888)
print(f"ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:8888\"")

# Print the ngrok URL for easy access
print(f"\nOpen the following URL in Google Colab to connect to the local runtime:\n{public_url}\n")

# Run Jupyter Notebook
cmd = [
    "jupyter", "notebook",
    "--ip=0.0.0.0",
    "--port=8888",
    "--no-browser",
    "--allow-root",
    "--NotebookApp.allow_origin='https://colab.research.google.com'",
    "--NotebookApp.disable_check_xsrf=True",
    "--NotebookApp.port_retries=0",
    "--NotebookApp.token=''",
    "--NotebookApp.password=''"
]
subprocess.run(cmd)
=======
#!/usr/bin/env python

import os
import subprocess
from pyngrok import ngrok

# Ensure NGROK_AUTHTOKEN is set
authtoken = os.getenv("NGROK_AUTHTOKEN")
if not authtoken:
    raise ValueError("NGROK_AUTHTOKEN environment variable is not set")

# Set your ngrok authtoken
ngrok.set_auth_token(authtoken)

# Start ngrok tunnel
public_url = ngrok.connect(8888)
print(f"ngrok tunnel \"{public_url}\" -> \"http://127.0.0.1:8888\"")

# Print the ngrok URL for easy access
print(f"\nOpen the following URL in Google Colab to connect to the local runtime:\n{public_url}\n")

# Run Jupyter Notebook
cmd = [
    "jupyter", "notebook",
    "--ip=0.0.0.0",
    "--port=8888",
    "--no-browser",
    "--allow-root",
    "--NotebookApp.allow_origin='https://colab.research.google.com'",
    "--NotebookApp.disable_check_xsrf=True",
    "--NotebookApp.port_retries=0",
    "--NotebookApp.token=''",
    "--NotebookApp.password=''"
]
subprocess.run(cmd)
>>>>>>> 444966083723f2d939442650d10d3e3ee1b1a7a1
