﻿# Home Credit Default Risk

This project includes two main notebooks for exploratory analysis, feature engineering, and modeling of credit default risk data.

- [Notebook exploratory analysis and feature engineering](./Fusilier_Antoine_1_notebook_exploratory_analysis_and_cleaning_and_feature_enginering_022024.ipynb)
- [Notebook modelization](./Fusilier_Antoine_2_notebook_modelization_032024.ipynb)

## Prerequisites

Make sure you have the following installed on your machine before starting:

1. [Docker](https://docs.docker.com/get-docker/)
2. [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
3. [NVIDIA Docker Runtime](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html) (for GPU support, if needed)
4. [ngrok](https://dashboard.ngrok.com/signup) (sign up and get your authtoken)

## Instructions

### 1. Clone the repository

Start by cloning this repository to your local machine:

```sh
git clone https://github.com/lessons-data-ai-engineer/project_4-home_credit_default_risk.git
cd project_4-home_credit_default_risk
```

### 2. Build the Docker image

#### Build the image without GPU (classic)

To build the Docker image without GPU support, use the following command:

```sh
docker build -f Dockerfile `
             --build-arg GITHUB_REPO="github.com/lessons-data-ai-engineer/project_4-home_credit_default_risk.git" `
             --build-arg GITHUB_BRANCH="main" `
             --build-arg GITHUB_USERNAME="your-username" `
             --build-arg GITHUB_TOKEN="your_github_token" `
             --build-arg GITHUB_EMAIL="your-email@gmail.com" `
             --build-arg NGROK_AUTHTOKEN="your_ngrok_authtoken" `
             -t home_credit_default_risk .
```

#### Build the image with GPU support

To build the Docker image with GPU support, use the following command:

```sh
docker build -f Dockerfile.gpu `
             --build-arg GITHUB_REPO="github.com/lessons-data-ai-engineer/project_4-home_credit_default_risk.git" `
             --build-arg GITHUB_BRANCH="main" `
             --build-arg GITHUB_USERNAME="your-username" `
             --build-arg GITHUB_TOKEN="your_github

_token" `
             --build-arg GITHUB_EMAIL="your-email@gmail.com" `
             --build-arg NGROK_AUTHTOKEN="your_ngrok_authtoken" `
             -t home_credit_default_risk_gpu .
```

### 3. Run the Docker container

#### Run the image without GPU

To run the Docker container without GPU support, use the following command:

```sh
docker run -p 8888:8888 home_credit_default_risk
```

#### Run the image with GPU support

To run the Docker container with GPU support, use the following command:

```sh
docker run --gpus all -p 8888:8888 home_credit_default_risk_gpu
```

### 4. Access Jupyter Notebook

After starting the Docker container, open your browser and go to the following address to open Jupyter Notebook:

```
http://localhost:8888
```

### 5. Connect to Google Colab as a local runtime

To connect your Docker container to Google Colab as a local runtime, follow these steps:

1. In your Jupyter Notebook interface (opened at `http://localhost:8888`), find the token used for authentication. This token is part of the URL shown when you start Jupyter Notebook in your terminal. It looks something like this:
   ```
   http://127.0.0.1:8888/?token=some_long_token_value
   ```
2. Open Google Colab in your browser and go to `File > Connect to local runtime...`.
3. In the dialog that appears, enter the URL of your local Jupyter Notebook instance, including the token. For example:
   ```
   http://127.0.0.1:8888/?token=some_long_token_value
   ```
   Or
   ```
   http://127.0.0.1:8888/tree
   ```
4. Click the "Connect" button.

### 6. File Management

- Source files are mounted in the `/content/resources` directory.
- Files generated by the notebooks are stored in the `/content/exports` directory.

### Additional Documentation

- [Docker Documentation](https://docs.docker.com/)
- [NVIDIA Docker Documentation](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)
- [Jupyter Notebook Documentation](https://jupyter-notebook.readthedocs.io/en/stable/)
- [Google Colab Local Runtime Documentation](https://research.google.com/colaboratory/local-runtimes.html)

### Script to update the GitHub repository

You can use the following script to automate updating the GitHub repository from your Docker container. Run this script from your notebook by adding the following cell to the `Technical_Notebook.ipynb` notebook:

```python
import os
from subprocess import check_call, CalledProcessError

COMMIT_MESSAGE = "Update notebooks"

def git_add_commit_push():
    try:
        check_call(["git", "add", "."])
        check_call(["git", "commit", "-m", COMMIT_MESSAGE])
        check_call(["git", "push"])
    except CalledProcessError as e:
        print(f"Error during git operations: {e}")

def main():
    git_add_commit_push()

if __name__ == "__main__":
    main()
```

With these configurations, you can efficiently manage your notebooks, leverage GPU resources for intensive tasks, connect to Google Colab as a local runtime, and keep your repository up to date easily.