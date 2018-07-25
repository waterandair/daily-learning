all: gotool
	@go build -v .
clean:
	rm -f apiserver
	find . -name "[._]*.s[a-w][a-z]" | xargs -i rm -f {}
gotool:
	gofmt -w .
	go tool vet . | grep -v vendor;true

help:
	@echo "make - compile the source code"
	@echo "make clean - remove binary file and vim swp files"
	@echo "make gotool - run go tool 'fmt' and 'vet'"
	@echo "make ca - generate ca files"

.PHONY: clean gotool help