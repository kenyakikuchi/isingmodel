CC		= gcc
CXX		= g++

CFLAGS	= -O2 -Wall
CXXFLAGS = -O2 -Wall -std=c++11

TARGET	= duck.out

TARGETDIR := ./bin
CDIR    := ./
CXXDIR  := ./sources
OBJDIR  := ./objects

CSOURCES := $(shell ls $(CDIR)/*.c)
CXXSOURCES := $(shell ls $(CXXDIR)/*.cpp)
OBJS	:= $(subst $(CXXDIR), $(OBJDIR),  $(CXXSOURCES:.cpp=.o))

LDFLAGS	= 
INCLUDES = `pkg-config --libs --cflags opencv` -I ./includes
LIBS	= `pkg-config --libs --cflags opencv`#-lglut -lGLU -lGL -lm



$(TARGET): $(OBJS)
	$(CXX) $(LDFLAGS) -o $(TARGETDIR)/$@ $(OBJS) $(LIBS)

$(OBJDIR)/%.o: %(CDIR)/%.c
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

$(OBJDIR)/%.o: $(CXXDIR)/%.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

clear:
	rm bin/*
	rm objects/*

#objects/main.o: includes/resources.h
#objects/Nodes.o: includes/Nodes.h
#objects/Fisher_Yates.o: includes/Fisher_Yates.h
#objects/TSP.o: includes/TSP.h
