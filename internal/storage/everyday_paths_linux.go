package storage

import (
	"errors"
	"io"
	"os"
	"sort"
	"strings"
	"sync"
	"syscall"
	"time"
)

// Workspace is one explicit Linux root mapped to DOS drive C. It owns all
// directory handles acquired through navigation. Copies share its lifetime.
type Workspace struct{ state *workspaceState }
type workspaceState struct {
	mu     sync.Mutex
	closed bool
	nodes  []*WorkspaceDirectory
}
type WorkspaceDirectory struct {
	workspace *workspaceState
	directory *Directory
	parent    *WorkspaceDirectory
	name      string
}

// MaxDirectoryEntries bounds the complete observation; oversized lists fail
// instead of reporting misleading partial file counts or ambiguous names.
const MaxDirectoryEntries = 16384
const MaxWorkspaceDepth = 64

// MaxWorkspaceDirectories bounds retained directory capabilities for the session.
const MaxWorkspaceDirectories = 256

func OpenWorkspace(path string) (*Workspace, error) {
	d, e := OpenDirectory(path)
	if e != nil {
		return nil, e
	}
	s := &workspaceState{}
	s.nodes = []*WorkspaceDirectory{{workspace: s, directory: d}}
	return &Workspace{state: s}, nil
}
func (w *Workspace) Root() (*WorkspaceDirectory, error) {
	if w == nil || w.state == nil {
		return nil, failure(InvalidRequest, "workspace root", "", nil)
	}
	s := w.state
	s.mu.Lock()
	defer s.mu.Unlock()
	if s.closed {
		return nil, failure(InvalidRequest, "workspace root", "", os.ErrClosed)
	}
	return s.nodes[0].copy(), nil
}

// OwnsDirectory reports whether d belongs to this live workspace and still
// has an open directory capability. A subsequent operation checks its own
// lifetime and filesystem observations again.
func (w *Workspace) OwnsDirectory(d *WorkspaceDirectory) bool {
	if w == nil || w.state == nil || d == nil || d.workspace != w.state {
		return false
	}
	s := w.state
	s.mu.Lock()
	defer s.mu.Unlock()
	return !s.closed && s.directoryNode(d) != nil && d.directory.acquired().open()
}

// OwnsSelection checks provenance, not the freshness of a selected name.
// Read and Enter revalidate the observation against the pinned directory.
func (w *Workspace) OwnsSelection(selection *EntrySelection) bool {
	return selection != nil && selection.entry.view.Supported && w.OwnsDirectory(selection.directory)
}

// directoryNode resolves a public copy to the private node. The caller holds mu.
func (s *workspaceState) directoryNode(d *WorkspaceDirectory) *WorkspaceDirectory {
	for _, node := range s.nodes {
		if node.directory == d.directory {
			return node
		}
	}
	return nil
}

func (d *WorkspaceDirectory) copy() *WorkspaceDirectory {
	if d == nil {
		return nil
	}
	c := *d
	return &c
}

func (w *Workspace) Close() error {
	if w == nil || w.state == nil {
		return failure(InvalidRequest, "workspace close", "", nil)
	}
	s := w.state
	s.mu.Lock()
	defer s.mu.Unlock()
	if s.closed {
		return os.ErrClosed
	}
	s.closed = true
	var errs []error
	for i := len(s.nodes) - 1; i >= 0; i-- {
		errs = append(errs, s.nodes[i].directory.Close())
	}
	return errors.Join(errs...)
}

