from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output' / 'pdf'
OUT.mkdir(parents=True, exist_ok=True)
INK = colors.HexColor('#172b38')
TEAL = colors.HexColor('#167b86')
GRAY = colors.HexColor('#54636d')
STYLES = {
    'title': ParagraphStyle('title', fontName='Helvetica-Bold', fontSize=29, leading=32, textColor=INK, spaceAfter=12),
    'sub': ParagraphStyle('sub', fontName='Helvetica', fontSize=10, leading=14, textColor=GRAY, spaceAfter=13),
    'h': ParagraphStyle('h', fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=TEAL, spaceBefore=14, spaceAfter=8, keepWithNext=True),
    'body': ParagraphStyle('body', fontName='Helvetica', fontSize=10.5, leading=15, textColor=INK, spaceAfter=8),
    'line': ParagraphStyle('line', fontName='Helvetica', fontSize=10.5, leading=14.5, textColor=INK, leftIndent=23, rightIndent=12, spaceAfter=6),
    'caption': ParagraphStyle('caption', fontName='Helvetica', fontSize=8.5, leading=12, textColor=GRAY, spaceBefore=7, spaceAfter=8),
}

def para(text, style='body'):
    return Paragraph(escape(text), STYLES[style])

def footer(c, doc):
    c.setStrokeColor(TEAL)
    c.setLineWidth(1)
    c.line(48, 41, 564, 41)
    c.setFont('Helvetica', 8)
    c.setFillColor(GRAY)
    c.drawString(48, 28, 'LOST VANGUARD  /  WORKING DRAFT  /  OCTOBER 7, 2026')
    c.drawRightString(564, 28, str(doc.page))

def build(name, flow):
    path = OUT / name
    doc = SimpleDocTemplate(str(path), pagesize=(612, 792), leftMargin=48, rightMargin=48,
                            topMargin=44, bottomMargin=57, title=name.replace('_', ' ').replace('.pdf', ''),
                            author='Lost Vanguard project')
    doc.build(flow, onFirstPage=footer, onLaterPages=footer)
    reader = PdfReader(path)
    print(f'{name}: {len(reader.pages)} pages, {path.stat().st_size} bytes')
    assert all((p.extract_text() or '').strip() for p in reader.pages)
    return len(reader.pages)

def scene_md(section):
    result = []
    for block in section.strip().split('\n\n'):
        block = block.strip()
        if not block:
            continue
        if block.startswith('### '):
            result.append(para(block[4:], 'h'))
        elif block.startswith(('CLANK:', 'EVAN:', 'HUMAN SIGNAL:', 'FIELD COMMANDER:', 'ENGINEER:')):
            who, line = block.split(':', 1)
            result.append(Paragraph(f'<b>{escape(who)}</b>  {escape(line.strip())}', STYLES['line']))
        else:
            result.append(para(block))
    return result

source = (ROOT / 'docs' / 'SHARE_SCRIPT.md').read_text(encoding='utf-8')
opening = source.split('## Mission 1: Wreckage\n', 1)[1].split('## Proposed opening campaign arc', 1)[0]
parts = opening.split('### Scene ')
scenes = ['### Scene ' + x for x in parts[1:]]
script = [para('Lost Vanguard', 'title'), para('STORY SCRIPT  /  MISSION 1: WRECKAGE', 'sub'),
          para('A complete opening-mission draft, followed by the proposed five-mission arc. Contains story spoilers. Dialogue and detailed staging remain proposals; this is not a transcript of the playable prototype.', 'caption')]
