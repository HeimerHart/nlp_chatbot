import kagglehub

# Download latest version
path = kagglehub.dataset_download("elvinagammed/chatbots-intent-recognition-dataset")

print("Path to dataset files:", path)