# WP43 first-native field observations (not constructor defaults)

Exact selected profile; each row delegates meaning/units to approved23 field authority.
All72 entries are literal original observations. Constructor permission is false for every row.

| Owner | Absolute offset | Width | Field | Representation / units | Original hex |
| --- | --- | --- | --- | --- | --- |
| header | 0 | 4 | signature | bytes; identity | ff575043 |
| header | 4 | 4 | body start | u32le; bytes | 44010000 |
| header | 8 | 1 | product | u8; identity | 01 |
| header | 9 | 1 | file type | u8; identity | 0a |
| header | 10 | 1 | stored major | u8; identity | 00 |
| header | 11 | 1 | stored minor | u8; identity | 01 |
| header | 12 | 2 | encryption key | u16le; identity | 0000 |
| header | 14 | 2 | reserved | u16le; identity | 0000 |
| packet-7 | 66 | 14 | font name string pool | NUL-terminated ASCII; name | 436f757269657220313063706900 |
| packet-15 | 80 | 2 | font instance ID | u16le; resource identifier | 0000 |
| packet-15 | 82 | 2 | proportional-spacing cache ID | u16le; FFFF none | ffff |
| packet-15 | 84 | 2 | top shoulder height | u16le; PSU | 8900 |
| packet-15 | 86 | 2 | bottom shoulder height | u16le; PSU | 3f00 |
| packet-15 | 88 | 2 | printed character width | u16le; WPU | 7800 |
| packet-15 | 90 | 2 | optimal space width | u16le; WPU | 7800 |
| packet-15 | 92 | 2 | normal space width | u16le; WPU | 7800 |
| packet-15 | 94 | 2 | horizontal motion units | u16le; resource units | 0a00 |
| packet-15 | 96 | 2 | horizontal fractional numerator | u16le; resource ratio numerator | 0100 |
| packet-15 | 98 | 2 | font string pool offset | u16le; packet-relative bytes | 0000 |
| packet-15 | 100 | 1 | font flags | u8 flags; bitset; bit meanings unexpanded here | 00 |
| packet-15 | 101 | 2 | descriptor match hash | u16le; resource hash | e724 |
| packet-15 | 103 | 2 | descriptor: cell height | u16le; 1/3600 inch | f401 |
| packet-15 | 105 | 2 | descriptor: optimal width | u16le; WPU | 7800 |
| packet-15 | 107 | 2 | descriptor: cap height | u16le; PSU | fe15 |
| packet-15 | 109 | 2 | descriptor: x height | u16le; PSU | 3610 |
| packet-15 | 111 | 2 | descriptor: descender height | u16le; PSU | 5807 |
| packet-15 | 113 | 2 | descriptor: italic adjustment | i16le; PSU signed | 0000 |
| packet-15 | 115 | 3 | descriptor: typeface descriptor | u24le bitset; traits; high bit reserved0 | 000411 |
| packet-15 | 118 | 1 | descriptor: 5.0 typeface flags | u8 bitset; traits/weight | 40 |
| packet-15 | 119 | 1 | descriptor: typeface-name hash | u8; resource hash | c9 |
| packet-15 | 120 | 1 | descriptor: display-resource quality | u8; DRS-only quality enum | 00 |
| packet-15 | 121 | 2 | descriptor: font-name hash | u16le; resource hash | 9338 |
| packet-15 | 123 | 4 | descriptor: character-set completeness | 2xu16le bitsets; two planes, bit n indexes WP character set | 01000100 |
| packet-15 | 127 | 2 | descriptor: 5.1 point size | u16le; 1/3600 inch | 5802 |
| packet-15 | 129 | 1 | descriptor: 5.1 typeface flags | u8 bitset; traits/PS/weight | 40 |
| packet-15 | 130 | 16 | attribute AFC | array u8; one byte per code/charset/orientation index | fffffffffffffffffffffffffffffffe |
| packet-15 | 146 | 16 | character-set AFC | array u8; one byte per code/charset/orientation index | ffffffffffffffffffffffffffffffff |
| packet-15 | 162 | 4 | orientation AFC | array u8; one byte per code/charset/orientation index | ffffffff |
| packet-12 | 166 | 37 | printer long name | NUL string padded; name | 5374616e64617264205072696e746572000000000000000000000000000000000000000000 |
| packet-12 | 203 | 13 | PRS filename | NUL string; resource name | 5354414e5052494e2e50525300 |
| packet-12 | 216 | 2 | initial font descriptor: cell height | u16le; 1/3600 inch | db01 |
| packet-12 | 218 | 2 | initial font descriptor: optimal width | u16le; WPU | 7800 |
| packet-12 | 220 | 2 | initial font descriptor: cap height | u16le; PSU | 141e |
| packet-12 | 222 | 2 | initial font descriptor: x height | u16le; PSU | 0c17 |
| packet-12 | 224 | 2 | initial font descriptor: descender height | u16le; PSU | 8c0a |
| packet-12 | 226 | 2 | initial font descriptor: italic adjustment | i16le; PSU signed | 0000 |
| packet-12 | 228 | 3 | initial font descriptor: typeface descriptor | u24le bitset; traits; high bit reserved0 | 000411 |
| packet-12 | 231 | 1 | initial font descriptor: 5.0 typeface flags | u8 bitset; traits/weight | 40 |
| packet-12 | 232 | 1 | initial font descriptor: typeface-name hash | u8; resource hash | c9 |
| packet-12 | 233 | 1 | initial font descriptor: display-resource quality | u8; DRS-only quality enum | 00 |
| packet-12 | 234 | 2 | initial font descriptor: font-name hash | u16le; resource hash | 87cf |
| packet-12 | 236 | 4 | initial font descriptor: character-set completeness | 2xu16le bitsets; two planes, bit n indexes WP character set | 01000100 |
| packet-12 | 240 | 2 | minimum top | u16le; resource margin | 0000 |
| packet-12 | 242 | 2 | minimum bottom | u16le; resource margin | 0000 |
| packet-12 | 244 | 2 | minimum left | u16le; resource margin | 0000 |
| packet-12 | 246 | 2 | minimum right | u16le; resource margin | 0000 |
| packet-12 | 248 | 1 | printer flags | u8 bitset; selection/init/hzone/orientations | 18 |
| packet-12 | 249 | 2 | PRS date | u16le packed; DOS day5/month4/year7+1980 | 6918 |
| packet-12 | 251 | 2 | PRS time | u16le packed; DOS sec/2,min6,hour5 | 8a60 |
| packet-12 | 253 | 2 | current font point size | u16le; 1/3600 inch | 5802 |
| packet-12 | 255 | 1 | current typeface flags | u8 bitset; traits/weight | 40 |
| packet-6 | 256 | 1 | document flags | u8 bits; bit3 must-format; all other bits zero in admitted slice | 00 |
| packet-6 | 257 | 1 | quality nibbles | u8; low text / high graphics;0none1draft2medium3high | 23 |
| packet-6 | 258 | 2 | redline character | u16le; character setting | 7c00 |
| packet-6 | 260 | 2 | screen character width | u16le; WPU | 7800 |
| packet-6 | 262 | 2 | binding width | u16le; WPU | 0000 |
| packet-6 | 264 | 1 | printer-select counter for equation hash | u8; opaque original counter value | 01 |
| packet-6 | 265 | 1 | reserved | u8; zero | 00 |
| packet-6 | 266 | 2 | display pitch | u16le; documentary0100=100%; observed0 not given invented physical meaning | 0000 |
| packet-6 | 268 | 2 | screen resolution | u16le; resource/display setting | 0000 |
| packet-6 | 270 | 2 | reserved | u16le; zero | 0000 |
| packet-8 | 322 | 2 | graphics count | u16le; zero only | 0000 |

Index spans and linked relationships are listed in contract.md and the raw field reports.
Resource hashes/packed stamps/flags remain qualified observations; universal values and
generation algorithms are not inferred from this table or its two-run equality.
Native files and each field also retain SHA, parent case, revision and exact source pointers
in genesis-ledger.json; first-prefix coverage has no unmapped bytes. Original-resaved
deleted/unmapped families remain a separate B/C admission prerequisite.
