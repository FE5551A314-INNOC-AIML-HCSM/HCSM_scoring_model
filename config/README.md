# Config Folder

This folder contains configuration files and environment variables to manage settings for various environments (development, production, testing).

## Folder Structure
- `settings.yaml`: Main configuration file with project-wide settings.
- `environment/`: Environment-specific configurations (e.g., `dev.env`, `prod.env`, `staging.env`).
- `secrets/`: Encrypted files with sensitive credentials (e.g., AWS keys, database passwords).

## Notes
- **Environment Separation**: Use environment-specific files to avoid mixing dev and production settings.
- **Security**: Store secrets encrypted and do not commit them to version control.
