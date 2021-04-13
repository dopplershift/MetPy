FROM mcr.microsoft.com/vscode/devcontainers/miniconda:0-3

# [Option] Install Node.js
ARG INSTALL_NODE="true"
ARG NODE_VERSION="lts/*"
RUN if [ "${INSTALL_NODE}" = "true" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

COPY ci/*.txt /tmp/conda-tmp
RUN /opt/conda/bin/conda install --quiet --yes --file /tmp/conda-tmp/ci/test_requirements.txt --file /tmp/conda-tmp/ci/extra_requirements.txt --file /tmp/conda-tmp/ci/requirements.txt --file /tmp/conda-tmp/ci/linting_requirements.txt --file /tmp/conda-tmp/ci/doc_requirements.txt

