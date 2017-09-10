
# build some things for great good

# g++ -std=c++14 -o cs -Iboost_1_65_0 main.cpp count_skipgrams.cpp 

# # lib paths gdb wants to see
# /lib64
# /cm/shared/apps/mpich/ge/gcc/64/3.1/lib
# /usr/lib64

MPICC = mpic++
CPP = g++

FLAGS = -std=c++11 -O3
I = -Iboost_1_65_0
bin = count_skipgrams

FLAGS = -std=c++11 -g
INCLUDE_PATH = -I/om/user/ckringen/thirdparty/boost-materials/boost_1_65_0
LIB_PATH = -L/om/user/ckringen/thirdparty/boost-materials/boost_1_65_0/stage/lib
libs = -lboost_mpi -lboost_serialization -lboost_iostreams -lboost_zlib

b2 = /om/user/ckringen/thirdparty/boost-materials/boost_1_65_0/b2


# main project
mainMPI: mainMPI.o count_skipgrams.o
	$(MPICC) $(FLAGS) mainMPI.o count_skipgrams.o $(INCLUDE_PATH) $(LIB_PATH) $(libs) -o mainMPI

mainMPI.o: mainMPI.cpp
	$(MPICC) $(FLAGS) -c mainMPI.cpp $(INCLUDE_PATH) $(LIB_PATH) $(libs) -o mainMPI.o

count_skipgrams.o: count_skipgrams.cpp count_skipgrams.h gzip.o zlib.o
	$(MPICC) $(FLAGS) -c count_skipgrams.cpp $(INCLUDE_PATH) $(LIB_PATH) $(libs) \
	-o count_skipgrams.o

gzip.o: gzip.cpp
	$(MPICC) $(FLAGS) -c gzip.cpp $(INCLUDE_PATH) $(LIB_PATH) $(libs) -L/om/user/thirdparty/zlib-materials/zlib-1.2.11 -o gzip.o

zlib.o: zlib.cpp 
	$(MPICC) $(FLAGS) -c zlib.cpp $(INCLUDE_PATH) $(LIB_PATH) $(libs) -L/om/user/thirdparty/zlib-materials/zlib-1.2.11 -o zlib.o

clean:
	$(RM) *.o $(bin) testBoost mainMPI


# the monster itself
boost: 
	pushd /om/user/ckringen/thirdparty/boost-materials/boost_1_65_0 && \
	$(b2) variant=debug -sZLIB_SOURCE=/om/user/ckringen/thirdparty/zlib-materials/zlib-1.2.11 --debug-building



# older
count_skipgrams: main.o count_skipgrams.o
	$(CPP) $(FLAGS) $(INCLUDE_PATH) main.o count_skipgrams.o -o $(bin)

main.o: main.cpp
	$(CPP) $(FLAGS) $(INCLUDE_PATH) -c main.cpp -o main.o

testBoost: testBoost.o
	$(MPICC) $(FLAGS) testBoost.o $(INCLUDE_PATH) $(LIB_PATH) $(libs) -o testBoost

testBoost.o: testBoost.cpp
	$(MPICC) $(FLAGS) -c testBoost.cpp $(INCLUDE_PATH) $(LIB_PATH) $(libs) -o testBoost.o

