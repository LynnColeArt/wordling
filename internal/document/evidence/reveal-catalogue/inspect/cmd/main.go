package main

import (
	host "github.com/lynncoleart/wordling/internal/document/evidence/reveal-catalogue/inspect"
	"os"
)

func main() { os.Exit(host.Run(os.Args[1:], os.Stdout, os.Stderr)) }
