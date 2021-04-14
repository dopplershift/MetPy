FROM mcr.microsoft.com/vscode/devcontainers/miniconda:0-3

# [Option] Install Node.js
#ARG INSTALL_NODE="true"
#ARG NODE_VERSION="lts/*"
#RUN if [ "${INSTALL_NODE}" = "true" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

COPY ci/*.txt /tmp/conda-tmp/
RUN /opt/conda/bin/conda config --add channels conda-forge
RUN /opt/conda/bin/conda config --set channel_priority strict
RUN sed -i -e "s/scipy==.*/scipy==1.5.3/" /tmp/conda-tmp/requirements.txt
RUN /opt/conda/bin/conda install --quiet --yes --file /tmp/conda-tmp/test_requirements.txt --file /tmp/conda-tmp/extra_requirements.txt --file /tmp/conda-tmp/requirements.txt --file /tmp/conda-tmp/linting_requirements.txt --file /tmp/conda-tmp/doc_requirements.txt