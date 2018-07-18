# Makefile is a part of the PYTHIA event generator.
# Copyright (C) 2018 Torbjorn Sjostrand.
# PYTHIA is licenced under the GNU GPL v2 or later, see COPYING for details.
# Please respect the MCnet Guidelines, see GUIDELINES for details.
# Author: Philip Ilten, September 2014.
#
# This is is the Makefile used to build PYTHIA examples on POSIX systems.
# Example usage is:
#     make main01
# For help using the make command please consult the local system documentation,
# i.e. "man make" or "make --help".

################################################################################
# VARIABLES: Definition of the relevant variables from the configuration script.
################################################################################

# Set the shell.
SHELL=/usr/bin/env bash

# Include the configuration.
-include Makefile.inc
CXX_COMMON:=-I$(PREFIX_INCLUDE) $(CXX_COMMON)
CXX_COMMON+= -L$(PREFIX_LIB) -Wl,-rpath,$(PREFIX_LIB) -lpythia8 -ldl -g

################################################################################
# RULES: Definition of the rules used to build the PYTHIA examples.
################################################################################

# Rules without physical targets (secondary expansion for specific rules).
.SECONDEXPANSION:
.PHONY: all clean

# All targets (no default behavior).
all:
	@echo "Usage: make pythia2fastjet"

pythia2fastjet: $$@.cc
ifeq ($(FASTJET3_USE),true)
	$(CXX) $< -o $@ -w $(CXX_COMMON) -L./ -L$(FASTJET3_LIB) -Wl,-rpath,$(FASTJET3_LIB) -lRecursiveTools -lfastjettools -lfastjet 
else
	@echo "Error: $@ requires ROOT"
endif

# Clean.
clean:
	rm -f pythia2fastjet
