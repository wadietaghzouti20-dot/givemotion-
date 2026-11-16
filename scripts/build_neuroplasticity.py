import pathlib, subprocess, html, json, re
ROOT = pathlib.Path(".")
OUT = ROOT / "out"
TMP = pathlib.Path("/tmp/neuro")
OUT.mkdir(exist_ok=True)
TMP.mkdir(exist_ok=True)

chapters = [
("01","LE CERVEAU N’EST PAS FIGÉ","Une idée qui change tout",
"""Pendant longtemps, on a imaginé le cerveau adulte comme une structure presque achevée : les connexions se formaient pendant l’enfance, puis l’essentiel était joué. Cette représentation est dépassée. Le cerveau reste capable de modifier son organisation en réponse à l’expérience, à l’apprentissage et parfois aux lésions. Cette capacité porte un nom : la neuroplasticité. Elle ne signifie pas que tout changement est facile, ni que le cerveau peut tout faire. Elle décrit un ensemble de mécanismes biologiques mesurables."""),
("02","QU’EST-CE QUE LA NEUROPLASTICITÉ ?","Modifier les connexions, les fonctions et les réseaux",
"""La neuroplasticité désigne la capacité du système nerveux à changer sa structure, son fonctionnement ou l’efficacité de ses connexions. Elle peut être synaptique, lorsque la transmission entre neurones se renforce ou s’affaiblit ; structurelle, lorsque des épines dendritiques ou des ramifications changent ; fonctionnelle, lorsque des réseaux réorganisent leur contribution à une tâche. Ces dimensions interagissent. Apprendre une compétence ne consiste donc pas simplement à stocker une information dans une case : c’est transformer progressivement l’activité de réseaux distribués."""),
("03","L’ARCHITECTURE D’UN NEURONE","Dendrites, soma, axone et synapse",
"""Un neurone reçoit des signaux principalement par ses dendrites. Son corps cellulaire intègre une partie de ces informations. Si les conditions électriques sont réunies, un potentiel d’action se propage le long de l’axone. À son extrémité, le neurone communique avec d’autres cellules au niveau des synapses. Les neurotransmetteurs libérés dans la fente synaptique se lient à des récepteurs et modifient l’activité de la cellule suivante. La plasticité peut changer l’efficacité de cette communication, le nombre de contacts ou leur organisation."""),
("04","LA SYNAPSE EN ACTION","Le point de rencontre entre deux neurones",
"""Une synapse n’est pas un simple câble. C’est une zone de communication réglable. La quantité de neurotransmetteur libérée, le nombre et le type de récepteurs, ainsi que l’état de la cellule postsynaptique influencent la réponse. Certaines synapses deviennent plus efficaces après des schémas d’activité particuliers ; d’autres deviennent moins efficaces. Ces changements permettent aux circuits de s’ajuster à l’expérience. La mémoire dépend de modifications coordonnées de nombreux contacts, dans plusieurs régions cérébrales, plutôt que d’une synapse unique qui contiendrait un souvenir complet."""),
("05","POTENTIATION À LONG TERME","Quand une connexion devient plus efficace",
"""La potentialisation à long terme, ou PLT, est une augmentation durable de l’efficacité synaptique après certaines formes d’activité. Dans des synapses de l’hippocampe, l’activation de récepteurs NMDA peut permettre l’entrée de calcium dans la cellule postsynaptique. Cette hausse de calcium déclenche des cascades moléculaires qui peuvent augmenter le nombre ou l’efficacité de récepteurs AMPA. Le mécanisme varie selon les circuits et les protocoles. La PLT est un modèle majeur pour étudier les bases cellulaires de l’apprentissage, mais elle n’explique pas à elle seule toute la mémoire."""),
("06","DÉPRESSION À LONG TERME","L’apprentissage demande aussi d’affaiblir",
"""La dépression à long terme, ou DLT, correspond à une diminution durable de l’efficacité de certaines synapses. Elle peut contribuer à éliminer des associations devenues peu utiles, à ajuster la sensibilité des réseaux et à éviter leur saturation. Apprendre n’est donc pas seulement renforcer toutes les connexions. Le cerveau doit aussi sélectionner, affaiblir et parfois supprimer des contacts. L’équilibre entre renforcement et affaiblissement aide les réseaux à rester adaptables. La plasticité est une régulation, pas une accumulation illimitée de connexions."""),
("07","LE RÔLE DU CALCIUM ET DES RÉCEPTEURS","Une cascade moléculaire",
"""Dans plusieurs formes de plasticité, le calcium agit comme un signal intracellulaire. Son amplitude, sa durée et sa localisation peuvent activer des voies différentes. Les récepteurs NMDA jouent souvent un rôle de détecteur de coïncidence : leur activation dépend à la fois du glutamate et de l’état électrique de la membrane. Les récepteurs AMPA contribuent ensuite à la réponse excitatrice rapide. Des enzymes, des protéines d’échafaudage et l’expression de gènes peuvent stabiliser les changements. Les détails diffèrent selon l’âge, la région cérébrale et le type de synapse."""),
("08","L’APPRENTISSAGE REMODELLE LE CERVEAU","La pratique laisse une trace biologique",
"""Quand nous apprenons une nouvelle compétence, les réseaux actifs sont sollicités de façon répétée. Avec la pratique, certaines réponses deviennent plus précises et plus efficaces. Des études d’imagerie ont observé des changements associés à l’apprentissage, par exemple chez des personnes qui apprennent à jongler. Ces résultats montrent une association entre expérience et changements cérébraux ; ils ne signifient pas qu’une image cérébrale révèle directement le contenu d’un souvenir. La transformation dépend de la qualité de la pratique, du temps, de l’attention et de la consolidation."""),
("09","UN EXEMPLE : APPRENDRE À JONGLER","Une étude devenue classique",
"""Dans une étude publiée en 2004, Draganski et ses collègues ont suivi des adultes qui apprenaient à jongler. Après l’entraînement, ils ont observé des changements de matière grise dans des régions visuelles et motrices, puis une diminution partielle après une période sans pratique. L’étude est importante parce qu’elle a montré que des changements mesurables peuvent apparaître chez l’adulte sur une période relativement courte. Elle ne prouve pas que la matière grise augmente toujours avec chaque apprentissage, ni que toutes les modifications sont permanentes."""),
("10","LE CERVEAU QUI COMPENSE","Plasticité après une lésion",
"""Après une lésion cérébrale, les fonctions ne reviennent pas toujours spontanément. Pourtant, les réseaux peuvent parfois se réorganiser. Des régions préservées peuvent contribuer davantage à une tâche, des connexions peuvent changer et l’entraînement peut favoriser la récupération. Les résultats dépendent de la nature et de l’étendue de la lésion, de l’âge, du délai, de l’état de santé et de la rééducation. La plasticité n’est pas une garantie de guérison. Elle représente une base biologique sur laquelle des interventions ciblées peuvent agir."""),
("11","LA RÉÉDUCATION ET LA SPÉCIFICITÉ","Le cerveau change ce qu’on lui demande de pratiquer",
"""Une conséquence essentielle est la spécificité : les circuits sollicités par un entraînement sont ceux qui ont le plus de chances de s’adapter. Répéter une tâche pertinente, avec un niveau de difficulté adapté et un retour d’information, peut soutenir l’apprentissage moteur ou cognitif. En rééducation, les exercices sont donc conçus pour correspondre aux capacités à reconstruire. La répétition seule ne suffit pas toujours : la motivation, l’attention, la progression, la fatigue et le contexte influencent aussi les résultats."""),
("12","LES PÉRIODES SENSIBLES","Le cerveau n’est pas également plastique à tout âge",
"""La plasticité existe tout au long de la vie, mais elle n’a pas la même intensité ni les mêmes conditions à chaque étape. Pendant le développement, certaines périodes sont particulièrement sensibles à l’expérience sensorielle et sociale. Les circuits se stabilisent progressivement, notamment grâce à l’équilibre entre excitation et inhibition et à des mécanismes de maturation. Chez l’adulte, l’apprentissage reste possible, mais il peut demander davantage de temps ou des conditions différentes. Il faut donc éviter deux extrêmes : croire que tout se joue avant l’âge adulte, ou prétendre que l’âge n’a aucun effet."""),
("13","LE SOMMEIL ET LA CONSOLIDATION","Stabiliser ce qui a été appris",
"""Le sommeil participe à la consolidation de nombreuses formes de mémoire. Pendant certaines phases, l’activité cérébrale réactive des motifs liés aux expériences récentes. Ces réactivations pourraient contribuer à renforcer, réorganiser ou intégrer des informations. Le sommeil n’est pas un bouton magique qui transforme automatiquement une séance en expertise. Mais une privation répétée peut nuire à l’attention, à l’apprentissage et à la mémoire. Une stratégie réaliste associe pratique espacée, sommeil suffisant et révisions actives plutôt que des nuits blanches."""),
("14","L’ATTENTION ET L’ERREUR","Le cerveau apprend grâce au retour d’information",
"""L’attention aide à sélectionner les informations pertinentes. Le retour d’information permet de comparer le résultat obtenu à celui qui était attendu. Une erreur détectée peut modifier la stratégie et orienter les essais suivants. Dans l’apprentissage moteur, les ajustements se construisent souvent à partir de petites erreurs répétées. Cela ne veut pas dire qu’il faut rechercher l’échec pour lui-même. Un défi productif se situe à un niveau où la tâche reste réalisable, mais exige une adaptation. Trop facile, elle enseigne peu ; trop difficile, elle peut décourager."""),
("15","MYÉLINE ET EFFICACITÉ DES CIRCUITS","Au-delà des synapses",
"""La plasticité ne concerne pas uniquement les synapses. La myéline, une gaine qui entoure certains axones, influence la vitesse et la synchronisation de la transmission nerveuse. Des recherches suggèrent que l’activité et l’apprentissage peuvent être associés à des changements dans les cellules qui produisent la myéline. Cette plasticité de la substance blanche est un domaine de recherche actif. Elle rappelle que l’adaptation cérébrale implique plusieurs échelles : molécules, synapses, cellules gliales, fibres et réseaux entiers."""),
("16","LA PLASTICITÉ A SES LIMITES","Changer n’est pas toujours s’améliorer",
"""La plasticité est neutre : elle décrit une capacité de changement, pas une amélioration automatique. Des habitudes répétées peuvent renforcer des circuits utiles, mais aussi entretenir des comportements indésirables. La douleur chronique, certaines dépendances et des troubles neurologiques impliquent des changements de réseaux complexes. Il serait simpliste de les réduire à une mauvaise habitude ou de promettre de les corriger par la seule volonté. Comprendre la plasticité permet de concevoir de meilleures interventions, mais ne remplace ni l’évaluation médicale ni les traitements validés."""),
("17","COMMENT APPRENDRE PLUS EFFICACEMENT ?","Des principes issus de la recherche",
"""Plusieurs principes sont utiles : pratiquer régulièrement plutôt que tout concentrer en une séance ; espacer les révisions ; récupérer activement l’information sans regarder la réponse ; varier les exemples ; recevoir un retour précis ; augmenter progressivement la difficulté ; et protéger le sommeil. Ces méthodes ne garantissent pas un résultat identique pour tout le monde. Leur efficacité dépend de la tâche et du contexte. Elles ont cependant un point commun : elles transforment l’apprentissage en processus actif, répété et ajusté."""),
("18","CE QUE LES SCIENCES MESURENT","Des méthodes complémentaires",
"""Les chercheurs étudient la plasticité avec des approches complémentaires. L’électrophysiologie mesure l’activité électrique et l’efficacité synaptique. L’imagerie par résonance magnétique observe certaines propriétés structurelles ou fonctionnelles à grande échelle. Les modèles animaux permettent d’examiner des mécanismes cellulaires avec un niveau de détail difficile à atteindre chez l’humain. Chaque méthode a ses limites : une variation d’imagerie n’est pas une preuve directe de création de neurones, et un mécanisme observé chez l’animal ne se transpose pas automatiquement à l’être humain."""),
("19","TROIS IDÉES À RETENIR","La plasticité est réelle, complexe et contextuelle",
"""Première idée : le cerveau adulte conserve une capacité d’adaptation. Deuxième idée : cette adaptation repose sur plusieurs mécanismes, du changement synaptique à la réorganisation des réseaux. Troisième idée : l’expérience compte, mais les effets dépendent de la répétition, de l’attention, du sommeil, de l’âge et du contexte biologique. La neuroplasticité n’est ni un superpouvoir ni une promesse de transformation instantanée. C’est un cadre scientifique puissant pour comprendre comment le cerveau apprend, s’ajuste et parfois récupère."""),
("20","LE CERVEAU EN CONSTRUCTION","Chaque apprentissage est une interaction avec le vivant",
"""La prochaine fois que vous apprenez un mouvement, une langue ou un concept difficile, pensez à ce qui se passe sous la surface. Des neurones échangent des signaux, des synapses ajustent leur efficacité et des réseaux coordonnent leur activité. Le cerveau ne devient pas une page blanche à chaque expérience : il transforme une architecture déjà construite. C’est précisément ce qui rend la neuroplasticité fascinante. Nous terminons avec une question ouverte : quelles expériences choisissons-nous de répéter, et quels circuits voulons-nous entraîner ?""")
]
assert len(chapters)==20

