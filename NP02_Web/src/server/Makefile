CC = gcc
OBJDIR = ./includes
EXEDIR = ../../exe
NAME = 1712897_18120059_18120360_19120163_19120257

all: main.o web.o mkdirexe
	$(CC) $(OBJDIR)/main.o $(OBJDIR)/web.o \
		-o ${EXEDIR}/${NAME}

main.o: Header.h web.o mkdirObject
	$(CC) -c main.c -o $(OBJDIR)/main.o

web.o: Header.h mkdirObject
	$(CC) -c web.c -o $(OBJDIR)/web.o

mkdirexe:
	mkdir -p ${EXEDIR}

mkdirObject:
	mkdir -p ${OBJDIR}

rmdirObject:
	rm -rf ${OBJDIR}

clean:
	rm -rf ${OBJDIR} ${EXEDIR}/${NAME}