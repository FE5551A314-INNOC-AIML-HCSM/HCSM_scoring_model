# Models Folder

This folder stores saved model artifacts and metadata to track version history and manage production-ready models.

## Folder Structure
- `trained/`: Stores production-ready models along with metadata.
- `experiments/`: Holds models from various experiments.
- `registry/`: Tracks model versions, with `current_model.json` pointing to the active version.
- `serving/`: Contains models formatted for deployment (e.g., ONNX, TensorFlow SavedModel).
- `monitoring/`: Logs and metrics related to model performance in production.

## Guidelines
- **Model Metadata**: Each model should include a metadata file with training parameters and performance metrics.
- **Versioning**: Keep each model version in a dedicated folder to track history.
