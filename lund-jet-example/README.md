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

After creating samples with the name
 * W-lund-pt2000-parton.json.gz
 * dijet-lund-pt2000-parton.json.gz

Or having downloaded them from the link above, you can create an image
in pyplot using
`./plot_lund.py`