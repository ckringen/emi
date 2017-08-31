
# build some things for great good

MPICC = mpic++
CPP = g++

FLAGS = -std=c++11 -O3
INCLUDE_PATH = -I/om/user/ckringen/include
LIB_PATH = -L/om/user/ckringen/lib

libs = -lboost_mpi -lboost_serialization
bin = count_skipgrams


count_skipgrams: main.o count_skipgrams.o
	$(CPP) $(FLAGS) $(INCLUDE_PATH) main.o count_skipgrams.o -o $(bin)

main.o: main.cpp
	$(CPP) $(FLAGS) $(INCLUDE_PATH) -c main.cpp -o main.o



mainMPI: mainMPI.o count_skipgrams.o
	$(MPICC) $(FLAGS) mainMPI.o count_skipgrams.o $(INCLUDE_PATH) $(LIB_PATH) $(libs) -o mainMPI

mainMPI.o: mainMPI.cpp
	$(MPICC) $(FLAGS) -c mainMPI.cpp $(INCLUDE_PATH) $(LIB_PATH) $(libs) -o mainMPI.o

count_skipgrams.o: count_skipgrams.cpp count_skipgrams.h
	$(MPICC) $(FLAGS) -c count_skipgrams.cpp $(INCLUDE_PATH) $(LIB_PATH) $(libs) -o count_skipgrams.o



testBoost: testBoost.o
	$(MPICC) $(FLAGS) testBoost.o $(INCLUDE_PATH) $(LIB_PATH) $(libs) -o testBoost

testBoost.o: testBoost.cpp
	$(MPICC) $(FLAGS) -c testBoost.cpp $(INCLUDE_PATH) $(LIB_PATH) $(libs) -o testBoost.o



clean:
	$(RM) *.o $(bin) testBoost mainMPI
