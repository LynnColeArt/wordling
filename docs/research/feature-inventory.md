# WordPerfect 5.1 parity feature inventory

Generated from `feature-inventory.json`; edit that registry and run
`python3 scripts/render-inventory.py` to update this view.

Current catalogue: **91 feature groups**, all in Mission 1. These are
coverage groups, not a complete command-level inventory or implementation
work packages. Every group must be decomposed during section-by-section study.
No feature is implemented or verified against an original executable yet.

[Command scenarios](command-scenarios.md) provide representative command-level
drafts. [Coverage matrix](scenario-coverage.md) links each parent to its cases.
The presence of cases does not mean every subcommand or branch is covered.

`indexed` means located in the manual contents or toolkit structure.
`studied` means selected relevant passages were examined in this initial pass;
it does not mean the entire cited range has been exhaustively studied.
See findings.md for the specific studied behavior. Original-app observations
are tracked at command-scenario level; no parent group is verified.
Implementation and documentary status are independent.

Page locators use the exact checksummed editions in sources.json. Printed
toolkit page numbers below refer to its **WP** section only. PDF pages are
one-based. Range endpoints are inclusive. OCR needs visual verification for
ambiguous keystrokes, numbers and diagrams.

## Interaction

| ID | Feature group | Manual evidence | Study | Acceptance probe |
| --- | --- | --- | --- | --- |
| WP51-001 | Clean screen, status, menus and function keys | [REF51 pp. 3-12; PDF 20-29](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=20) | studied | Replay start, edit, nested menus, cancel and exit; record screen and prompts. |
| WP51-002 | Context-sensitive help | [REF51 pp. 275-276; PDF 292-293](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=292) | studied | Open help from document and nested dialogs; return to the previous state. |
| WP51-003 | Original keyboard layouts and remapping | [REF51 pp. 304-318; PDF 321-335](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=321) | studied | Load, edit, persist and exercise keyboard definitions. |
| WP51-004 | Mouse interactions | [REF51 pp. 434-437; PDF 451-454](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=451) | studied | Exercise original menu and selection actions with terminal event mapping recorded. |
| WP51-005 | Display configuration and screen type | [REF51 pp. 68-74; PDF 85-91](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=85); [REF51 pp. 120-123; PDF 137-140](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=137); [REF51 pp. 266-268; PDF 283-285](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=283); [REF51 pp. 689-691; PDF 706-708](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=706) | studied | Compare text attributes, display pitch, dimensions and graphics capabilities. |
| WP51-006 | Two-document switching and windows | [REF51 pp. 628-630; PDF 645-647](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=645); [REF51 pp. 706-707; PDF 723-724](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=723) | studied | Switch and split documents; verify independent cursor and formatting state. |
| WP51-007 | Cancel and command repetition | [REF51 pp. 55; PDF 72](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=72); [REF51 pp. 550; PDF 567](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=567) | studied | Cancel at multiple prompt depths; repeat input and commands. |

## Editing