def run(args):
    subprocess.run(args, check=True, stdout=subprocess.DEVNULL if args[0]=="ffmpeg" else None)
def probe(p):
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",str(p)],text=True).strip())

# One narrated segment per chapter, each padded to an exact 30-second chapter.
voice_files=[]
for i, ch in enumerate(chapters, 1):
    mp3=TMP/f"{i:02d}.mp3"
    wav=TMP/f"{i:02d}.wav"
    text=ch[3].replace("\n"," ")
    run([".venv/bin/edge-tts","--voice","fr-FR-DeniseNeural","--rate=-6%","--text",text,"--write-media",str(mp3)])
    run(["ffmpeg","-y","-i",str(mp3),"-af","apad=whole_dur=30,atrim=duration=30","-ar","48000","-ac","2",str(wav)])
    voice_files.append(wav)

# Build a calm original electronic-ambient bed without third-party music.
run(["ffmpeg","-y","-f","lavfi","-i","sine=frequency=110:sample_rate=48000:duration=600",
     "-f","lavfi","-i","sine=frequency=164.81:sample_rate=48000:duration=600",
     "-f","lavfi","-i","sine=frequency=220:sample_rate=48000:duration=600",
     "-filter_complex","[0:a]volume=0.045,lowpass=f=350[a0];[1:a]volume=0.025,lowpass=f=500[a1];[2:a]volume=0.015,lowpass=f=700[a2];[a0][a1][a2]amix=inputs=3,afade=t=in:d=8,afade=t=out:st=585:d=15",
     "-t","600","-ar","48000","-ac","2",str(OUT/"ambient.wav")])

