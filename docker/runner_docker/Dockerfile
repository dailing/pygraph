from nvidia/cuda:10.1-devel-ubuntu18.04


RUN rm /etc/apt/sources.list.d/* && \
        apt-get update && apt-get install -y python3.8 wget curl zsh fish\
        python3.8-distutils libglib2.0-dev python3.8-dev git cmake\
        ninja-build protobuf-compiler libprotobuf-dev wget ca-certificates \
        unzip sudo \
        && ln -sf /usr/bin/python3.8 /usr/bin/python

RUN wget -O /tmp/xx.tar.xz https://nodejs.org/dist/v12.18.3/node-v12.18.3-linux-x64.tar.xz && mkdir -p /usr/local/lib/nodejs && tar -xJvf /tmp/xx.tar.xz -C /usr/local/lib/nodejs && rm /tmp/xx.tar.xz

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py 
RUN python get-pip.py && rm get-pip.py

RUN pip install torch==1.5.1+cu101 torchvision==0.6.1+cu101 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install jupyterlab flask peewee pandas redis xlrd \
                opencv-python-headless tqdm Pillow matplotlib pycocotools \
                cityscapesscripts sqlitedict tensorboard cython six terminaltables \
                torchvision addict yapf ipywidgets
ENV PATH=/usr/local/lib/nodejs/node-v12.18.3-linux-x64/bin/:${PATH}
RUN jupyter labextension install @jupyterlab/toc

# RUN python -m pip install detectron2 -f \
#   https://dl.fbaipublicfiles.com/detectron2/wheels/cu101/torch1.5/index.html

# RUN pip install 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'
# RUN pip install 'git+https://github.com/facebookresearch/fvcore'
# RUN pip install ipywidgets

# RUN git clone https://github.com/open-mmlab/mmdetection.git /mmd
# WORKDIR /mmd
# ENV MAX_JOBS=32
# RUN pip install -r requirements/build.txt
# RUN pip install "git+https://github.com/open-mmlab/cocoapi.git#subdirectory=pycocotools"
# RUN pip install -v -e .



RUN groupadd -g 1000 d && useradd -g 1000 -m d
RUN usermod -a -G sudo d
USER d
