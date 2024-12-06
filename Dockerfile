FROM quay.io/jupyter/minimal-notebook:afe30f0c9ad8

COPY conda-linux-64.lock /tmp/conda-linux-64.lock

# using root user (power user) to use sudo install

USER root

RUN sudo apt update \
    && sudo apt install -y lmodern \
    && chown -R $NB_UID /home \
    && chmod -R 0777 /home

# switch back to default notebook user
USER $NB_UID

RUN mamba update --file /tmp/conda-linux-64.lock \
    &&  mamba clean --all -y -f \
    && fix-permissions "${CONDA_DIR}" \
    && fix-permissions "/home/${NB_USER}"

# expose port 8888 of container
EXPOSE 8888

# start jupyter lab without auth token
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root", "--NotebookApp.token=''"]