# A consistent editorial visual system: animated typography, diagrams, timelines and data cards.
css = """
*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#07121d;color:#f5f7f5;font-family:Arial,Helvetica,sans-serif}
.scene{width:1920px;height:1080px;position:relative;overflow:hidden;padding:76px 110px;background:radial-gradient(ellipse at 82% 34%,rgba(24,103,112,.28),transparent 39%),linear-gradient(125deg,#07121d 0%,#102635 58%,#091722 100%)}
.scene:before{content:"";position:absolute;width:900px;height:900px;border:1px solid rgba(121,220,207,.12);border-radius:50%;right:-300px;top:90px}
.scene:after{content:"";position:absolute;inset:0;background:linear-gradient(110deg,transparent 0 68%,rgba(255,255,255,.018) 68% 68.2%,transparent 68.2%);pointer-events:none}
.top{display:flex;justify-content:space-between;align-items:center;position:relative;z-index:3}
.brand{font-size:22px;letter-spacing:8px;font-weight:800;color:#8ce0cf}.chapter{font-size:16px;letter-spacing:4px;color:#7c9ba8}
.main{position:absolute;left:110px;right:110px;top:220px;bottom:140px;display:grid;grid-template-columns:44% 56%;gap:30px;align-items:center;z-index:2}
.kicker{font-size:18px;letter-spacing:5px;color:#8ce0cf;font-weight:bold;margin-bottom:28px}
h1{font-size:70px;line-height:1.05;letter-spacing:-2px;margin:0 0 28px;max-width:780px}
.sub{font-size:29px;line-height:1.45;color:#b8cbd0;max-width:720px}
.visual{height:650px;position:relative;display:flex;align-items:center;justify-content:center}
.panel{width:100%;border:1px solid rgba(140,224,207,.25);border-radius:28px;background:linear-gradient(145deg,rgba(23,53,67,.94),rgba(11,31,44,.96));padding:38px;box-shadow:0 30px 90px rgba(0,0,0,.24)}
.label{font-size:15px;letter-spacing:4px;color:#8ce0cf;margin-bottom:26px}
.big{font-size:66px;font-weight:800;line-height:1.08;letter-spacing:-2px}
.small{font-size:22px;color:#a9c0c7;line-height:1.45;margin-top:18px}
.nodes{display:flex;align-items:center;justify-content:center;gap:18px;margin:38px 0}
.node{width:110px;height:110px;border-radius:50%;display:grid;place-items:center;border:2px solid #5fc9bd;background:radial-gradient(circle,#286b70,#123441 70%);box-shadow:0 0 45px rgba(95,201,189,.17);font-size:17px;text-align:center}
.line{height:3px;width:55px;background:linear-gradient(90deg,#5fc9bd,#d7bd82)}
.bars{display:flex;align-items:end;gap:22px;height:270px;margin:35px 0 10px}
.bar{flex:1;border-radius:12px 12px 0 0;background:linear-gradient(0deg,#1b7778,#84dfc9);position:relative;min-height:30px}
.bar span{position:absolute;bottom:-38px;left:0;right:0;text-align:center;font-size:16px;color:#a8c1c7}
.callout{border-left:4px solid #d7bd82;padding:18px 25px;margin-top:35px;color:#d8e5e2;font-size:23px;line-height:1.4;background:rgba(215,189,130,.07)}
.footer{position:absolute;left:110px;right:110px;bottom:55px;display:flex;justify-content:space-between;color:#7896a1;font-size:14px;letter-spacing:3px;z-index:3}
.progress{height:3px;background:#233d49;position:absolute;bottom:0;left:0;right:0}.progress i{display:block;height:100%;width:5%;background:#8ce0cf}
.visual,.copy{animation:rise .9s cubic-bezier(.2,.8,.2,1) both}
@keyframes rise{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:translateY(0)}}
"""

