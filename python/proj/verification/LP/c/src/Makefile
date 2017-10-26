all: comp run

CFLAGS = -w -pipe -fPIC -O -c
LDFLAGS = -l${TARGET} -L./

TARGET = hello_world
TARGET_LIB = libhello_world.so

OBJECTS = ${patsubst %.c, %.c.o, ${wildcard ./*.c}}
OBJECTS += ${patsubst %.cpp, %.cpp.o, ${wildcard ./*.cpp}}
OBJECTS += ${patsubst %.cc, %.cc.o, ${wildcard ./*.cc}}
OBJECTS += ${patsubst %.cxx, %.cxx.o, ${wildcard ./*.cxx}}

${info $$OBJECTS is [${OBJECTS}]}

${TARGET}: ${OBJECTS}
	${CXX} -pthread -o $@ $^
${TARGET_LIB}: ${OBJECTS}
	${CXX} -pthread -shared -o $@ $^

%.c.o: %.c
	${CC} ${CFLAGS} -o $@ $^
%.cpp.o: %.cpp
	${CXX} ${CFLAGS} -o $@ $^
%.cc.o: %.cc
	${CXX} ${CFLAGS} -o $@ $^
%.cxx.o: %.cxx
	${CXX} ${CFLAGS} -o $@ $^

.PHONY: pre_cmd
pre_cmd:
	${CC} --version
	${CXX} --version
comp: ${TARGET_LIB}
run: pre_cmd ${TARGET}
	./${TARGET}

clean:
	rm ${TARGET} ${TARGET_LIB} ${OBJECTS}
