me/
# include <fstream>
# include <iostream>
# include <iterator>
# include <utility>

# include <cstring>
# include <memory>
#include <cassert>

# include <string>
# include <vector>

# include <boost/iostreams/stream.hpp>
# include <boost/iostreams/device/file.hpp>
# include <boost/iostreams/copy.hpp>
# include <boost/iostreams/filter/gzip.hpp>
# include <boost/iostreams/filter/zlib.hpp>
# include <boost/iostreams/filtering_stream.hpp>
# include <boost/iostreams/filtering_streambuf.hpp>

# include "count_skipgrams.h"

namespace io = boost::iostreams;


counter combineCounters( counter c1, counter c2 ) {
  for( auto ci=c1.begin( ); ci!=c1.end( ); ++ci ) {
    tgram key = std::make_pair( ci->first.first, ci->first.second );
    auto got = c2.find( key );    
    if ( got == c2.end( ) ) {
      c2[ key ] = ci->second;
    }
    else {
      c2[ key ] += ci->second;
    }    
  }
  return c2;
}

skipgram::skipgram( const std::string& fname, int window_sz=2 ) {
  infname = fname;
  window_size = window_sz;
  //outfname = infname + "." + "counts";      
}

void sanitize(std::string &stringValue) {
  // Add backslashes.
  for (auto i = stringValue.begin();;) { // i!=stringValue.end( ); ++i) {
    auto const pos = std::find_if(
				  i, stringValue.end(),
				  [](char const c) { return '\\' == c 
						     || '\'' == c 
						     || '"' == c; }
				  );
    if (pos == stringValue.end()) {
      break;
    }
    i = std::next(stringValue.insert(pos, '\\'), 2);
  }
  
  // Removes others.
  stringValue.erase(
		    std::remove_if(
				   stringValue.begin(), stringValue.end(), [](char const c) {
				     return '\n' == c 
				       || '\r' == c 
				       || '\0' == c 
				       || '\x1A' == c;
				   }
				   ),
		    stringValue.end()
		    );
}

void skipgram::readGzip( ) {
  std::ifstream file(infname, std::ios_base::in | std::ios_base::binary);
  try {
    boost::iostreams::filtering_istream in;
    in.push(boost::iostreams::gzip_decompressor());
    in.push(file);
    for(std::string str; std::getline(in, str); )
      {
	assert( str.length( ) > 0 ); 
	split2( str );
	//std::cout << "Processed line: " << str << '\n';
      }
  }
  catch(const boost::iostreams::gzip_error& e) {
    std::cout << e.what() << '\n';
  }

}


void skipgram::readStdin( ) {
  std::string line;
  while ( std::getline( std::cin, line ) )
    {
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



