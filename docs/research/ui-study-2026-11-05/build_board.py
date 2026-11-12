"""Build a local visual research board from original VM captures."""
import json, html, hashlib
from pathlib import Path
from collections import Counter
from PIL import Image
P=Path(__file__).resolve().parent
cards=[
("01-startup","Foundation","The quiet editing screen","Fresh fingerprinted reference boot.","The document begins at the first cell. The status occupies the final row toward the right. There is no application title or permanent shortcut toolbar."),
("03-function-key-template","Foundation","The original keyboard vocabulary","F3, then F3 again.","The app teaches its modifier families. F11 Reveal Codes and F12 Block are present in the Enhanced template. Treat the keyboard template as an acceptance surface, including Ctrl combinations with original meanings."),
("05-file-menu","Menus","A menu carries more than labels","Alt+=, F.","Borders, separators, red mnemonic letters, right-aligned shortcuts and submenu arrows make the menu readable. The live File menu differs from the later manual inventory used in the preview."),
("06-edit-menu","Menus","Unavailable commands have a visual state","Right from File.","Several entries are bracketed. The original communicates availability before activation. Wordling currently presents several entries whose only action is an unimplemented message."),
("07-layout-menu","Menus","Groups express the document model","Move across the menu bar to Layout.","Line, Page, Document and Other form one group. Columns, tables and math form another. Preserve these groupings, borders and shortcut columns."),
("37-nested-menu","Menus","Submenus attach to the selected row","Alt+=, L, J from the saved sample.","The Justify submenu opens alongside its parent row, while the parent remains visible. The current preview puts child menus at the top of the screen and loses this relationship."),
("38-f1-submenu-still-visible","Menus","An unresolved cancellation detail","F1 from the Justify submenu, followed by an explicit wait.","The submenu remained visible in two attempts. The manual describes F1 backing up a level. Automatic reopening, focus and timing need a controlled follow-up. Do not turn the manual expectation into an observed result."),
("42-menu-options","Menus","Visibility is a real original preference","Shift+F1, 2 Display, 4 Menu Options.","The pinned profile has Alt-key activation and Menu Bar Remains Visible both set to No. Separator-line and mnemonic/text appearance settings also exist."),
("45-visible-option-enabled","Menus","A persistent menu is historically supported","Menu Options, 8, Y.","This changes Menu Bar Remains Visible to Yes in the scratch guest only. The selected profile must include this preference when we compare Wordling with the original."),
("46-visible-bar-document","Menus","Visible menus and editing focus coexist","F7 from Setup after enabling persistent visibility.","The menu bar remains visible above the text and the editor resumes. This is the reference for the user's preferred visible-menu experience."),
("14-editing-settled","Editing","Attributes have specific screen appearances","Type the sample, using F6 and F8 around two words.","Bold and underline have distinct renderings. The underline word uses contrasting cells in this profile. Faithfulness includes attribute colors and cursor shape, beyond terminal bold and underline escapes."),
("13-reveal-settled","Editing","Reveal Codes is a second document view","Alt+F3 on the formatted three-line sample.","Paragraph structure appears in both panes. The upper pane ends with status, then a red ruler with margin and tab markers. Codes and content span multiple lower-pane lines. The bottom line explains how to restore the screen."),
("47-visible-bar-wrapped-document","Editing","Wrapping follows document geometry","Shift+F3 to Doc 2, then type the research sentence.","The 122-character paragraph wraps before the right edge of the 80-column display. The status advances to Ln 1.17 inches. Terminal width and printed text width are separate concerns."),
("48-wrapped-reveal","Editing","A soft return is visible and meaningful","Alt+F3 on the wrapped paragraph.","The original displays [SRt] at the wrapping boundary. This connects layout, cursor navigation and Reveal Codes. A view that merely splits on hard returns cannot reproduce this interaction."),
("15-save-prompt","Prompts","Save leaves the document in view","F10 in Doc 1.","The bottom line becomes Document to be saved. The document remains visible, with prompt input focus. This requires explicit modal state and reliable cancellation."),
("22-search-entry","Prompts","Search uses the same prompt grammar","Home, Home, Up; F2; type bold.","The bottom line shows -> Srch: bold. Search needs its own input semantics, including native code searches. It is a core editing workflow."),
("23-search-result","Prompts","Search returns to editing at the match","F2 completes the entered search.","The prompt disappears and the physical position changes to 2.2 inches. Text content remains intact. We need to compare cursor placement as well as the presence of a result."),
("33-directory-request","Files","F5 starts with a directory request","F5 from editing.","The current document remains visible while the bottom line asks for Dir C:\\WP51\\*.*. The hint explains how to change the default directory."),
("24-file-selected","Files","The full List Files screen","F5, accept the default directory, Down.","The dense two-column list has DOS name/extension alignment, directory entries, dates, a divider, scrolling indicator, red header and full-row selection. Statistics distinguish document size from disk file size."),
("34-out-file-selected","Files","A selected native file","Enter C:\\OUT\\ at the directory request, then Down.","STUDY.WP is selected. The original displays an in-memory document size of 347 and a disk file size of 397. These fields must be measured according to their original definitions."),
("35-look-confirmed","Files","Look has its own screen and navigation","6 with STUDY.WP selected.","The header shows the path, WP5.1 type and revision time. The footer offers Next Doc and Prev Doc. This view previews a file without replacing the current editing document."),
("36-look-to-list","Files","Returning preserves browser context","F1 from Look.","The list and selected STUDY.WP return. Browser state is part of the experience, including the current directory, selected item and chosen operation."),
("32-exit-save-question","Prompts","Even an unmodified document has an exit flow","F7 from the saved document.","Save document? appears with the Text was not modified annotation. Implement the actual defaults and prompt transitions rather than a generic modern confirmation dialog."),
("49-unsaved-exit-question","Prompts","Unsaved exit is a distinct case","F7 from the unsaved wrapped Doc 2.","The original asks Save document? Yes (No), while preserving the visible text and persistent menu. Compare this with the saved-document case."),

("50-after-declining-save","Prompts","Closing Doc 2 has its own confirmation","N at the Doc 2 save question.","The prompt is Exit doc 2? No (Yes). Confirming it returns to Doc 1. This differs from terminating the application."),
("51-exit-wp-confirmation","Prompts","The final document controls application exit","After closing Doc 2, F7 and N in Doc 1.","The prompt is now Exit WP? No (Yes). Y returns to the DOS prompt. A single generic Exit state would miss this distinction."),
]
for name, *_ in cards:
    assert (P/name/"screen.png").is_file(), name
