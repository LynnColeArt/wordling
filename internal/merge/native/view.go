package native

// CommandKind is a native DE subfunction, not a WPM instruction.
type CommandKind byte

const (
	Break         CommandKind = 0x22
	Else          CommandKind = 0x30
	EndField      CommandKind = 0x31
	EndIf         CommandKind = 0x33
	EndRecord     CommandKind = 0x34
	FieldCommand  CommandKind = 0x36
	IfBlank       CommandKind = 0x3b
	NestPrimary   CommandKind = 0x45
	NestSecondary CommandKind = 0x46
	PageOff       CommandKind = 0x4d
	PageOn        CommandKind = 0x4e
)

type OperandKind uint8

const (
	FieldNumber OperandKind = iota + 1
	NativeDOSName
)

type Operand struct {
	Kind             OperandKind
	Data, Terminator Span
	Number           uint16
}
type Command struct {
	Kind              CommandKind
	Function, Payload Span
	Operand           Operand
	RawCount          uint16
	HasRawCount       bool
	Match             int
}
type Finding struct {
	Code   string
	At     Span
	Detail string
}
type Field struct {
	Ordinal                           int
	Content, EndField, Separator      Span
	Empty, WhitespaceOnly, PlainASCII bool
}
type Record struct {
	Ordinal              int
	Raw, EndRecord, Tail Span
	StoredCount          uint16
	Fields               []Field
	Interstitial         []Span
}
type Inspection struct {
	Role           Role
	Source         Source
	Tokens         []Token
	Commands       []Command
	Records        []Record
	Findings       []Finding
	FindingsCapped bool
	WorkBytes      int
}
type viewState struct {
	source  *state
	info    Inspection
	blocked bool
}

// View captures accepted immutable ownership, not the caller's Image wrapper.
type View struct{ state *viewState }

func (v *View) Valid() bool     { return v != nil && v.state != nil }
func (v *View) Supported() bool { return v.Valid() && !v.state.blocked }
func (v *View) Export() []byte {
	if !v.Valid() {
		return nil
	}
	return v.state.source.image.Export()
}
func (v *View) Bytes(s Span) ([]byte, bool) {
	if !v.Valid() {
		return nil, false
	}
	return (&Image{v.state.source}).Bytes(s)
}
func (v *View) Inspect() (Inspection, bool) {
	if !v.Valid() {
		return Inspection{}, false
	}
	c := v.state.info
	c.Tokens = append([]Token(nil), c.Tokens...)
	c.Commands = append([]Command(nil), c.Commands...)
	c.Findings = append([]Finding(nil), c.Findings...)
	c.Records = append([]Record(nil), c.Records...)
	for j := range c.Records {
		c.Records[j].Fields = append([]Field(nil), c.Records[j].Fields...)
		c.Records[j].Interstitial = append([]Span(nil), c.Records[j].Interstitial...)
	}
	return c, true
}
func (i *Image) View(role Role) (*View, error) {
	if !i.Valid() {
		return nil, failure("InvalidImage", 0, "nil or zero image")
	}
	if role < Primary || role > Result {
		return nil, failure("InvalidRole", 0, "explicit Primary Secondary Result required")
	}
	b := builder{v: &viewState{source: i.state, info: Inspection{Role: role, Source: Source{i.state}, Tokens: i.state.tokens, WorkBytes: i.state.work}}, fieldStart: -1, recordStart: -1}
	if role == Result {
		b.find("ResultNotProgram", span(i.state, 0, 0), "framing/inspection only, never execution admission")
	}
	if err := b.scan(); err != nil {
		return nil, err
	}
	return &View{b.v}, nil
}

// Program is a captured, immutable bounded-role admission. Pass it by value to
// future consumers. Caller replacement of an Image/View wrapper or inspection
// cannot retarget this handle. It supplies NO interpreter, writer or host action.
type Program struct{ view *viewState }

func (p Program) Valid() bool { return p.view != nil && !p.view.blocked && p.view.info.Role != Result }
func (p Program) Source() Source {
	if !p.Valid() {
		return Source{}
	}
	return Source{p.view.source}
}
func (p Program) Inspect() (Inspection, bool) {
	if !p.Valid() {
		return Inspection{}, false
	}
	return (&View{p.view}).Inspect()
}
func (p Program) Bytes(s Span) ([]byte, bool) {
	if !p.Valid() {
		return nil, false
	}
	return (&View{p.view}).Bytes(s)
}
func (v *View) Admit() (Program, error) {
	if !v.Supported() {
		return Program{}, failure("UnsupportedRoleProgram", 0, "invalid, Result or blocking semantic findings")
	}
	return Program{v.state}, nil
}
