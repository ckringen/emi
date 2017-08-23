
# include <fstream>
# include <iostream>
# include <iterator>

# include <cstring>
# include <memory>

# include <string>
# include <vector>

// need Boost to tokenize strings, read gzip files
//# include <boost/iostreams/filter/gzip.hpp>
# include <boost/tokenizer.hpp>

# include "count_skipgrams.h"



skipgram::skipgram( const std::string& fname, int window_sz=2 ) {
  infname = fname;
  window_size = window_sz;
  //outfname = infname + "." + "counts";      
}


// need Boost to read a gzipped file either by bytes or newlines
// void skipgram::readGzip( ) {
// }


// void skipgram::readFile( ) {
//   std::string line;
//   std::ifstream myfile;

//   myfile.open (infname, std::ios::in);
//   if (myfile.is_open())
//   {
//     while ( std::getline (myfile,line) )
//     {
//       processLine( line );
//     }
//     myfile.close();
//   }
//   else std::cout << "Unable to open file\n"; 
// }


void skipgram::readStdin( ) {
  std::string line;
  while ( std::getline( std::cin, line ) )
    {
      //processLine( line );
      split2( line );      
    }
}

// void skipgram::split1(std::string text, const std::string& delims)
// {
//   std::vector<std::string> tokens;
//   std::size_t start = text.find_first_of(delims), end = 0;
//   while((end = text.find_first_of(delims, start)) != std::string::npos)
//     {
//       tokens.push_back(text.substr(start, end - start));
//       start = text.find_first_not_of(delims, end);
//     }
//   if(start != std::string::npos)
//     tokens.push_back(text.substr(start));
//   for( auto i=tokens.begin( ); i!=tokens.end( ); ++i ) {
//     std::cout << *i << std::endl;
//   }
//   //return tokens;
// }


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



