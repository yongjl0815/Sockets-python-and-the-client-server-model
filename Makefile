
#  Yong Lee
#  leey2@onid.oregonstate.edu
#  CS 344 - 400
#  Homework6


CC= gcc
CFLAGS= -Wall -Wshadow -std=c99 -Wunreachable-code -Wredundant-decls -Wmissing-declarations -Wold-style-definition -Wmissing-prototypes -Wdeclaration-after-statement
PROGS= compute


all: $(PROGS)

compute: compute.o
	$(CC) $(CFLAGS) compute.o -o compute

compute.o: compute.c
	$(CC) $(CFLAGS) -c compute.c		

#tested by using these commands:
#python manage.py
#time ./compute [ip_address]
#python report.py [ip_address] -k
	
clean:
	rm -f $(PROGS) *.o *~	