| ID | Feature group | Manual evidence | Study | Acceptance probe |
| --- | --- | --- | --- | --- |
| WP51-008 | Cursor movement and go-to | [REF51 pp. 103-104; PDF 120-121](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=120); [REF51 pp. 224; PDF 241](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=241) | studied | Move across text, codes, pages and subdocuments; compare cursor positions. |
| WP51-009 | Block selection and protection | [REF51 pp. 48-54; PDF 65-71](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=65) | studied | Select original block types and test protection during editing and reflow. |
| WP51-010 | Copy, move and append | [REF51 pp. 34-36; PDF 51-53](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=51); [REF51 pp. 438-443; PDF 455-460](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=455) | studied | Copy or move selections and append to new/existing files with codes intact. |
| WP51-011 | Text deletion and restoration | [REF51 pp. 112-116; PDF 129-133](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=129); [REF51 pp. 697; PDF 714](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=714) | studied | Compare deletion units and three-entry undelete behavior including paired codes. |
| WP51-012 | Insert versus typeover | [REF51 pp. 695-696; PDF 712-713](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=712) | studied | Type across text and formatting codes; verify codes are not overwritten. |
| WP51-013 | Reveal Codes | [REF51 pp. 560-562; PDF 577-579](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=577) | studied | Toggle Alt-F3; move/delete in the code pane and compare effects in the normal pane. |
| WP51-014 | Search and replacement | [REF51 pp. 551-554; PDF 568-571](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=568); [REF51 pp. 571-573; PDF 588-590](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=588) | studied | Exercise text/code searches, direction, case and extended subdocument replacement. |
| WP51-015 | Case changes and repeat input | [REF51 pp. 56-57; PDF 73-74](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=73); [REF51 pp. 550-551; PDF 567-568](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=567) | studied | Apply commands to text and blocks; compare boundaries and formatting. |
| WP51-016 | Hard and soft returns and spaces | [REF51 pp. 269; PDF 286](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=286); [REF51 pp. 557-560; PDF 574-577](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=574) | studied | Distinguish explicit paragraph boundaries from reflow; preserve code identity. |
| WP51-017 | Line-drawing text | [REF51 pp. 337-338; PDF 354-355](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=354) | studied | Create and modify line-drawing structures without corrupting text or characters. |
| WP51-018 | Refresh and reformat | [REF51 pp. 563-564; PDF 580-581](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=580) | studied | Trigger rewrite and inspect layout and cursor effects. |

## Files

| ID | Feature group | Manual evidence | Study | Acceptance probe |
| --- | --- | --- | --- | --- |
| WP51-019 | Retrieve and insert documents | [REF51 pp. 554-557; PDF 571-574](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=571) | studied | Retrieve whole documents and blocks, preserving their codes and resource references. |
| WP51-020 | Native save and overwrite workflow | [REF51 pp. 565-566; PDF 582-583](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=582) | studied | Save F10; verify filename editing, overwrite confirmation and initial codes. |
| WP51-021 | Original and timed backups | [REF51 pp. 41-44; PDF 58-61](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=58) | studied | Exercise both existing backup modes and recovery behavior; compare artifacts. |
| WP51-022 | Fast Save | [REF51 pp. 197; PDF 214](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=214) | studied | Compare saved bytes and formatting with the option enabled and disabled. |
| WP51-023 | File lists, directories and resource locations | [REF51 pp. 117-119; PDF 134-136](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=134); [REF51 pp. 347-354; PDF 364-371](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=364); [REF51 pp. 358-361; PDF 375-378](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=375) | studied | Replay file operations and path resolution with explicit Linux mapping. |
| WP51-024 | Password-locked documents | [REF51 pp. 362-363; PDF 379-380](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=379) | studied | Open and save correct/wrong-password fixtures without touching the original on failure. |
| WP51-025 | Original text import/export modes | [REF51 pp. 685-688; PDF 702-705](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=702) | studied | Compare each original mode, encoding and documented losses. |
| WP51-026 | Original 4.2 conversion modes | [REF51 pp. 130-142; PDF 147-159](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=147) | studied | Compare both conversion directions using original-version fixtures. |
| WP51-027 | Document comments and comparison | [REF51 pp. 124-129; PDF 141-146](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=141) | studied | Persist comments and compare documents, inspecting marked changes. |
| WP51-028 | Document look/find operations | [REF51 pp. 197-202; PDF 214-219](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=214); [REF51 pp. 364-368; PDF 381-385](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=381) | studied | Exercise file-content inspection and conditional file finding. |
| WP51-029 | Exit and save decisions | [REF51 pp. 194-196; PDF 211-213](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=211) | studied | Replay saved/modified/unnamed documents through all exit decisions. |
| WP51-090 | Document summaries and descriptive names | [REF51 pp. 145-149; PDF 162-166](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=162) | studied | Create, cancel, save and retrieve document summaries; inspect long-name file lists. |

## Format

