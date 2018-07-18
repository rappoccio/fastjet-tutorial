# BOOST Conference Series Software Tutorial



## Software

You must have [Docker](https://www.docker.com/community-edition) installed (Community edition is free, so get that).

Then in a terminal:

```
docker push srappoccio/fastjet-tutorial:latest
```


You should then be able to run as:

```
docker run -it -p 8888:8888 srappoccio/fastjet-tutorial:latest
```

You will get a prompt, and you can see the results of "ls":

```
root@588a429d41d2:/app# ls
Dockerfile  bin  fastjet-3.3.1  fjcontrib-1.036  include  lib  pythia8235  share
```

## Fastjet Tutorial

You have access to all of the fastjet and fastjet-contrib tutorials in your docker image. For instance:


```
cd /app/fastjet-3.3.1/examples
make 01-basic
./01-basic < data/single-event.dat
```

or in fastjet-contrib:
```
cd /app/fjcontrib-1.036/
make example_softdrop
./example_softdrop < ../../fastjet-3.3.1/example/data/single-event.dat
```


Happy thinking!


## Machine Learning Tutorial

Be sure to run your docker image as shown above with the port set to '8888:8888'. Then within the docker image, you can start a jupyter notebook as:

```
jupyter notebook --ip 0.0.0.0 --no-browser --allow-root
```

You can then access the jupyter notebook on your host machine here: [http://localhost:8888/tree](http://localhost:8888/tree).

Happy learning! 
