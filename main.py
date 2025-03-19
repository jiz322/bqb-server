import yaml
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import torch
import torch.nn.functional as F
from gme_inference import GmeQwen2VL

# Utility function to load configuration from a YAML file
def load_config(config_file="config.yaml"):
    with open(config_file, "r") as f:
        return yaml.safe_load(f)

# Load configuration
config = load_config()

# Extract configuration parameters
gme_path = config.get("gme_path")
embedding_dict_path = config.get("embedding_dict_path")
device = config.get("device", "cpu")

# Initialize and prepare the model using the config parameters
gme = GmeQwen2VL(gme_path, device=device)
gme.base.model = gme.base.model.float()  # Convert parameters to float32

# Load the embeddings dictionary once at startup
try:
    embeddings_dict = torch.load(embedding_dict_path, map_location="cpu")
except Exception as e:
    raise RuntimeError(f"Failed to load embeddings dictionary: {e}")

def find_top_k_similar_text(
    text_embedding, 
    embeddings_dict,
    k=5,
    similarity_type="dot"
):
    """
    Given a text embedding, compute similarities with image embeddings 
    from embeddings_dict and return the top-k matches.
    """
    similarities = []
    for file_path, img_embedding in embeddings_dict.items():
        # Ensure the image embedding is at least 2D
        if len(img_embedding.shape) == 1:
            img_embedding = img_embedding.unsqueeze(0)
        img_embedding = img_embedding.to(torch.float32).cpu()

        if similarity_type == "cosine":
            # Normalize both embeddings
            text_norm = F.normalize(text_embedding, p=2, dim=-1)
            img_norm = F.normalize(img_embedding, p=2, dim=-1)
            sim = torch.mm(text_norm, img_norm.transpose(0, 1))
            similarity_score = sim.item()
        elif similarity_type == "dot":
            sim = torch.mm(text_embedding, img_embedding.transpose(0, 1))
            similarity_score = sim.item()
        else:
            raise ValueError(f"Unknown similarity type: {similarity_type}")

        similarities.append((file_path, similarity_score))
    
    # Sort by similarity descending and return top-k results
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:k]

# Request and response models for FastAPI
class SimilarityRequest(BaseModel):
    text: str
    k: int = 5
    similarity_type: str = "cosine"

class SimilarityResponse(BaseModel):
    results: list

app = FastAPI()

@app.post("/search_k", response_model=SimilarityResponse)
def get_similar_images(req: SimilarityRequest):
    try:
        # Prepare the text for the model
        query = f'given text: "{req.text}"'
        instruction = "Find a expressive image that matches the given text."
        text_embeddings = gme.get_text_embeddings(texts=[query], instruction=instruction)
        top_k_results = find_top_k_similar_text(
            text_embedding=text_embeddings, 
            embeddings_dict=embeddings_dict, 
            k=req.k, 
            similarity_type=req.similarity_type
        )
        return SimilarityResponse(results=top_k_results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