| ID | Feature group | Manual evidence | Study | Acceptance probe |
| --- | --- | --- | --- | --- |
| WP51-030 | Attributes and change markings | [REF51 pp. 36-40; PDF 53-57](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=53); [REF51 pp. 549; PDF 566](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=566) | studied | Apply/remove attributes and redline/strikeout; inspect paired codes and print results. |
| WP51-031 | Fonts and kerning | [REF51 pp. 205-208; PDF 222-225](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=222); [REF51 pp. 303; PDF 320](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=320) | studied | Compare font changes, sizes, printer substitutions and kerning with fixed resources. |
| WP51-032 | Initial document and application codes | [REF51 pp. 143-144; PDF 160-161](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=160); [REF51 pp. 292-298; PDF 309-315](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=309) | studied | Distinguish default settings from document initial codes and saved state. |
| WP51-033 | Margins and format menus | [REF51 pp. 218-220; PDF 235-237](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=235); [REF51 pp. 339-340; PDF 356-357](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=356); [REF51 pp. 394-396; PDF 411-413](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=411); [REF51 pp. 473; PDF 490](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=490) | studied | Change line/page/document defaults and verify their code scope. |
| WP51-034 | Alignment, centering and indents | [REF51 pp. 63-67; PDF 80-84](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=80); [REF51 pp. 203-204; PDF 220-221](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=220); [REF51 pp. 285-286; PDF 302-303](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=302); [REF51 pp. 299-302; PDF 316-319](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=316) | studied | Compare centered/right-aligned/justified text and indents across reflow. |
| WP51-035 | Tabs and tab alignment | [REF51 pp. 631-639; PDF 648-656](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=648) | studied | Set tab types, alignment and leaders; verify native codes and layout. |
| WP51-036 | Line height, spacing and numbering | [REF51 pp. 341-346; PDF 358-363](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=358) | studied | Combine proportional fonts, line height, spacing and line numbers. |
| WP51-037 | Word/letter spacing and measurement units | [REF51 pp. 698-700; PDF 715-717](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=715); [REF51 pp. 708-711; PDF 725-728](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=725) | studied | Check unit conversion and spacing without cumulative layout drift. |
| WP51-038 | Precise positioning and advance | [REF51 pp. 31-34; PDF 48-51](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=48) | studied | Compare absolute/relative advances, page limits and text-box origins. |
| WP51-039 | Hyphenation and zones | [REF51 pp. 277-284; PDF 294-301](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=294) | studied | Compare word breaking, zones, manual decisions and saved codes. |

## Pagination

| ID | Feature group | Manual evidence | Study | Acceptance probe |
| --- | --- | --- | --- | --- |
| WP51-040 | Hard/soft pages and conditional breaks | [REF51 pp. 88; PDF 105](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=105); [REF51 pp. 217; PDF 234](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=234); [REF51 pp. 471-473; PDF 488-490](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=488) | studied | Reflow through hard, soft, conditional and odd/even page transitions. |
| WP51-041 | Page numbering and paper definitions | [REF51 pp. 474-486; PDF 491-503](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=491) | studied | Use paper definitions and page numbering across format changes. |
| WP51-042 | Keep-together and widow/orphan rules | [REF51 pp. 51-54; PDF 68-71](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=68); [REF51 pp. 705; PDF 722](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=722) | studied | Force borderline pagination and compare page membership. |
| WP51-043 | Columns and screen column presentation | [REF51 pp. 74-83; PDF 91-100](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=91) | studied | Compare newspaper and parallel columns, breaks, balancing and display. |
| WP51-044 | Headers, footers and suppression | [REF51 pp. 269-274; PDF 286-291](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=286); [REF51 pp. 626-627; PDF 643-644](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=643) | studied | Create header/footer variants; compare suppression and page-dependent placement. |
| WP51-045 | Footnotes and endnotes | [REF51 pp. 209-216; PDF 226-233](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=226) | studied | Test nested text, numbering, continuation and pagination. |
| WP51-091 | Binding offsets and logical page parity | [REF51 pp. 46-48; PDF 63-65](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=63) | studied | Compare odd/even logical page offsets, labels and top-binding behavior. |

