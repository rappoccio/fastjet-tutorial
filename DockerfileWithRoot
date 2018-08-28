FROM rootproject/root-ubuntu16:6.12

ENV ROOT_VERSION=6.12/07

# Run the following commands as super user (root):
USER root

WORKDIR /app
ADD . /app

# Install required packages for notebooks
RUN sudo ./install_software_root.sh

# Set the python path
ENV PYTHONPATH /app/lib/:/usr/local/lib/:/usr/local/lib/root/:/app/lib/python2.7/site-packages/

# Create a user that does not have root privileges 
ARG username=physicist
ENV MY_UID 1000
RUN useradd --create-home --home-dir /home/${username} --uid ${MY_UID} ${username}
ENV HOME /home/${username}

# Set the cwd to /home/{username}
WORKDIR /home/${username}

# Switch to our newly created user
USER ${username}


COPY . ${HOME}
USER root
RUN chown -R ${MY_UID} ${HOME}
USER ${username}

# Allow incoming connections on port 8888
EXPOSE 8888

# Run notebook when the container launches
CMD ["jupyter", "notebook", "--ip", "0.0.0.0"]
