// taken from main92.cc from pythia8 as a part of the PYTHIA event generator.
// Copyright (C) 2018 Torbjorn Sjostrand.
// PYTHIA is licenced under the GNU GPL v2 or later, see COPYING for details.
// Please respect the MCnet Guidelines, see GUIDELINES for details.

// Header file to access Pythia 8 program elements.
#include "Pythia8/Pythia.h"
#include "fastjet/ClusterSequence.hh"
#include "fastjet/contrib/SoftDrop.hh"

using namespace Pythia8;

int main(int argc, char ** argv) {

  if ( argc < 3 ) {
    std::cout << "usage: " << argv[0] << " config_file n_events (verbose?)" << std::endl;
    return 0;
  }

  bool verbose = false;    
  if ( argc >= 4 ) {    
    verbose = static_cast<bool>( atol(argv[3]) );
  }


  char * configfile = argv[1];
  unsigned int nEvents = atol(argv[2]);

  
  std::stringstream ss;
  ss << configfile << "_n" << nEvents << "_output.txt";
  std::ofstream output(ss.str());

  
  // Define the AK8 jet finder.
  double R = 0.8, ptmin = 170.0, lepfrac = 0.9;
  fastjet::JetDefinition jet_def(fastjet::antikt_algorithm, R);

  // Define some groomed jets: soft drop beta=0 (mmdt), beta=1, beta=2
  // give the soft drop groomer a short name
  // Use a symmetry cut z > z_cut R^beta
  // By default, there is no mass-drop requirement
  double z_cut = 0.10;
  double beta0  = 0.0;
  fastjet::contrib::SoftDrop sdb0(beta0, z_cut);
  double beta1  = 1.0;
  fastjet::contrib::SoftDrop sdb1(beta1, z_cut);
  double beta2  = 2.0;
  fastjet::contrib::SoftDrop sdb2(beta2, z_cut);


  // Create Pythia instance. Read config from a text file. 
  Pythia pythia;
  std::ifstream config( configfile );
  while (!config.eof() ) {
    std::string line;
    std::getline( config, line );
    if ( line[0] != '!' && line != "" && line != "\n" ){
      pythia.readString(line);
    }
  }
  pythia.init();
  Event *event = &pythia.event;

  for (int iEvent = 0; iEvent < nEvents; ++iEvent) {
    if (!pythia.next()) continue;  

    if ( verbose ) {
      std::cout << "------- Event " << iEvent << std::endl;
    }
    // Create AK8 jets with pt > 170 GeV from final state particles
    std::vector<fastjet::PseudoJet> fj_particles;
    for (int i = 0; i < event->size(); ++i){      
      if (pythia.event[i].isFinal() ) {
	auto const & p = pythia.event[i];
	fj_particles.emplace_back( p.px(), p.py(), p.pz(), p.e()  );
	// Set the user index to the pythia index
	fj_particles.back().set_user_index( i );
      }
    }
    fastjet::ClusterSequence cs(fj_particles, jet_def);
    std::vector<fastjet::PseudoJet> jets = fastjet::sorted_by_pt(cs.inclusive_jets(ptmin));

    if ( jets.size() > 0 ) {
      auto ibegin = jets.begin();
      auto iend = jets.end();      
      for ( auto ijet=ibegin;ijet!=iend;++ijet ) {
	auto constituents = ijet->constituents();

	// Get the fraction of the jet originating from leptons.
	// This is to remove jets that are comprised entirely of isolated leptons
	// such as Z->ll.
	// We ignore jets with >90% of their energy from leptons. 
	unsigned nlepton = 0;
	auto lepp4 = fastjet::PseudoJet();
	for ( auto icon = constituents.begin(); icon != constituents.end(); ++icon ) {
	  auto const & py8part = pythia.event[ icon->user_index() ];
	  if ( std::abs( py8part.id() ) > 10 && std::abs(py8part.id()) < 16)
	    lepp4 += *icon;
	}
	if ( lepp4.e() / ijet->e() > lepfrac){
	  continue;
	}

	fastjet::PseudoJet jet = *ijet;
	fastjet::PseudoJet jetsdb0 = sdb0( jet );
	fastjet::PseudoJet jetsdb1 = sdb1( jet );
	fastjet::PseudoJet jetsdb2 = sdb2( jet );

	char buff[1000];
	sprintf(buff, " %8.4f %6.2f %6.2f %8.4f %8.4f %8.4f %8.4f", jet.perp(), jet.eta(), jet.phi(), jet.m(), jetsdb0.m(), jetsdb1.m(), jetsdb2.m() );
	output << buff << std::endl;
	if ( verbose ) {

	  sprintf(buff, " ungroomed: %8.4f %6.2f %6.2f %8.4f", jet.perp(), jet.eta(), jet.phi(), jet.m() );
	  std::cout << buff << std::endl;
	  sprintf(buff, " sd beta=0: %8.4f %6.2f %6.2f %8.4f", jetsdb0.perp(), jetsdb0.eta(), jetsdb0.phi(), jetsdb0.m() );
	  std::cout << buff << std::endl;
	  sprintf(buff, " sd beta=1: %8.4f %6.2f %6.2f %8.4f", jetsdb1.perp(), jetsdb1.eta(), jetsdb1.phi(), jetsdb1.m() );
	  std::cout << buff << std::endl;
	  sprintf(buff, " sd beta=2: %8.4f %6.2f %6.2f %8.4f", jetsdb2.perp(), jetsdb2.eta(), jetsdb2.phi(), jetsdb2.m() );
	  std::cout << buff << std::endl;
	}
      }
    }
    // End event loop.
  }

  // Statistics on event generation.
  pythia.stat();

  output.close();

  // Done.
  return 0;
}
