# Ubuntu+tools, python, pip, python modules
apt-get update
apt-get install -y wget g++ libtool rsync make x11-apps python3-dev python3-numpy python3-pip python3-tk 
rm -rf /var/lib/apt/lists/*
#pip install --no-cache-dir matplotlib scipy numpy scikit-learn keras tensorflow jupyter metakernel zmq notebook==5.* plaidml-keras plaidbench energyflow
pip3 install --no-cache-dir matplotlib scipy numpy scikit-learn keras tensorflow jupyter metakernel zmq notebook==5.* plaidml-keras plaidbench energyflow uproot
update-alternatives --install /usr/bin/python python /usr/bin/python3 10
# fastjet
wget http://fastjet.fr/repo/fastjet-3.3.1.tar.gz \
    && tar xzf fastjet-3.3.1.tar.gz && rm fastjet-3.3.1.tar.gz \
    && cd fastjet-3.3.1 \
    && ./configure --prefix=/app --enable-pyext && make && make install \
    && cd .. 
# fastjet-contrib
wget http://fastjet.hepforge.org/contrib/downloads/fjcontrib-1.036.tar.gz \
    && tar xzf fjcontrib-1.036.tar.gz && rm fjcontrib-1.036.tar.gz \
    && cd fjcontrib-1.036 \
    && ./configure --fastjet-config=/app/bin/fastjet-config && make && make install \
    && cd .. 
