FROM nvidia/cuda:9.0-cudnn7-devel-centos7

WORKDIR /root

RUN yum -y update \
    && yum -y install curl bzip2 \
    && curl -sSL https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -o /tmp/miniconda.sh \
    && bash /tmp/miniconda.sh -bfp /usr/local/ \
    && rm -rf /tmp/miniconda.sh \
    && conda install -y python=2 \
    && conda update conda \
    && conda clean --all --yes \
    && rpm -e --nodeps bzip2 \
    && yum -y autoremove \
    && yum clean all

RUN yum -y install git make which gcc gcc-c++ libcurl-devel unzip zip jq

COPY battler.env.yml /root
RUN conda env create -f battler.env.yml

# Need to install pytorch after intel-openmp for pytorch to use omp
RUN bash -c 'source activate metagrok && conda install -y pytorch=1.0.1 cudatoolkit=9.0 -c pytorch'

RUN mkdir -p /root/scripts
COPY scripts/predef /root/scripts
COPY config.json /root

# Install vmtouch
COPY scripts/install-vmtouch.bash /root/scripts
RUN bash scripts/install-vmtouch.bash && rm scripts/install-vmtouch.bash

# Install htop
COPY scripts/install-htop.bash /root/scripts
RUN bash scripts/install-htop.bash && rm scripts/install-htop.bash

# Install nvm
COPY scripts/install-nvm.bash /root/scripts
RUN bash scripts/install-nvm.bash && rm scripts/install-nvm.bash

# Install Pokemon Showdown
COPY scripts/install.bash /root/scripts
RUN bash scripts/install.bash --no-client && rm scripts/install.bash

# Install everything else
COPY scripts /root/scripts
RUN echo 'set -o vi' >> /root/.bashrc