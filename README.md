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

### Persistifying data

You will remove all of your work on your Docker container when it
exist unless you specify otherwise. The way to do that is to mount a
directory from your host machine onto your docker image. There are
bash scripts included that will do this for either Mac OS X or Ubuntu
flavors:



```
./runDockerX11OSX.sh srappoccio/fastjet-tutorial:latest
```

(or change ```OSX``` above to ```Ubuntu```). 

This will give you a prompt, and mount a directory ```results``` in
the current working directory of the docker image. You can then use
that for communication back and forth from the docker container. Store
any results you want, and they will exist after your image is
deleted.

### With ROOT

If you want to use ROOT, then you can do everything as above, but
change ```fastjet-tutorial``` to ```fastjet-tutorial-root```.

```
docker pull srappoccio/fastjet-tutorial-root:latest
docker run -it -p 8888:8888 srappoccio/fastjet-tutorial-root:latest
```

The rest
works as above, except by default it runs a jupyter instance instead
of bash. You can also persistify your data if you want, with

```
./runDockerX11OSX.sh srappoccio/fastjet-tutorial-root:latest
```

(or change ```OSX``` above to ```Ubuntu```). 

If you want a bash shell and not a jupyter pyroot script, you can use
the "Command Line" flavors of the bash scripts, which are the same
except they have an explicit ```/bin/bash``` entry point. 

```
./runDockerX11OSXCommandLine.sh srappoccio/fastjet-tutorial-root:latest
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