## Structure

| ID | Feature group | Manual evidence | Study | Acceptance probe |
| --- | --- | --- | --- | --- |
| WP51-046 | Styles and definitions | [REF51 pp. 616-625; PDF 633-642](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=633) | studied | Create and apply styles, edit definitions and compare resulting code scope. |
| WP51-047 | Outlines and numbering | [REF51 pp. 449-468; PDF 466-485](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=466) | studied | Create, redefine, promote/demote and restyle outline levels. |
| WP51-048 | Tables and structural editing | [REF51 pp. 640-664; PDF 657-681](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=657) | studied | Create tables; edit rows, columns, joins and splits; preserve native structure. |
| WP51-049 | Table formatting and calculations | [REF51 pp. 665-675; PDF 682-692](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=682) | studied | Compare cell/column formatting, formulas and recalculation. |
| WP51-050 | Generated contents, lists and index | [REF51 pp. 221-223; PDF 238-240](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=238); [REF51 pp. 287-291; PDF 304-308](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=304); [REF51 pp. 355-357; PDF 372-374](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=372); [REF51 pp. 682-685; PDF 699-702](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=699) | studied | Mark text, define and regenerate indexes/lists/contents; verify page references. |
| WP51-051 | Table of authorities | [REF51 pp. 676-681; PDF 693-698](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=693) | studied | Mark citations, define categories and regenerate with original ordering. |
| WP51-052 | Master documents and subdocuments | [REF51 pp. 397-400; PDF 414-417](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=414) | studied | Expand/condense subdocuments and regenerate references across them. |
| WP51-053 | Labels and envelopes | [REF51 pp. 319-327; PDF 336-344](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=336); [REF51 pp. 771-772; PDF 788-789](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=788) | studied | Compare definitions, repeated labels and envelope placement with fixed printer settings. |
| WP51-054 | Date values and codes | [REF51 pp. 109-112; PDF 126-129](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=126) | studied | Compare inserted values and generated dates under fixed clock and language settings. |
| WP51-089 | Cross-reference targets and generated references | [REF51 pp. 96-103; PDF 113-120](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=113) | studied | Mark references and named targets separately and together; regenerate after pagination changes. |

## Graphics

| ID | Feature group | Manual evidence | Study | Acceptance probe |
| --- | --- | --- | --- | --- |
| WP51-055 | Graphics boxes, wrapping and captions | [REF51 pp. 232-250; PDF 249-267](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=249) | studied | Create/edit boxes and anchored objects; verify wrapping, sizing and captions. |
| WP51-056 | Graphics formats and conversion utility | [REF51 pp. 228-231; PDF 245-248](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=245); [REF51 pp. 251-256; PDF 268-273](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=268) | studied | Reproduce original import/conversion behavior and preserve embedded/linked resources. |
| WP51-057 | Graphic rules and display options | [REF51 pp. 257-268; PDF 274-285](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=274) | studied | Compare rules, boxes, display settings and printed placement. |
| WP51-058 | Equations and equation editor | [REF51 pp. 163-193; PDF 180-210](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=180); [REF51 pp. 729-740; PDF 746-757](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=746) | studied | Edit equation expressions and compare native representation and rendering. |

## Automation