// Directory returns a capability wrapper for ordinary Read/Observe/publication;
// the Workspace owns Close. Mutating the wrapper cannot rebind this location.
func (d *WorkspaceDirectory) Directory() *Directory {
	if d == nil || d.directory == nil {
		return nil
	}
	c := *d.directory
	return &c
}
func (d *WorkspaceDirectory) DOSPath() string {
	if d == nil {
		return ""
	}
	parts := []string{}
	for n := d; n.parent != nil; n = n.parent {
		parts = append(parts, n.name)
	}
	for i, j := 0, len(parts)-1; i < j; i, j = i+1, j-1 {
		parts[i], parts[j] = parts[j], parts[i]
	}
	return `C:\` + strings.Join(parts, `\`)
}

// DOSName accepts directly representable 8.3 ASCII names. No generated ~1 alias,
// Unicode folding, reserved device or case-collision resolution is implicit.
func DOSName(name string) (string, error) {
	upper := strings.ToUpper(name)
	parts := strings.Split(upper, ".")
	if len(parts) > 2 || len(parts[0]) < 1 || len(parts[0]) > 8 || (len(parts) == 2 && (len(parts[1]) < 1 || len(parts[1]) > 3)) {
		return "", failure(UnsafePath, "DOS 8.3 name", name, nil)
	}
	for _, c := range []byte(name) {
		if c < 33 || c > 126 || strings.ContainsRune(`"*/:<>?\|+,;=[]`, rune(c)) {
			return "", failure(UnsafePath, "DOS character", name, nil)
		}
	}
	switch parts[0] {
	case "CON", "PRN", "AUX", "NUL", "CLOCK$", "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9":
		return "", failure(UnsafePath, "DOS device", name, nil)
	}
	return upper, nil
}
func boundedEntries(cap *openedDirectory) ([]os.FileInfo, error) {
	if e := receiver(cap, "enumerate directory"); e != nil {
		return nil, e
	}
	f, e := cap.root.Open(".")
	if e != nil {
		return nil, e
	}
	entries, e := f.Readdir(MaxDirectoryEntries + 1)
	closeErr := f.Close()
	if e != nil && !errors.Is(e, io.EOF) {
		return nil, e
	}
	if closeErr != nil {
		return nil, closeErr
	}
	if len(entries) > MaxDirectoryEntries {
		return nil, failure(InputLimit, "directory entries", "", nil)
	}
	sort.Slice(entries, func(i, j int) bool { return entries[i].Name() < entries[j].Name() })
	return entries, nil
}
func resolveDOS(cap *openedDirectory, name string) (string, error) {
	canonical, e := DOSName(name)
	if e != nil {
		return "", e
	}
	entries, e := boundedEntries(cap)
	if e != nil {
		return "", e
	}
	actual := ""
	for _, entry := range entries {
		n, e := DOSName(entry.Name())
		if e == nil && n == canonical {
			if actual != "" {
				return "", failure(UnsafePath, "ambiguous DOS name", name, nil)
			}
			actual = entry.Name()
		}
	}
	if actual == "" {
		return canonical, nil
	}
	return actual, nil
}

