FROM mcr.microsoft.com/vscode/devcontainers/python:3.8

COPY ci/*.txt /tmp/conda-tmp/
RUN apt-get update && apt-get install libgeos-dev libproj-dev proj-bin
RUN python -m pip install --upgrade pip setuptools
RUN python -m pip install --no-binary :all: shapely
RUN python -m pip install -c /tmp/conda-tmp/requirements.txt numpy
RUN python -m pip install -r /tmp/conda-tmp/test_requirements.txt -c /tmp/conda-tmp/requirements.txt
RUN pip install -r /tmp/conda-tmp/test_requirements.txt -r /tmp/conda-tmp/extra_requirements.txt -r /tmp/conda-tmp/requirements.txt -r /tmp/conda-tmp/linting_requirements.txt -r /tmp/conda-tmp/doc_requirements.txt
