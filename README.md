# BOOST Conference Series Software Tutorial



## Software

You must have [Docker](https://www.docker.com/community-edition) installed (Community edition is free, so get that).

Then in a terminal:

```
docker pull srappoccio/fastjet-tutorial:latest
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
cd /app/fastjet-3.3.1/example
make 01-basic
./01-basic < data/single-event.dat
```

or in fastjet-contrib:
```
cd /app/fjcontrib-1.036/
make example_softdrop
./example_softdrop < ../../fastjet-3.3.1/example/data/single-event.dat
```


There is also an example to use PYTHIA8 to generate events with a given configuration (the example we have is boosted $Z\rightarrow ll+$jets):

```
cd examples
./pythia2fastjet test.cfg 100 1
```

Happy thinking!


## Machine Learning Tutorial

Be sure to run your docker image as shown above with the port set to '8888:8888'. Then within the docker image, you can start a jupyter notebook as:

```
jupyter notebook --ip 0.0.0.0 --no-browser --allow-root
```

You can then access the jupyter notebook on your host machine here: [http://localhost:8888/tree](http://localhost:8888/tree).

Note: sometimes you may get a page looking for a token. Instead of doing that you can just directly access the website from the text dump from jupyter, which looks something like:

```
    Copy/paste this URL into your browser when you connect for the first time,
    to login with a token:
        http://(a084677e0088 or 127.0.0.1):8888/?token=5f2dbda0e1b14fbb9efb3fd765bea4773d62f86093afe977
```

So then go to that website (pick either the equivalent of `a084677e0088` or `127.0.0.1`, not both). 

Happy learning! 
