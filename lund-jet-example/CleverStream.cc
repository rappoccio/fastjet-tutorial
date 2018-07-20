//----------------------------------------------------------------------
//  CleverSteram, written 2007-2011 by Gavin Salam and Gregory Soyez
//
//  CleverStream is free software; you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation; either version 2 of the License, or
//  (at your option) any later version.
//
//  CleverStream is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with FastJet; if not, write to the Free Software
//  Foundation, Inc.:
//      59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
//----------------------------------------------------------------------

#ifndef HAVENOBOOST
#include "CleverStream.hh"


#include <boost/iostreams/filtering_streambuf.hpp>
#include <boost/iostreams/copy.hpp>
#include <boost/iostreams/filter/zlib.hpp>
#include <boost/iostreams/filter/gzip.hpp>
#include <boost/iostreams/filter/bzip2.hpp>


#include <unistd.h>    // for getting PID
#include <pwd.h>       // for getting username
#include <sys/stat.h>  // for mkfifo

#include <sstream>
#include <iomanip>
#include <fstream>
#include <cstdlib>

using namespace std;

const string CleverFStream::_fifo_symbol = "|";

CleverFStream::CleverFStream(const std::string & name, bool in) : _name(name) {
  establish_type();

  if (type() == fifo) create_fifo();
 
  if (type() != stdio) {
    if (in) {
      _ifstr.reset( new std::ifstream(_name.c_str()));
      if (! _ifstr->good() ) {
        cerr << "CleverFStream ERROR: could not open " << _name << endl;
        exit(-1);
      }
    } else {
      _ofstr.reset( new std::ofstream(_name.c_str()) );
      if (! _ofstr->good() ) {
        cerr << "CleverFStream ERROR: could not open " << _name << endl;
        exit(-1);
      }
    }
  }
}


CleverFStream::~CleverFStream() {
  if (type() == fifo) {
    // for fifo's, first close the streams, then delete the fifo
    _ofstr.reset();
    _ifstr.reset();
    unlink(_name.c_str());
  }
}

void CleverFStream::establish_type() {
  size_t npos = std::string::npos; // shorthand
  if      (_name.find(std::string(".gz"))  != npos) { _type = gz;}
  else if (_name.find(std::string(".bz2")) != npos) { _type = bz2;}
  else if (_name.find(_fifo_symbol)        != npos) { _type = fifo;}
  else if (_name == "-") {_type = stdio;}
  else {_type = plain;}
}


//----------------------------------------------------------------------
void CleverFStream::create_fifo() {

  // make a record of the fifo command, since _name (which is set to
  // the command when the class is constructed) will get overwritten
  // with the fifo name;
  _fifo_command = _name;

  // try to create a fifo in /tmp with a name based on the username
  // the process id and an extra integer that can run up to max_tries
  const int max_tries = 1000;
  struct passwd * passwd;
  passwd = getpwuid(getuid());
  int counter = 0;
  _name = "";
  while (counter < max_tries) {
    std::ostringstream ss;
    ss << "/tmp/"
       << passwd->pw_name 
       << "-fifo-"
       << std::setw( 5 ) << std::setfill( '0' ) 
       << getpid()
       << "-"
       << std::setw( 4 ) << std::setfill( '0' ) 
       << counter++;
    
    if (mkfifo(ss.str().c_str(), 0700) == 0) {
      _name = ss.str();
      break;
    }
  }
  if (_name == "") {
    cerr << "CleverFStream ERROR: failed to create fifo for command " << _fifo_command << endl;
    exit(-1);
  }
  
  // now set the fifo name in the command
  //cout << "Original _fifo_command was : " << _fifo_command << endl;
  size_t pos = _fifo_command.rfind(_fifo_symbol);
  if (pos == string::npos) {
    cerr << "CleverFStream ERROR _fifo_command appears not to contain pipe symbol" << endl;
    exit(-1);
  } else {
    _fifo_command.replace(pos, _fifo_symbol.size(), _name);
  }
  //cout << "New _fifo_command is : " << _fifo_command << endl;
  
  // now spawn the child process
  int child_pid = fork();
  if (child_pid == 0) {
    // I am the child
    system(_fifo_command.c_str());
    exit(0);
  }

}

//----------------------------------------------------------------------
CleverOFStream::CleverOFStream(const std::string & filename) : 
  CleverFStream(filename,false), boostio::filtering_ostream() {
  switch (type()) {
  case gz:
  case bz2:
  case plain:
  case fifo:
    if      (type() == gz ) {push(boostio::gzip_compressor());}
    else if (type() == bz2) {push(boostio::bzip2_compressor());}
    push(ofstr());
    break;
  case stdio:
    push (std::cout);
    break;
  default:
    std::cerr << "CleverOFStream ERROR: Unrecognised CleverFStream type " 
              << type() << std::endl;
    exit(-1);
  }
}

CleverIFStream::CleverIFStream(const std::string & filename) : 
    CleverFStream(filename,true), boostio::filtering_istream() {
    switch ( type()) {
    case gz:
    case bz2:
    case plain:
    case fifo:
      if      (type() == gz ) {push(boostio::gzip_decompressor());}
      else if (type() == bz2) {push(boostio::bzip2_decompressor());}
      push(ifstr());
      break;
    case stdio:
      push (std::cin);
      break;
    default:
      std::cerr << "CleverIFStream ERROR: Unrecognised CleverFStream type " 
                << type() << std::endl;
      exit(-1);
    }
  }

#endif // ifndef HAVENOBOOST
