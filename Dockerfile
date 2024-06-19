# Utilisez une image de base avec Python 3 et pip installés
FROM python:3.9-slim

# Accepter des arguments pour les fichiers resources et exports
ARG RESOURCES_URL=""
ARG EXPORTS_URL=""

# Installez les dépendances de Jupyter
RUN pip install --no-cache-dir jupyter

# Créez les répertoires nécessaires
RUN mkdir -p /content/resources /content/exports

# Si RESOURCES_URL est spécifié, téléchargez et extrayez les fichiers
RUN if [ ! -z "$RESOURCES_URL" ]; then \
      apt-get update && apt-get install -y wget unzip && \
      wget -O /tmp/resources.zip "$RESOURCES_URL" && \
      unzip /tmp/resources.zip -d /content/resources && \
      rm /tmp/resources.zip && \
      apt-get clean && rm -rf /var/lib/apt/lists/*; \
    fi

# Si EXPORTS_URL est spécifié, téléchargez et extrayez les fichiers
RUN if [ ! -z "$EXPORTS_URL" ]; then \
      apt-get update && apt-get install -y wget unzip && \
      wget -O /tmp/exports.zip "$EXPORTS_URL" && \
      unzip /tmp/exports.zip -d /content/exports && \
      rm /tmp/exports.zip && \
      apt-get clean && rm -rf /var/lib/apt/lists/*; \
    fi

# Copiez votre notebook dans le répertoire /content
COPY Fusilier_Antoine_1_notebook_exploratory_analysis_and_cleaning_and_feature_enginering_022024.ipynb /content/Fusilier_Antoine_1_notebook_exploratory_analysis_and_cleaning_and_feature_enginering_022024.ipynb
COPY Fusilier_Antoine_2_notebook_modelization_032024.ipynb /content/Fusilier_Antoine_2_notebook_modelization_032024.ipynb
COPY Technical_Notebook.ipynb /content/Technical_Notebook.ipynb

# Définissez le répertoire de travail
WORKDIR /content

# Exposez le port par défaut de Jupyter
EXPOSE 8888

# Commande pour démarrer le serveur Jupyter
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
