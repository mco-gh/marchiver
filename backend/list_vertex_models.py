import os
import sys
from google.cloud import aiplatform

def list_available_models():
    """List all available models in the Vertex AI project."""
    # Get project and region from environment variables or use defaults
    project = os.environ.get("GOOGLE_CLOUD_PROJECT", "marchiver-5cb01")
    location = os.environ.get("GOOGLE_CLOUD_REGION", "us-central1")
    
    print(f"Listing models for project: {project}, location: {location}")
    
    try:
        # Initialize Vertex AI
        aiplatform.init(project=project, location=location)
        
        # List models
        models = aiplatform.Model.list()
        
        if not models:
            print("No custom models found in your project.")
            print("Checking for available public models...")
            
            # Try to list public models (this might not work directly)
            try:
                from vertexai.language_models import TextEmbeddingModel, TextGenerationModel
                
                # Try to get available embedding models
                print("\nAttempting to list available embedding models:")
                embedding_models = [
                    "textembedding-gecko",
                    "textembedding-gecko-multilingual",
                    "text-embedding-004",
                    "text-embedding-003",
                    "text-embedding-002",
                    "text-embedding-001"
                ]
                
                for model_name in embedding_models:
                    try:
                        print(f"Checking model: {model_name}")
                        model = TextEmbeddingModel.from_pretrained(model_name)
                        print(f"✓ Model {model_name} is available")
                    except Exception as e:
                        print(f"✗ Model {model_name} is not available: {str(e)}")
                
                # Try to get available text generation models
                print("\nAttempting to list available text generation models:")
                generation_models = [
                    "gemini-1.0-pro",
                    "gemini-1.5-pro",
                    "text-bison",
                    "chat-bison"
                ]
                
                for model_name in generation_models:
                    try:
                        print(f"Checking model: {model_name}")
                        model = TextGenerationModel.from_pretrained(model_name)
                        print(f"✓ Model {model_name} is available")
                    except Exception as e:
                        print(f"✗ Model {model_name} is not available: {str(e)}")
                
            except Exception as e:
                print(f"Error listing public models: {e}")
        else:
            print(f"Found {len(models)} custom models in your project:")
            for model in models:
                print(f"- {model.display_name} (ID: {model.name})")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_available_models()
