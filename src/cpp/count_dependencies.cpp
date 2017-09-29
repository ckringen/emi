
# include <fstream>
# include <iostream>
# include <string>
# include <vector>
# include <utility>

# include <boost/algorithm/string.hpp>    
# include <boost/iostreams/filter/gzip.hpp>
# include <boost/iostreams/filtering_stream.hpp>

# include "count_dependencies.h"

namespace io = boost::iostreams;


template<typename Out>
void split(const std::string &s, char delim, Out result) {
  std::stringstream ss;
  ss.str(s);
  std::string item;
  while (std::getline(ss, item, delim)) {
    *(result++) = item;
  }
}

std::vector<std::string> split(const std::string &s, char delim) {
  std::vector<std::string> elems;
  split(s, delim, std::back_inserter(elems));
  return elems;
}


skipgram::skipgram( const std::string& fname, int window_sz=2 ) {
  infname = fname;
  window_size = window_sz;
}


void skipgram::readGzip( ) {
  std::ifstream file(infname, std::ios_base::in | std::ios_base::binary);

  try {    

    boost::iostreams::filtering_istream in;
    in.push(boost::iostreams::gzip_decompressor());
    in.push(file);

    std::vector< std::vector<std::string > > p_list;

    for(std::string str; std::getline(in, str); )
      {	
	
	if( str.length( ) > 0 ) {

	  // lowercase
	  boost::algorithm::to_lower(str);

	  std::vector<std::string> results = split( str, '\t' );	   
	  std::vector<std::string> columns;
	  for( auto i = results.begin(); i != results.end(); ++i) {	  
	    
	    int num = std::distance(results.begin( ), results.end( ) ) - std::distance(i, results.end( ) );	      
	    if( num == 0 || num == 1 || num == 6 || num == 7 ) {	    		
	      columns.push_back( *i );	      			
	    }	    
	  }
	  p_list.push_back( columns );
	}
	else {	    
	  processDependency( p_list );	    
	  p_list.clear( );
	}	
      }
  }
  catch(const boost::iostreams::gzip_error& e) {
    std::cout << e.what() << '\n';
  }
}

dict skipgram::getCounter( ) {
  return counter;
}

void skipgram::processDependency( const std::vector<std::vector<std::string>>& p_list ) {
  std::unordered_map< std::string, std::string > nodes;
  std::vector< tgram > edges;

  for( int i=0; i!=p_list.size( ); ++i) {
    nodes[ p_list[i][0] ] = p_list[i][1];
    edges.push_back( std::make_pair( p_list[i][0], p_list[i][2] ) );    
  }
  
  for(auto j=edges.begin( ); j != edges.end( ); ++j ) {    
    tgram key(std::make_pair(nodes[j->first],nodes[j->second]));

    auto got = counter.find( key );
    
    if ( got == counter.end() ) {
      counter[ key ] = 1;
    }
    else {
      ++counter[ key ];
    }
  }
}
