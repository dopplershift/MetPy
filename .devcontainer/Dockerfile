FROM mcr.microsoft.com/vscode/devcontainers/miniconda:0-3

# [Option] Install Node.js
ARG INSTALL_NODE="true"
ARG NODE_VERSION="lts/*"
RUN if [ "${INSTALL_NODE}" = "true" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

COPY ci/*.txt /tmp/conda-tmp
RUN /opt/conda/bin/conda install --quiet --yes --file ci/test_requirements.txt --file ci/extra_requirements.txt --file ci/requirements.txt --file linting_requirements.txt --file doc_requirements.txt
