
# include <fstream>
# include <iostream>
# include <iterator>

# include <cstring>
# include <memory>

# include <string>
# include <vector>

# include "count_skipgrams.h"

skipgram::skipgram( const std::string& fname, int window_sz=2 ) {
  infname = fname;
  window_size = window_sz;
  //outfname = infname + "." + "counts";      
}


void skipgram::readFile( ) {
  std::string line;
  std::ifstream myfile;

  myfile.open (infname, std::ios::in);
  if (myfile.is_open())
  {
    while ( std::getline (myfile,line) )
    {
      std::cout << line << std::endl;
      split2( line );
    }
    myfile.close();
  }
  else {
    std::cout << "Unable to open file: " << infname << '\n'; 
  }
}


void skipgram::readStdin( ) {
  std::string line;
  while ( std::getline( std::cin, line ) )
    {
      std::cout << line << std::endl; 
      //processLine( line );
      split2( line );      
    }
}


void skipgram::split2( const std::string &source ) {
  std::vector<std::string> results;
  const char *delimiter = " ,.-";
  bool keepEmpty = false;
  size_t prev = 0;
  size_t next = 0;

  // tokenize
  while ((next = source.find_first_of(delimiter, prev)) != std::string::npos)
    {
      if (keepEmpty || (next - prev != 0))
	{
	  results.push_back(source.substr(prev, next - prev));
	}
      prev = next + 1;
    }
  if (prev < source.size())
    {
      results.push_back(source.substr(prev));
    }

  // skipgram
  std::vector< std::string >::iterator effend = results.end( );
  std::advance(effend, -window_size);
  
  for( auto i=results.begin( ); i!=results.end( ); ++i ) {
    if( i >= effend ) {
      break;
    }
    else {
      auto j = i;
      std::advance( j, window_size );
      tgram skip = std::make_pair( *i, *j );
      
      // count skigprams  
      auto got = c.find( skip );
      if ( got == c.end() ) {
	c[ skip ] = 1;
      }
      else {
    	++c[ skip ];
      }
    }    
  }
}

void skipgram::writeOut( ) {
  
  // std::ofstream outfile;
  // outfile.open(outfname, std::ios::out );
  
  for( auto i=c.begin( ); i != c.end( ); ++i ) {
    std::cout << i->first.first << ' ' << i->first.second << '\t' << i->second << '\n';
    //outfile << i->first.first << ' ' << i->first.second << '\t' << i->second << '\n';
  }
}