script += scene_md(scenes[0]) + scene_md(scenes[1])
script += [PageBreak(), para('Wreckage', 'title'), para('FIRST CONTACT WITH THE SEARCHERS', 'sub')]
script += scene_md(scenes[2]) + scene_md(scenes[3])
script += [PageBreak(), para('Wreckage', 'title'), para('A WAY FORWARD', 'sub')]
script += scene_md(scenes[4]) + scene_md(scenes[5])
arc = source.split('## Proposed opening campaign arc\n', 1)[1].split('## Underlying story truth', 1)[0]
script += [PageBreak(), para('Beyond the wreck', 'title'), para('PROPOSED OPENING CAMPAIGN ARC', 'sub')]
arc_start, arc_end = arc.split('### Mission 4 - Empty Archive', 1)
script += scene_md(arc_start)
script += [PageBreak(), para('Following the evidence', 'title'), para('PROPOSED OPENING CAMPAIGN ARC - CONTINUED', 'sub')]
script += scene_md('### Mission 4 - Empty Archive' + arc_end)
truth = source.split('## Underlying story truth - spoilers\n', 1)[1]
script += [PageBreak(), para('The truth behind the war', 'title'), para('STORY BACKGROUND  /  MAJOR SPOILERS', 'sub')]
script += [para(b) for b in truth.strip().split('\n\n')]
script += [para('Still to develop', 'h'), para('The full campaign ending, Evan\'s survival, Clank\'s retained objective, enemy designs, officer duties, and the artifact\'s final location remain open. This package shares the current story direction without settling those choices.')]
n = build('Lost_Vanguard_Story_Script.pdf', script)
assert n == 6, f'Unexpected script overflow: {n}'

brief = [para('Lost Vanguard', 'title'), para('ORIGINAL MILITARY SCIENCE FICTION  /  EARLY PROTOTYPE', 'sub'),
         para('A soldier built by the enemy wakes inside his destroyed ship, days after an attack he cannot remember. With his damaged robot companion, he fights through the wreck and investigates a war whose true cause humanity does not understand.'),
         Spacer(1, 4), Image(str(ROOT / 'assets/references/level_01/opening_wreck_alien_forest_reference.png'), width=516, height=281.7),
         para('USER-SUPPLIED VISUAL REFERENCE. Intended atmosphere, not current gameplay or finished game art. Final designs and sky details remain open.', 'caption'),
         para('A world to uncover', 'h'),
         para('Orison holds technology left by an extinct civilization. Humanity is at war with an alien species while the escaped AI Meridian threatens both sides. Missions combine military action, exploration, and evidence that changes what the player understands.'),
         para('The people at its center', 'h'),
         para('Evan is a restrained Praetorian leader, created through forced enemy experiments and later rescued by humans. Clank is his small robot companion and best friend, surviving with EMP-damaged memories. Major Lena Cross and Commander Dorian Vale are separate supporting officers whose exact roles are still being developed.'),
         PageBreak(), para('From idea to playable', 'title'), para('WHAT EXISTS NOW  /  WHAT COMES NEXT', 'sub'),
         Image(str(ROOT / 'reports/opening_starting_view_play.png'), width=454, height=256.2),
         para('ACTUAL UNREAL EDITOR PLAY SCREENSHOT. Simple shapes represent the wreck and forest while the route and gameplay are developed.', 'caption'),
         para('The first mission', 'h'),
         para('Free Evan from debris, follow Clank\'s recovery checks, collect a weapon, defeat wreck searchers, recover a search record, and restore communications. The tutorial checks a trained soldier\'s condition while teaching the controls.'),
         para('Current progress', 'h'),
         para('A saved first-level prototype includes these interactions, damage, restart, and a gated exit. Its baseline passed 19 recorded automated editor play checks. A separate opening map explores the visual reference; its full route verification was still pending in the visual build report. Art, voices, combat balance, physical controls, and performance need further work. No packaged game is ready.'),
         para('The next step', 'h'),
         para('Make one convincing opening, then replace placeholders with reusable assets and develop voices and animation. The proposed story continues through a rally point, enemy relay, research archive, and departure record. Those later missions are drafts. AI assists production; creative decisions stay with the project creator.'),
         para('FEEDBACK: Does the opening make you want to learn what happened? Which character or part of the world interests you most?', 'caption')]
n = build('Lost_Vanguard_Project_Overview.pdf', brief)
assert n == 2, f'Unexpected brief overflow: {n}'