// Navigate accepts C:\..., \..., or a relative DOS directory path. Parent
// traversal uses pinned navigation ancestry; it never opens filesystem '..'.
func (d *WorkspaceDirectory) Navigate(path string) (*WorkspaceDirectory, error) {
	if d == nil || d.workspace == nil {
		return nil, failure(InvalidRequest, "navigate", path, nil)
	}
	s := d.workspace
	s.mu.Lock()
	defer s.mu.Unlock()
	if s.closed {
		return nil, os.ErrClosed
	}
	at := s.directoryNode(d)
	if at == nil || !at.directory.acquired().open() {
		return nil, failure(InvalidRequest, "navigate", path, os.ErrClosed)
	}
	if len(path) > 1024 || strings.Contains(path, "/") || strings.ContainsRune(path, 0) {
		return nil, failure(UnsafePath, "DOS directory path", path, nil)
	}
	if len(path) >= 2 && path[1] == ':' {
		if !strings.EqualFold(path[:2], "C:") {
			return nil, failure(UnsafePath, "unmapped DOS drive", path, nil)
		}
		at = s.nodes[0]
		path = path[2:]
	}
	if strings.HasPrefix(path, `\`) {
		at = s.nodes[0]
		path = strings.TrimLeft(path, `\`)
	}
	for _, part := range strings.Split(path, `\`) {
		if part == "" || part == "." {
			continue
		}
		if part == ".." {
			if at.parent == nil {
				return nil, failure(UnsafePath, "workspace parent boundary", path, nil)
			}
			at = at.parent
			continue
		}
		depth := 0
		for n := at; n.parent != nil; n = n.parent {
			depth++
		}
		if depth >= MaxWorkspaceDepth {
			return nil, failure(InputLimit, "directory depth", path, nil)
		}
		actual, e := resolveDOS(at.directory.acquired(), part)
		if e != nil {
			return nil, e
		}
		child, e := at.child(actual)
		if e != nil {
			return nil, e
		}
		at = child
	}
	return at.copy(), nil
}
func (d *WorkspaceDirectory) child(name string) (*WorkspaceDirectory, error) {
	depth := 0
	for n := d; n.parent != nil; n = n.parent {
		depth++
	}
	if depth >= MaxWorkspaceDepth {
		return nil, failure(InputLimit, "directory depth", name, nil)
	}
	cap := d.directory.acquired()
	if err := receiver(cap, "child acquisition"); err != nil {
		return nil, err
	}
	info, e := cap.ops.Lstat(name)
	if e != nil {
		return nil, e
	}
	if !info.IsDir() || info.Mode()&os.ModeSymlink != 0 {
		return nil, failure(UnsafePath, "child directory", name, nil)
	}
	before, e := identity(info)
	if e != nil {
		return nil, e
	}
	canonical, nameErr := DOSName(name)
	if nameErr != nil {
		return nil, nameErr
	}
	for _, node := range d.workspace.nodes {
		if node.parent == d && node.name == canonical && node.directory.acquired().open() && node.directory.ID() == before.ID {
			return node, nil
		}
	}
	if len(d.workspace.nodes) >= MaxWorkspaceDirectories {
		return nil, failure(InputLimit, "workspace directory handles", name, nil)
	}
	r, e := cap.root.OpenRoot(name)
	if e != nil {
		return nil, e
	}
	dir, e := r.Open(".")
	if e != nil {
		r.Close()
		return nil, e
	}
	closeOnError := func(err error) (*WorkspaceDirectory, error) { dir.Close(); r.Close(); return nil, err }
	opened, e := dir.Stat()
	if e != nil {
		return closeOnError(e)
	}
	id, e := identity(opened)
	if e != nil {
		return closeOnError(e)
	}
	after, e := cap.ops.Lstat(name)
	if e != nil {
		return closeOnError(e)
	}
	stamp, e := identity(after)
	if e != nil {
		return closeOnError(e)
	}
	if !sameStamp(before, stamp) || id.ID != before.ID || !after.IsDir() {
		return closeOnError(failure(StaleSource, "child acquisition", name, nil))
	}
	c := &Directory{openedDirectory: &openedDirectory{root: r, dir: dir, ops: rooted{Root: r, dir: dir}, id: id.ID}}
	node := &WorkspaceDirectory{workspace: d.workspace, directory: c, parent: d, name: canonical}
	d.workspace.nodes = append(d.workspace.nodes, node)
	return node, nil
}

// FileEntry is observation data. Only an EntrySelection produced from a listing
// carries its original private name/stamp for later revalidation.
type FileEntry struct {
	Name, DOSName        string
	Size                 int64
	Modified             time.Time
	Mode                 os.FileMode
	Supported, Ambiguous bool
}
type entryObservation struct {
	view     FileEntry
	identity Identity
}
type Listing struct {
	directory *WorkspaceDirectory
	entries   []entryObservation
	metrics   DirectoryMetrics
}
type EntrySelection struct {
	directory *WorkspaceDirectory
	entry     entryObservation
}

// Directory returns a copy of the pinned directory that issued the selection.
func (s *EntrySelection) Directory() *WorkspaceDirectory {
	if s == nil {
		return nil
	}
	return s.directory.copy()
}

// Name returns the actual filesystem spelling observed by the listing.
func (s *EntrySelection) Name() string {
	if s == nil {
		return ""
	}
	return s.entry.view.Name
}

// MatchesDocument reports whether doc carries this selection's pinned directory,
// actual name and observed file stamp. It does not perform a new filesystem
// observation or imply that the workspace is still open.
func (s *EntrySelection) MatchesDocument(doc *Document) bool {
	return s != nil && s.directory != nil && s.entry.view.Supported &&
		doc != nil && doc.origin == s.directory.directory.acquired() &&
		doc.name == s.entry.view.Name && sameStamp(doc.identity, s.entry.identity)
}

type DirectoryMetrics struct {
	Entries, Unsupported                  int
	TotalBytes, FreeBytes, AvailableBytes uint64
}

func (l *Listing) Entries() []FileEntry {
	if l == nil {
		return nil
	}
	out := make([]FileEntry, len(l.entries))
	for i, v := range l.entries {
		out[i] = v.view
	}
	return out
}
func (l *Listing) Metrics() DirectoryMetrics {
	if l == nil {
		return DirectoryMetrics{}
	}
	return l.metrics
}
func (l *Listing) Select(index int) (*EntrySelection, error) {
	if l == nil || index < 0 || index >= len(l.entries) {
		return nil, failure(InvalidRequest, "list selection", "", nil)
	}
	return &EntrySelection{l.directory, l.entries[index]}, nil
}
func (l *Listing) Find(prefix string) int {
	if l == nil {
		return -1
	}
	directory := strings.HasPrefix(prefix, `\`)
	prefix = strings.TrimPrefix(strings.ToUpper(prefix), `\`)
	for i, e := range l.entries {
		if (!directory || e.view.Mode.IsDir()) && strings.HasPrefix(e.view.DOSName, prefix) {
			return i
		}
	}
	return -1
}
func (d *WorkspaceDirectory) List(pattern string) (*Listing, error) {
	if d == nil || d.workspace == nil {
		return nil, failure(InvalidRequest, "workspace listing", "", nil)
	}
	s := d.workspace
	s.mu.Lock()
	defer s.mu.Unlock()
	if s.closed {
		return nil, os.ErrClosed
	}
	match, e := dosPattern(pattern)
	if e != nil {
		return nil, e
	}
	node := s.directoryNode(d)
	if node == nil {
		return nil, failure(InvalidRequest, "workspace listing", "", nil)
	}
	cap := node.directory.acquired()
	entries, e := boundedEntries(cap)
	if e != nil {
		return nil, e
	}
	counts := map[string]int{}
	for _, v := range entries {
		n, e := DOSName(v.Name())
		if e == nil {
			counts[n]++
		}
	}
	l := &Listing{directory: node}
	for _, v := range entries {
		if strings.HasPrefix(v.Name(), candidatePrefix) {
			continue
		}
		canonical, nameErr := DOSName(v.Name())
		ambiguous := canonical != "" && counts[canonical] > 1
		supported := nameErr == nil && !ambiguous && (v.Mode().IsRegular() || v.IsDir())
		// Incompatible entries remain explicit in the unfiltered view; they are never
		// projected into a silently invented DOS alias or usable capability.
		if canonical != "" && !match(canonical) && !v.IsDir() {
			continue
		}
		if canonical == "" && pattern != "" && pattern != "*.*" && pattern != "*" {
			continue
		}
		id, e := identity(v)
		if e != nil {
			return nil, e
		}
		l.entries = append(l.entries, entryObservation{FileEntry{v.Name(), canonical, v.Size(), v.ModTime(), v.Mode(), supported, ambiguous}, id})
		if !supported {
			l.metrics.Unsupported++
		}
	}
	sort.SliceStable(l.entries, func(i, j int) bool {
		a, b := l.entries[i].view, l.entries[j].view
		if a.Mode.IsDir() != b.Mode.IsDir() {
			return a.Mode.IsDir()
		}
		if a.DOSName != b.DOSName {
			return a.DOSName < b.DOSName
		}
		return a.Name < b.Name
	})
	l.metrics.Entries = len(l.entries)
	var st syscall.Statfs_t
	raw, e := cap.dir.SyscallConn()
	if e != nil {
		return nil, e
	}
	var statErr error
	e = raw.Control(func(fd uintptr) { statErr = syscall.Fstatfs(int(fd), &st) })
	if e != nil {
		return nil, e
	}
	if statErr != nil {
		return nil, statErr
	}
	l.metrics.TotalBytes = st.Blocks * uint64(st.Bsize)
	l.metrics.FreeBytes = st.Bfree * uint64(st.Bsize)
	l.metrics.AvailableBytes = st.Bavail * uint64(st.Bsize)
	return l, nil
}
func (s *EntrySelection) check() error {
	if s == nil || s.directory == nil || !s.entry.view.Supported {
		return failure(UnsafePath, "selected entry", "", nil)
	}
	d := s.directory
	if d.workspace.closed {
		return os.ErrClosed
	}
	info, e := d.directory.acquired().ops.Lstat(s.entry.view.Name)
	if e != nil {
		return e
	}
	id, e := identity(info)
	if e != nil {
		return e
	}
	if !sameStamp(id, s.entry.identity) {
		return failure(StaleSource, "selected entry", s.entry.view.Name, nil)
	}
	actual, e := resolveDOS(d.directory.acquired(), s.entry.view.DOSName)
	if e != nil {
		return e
	}
	if actual != s.entry.view.Name {
		return failure(StaleSource, "selected DOS alias", actual, nil)
	}
	return nil
}

// Read acquires a native snapshot for Look or Retrieve without changing a buffer.
// A stale selection cannot silently acquire replacement bytes.
func (s *EntrySelection) Read() (*Document, error) {
	if s == nil || s.directory == nil {
		return nil, failure(InvalidRequest, "read selection", "", nil)
	}
	w := s.directory.workspace
	w.mu.Lock()
	defer w.mu.Unlock()
	if e := s.check(); e != nil {
		return nil, e
	}
	doc, e := s.directory.directory.Read(s.entry.view.Name)
	if e != nil {
		return nil, e
	}
	if !s.MatchesDocument(doc) {
		return nil, failure(StaleSource, "selected read", s.entry.view.Name, nil)
	}
	return doc, nil
}
func (s *EntrySelection) Enter() (*WorkspaceDirectory, error) {
	if s == nil || s.directory == nil {
		return nil, failure(InvalidRequest, "enter selection", "", nil)
	}
	w := s.directory.workspace
	w.mu.Lock()
	defer w.mu.Unlock()
	if e := s.check(); e != nil {
		return nil, e
	}
	child, err := s.directory.child(s.entry.view.Name)
	if err != nil {
		return nil, err
	}
	return child.copy(), nil
}
func (d *WorkspaceDirectory) Observe(name string) (*Destination, error) {
	if d == nil || d.workspace == nil {
		return nil, failure(InvalidRequest, "workspace destination", name, nil)
	}
	s := d.workspace
	s.mu.Lock()
	defer s.mu.Unlock()
	if s.closed {
		return nil, os.ErrClosed
	}
	actual, e := resolveDOS(d.directory.acquired(), name)
	if e != nil {
		return nil, e
	}
	return d.directory.Observe(actual)
}
func dosPattern(pattern string) (func(string) bool, error) {
	if pattern == "" {
		pattern = "*.*"
	}
	p := strings.Split(strings.ToUpper(pattern), ".")
	if len(p) > 2 || len(p[0]) > 8 || (len(p) == 2 && len(p[1]) > 3) {
		return nil, failure(UnsafePath, "DOS wildcard", pattern, nil)
	}
	for _, c := range pattern {
		if c > 126 || c < 33 || strings.ContainsRune(`"/:<>\|+,;=[]`, c) {
			return nil, failure(UnsafePath, "DOS wildcard", pattern, nil)
		}
	}
	if len(p) == 1 {
		p = append(p, "")
	}
	if pattern == "*" {
		p[1] = "*"
	}
	partMatch := func(p, s string) bool {
		for len(p) > 0 {
			if p[0] == '*' {
				return true
			}
			if p[0] == '?' {
				if len(s) > 0 {
					s = s[1:]
				}
			} else {
				if len(s) == 0 || p[0] != s[0] {
					return false
				}
				s = s[1:]
			}
			p = p[1:]
		}
		return s == ""
	}
	return func(name string) bool {
		n := strings.SplitN(name, ".", 2)
		if len(n) == 1 {
			n = append(n, "")
		}
		return partMatch(p[0], n[0]) && partMatch(p[1], n[1])
	}, nil
}
