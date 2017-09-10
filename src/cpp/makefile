
# build count_skipgrams for great good

# g++ -std=c++14 -o cs -Iboost_1_65_0 main.cpp count_skipgrams.cpp 

CPP = g++
FLAGS = -std=c++11 -O3
I = -Iboost_1_65_0
bin = count_skipgrams

count_skipgrams: main.o count_skipgrams.o
	$(CPP) $(FLAGS) $(I) main.o count_skipgrams.o -o $(bin)

main.o: main.cpp
	$(CPP) $(FLAGS) $(I) -c main.cpp -o main.o

count_skipgrams.o: count_skipgrams.cpp count_skipgrams.h
	$(CPP) $(FLAGS) $(I) -c count_skipgrams.cpp -o count_skipgrams.o

clean:
	$(RM) *.o $(bin)
