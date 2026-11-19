# Delete Remainder of Page

The March 9, 1992 reference displays “Delete Remainder of page? No (Yes)”
for Ctrl+Page Down. No leaves the text and cursor unchanged. Yes deletes
from the cursor through the last line of page 1, leaving the explicit
hard page and the text of page 2 in place. WordPerfect refreshes the
end-of-page cache for the shortened first page. [Question](delete-question.txt) ·
[Declined](declined.txt) · [Confirmed](confirmed.txt) · [Reveal Codes](reveal.txt) ·
[Native save](DELPG.WP)

The Linux replay compares the saved body for this hard-page fixture.
The Go regression also verifies that one Undelete restores the removed text.
Automatically paginated boundaries and additional formatting combinations
remain open. [Linux terminal replay](../../../../tests/everyday_qualification/navigation_deletion.py)

Run `replay.py` from the repository root with `PYTHONPATH=scripts/reference`.
