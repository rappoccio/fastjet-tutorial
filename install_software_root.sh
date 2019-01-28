# Ubuntu+tools, python, pip, python modules
apt-get update
apt-get install -y wget g++ libtool rsync make x11-apps python-dev python-numpy python-pip python-tk 
rm -rf /var/lib/apt/lists/*
pip2 install --upgrade pip
pip2 install --no-cache-dir matplotlib==2.1 scipy numpy scikit-learn keras tensorflow ipykernel==4.10.0 ipython==5.7 jupyter metakernel zmq notebook==5.* uproot
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
# Pythia
wget http://home.thep.lu.se/~torbjorn/pythia8/pythia8235.tgz \
    && tar xzf pythia8235.tgz && rm pythia8235.tgz \
    && cd pythia8235 \
    && ./configure --prefix=/app --with-python-include=/usr/include/python2.7 --with-python-bin=/usr/bin/ --with-root=/usr/local/root && make \
    && cd examples && rootcint -f pythiaDict.cxx -c -I../include main92.h main92LinkDef.h \
    && g++ -I../include `root-config --glibs` `root-config --cflags` -L../lib -lpythia8 -shared -fPIC -o pythiaDict.so pythiaDict.cxx \
    && cp pythiaDict.so ../lib \
    && cd .. \
    && make install