def visual_for(i, title):
    if i in (3,4,5,6,7):
        return '<div class="panel"><div class="label">ÉCHELLE CELLULAIRE</div><div class="nodes"><div class="node">DENDRITES</div><div class="line"></div><div class="node">SOMA</div><div class="line"></div><div class="node">AXONE</div></div><div class="callout">Signal électrique → libération de neurotransmetteurs → réponse postsynaptique</div><div class="small">Schéma conceptuel simplifié — les circuits réels sont beaucoup plus complexes.</div></div>'
    if i in (8,9,10,11,12,13,14,15,16,17):
        return '<div class="panel"><div class="label">ADAPTATION DES RÉSEAUX</div><div class="big">EXPÉRIENCE</div><div class="nodes"><div class="node">ACTIVITÉ</div><div class="line"></div><div class="node">AJUSTEMENT</div><div class="line"></div><div class="node">CONSOLIDATION</div></div><div class="callout">La pratique modifie les probabilités et l’efficacité des connexions sollicitées.</div></div>'
    if i==18:
        return '<div class="panel"><div class="label">OUTILS DE RECHERCHE</div><div class="bars"><div class="bar" style="height:85%"><span>EEG</span></div><div class="bar" style="height:65%"><span>IRM</span></div><div class="bar" style="height:100%"><span>ÉLECTROPHYSIOLOGIE</span></div><div class="bar" style="height:75%"><span>MODÈLES</span></div></div><div class="small">Chaque méthode observe une échelle différente et possède ses propres limites.</div></div>'
    return '<div class="panel"><div class="label">UNE PROPRIÉTÉ FONDAMENTALE DU VIVANT</div><div class="big">LE CERVEAU<br><span style="color:#8ce0cf">S’ADAPTE.</span></div><div class="nodes"><div class="node">STRUCTURE</div><div class="line"></div><div class="node">FONCTION</div><div class="line"></div><div class="node">RÉSEAUX</div></div><div class="callout">Comprendre le changement, c’est comprendre une partie de l’apprentissage.</div></div>'

