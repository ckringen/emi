
# include <fstream>
# include <iostream>
# include <algorithm>
# include <iterator>
# include <utility>

# include <cstring>
# include <memory>
# include <cassert>

# include <string>
# include <vector>

# include <boost/tokenizer.hpp>
# include <boost/iostreams/stream.hpp>
# include <boost/iostreams/device/file.hpp>
# include <boost/iostreams/copy.hpp>
# include <boost/iostreams/filter/gzip.hpp>
# include <boost/iostreams/filter/zlib.hpp>
# include <boost/iostreams/filtering_stream.hpp>
# include <boost/iostreams/filtering_streambuf.hpp>

# include "count_skipgrams.h"

namespace io = boost::iostreams;

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

// need Boost to read a gzipped file either by bytes or newlines
// void skipgram::readGzip( ) {
// }


void skipgram::readFile( ) {
  std::string line;
  std::ifstream myfile;
  
  myfile.open (infname, std::ios::in);
  if (myfile.is_open())
    {
      while ( std::getline (myfile,line) )
	{
	  //processLine( line );
	  
	  // begin and end tokens, lowercase
	  line = "<s> " + line + " </s>";
	  std::transform( line.begin( ), line.end( ), line.end( ), ::tolower );  
	  split2( line );
	}
      myfile.close();
    }
  else std::cout << "Unable to open file\n"; 

}

dict skipgram::getCounter( ) {
  return counter;
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
      auto got = counter.find( skip );
      if ( got == counter.end() ) {
	counter[ skip ] = 1;
      }
      else {
    	++counter[ skip ];
      }
    }  
  }

  //return results;
}


// just use C's strtok
// void skipgram::split3(const std::string& text){
//   char* dst = new char[std::strlen(text.c_str()+1)];
//   std::strcpy(dst, text.c_str( ));
//   char * pch;
//   printf("Splitting string \"%s\" into tokens:\n", dst);
//   pch = strtok(dst," ,.-\t");
//   while (pch != NULL)
//     {
//       printf ("%s\n",pch);
//       pch = strtok(NULL, " ,.-\t");
//     }
//   delete dst;
// }


// loses window_size + 1 words; could store and concat to next line read if needed
void skipgram::processLine( const std::string& line ) {
  // tokenize 
  boost::tokenizer<> tok( line );
  
  // skipgram
  for( boost::tokenizer<>::iterator i = tok.begin(); i != tok.end(); ++i) {
    int remaining = std::distance( i, tok.end( ) );
    if( remaining <= ( window_size + 1 ) ) {
      break;
    }
    else {
      boost::tokenizer<>::iterator j = i;  
      std::advance( j, window_size );
      tgram skip = std::make_pair( *i, *j );
      
      // count skigprams  
      auto got = counter.find( skip );
      if ( got == counter.end() ) {
	counter[ skip ] = 1;
      }
      else {
	++counter[ skip ];
      }
    }
  }
}

void skipgram::writeOut( ) {
  
  // std::ofstream outfile;
  // outfile.open(outfname, std::ios::out );
  
  for( auto i=counter.begin( ); i != counter.end( ); ++i ) {
    std::cout << i->first.first << ' ' << i->first.second << '\t' << i->second << '\n';
    //outfile << i->first.first << ' ' << i->first.second << '\t' << i->second << '\n';
  }
}



