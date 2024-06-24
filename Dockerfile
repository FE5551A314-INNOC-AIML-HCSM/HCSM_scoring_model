# Use a base image with Python 3.10 and pip installed
FROM python:3.10-slim

# Accept arguments for GitHub and ngrok
ARG GITHUB_REPO=""
ARG GITHUB_BRANCH="main"
ARG GITHUB_USERNAME=""
ARG GITHUB_TOKEN=""
ARG GITHUB_EMAIL=""
ARG NGROK_AUTHTOKEN=""

# Set environment variables
ENV NGROK_AUTHTOKEN=${NGROK_AUTHTOKEN}

# Install basic dependencies
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    git \
    python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install --no-cache-dir jupyter ipython jupyter-server-proxy pyngrok

# Clone the GitHub repository
WORKDIR /content
RUN if [ ! -z "$GITHUB_REPO" ]; then \
      git clone --branch $GITHUB_BRANCH https://$GITHUB_USERNAME:$GITHUB_TOKEN@$GITHUB_REPO repo && \
      cd repo && \
      git config user.name "$GITHUB_USERNAME" && \
      git config user.email "$GITHUB_EMAIL"; \
    fi

# Copy your notebook and the script into the /content/repo directory
COPY Technical_Notebook.ipynb /content/repo/Technical_Notebook.ipynb
COPY run_jupyter_with_ngrok.py /content/repo/run_jupyter_with_ngrok.py

# Set the working directory
WORKDIR /content/repo

# Install additional dependencies for the notebook
RUN pip3 install --no-cache-dir notebook

# Expose the default port for Jupyter
EXPOSE 8888

# Command to start the Jupyter server with ngrok
CMD ["python3", "run_jupyter_with_ngrok.py"]