parts=[]
for i,ch in enumerate(chapters,1):
    n, title, subtitle, narration = ch
    parts.append(f'''<section class="scene" data-duration="30" data-camera="push 1.025">
      <div class="top"><div class="brand">NEUROSCIENCES / DOSSIER 01</div><div class="chapter">CHAPITRE {n} — 20</div></div>
      <div class="main"><div class="copy"><div class="kicker">NEUROPLASTICITÉ</div><h1>{html.escape(title)}</h1><div class="sub">{html.escape(subtitle)}</div><div class="callout">{html.escape(narration[:145])}…</div></div>
      <div class="visual" data-enter="fade-up">{visual_for(i,title)}</div></div>
      <div class="footer"><span>LE CERVEAU QUI SE TRANSFORME</span><span>{i:02d} / 20</span></div><div class="progress"><i style="width:{i*5}%"></i></div>
    </section>''')
# Dedicated title and bibliography/end-credit cards are each 30 seconds.
parts.insert(0,'''<section class="scene" data-duration="30" data-camera="push 1.04"><div class="top"><div class="brand">DOCUMENTAIRE SCIENTIFIQUE</div><div class="chapter">NEUROSCIENCES</div></div><div style="position:absolute;left:120px;top:265px;z-index:2"><div class="kicker">LE CERVEAU QUI SE TRANSFORME</div><div style="font-size:112px;font-weight:800;line-height:1.0;max-width:1250px">NEURO<br><span style="color:#8ce0cf">PLASTICITÉ</span></div><div class="sub" style="margin-top:35px">Comment l’expérience remodèle le cerveau humain</div></div><div class="visual" style="position:absolute;right:100px;top:180px;width:700px"><div class="panel"><div class="nodes"><div class="node">EXPÉRIENCE</div><div class="line"></div><div class="node">SYNAPSE</div><div class="line"></div><div class="node">RÉSEAU</div></div><div class="big" style="font-size:42px;text-align:center;color:#8ce0cf">APPRENDRE<br>TRANSFORME</div></div></div><div class="footer"><span>PRÉSENTATION UNIVERSITAIRE</span><span>10:00</span></div></section>''')
parts.append('''<section class="scene" data-duration="30"><div class="top"><div class="brand">RÉFÉRENCES SCIENTIFIQUES</div><div class="chapter">POUR ALLER PLUS LOIN</div></div><div style="position:absolute;left:120px;right:120px;top:190px"><div class="kicker">SÉLECTION DE TRAVAUX FONDATEURS</div><div style="font-size:28px;line-height:1.65;color:#d7e4e4">
• Bliss &amp; Lømo (1973), Long-lasting potentiation of synaptic transmission in the dentate area of the anaesthetized rabbit, Journal of Physiology.<br>
• Kandel (2001), The molecular biology of memory storage: a dialogue between genes and synapses, Science.<br>
• Maguire et al. (2000), Navigation-related structural change in the hippocampi of taxi drivers, PNAS.<br>
• Draganski et al. (2004), Neuroplasticity: changes in grey matter induced by training, Nature.<br>
• Nudo et al. (1996), Use-dependent alterations of movement representations in primary motor cortex, Journal of Neuroscience.<br>
• Lövdén et al. (2010), A theoretical framework for the study of adult cognitive plasticity, Psychological Bulletin.
</div><div class="callout">Les résultats scientifiques ont été simplifiés pour la présentation. Les schémas sont illustratifs et ne représentent pas des données expérimentales.</div></div><div class="footer"><span>FIN DU DOCUMENTAIRE</span><span>MERCI</span></div></section>''')
page=f'''<!doctype html><html lang="fr" data-width="1920" data-height="1080" data-fps="30"><head><meta charset="utf-8"><style>{css}</style></head><body><main data-sequence data-transition="fade 0.6">{"".join(parts)}</main></body></html>'''
(ROOT/"compositions").mkdir(exist_ok=True)
(ROOT/"compositions/neuroplasticity.html").write_text(page,encoding="utf-8")

