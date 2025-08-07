# Deploying to Hugging Face Spaces

This document provides instructions for deploying this Streamlit application with Ollama to [Hugging Face Spaces](https://huggingface.co/spaces).

## Prerequisites

1. A Hugging Face account
2. This repository containing the Streamlit app
3. Basic knowledge of Docker and Streamlit

## Step 1: Create a New Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Choose a name for your Space
4. Select "Docker" as the Space SDK
5. Choose visibility (public or private)
6. Click "Create Space"

## Step 2: Configure the Space

The application is already set up to run in a Docker container on Hugging Face Spaces. Here are the key components:

1. **Dockerfile**: Contains the setup for Python, necessary dependencies, and Ollama installation
2. **startup.sh**: Script that starts both Ollama and the Streamlit app
3. **streamlit/ollama_setup.py**: Contains logic to handle Ollama initialization

## Step 3: Push Your Code to the Space

You can push your code to the Space using Git:

```bash
# Clone the Space repository (replace with your Space name)
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME

# Copy your application files to the cloned repository
cp -r * YOUR_SPACE_NAME/

# Navigate to the Space directory
cd YOUR_SPACE_NAME

# Add all files
git add .

# Commit
git commit -m "Initial commit with Ollama Streamlit app"

# Push to Hugging Face
git push
```

Alternatively, you can use the Hugging Face web interface to upload your files directly.

## Step 4: Check Build Status

1. Navigate to your Space on Hugging Face
2. Click on "Settings" then "Repository"
3. Monitor the build logs for any issues

## Understanding the Ollama Setup

The application uses a custom setup to run Ollama in Hugging Face Spaces:

1. The Dockerfile downloads a specific version of Ollama (v0.11.3) directly from GitHub
2. The startup script runs Ollama in the background before starting Streamlit
3. The application is configured to connect to Ollama at the correct address

## Troubleshooting

### Common Issues:

1. **Build Fails**: Check the Dockerfile and ensure all dependencies are correctly specified.

2. **Ollama Not Starting**: Look at the logs to see if there are any errors during Ollama initialization. 
   The app is configured to continue even if there are issues with Ollama.

3. **Model Download Timeout**: Downloading models can take time in Hugging Face Spaces. The app 
   will try to continue even if the model download times out.

4. **Memory Issues**: Ollama requires significant memory to run models. Ensure your Space has 
   enough resources allocated.

## Customization

To use a different model:

1. Update the model name in `streamlit/ollama_setup.py` 
2. Also update it in `streamlit/streamlit_app.py` where the OllamaProvider is initialized

## Security Considerations

The Dockerfile is configured to run the application as a non-root user for security. 
The Ollama binary is installed in a system location and is owned by the app user.