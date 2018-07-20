# Lund jet plane tutorial

You can download jet samples here:
 * [Dijet sample](https://cernbox.cern.ch/index.php/s/i8BiWuQTv8Am3qL)
 * [W sample](https://cernbox.cern.ch/index.php/s/5FOfIT6oA54sqSR)


## Creating declusterings

Using the Lund class in lund.hpp, create json files containing
declusterings of QCD and W jets obtained from Pythia 8's dijet and WW
processes.
```
Lund lund("W-lund-pt2000-parton");
[...]
lund.write(jet);
```

## Plot lund images

After creating samples in pythia 8, or having downloaded them from the
link above, you can obtain a Lund image in pyplot using

`python3 plot_lund.py [--sig file_signal --bkg file_background --nev nevents --npxl npixels]`

## Tagging of W jets

You can try out a CNN Lund image tagger by downloading a trained model
[here](https://cernbox.cern.ch/index.php/s/KH2AvQVwo0FLifJ).

To try out the model, you can run

`python3 test_lund.py [--sig file_signal --bkg file_background --nev nevents --threshold threshold]`

Where threshold is a value between 0 and 1 (0.5 by default) used for the tagging.