# Concatenate the 22 exact 30-second voice segments (title + 20 chapters + references).
with open(TMP/"concat.txt","w") as f:
    for p in voice_files:
        f.write(f"file '{p}'\n")
# Add a spoken title and bibliography narration as the opening and closing sections.
for name, text in [("title","Neuroplasticité : comment l’expérience remodèle le cerveau humain. Un documentaire scientifique sur les mécanismes de l’apprentissage, de la mémoire et de l’adaptation."),("refs","Références : Bliss et Lømo, 1973. Kandel, 2001. Maguire et ses collègues, 2000. Draganski et ses collègues, 2004. Nudo et ses collègues, 1996. Lövdén et ses collègues, 2010. Retrouvez les références complètes à l’écran.")]:
    mp3=TMP/f"{name}.mp3"; wav=TMP/f"{name}.wav"
    run([".venv/bin/edge-tts","--voice","fr-FR-DeniseNeural","--rate=-6%","--text",text,"--write-media",str(mp3)])
    run(["ffmpeg","-y","-i",str(mp3),"-af","apad=whole_dur=30,atrim=duration=30","-ar","48000","-ac","2",str(wav)])
# Title segment, 20 chapter segments, reference segment = 660 seconds; trim composition to exact same length.
all_audio=[TMP/"title.wav"]+voice_files+[TMP/"refs.wav"]
with open(TMP/"all.txt","w") as f:
    for p in all_audio: f.write(f"file '{p}'\n")