def esc(s):return html.escape(s)
manifest={"reference":"WP 5.1 US 03/09/92","date":"2026-11-05","selected_captures":[],"limits":[
"FreeDOS 1.4 and the pinned Standard Printer resources are the established reference profile, not an untouched 1992 shipping environment.",
"This is qualitative observation from one scratch guest. These sequences have not been independently repeated as acceptance tests.",
"Initial captures 09, 11 and 12 were premature. Captures 18-19 and 25 show directory prompts rather than a successful Look preview. Captures 26-31 and 44 arose during unsuccessful navigation. They are retained as raw evidence and excluded from the board.",
"F1 submenu cancellation is unresolved. The report distinguishes manual expectations from observations.",
"Mouse hover/drag, alternate display adapters, graphics preview, startup splash, printer output and full feature parity were not evaluated."
]}
for name, group, title, keys, note in cards:
    image=P/name/"screen.png"
    manifest["selected_captures"].append(dict(id=name,group=group,title=title,sequence=keys,notes=note,sha256=hashlib.sha256(image.read_bytes()).hexdigest()))
(P/"observations.json").write_text(json.dumps(manifest,indent=2)+"\n")
parts=[]
for name,group,title,keys,note in cards:
    parts.append(f'''<article data-group="{group}"><div class="eyebrow">{group} · {name.split("-")[0]}</div><h3>{esc(title)}</h3><button class="image" aria-label="Enlarge {esc(title)}"><img loading="lazy" src="{name}/screen.png" alt="{esc(title)}"></button><p class="sequence">{esc(keys)}</p><p>{esc(note)}</p><a href="{name}/screen.txt">Text capture</a> · <a href="{name}/vram.bin">Original character and attribute bytes</a></article>''')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Wordling · Original WordPerfect interface study</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#f3f0e9;color:#202632;font:17px/1.55 system-ui,sans-serif}main{max-width:1504px;margin:auto;padding:48px 32px}h1{font-size:clamp(32px,4vw,58px);line-height:1.08;max-width:950px;margin:12px 0 20px}h2{font-size:29px;margin:42px 0 14px}h3{font-size:22px;line-height:1.25;margin:7px 0 16px}.eyebrow{font-size:12px;letter-spacing:1.5px;text-transform:uppercase;color:#59657b;font-weight:700}.lead{font-size:22px;max-width:1100px}.intro{max-width:1100px}a{color:#243b94}nav{display:flex;gap:8px;flex-wrap:wrap;margin:22px 0}nav button,.close{font:inherit;border:1px solid #aaa;background:white;padding:8px 16px;cursor:pointer}nav button[aria-pressed=true]{background:#202632;color:white}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}article{padding:24px;background:#fff;border:1px solid #d9d5cc;border-radius:6px}article p{margin:12px 0}.image{border:0;background:#0000a8;padding:0;display:block;width:100%;cursor:zoom-in}img{width:100%;display:block;image-rendering:pixelated}.sequence{font-size:14px;color:#5b6371}article a{font-size:13px}.swatches{display:flex;gap:16px;flex-wrap:wrap;margin:22px 0}.swatch{border:1px solid #ccc;padding:10px;background:white}.chip{display:block;width:160px;height:45px;margin-bottom:8px}.note{padding:20px 24px;background:#e5e8ee;border-left:4px solid #435fa3}table{border-collapse:collapse;width:100%;background:white;font-size:16px}th,td{text-align:left;vertical-align:top;border:1px solid #d5d7dd;padding:14px}th{background:#e5e8ee}dialog{padding:20px;border:0;max-width:95vw;background:#f3f0e9}dialog img{width:min(1440px,85vw)}dialog::backdrop{background:#111c}footer{margin-top:40px;padding-top:20px;border-top:1px solid #ccc;font-size:14px}.hidden{display:none}@media(max-width:850px){.grid{grid-template-columns:1fr}main{padding:24px 16px}table{font-size:14px}}@media print{nav,dialog{display:none}main{padding:0}.grid{display:block}article{break-inside:avoid;margin-bottom:20px}article img{max-width:650px}.hidden{display:block}}
