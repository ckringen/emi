
# include <fstream>
# include <iostream>
# include <exception>
# include <string>
# include <vector>

// need Boost to tokenize strings, read gzip files
# include <boost/tokenizer.hpp>
# include <boost/iostreams/filter/gzip.hpp>

# include "count_skipgrams.h"


skipgram::skipgram( std::string fname, int window_sz=2 ) {
  infname = fname;
  window_size = window_sz;
  outfname = infname + "." + "counts";      
}


// need Boost to read a gzipped file either by bytes or newlines
void skipgram::readGzip( ) {
}


void skipgram::readFile( ) {
  std::string line;
  std::ifstream myfile;

  myfile.open (infname, std::ios::in);
  if (myfile.is_open())
  {
    while ( std::getline (myfile,line) )
    {
      processLine( line );
    }
    myfile.close();
  }
  else std::cout << "Unable to open file\n"; 
}


void skipgram::readStdin( ) {
  for (std::string line; std::getline(std::cin, line);) {
        std::cout << line << std::endl;
    }
}


void skipgram::processLine( std::string line ) {
  // tokenize 
  boost::tokenizer<> tok( line );

  // skipgram
  boost::tokenizer<>::iterator i = tok.begin();
  boost::tokenizer<>::iterator j = tok.begin();
  std::advance( j, window_size );

  for( ; j != tok.end(); ++i, ++j) {
    try {
      tgram skip = std::make_pair( *i, *j );
      	
      // count skigprams
      // std::unordered_map<std::string,double>::const_iterator got = mymap.find (input);
      auto got = counter.find( skip );
      if ( got == counter.end() ) {
	counter[ skip ] = 1;
      }
      else {
	++counter[ skip ];
      }
    }

    // loses window_size - 1 words; could store and concat to next line read if needed
    catch ( std::exception& e) {
      continue;
    }
  }
}
    


void skipgram::writeOut( ) {
  
  std::ofstream outfile;
  outfile.open(outfname, std::ios::out );
  
  for( auto i=counter.begin( ); i != counter.end( ); ++i ) {
    outfile << i->first.first << ' ' << i->first.second << '\t' << i->second << '\n';
  }
}