| ID | Feature group | Manual evidence | Study | Acceptance probe |
| --- | --- | --- | --- | --- |
| WP51-059 | Macro definition, execution and editor | [REF51 pp. 369-393; PDF 386-410](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=386) | studied | Record, edit and execute original macros; compare prompts, keys and errors. |
| WP51-060 | Macro language, expressions and variables | [REF51 pp. 777-892; PDF 794-909](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=794); [REF51 pp. 963-986; PDF 980-1003](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=980) | studied | Catalogue and test each command, expression, variable and value-table behavior. |
| WP51-061 | Original macro conversion utility | [REF51 pp. 370-372; PDF 387-389](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=387) | studied | Compare supported original conversions and unsupported-input handling. |
| WP51-062 | Merge documents, data and commands | [REF51 pp. 418-433; PDF 435-450](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=435); [REF51 pp. 777-892; PDF 794-909](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=794) | studied | Run simple and conditional merges using original file formats and command semantics. |
| WP51-063 | Sorting and record selection | [REF51 pp. 577-586; PDF 594-603](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=594) | studied | Compare keys, ordering, selected records and preservation of fields/codes. |
| WP51-064 | Column math and calculations | [REF51 pp. 401-414; PDF 418-431](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=418) | studied | Define columns and functions; compare arithmetic results and formatting. |
| WP51-065 | Spreadsheet import and links | [REF51 pp. 606-615; PDF 623-632](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=623) | studied | Import supported worksheets; update links and compare data/format refresh behavior. |

## Language

| ID | Feature group | Manual evidence | Study | Acceptance probe |
| --- | --- | --- | --- | --- |
| WP51-066 | WP characters and compose | [REF51 pp. 84-87; PDF 101-104](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=101); [REF51 pp. 913-920; PDF 930-937](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=930) | studied | Input original character-set identities and round-trip every supported mapping. |
| WP51-067 | Language selection and resources | [REF51 pp. 328-336; PDF 345-353](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=345) | studied | Switch language-dependent formatting and resources; record edition applicability. |
| WP51-068 | Spelling, dictionaries, lookup and counts | [REF51 pp. 587-605; PDF 604-622](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=604) | studied | Check corrections, dictionaries, lookup, counts and original utility behavior. |
| WP51-069 | Thesaurus | [REF51 pp. 692-694; PDF 709-711](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=709) | studied | Compare lookup, replacement and return-to-editor workflow using declared resources. |

## Print

| ID | Feature group | Manual evidence | Study | Acceptance probe |
| --- | --- | --- | --- | --- |
| WP51-070 | Print selection, options and quality | [REF51 pp. 487-503; PDF 504-520](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=504); [REF51 pp. 533-542; PDF 550-559](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=550) | studied | Print documents, pages and blocks; compare copies, quality, ordering and stopping. |
| WP51-071 | Printer selection and editing | [REF51 pp. 504-509; PDF 521-526](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=521) | studied | Select/edit original printer settings; preserve resource references and metrics. |
| WP51-072 | Printer commands and functions | [REF51 pp. 510-517; PDF 527-534](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=527) | studied | Exercise direct commands and layout-affecting printer controls. |
| WP51-073 | Printer-definition utility and fonts | [REF51 pp. 518-532; PDF 535-549](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=535); [REF51 pp. 763-764; PDF 780-781](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=780) | studied | Inventory resource-editing and substitution behavior; define Linux equivalent explicitly. |
| WP51-074 | Printing to disk | [REF51 pp. 543; PDF 560](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=560) | studied | Compare original printer-language output bytes with matching resources. |
| WP51-075 | Print jobs and delivery | [REF51 pp. 495-500; PDF 512-517](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=512); [REF51 pp. 576; PDF 593](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=593) | studied | Inspect, cancel and prioritize jobs; map delivery to Linux without changing print data. |
| WP51-076 | Document preview and options | [REF51 pp. 701-704; PDF 718-721](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=718) | studied | Compare page view and facing pages using declared printer metrics. |

## Platform

