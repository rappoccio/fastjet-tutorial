FROM ubuntu:16.04

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

RUN ./install_software.sh

# Run app.py when the container launches
CMD ["/bin/bash"]
