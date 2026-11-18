//go:build linux || darwin

package storage

import "errors"

func platformReplaceStep(s *saveStep, _ bool) error {
	return s.cap.ops.Rename(s.staged.name, s.target.name, renameExchange)
}

func (r rooted) Replace(string, string, string) error {
	return errors.New("ReplaceFile is a Windows primitive")
}
