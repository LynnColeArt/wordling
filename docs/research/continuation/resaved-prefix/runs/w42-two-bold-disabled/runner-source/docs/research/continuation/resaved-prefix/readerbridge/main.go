// Research adapter: invoke the unchanged production native reader. No serializer.
package main

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"io"
	"os"

	"github.com/lynncoleart/wordling/internal/wp51"
)

func main() {
	result := map[string]any{"accepted": false, "semantic_permission": false}
	if len(os.Args) != 2 {
		result["error"] = "one native input path required"
		emit(result)
		return
	}
	f, err := os.Open(os.Args[1])
	if err != nil {
		result["error"] = err.Error()
		emit(result)
		return
	}
	data, err := io.ReadAll(io.LimitReader(f, 65537))
	closeErr := f.Close()
	if err != nil || closeErr != nil || len(data) > 65536 {
		result["error"] = "research acquisition bound/read/close refusal"
		emit(result)
		return
	}
	image, err := wp51.Parse(data)
	if err != nil {
		result["error"] = err.Error()
		emit(result)
		return
	}
	hash := sha256.Sum256(data)
	result["accepted"] = true
	result["sha256"] = hex.EncodeToString(hash[:])
	result["size"] = len(data)
	result["inspection"] = image.Inspect()
	result["exact_export"] = bytes.Equal(data, image.Export())
	emit(result)
}
func emit(value map[string]any) {
	if json.NewEncoder(os.Stdout).Encode(value) != nil {
		os.Exit(2)
	}
}
