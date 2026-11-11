package proofreading

// Suspect is a bounded word range in one document.
type Suspect struct {
	Page  int
	Start int
	End   int
	Word  string
}

// CohortAccepted remains solely for the pre-WP96 session implementation.
// The admitted provider never consults this list.
var CohortAccepted = []string{
	"The", "brown", "fox", "met", "a", "cat", "saw", "again", "follows",
	"word", "provides", "enough", "context", "to", "wrap", "naturally",
	"Another", "waits", "here", "and", "is", "the", "of", "in", "on",
	"reads", "rest", "this", "paragraph", "It", "it", "that", "with",
	"for", "by", "as", "at", "was", "were", "has", "had", "an", "or",
}
