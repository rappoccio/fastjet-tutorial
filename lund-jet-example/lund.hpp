#ifndef __LUND_HPP__
#define __LUND_HPP__

#include "json.hpp"

// Frederic Dreyer, BOOST 2018 tutorial
// helper functions to write Lund coordinates to json file

using nlohmann::json;


class Lund {
public:
  
  struct Declustering {
    // the (sub)jet, and its two declustering parts, for subsequent use
    PseudoJet jj, j1, j2;
    // variables of the (sub)jet about to be declustered
    double pt, m;
    // properties of the declustering; NB kt is the _relative_ kt
    // = pt2 * delta_R (ordering is pt2 < pt1)
    double pt1, pt2, delta_R, z, kt, varphi;
  };
  
  Lund(string fn) {
    jsonfile_.reset(new CleverOFStream(fn+".json.gz"));
  }
  
  void write(PseudoJet j) {
    auto declusterings = jet_declusterings(j);
    //record_declusterings(declusterings, j, jet_def.R(), "primary");
      
    json J = declusterings;	    

    *jsonfile_ << J << endl;
  }
  
private:
	
  void to_json(json& j, const Declustering& d) {
    j = json{{"pt", float(d.pt)}, {"m", float(d.m)},
	     {"pt1", float(d.pt1)}, {"pt2", float(d.pt2)},
	     {"delta_R", float(d.delta_R)}, {"z",float(d.z)},
	     {"kt",float(d.kt)}, {"varphi", float(d.varphi)}};
  }

  vector<Declustering> jet_declusterings(const PseudoJet & jet_in) {

    PseudoJet j = jet_rec(jet_in);
    
    vector<Declustering> result;
    PseudoJet jj, j1, j2;
    jj = j;
    while (jj.has_parents(j1,j2)) {
      Declustering declust;
      // make sure j1 is always harder branch
      if (j1.pt2() < j2.pt2()) swap(j1,j2);

      // store the subjets themselves
      declust.jj   = jj;
      declust.j1   = j1;
      declust.j2   = j2;
        
      // get info about the jet 
      declust.pt   = jj.pt();
      declust.m    = jj.m();

      // collect info about the declustering
      declust.pt1     = j1.pt();
      declust.pt2     = j2.pt();
      declust.delta_R = j1.delta_R(j2);
      declust.z       = declust.pt2 / (declust.pt1 + declust.pt2);
      declust.kt      = j2.pt() * declust.delta_R;

      // this is now phi along the jet axis, defined in a
      // long. boost. inv. way
      declust.varphi = atan2(j1.rap()-j2.rap(), j1.delta_phi_to(j2));

      // add it to our result
      result.push_back(declust);

      // follow harder branch
      jj = j1;
    }
    return result;
    if (result.size() == 0) {
      cerr << "HEY THERE, empty declustering. Jet p_t and n_const = " << jet_in.pt() << " " << jet_in.constituents().size() << endl;
    }
  }

  unique_ptr<CleverOFStream> jsonfile_;
};

#endif // __LUND_HPP__