run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(TMP/"all.txt"),"-c:a","pcm_s16le",str(OUT/"narration.wav")])
run(["npx","givemotion","render","compositions/neuroplasticity.html","-o",str(OUT/"visuals.mp4"),"--quality","standard"])
# The visual sequence has 22 x 30 seconds. Mix narration and original ambient bed.
run(["ffmpeg","-y","-i",str(OUT/"visuals.mp4"),"-i",str(OUT/"narration.wav"),"-i",str(OUT/"ambient.wav"),
     "-filter_complex","[1:a]volume=1.0[voice];[2:a]volume=0.22[music];[voice][music]amix=inputs=2:duration=first:dropout_transition=2[a]",
     "-map","0:v","-map","[a]","-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-r","30",
     "-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",str(OUT/"NEUROPLASTICITE_DOCUMENTAIRE_FR.mp4")])
run(["ffmpeg","-y","-ss","3","-i",str(OUT/"NEUROPLASTICITE_DOCUMENTAIRE_FR.mp4"),"-frames:v","1","-q:v","2",str(OUT/"NEUROPLASTICITE_COUVERTURE.jpg")])
info=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries","stream=codec_type,codec_name,width,height,r_frame_rate","-show_entries","format=duration","-of","json",str(OUT/"NEUROPLASTICITE_DOCUMENTAIRE_FR.mp4")],text=True))
(OUT/"verification.json").write_text(json.dumps(info,indent=2),encoding="utf-8")
print("RENDERED",info["format"]["duration"],info["streams"])