| ID | Feature group | Manual evidence | Study | Acceptance probe |
| --- | --- | --- | --- | --- |
| WP51-077 | Setup, environment and sound | [REF51 pp. 45-47; PDF 62-64](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=62); [REF51 pp. 122-123; PDF 139-140](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=139); [REF51 pp. 159-162; PDF 176-179](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=176); [REF51 pp. 574-575; PDF 591-592](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=591) | studied | Persist original settings and document Linux adaptations. |
| WP51-078 | DOS and shell integration | [REF51 pp. 150-156; PDF 167-173](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=167); [REF51 pp. 225-227; PDF 242-244](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=242) | studied | Inventory external-process workflows and define explicit Linux mappings. |
| WP51-079 | Bundled conversion, cursor and capture utilities | [REF51 pp. 89-95; PDF 106-112](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=106); [REF51 pp. 105-108; PDF 122-125](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=122); [REF51 pp. 567-570; PDF 584-587](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=584) | studied | Study utility boundaries and original artifact behavior before choosing Linux implementation. |
| WP51-080 | Memory and startup controls | [REF51 pp. 415-417; PDF 432-434](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=432); [REF51 pp. 897-904; PDF 914-921](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=914) | studied | Classify original startup and memory controls; record hardware-only adaptations. |
| WP51-081 | Network and original resource files | [REF51 pp. 921-960; PDF 938-977](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=938) | indexed | Inventory shared-file behavior, locking, resource discovery and companion formats. |
| WP51-082 | Code tables, defaults, keyboards and errors | [REF51 pp. 715-728; PDF 732-745](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=732); [REF51 pp. 741-762; PDF 758-779](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=758); [REF51 pp. 765-776; PDF 782-793](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=782); [REF51 pp. 893-896; PDF 910-913](https://mendelson.org/wpdos/WPDOS51Reference.pdf#page=910) | studied | Reconcile appendices against feature coverage and negative scenarios. |

## Native formats

| ID | Feature group | Manual evidence | Study | Acceptance probe |
| --- | --- | --- | --- | --- |
| FMT51-001 | File prefix and document pointer | [SDK51 pp. 3-6; PDF 16-19](https://mendelson.org/wpdos/WP51DevelopersToolkit.pdf#page=16) | studied | Check identifiers, versions, byte order, encryption marker and document pointer against original files. |
| FMT51-002 | Prefix index chains and packets | [SDK51 pp. 7-16; PDF 20-29](https://mendelson.org/wpdos/WP51DevelopersToolkit.pdf#page=20) | studied | Preserve packet bytes and references while testing bounds, cycles and relocations. |
| FMT51-003 | Document code framing and nested text | [SDK51 pp. 17-18; PDF 30-31](https://mendelson.org/wpdos/WP51DevelopersToolkit.pdf#page=30) | studied | Validate fixed/variable frames, nested codes and unknown-code preservation. |
| FMT51-004 | Original character and function encoding | [SDK51 pp. 19-35; PDF 32-48](https://mendelson.org/wpdos/WP51DevelopersToolkit.pdf#page=32) | indexed | Check every defined code class against fixtures, including hard/soft boundary codes. |
| FMT51-005 | Formatting, structure and automation code groups | [SDK51 pp. 36-91; PDF 49-104](https://mendelson.org/wpdos/WP51DevelopersToolkit.pdf#page=49) | indexed | Map every WP code group to semantic behavior and round-trip fixtures. |
| FMT51-006 | Native WPM macro serialization | [SDK51 pp. 92-99; PDF 105-112](https://mendelson.org/wpdos/WP51DevelopersToolkit.pdf#page=105) | indexed | Read/write macro headers and command encodings with original interpreter evidence. |

## Coverage still to reconcile

- Audit every reference chapter, appendix, menu entry, macro/merge command,
  character/code table and original utility against stable inventory IDs.
- Decompose compound groups into independently testable obligations; preserve
  parent IDs and provenance when splitting entries.
- Expand the [36-lesson thematic map](workbook-map.md) (WB51 contents, PDF 4-5)
  into step-level acceptance scenarios without republishing lesson text.
- Fingerprint the [selected reference release](../decisions/0001-reference-release.md), language editions, original resources,
  proprietary fixture provenance and Linux platform adaptations.
- Check toolkit and reference-manual release differences against the original.
- No coverage percentage or parity claim until this reconciliation is complete.
