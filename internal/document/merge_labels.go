package document

import "github.com/lynncoleart/wordling/internal/merge/native"

// fixedMergeKind is used only after exact native frame validation.
func fixedMergeKind(code byte) Kind {
	switch native.CommandKind(code) {
	case native.FieldCommand:
		return MergeField
	case native.EndField:
		return MergeEndField
	case native.PageOff:
		return MergePageOff
	case native.PageOn:
		return MergePageOn
	case native.NestPrimary:
		return MergeNestPrimary
	case native.NestSecondary:
		return MergeNestSecondary
	case native.IfBlank:
		return MergeIfBlank
	case native.Else:
		return MergeElse
	case native.EndIf:
		return MergeEndIf
	case native.Break:
		return MergeBreak
	default:
		return Opaque
	}
}
