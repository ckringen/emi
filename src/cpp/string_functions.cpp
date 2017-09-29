
# include <cstring.h>

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



// needs to be outside of skipgram
// void writeGzip( const std::string& outfname, const dict& counter ) {
//   std::ofstream outfile(outfname, std::ios_base::out | std::ios_base::binary);
//   try {
//     boost::iostreams::filtering_ostream out;
//     out.push(boost::iostreams::gzip_compressor());
//     out.push(outfile);
//     for( auto i=counter.begin( ); i != counter.end( ); ++i ) {
//       std::cout << i->first.first << ' ' << i->first.second << '\t' << i->second << '\n';
//     }
//     catch(const boost::iostreams::gzip_error& e) {
//       std::cout << e.what() << '\n';
//     }
//   }
// }