</style><main>
<div class="eyebrow">Wordling 5.2 · Field study · 5 November 2026</div>
<h1>Reconstruct the experience around the document.</h1>
<p class="lead">A visual research board from a fresh run of WordPerfect 5.1 for DOS, release 03/09/92. The gap is broader than appearance. Menus, keyboard focus, document layout, codes, file browsing and prompts form one connected application.</p>
<div class="grid">
<figure style="margin:0"><img src="37-nested-menu/screen.png" alt="Original Layout menu with nested Justify menu"><figcaption>Menu hierarchy, alignment and command vocabulary</figcaption></figure>
<figure style="margin:0"><img src="13-reveal-settled/screen.png" alt="Original document and multiline Reveal Codes"><figcaption>Document layout, code structure and shared cursor context</figcaption></figure>
</div><p class="intro">Twenty-six selected captures cover the editor, Help, menus and settings, formatting, Reveal Codes, wrapping, Save, Search, List Files, Look and Exit. Each card includes an observation and its interaction context. Click an image to inspect it at a larger size. Raw captures and the chronological input trace accompany the board.</p>
<div class="note"><strong>What changed my assessment</strong><p>The current implementation has valuable native-document and safety machinery, but the visible application still exposes only a bounded part of WordPerfect. Completing individual command handlers has not produced complete everyday workflows. We should use complete original-app journeys as the next units of implementation and review.</p></div>
<h2>The visual vocabulary</h2>
<p>These values are sampled from the reference raster. The observed display is 720 × 400 pixels, with 80 × 25 character cells of 9 × 16 pixels. The raster uses gray body text, bright white emphasis, a deep blue canvas and red selection/ruler areas. Terminal font, cell dimensions and color themes can all change the result on Linux.</p>
<div class="swatches">
<div class="swatch"><span class="chip" style="background:#0000a8"></span>Canvas · #0000A8</div>
<div class="swatch"><span class="chip" style="background:#a8a8a8"></span>Text / menu · #A8A8A8</div>
<div class="swatch"><span class="chip" style="background:#a80000"></span>Selection · #A80000</div>
<div class="swatch"><span class="chip" style="background:#fff"></span>Emphasis · #FFFFFF</div>
</div>
<p>The color values belong to this QEMU capture profile. Preserve the original character attributes as the primary evidence as well as the rendered PNGs.</p>
<h2>The reference board</h2><nav aria-label="Filter research board">FILTERS</nav><div class="grid">CARDS</div>
<h2>What the reconstruction needs next</h2>
<table><thead><tr><th>Observed system</th><th>Current gap</th><th>Proposed acceptance target</th></tr></thead><tbody>
<tr><td>Menu grammar and settings</td><td>Missing borders, groups, shortcut columns, availability rules and many command implementations. Submenus have the wrong placement. Persistent visibility lacks the original settings workflow.</td><td>Reproduce File, Edit and Layout journeys from a defined original configuration. Check keyboard and mouse focus, command routing, cancellation, unavailable entries and document preservation at every step.</td></tr>
<tr><td>Document geometry</td><td>Printed positions remain unknown. General wrapping, vertical movement and layout are incomplete.</td><td>Begin with the exact Standard Printer profile. Make a paragraph wrap at the same word, navigate the same lines and code boundaries, and display the same page/line/position values. Test at 80 × 25 before testing larger Linux terminals.</td></tr>
<tr><td>Reveal Codes</td><td>The preview compresses the lower pane into one line and lacks the actual ruler and tab/margin presentation.</td><td>Keep both panes synchronized through hard returns, soft returns, attributes, code insertion and deletion. Match active-code emphasis, caret movement, scrolling and pane geometry.</td></tr>
<tr><td>File lifecycle</td><td>List Files can retrieve a flat local file, but directory navigation, Look and most numbered operations remain incomplete.</td><td>Browse, select, preview, return to the same selection, retrieve, edit, save, decline replacement and reopen. Define how DOS drive/directory semantics map onto Linux while keeping the original prompts and interaction sequence.</td></tr>
<tr><td>Command and prompt coverage</td><td>Search, Help and many menu actions are placeholders or absent. Some low-level refusals leak into normal interaction.</td><td>Complete the ordinary typing, correction, search, formatting and save loop. Every advertised command should have a working path or an accurately represented original availability state.</td></tr>
<tr><td>Release and display profile</td><td>The later manual and live March 1992 menus differ. Linux terminal appearance varies with font and window size.</td><td>Record release, keyboard, printer and menu settings together. Treat the live reference as the release-specific oracle, with manuals explaining options. Specify supported terminal geometry and rendering limits.</td></tr>
</tbody></table>
<h2>A practical implementation sequence</h2>
<ol>
<li><strong>Capture complete journeys.</strong> Convert this board into scripts with explicit checkpoints, including defaults, focus, cancellation, file effects and settings. Repeat the uncertain observations. Keep later-manual expectations separate from March 1992 observations.</li>
<li><strong>Complete the application shell.</strong> Build a shared model of screens, menus, focus and bottom-line prompts. Reuse the native document/session/storage layers. Add the original Help template and preference-backed menu visibility.</li>
<li><strong>Deliver one usable editing journey.</strong> Create a document, type and wrap text, move around it, apply Bold and Underline, inspect and edit codes, search, save, reopen and exit. Include the full file browser path. Finish and review every transition before calling this milestone usable.</li>
<li><strong>Expand against the parity inventory.</strong> Continue through page formatting, printing, tables, styles, macros, merges, graphics and the remaining commands. A usable basic editor is a milestone within parity, not completion of the mission.</li>
<li><strong>Gate completion on differential evidence and use.</strong> Run the same scripts in the original and Wordling. Compare character/attribute grids, cursor and focus, prompts, document bytes and file outcomes. Add independent review and a real interactive trial. PDF export should use the same qualified layout work.</li>
</ol>
<p><strong>Recommended immediate milestone</strong> A complete everyday editing session with faithful menus and Reveal Codes. This provides a concrete product checkpoint while retaining the full parity mission. Estimate the rest only after mapping the incomplete commands and their layout dependencies.</p>
<h2>Presentation notes</h2>
<ol>
<li><strong>Open with the original blank screen and keyboard template.</strong> Explain the fixed cell grid and the original key vocabulary. Point out that a blank blue screen is an authentic state, but discoverability must follow the selected menu setting.</li>
<li><strong>Show File, Layout and the nested Justify menu.</strong> Walk through grouping, shortcut labels, borders and parent-child alignment. Show the unresolved F1 capture as a research question.</li>
<li><strong>Show Menu Options beside the persistent-bar editing screen.</strong> The original already supports the user's preference. Reconstruct its configuration and focus behavior rather than introducing an unexplained default.</li>
<li><strong>Compare normal text, wrapped text and Reveal Codes.</strong> Explain why layout, cursor motion and code presentation must be implemented together.</li>
<li><strong>Walk through directory request, List Files, Look and return.</strong> This is one connected file workflow. A two-column rendering alone does not complete F5.</li>
<li><strong>End with the proposed everyday editing milestone.</strong> Review a full journey with a usable executable, then grow the remaining parity inventory. State the outstanding work and evidence limits plainly.</li>
</ol>
<h2>Evidence and limits</h2>
<p>The existing harness verified hashes for the master disk, boot image, QEMU executable and firmware before launching this independent offline guest. Help displays WP 5.1 03/09/92. The guest uses FreeDOS 1.4 and the established Standard Printer installation. The original profile includes printer resources dated July 1992. These details qualify the reference environment.</p>
<p>This is a qualitative study from one scratch guest. Early or misdirected captures remain in the raw evidence but are excluded from the selected board. The F1 nested-menu behavior remains unresolved. No graphics-mode, printer-output, startup-splash or mouse-drag fidelity claim follows from this study. The application source and preview were not changed during this exercise. The scratch session closed both documents, returned to the DOS prompt, and the guest was stopped.</p>
<footer><a href="observations.json">Structured observations and capture hashes</a> · <a href="trace.jsonl">Chronological actions, waits and failures</a> · <a href="capture.py">Reference capture driver</a> · <a href="../reference-environment/environment.json">Pinned environment</a> · <a href="../../../../research/cache/reference.txt">Local manual transcription</a><p>Local research artifact. The board uses direct screenshots of the original app, with notes outside the images.</p></footer>
</main><dialog><button class="close">Close</button><img alt=""><p></p></dialog>
<script>
const dialog=document.querySelector('dialog');
document.querySelectorAll('.image').forEach(button=>button.onclick=()=>{dialog.querySelector('img').src=button.querySelector('img').src;dialog.querySelector('img').alt=button.querySelector('img').alt;dialog.querySelector('p').textContent=button.closest('article').querySelector('h3').textContent;dialog.showModal()});
document.querySelector('.close').onclick=()=>dialog.close();
dialog.onclick=e=>{if(e.target===dialog)dialog.close()};
document.querySelectorAll('nav button').forEach(button=>button.onclick=()=>{document.querySelectorAll('nav button').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));document.querySelectorAll('article').forEach(card=>card.classList.toggle('hidden',button.textContent!=='All'&&card.dataset.group!==button.textContent))});
</script></html>'''
filters=''.join(f'<button aria-pressed="{str(group=="All").lower()}">{group}</button>' for group in ["All","Foundation","Menus","Editing","Prompts","Files"])
page=page.replace("FILTERS",filters).replace("CARDS","".join(parts))
# Paths are relative to docs/research/ui-study-2026-11-05.
page=page.replace('../../../../research/cache/reference.txt','../../../research/cache/reference.txt')
(P/"index.html").write_text(page)
print(f"Built board with {len(cards)} original captures")
