import json, math, os, pathlib, subprocess, wave, struct, textwrap, sys

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "out"
COMPS = ROOT / "compositions"
OUT.mkdir(parents=True, exist_ok=True)
COMPS.mkdir(parents=True, exist_ok=True)

REELS = {
    "fr": {
        "voice": "fr-FR-DeniseNeural",
        "rate": "+4%",
        "scenes": [
            {
                "eyebrow": "LE QUOTIDIEN DU CABINET",
                "headline": "À L’ACCUEIL, TOUT ARRIVE EN MÊME TEMPS.",
                "body": "Un appel. Un patient. Une demande à noter.",
                "kind": "desk",
                "voice": "À l’accueil, le téléphone sonne pendant qu’un patient attend et qu’une demande doit être notée."
            },
            {
                "eyebrow": "CÔTÉ PATIENT",
                "headline": "UNE AUTRE PORTE D’ENTRÉE.",
                "body": "Le patient envoie sa demande depuis une page mobile.",
                "kind": "phone",
                "voice": "RENDEVO donne aux patients une page pour envoyer leur demande de rendez-vous en ligne."
            },
            {
                "eyebrow": "CÔTÉ CABINET",
                "headline": "LES DEMANDES RESTENT VISIBLES.",
                "body": "Un tableau de suivi. Une confirmation par e-mail configurable.",
                "kind": "dashboard",
                "voice": "Votre équipe retrouve les informations dans son tableau de suivi. Une confirmation par e-mail peut être configurée."
            },
            {
                "eyebrow": "RENDEVO",
                "headline": "UN PARCOURS PLUS CLAIR.",
                "body": "Cabinet médical ? Écrivez « RENDEVO » en DM.",
                "kind": "end",
                "voice": "Cabinet médical ? Écrivez RENDEVO en message privé."
            }
        ],
        "caption": "Quand l’accueil est occupé, les demandes de rendez-vous peuvent attendre. RENDEVO propose une page de demande en ligne et un tableau de suivi pour l’équipe. Cabinet médical ? Écrivez « RENDEVO » en DM.\n\n#RENDEVO #Oran #Algerie #RendezVousEnLigne #CabinetMedical #ReservationEnLigne",
        "filename": "RENDEVO_FR_2026-11-16.mp4"
    },
    "en": {
        "voice": "en-US-JennyNeural",
        "rate": "+4%",
        "scenes": [
            {
                "eyebrow": "THE BOOKING EXPERIENCE",
                "headline": "BOOKING SHOULDN’T BE A PHONE TAG GAME.",
                "body": "A missed call shouldn’t be the only way to reach a clinic.",
                "kind": "call",
                "voice": "Booking shouldn't mean calling again and again just to request an appointment."
            },
            {
                "eyebrow": "ONE CLEAR BOOKING PAGE",
                "headline": "CHOOSE A SERVICE. PICK A TIME.",
                "body": "Choose a service, date and available time, then send a request.",
                "kind": "booking",
                "voice": "With RENDEVO, patients can open a clinic booking page, choose a service, date and available time, then send their request."
            },
            {
                "eyebrow": "A CLEARER VIEW FOR YOUR TEAM",
                "headline": "FOLLOW REQUESTS IN ONE ADMIN VIEW.",
                "body": "Incoming requests are followed in an admin sheet. Email confirmation can be configured.",
                "kind": "admin",
                "voice": "Your team follows incoming requests in an admin sheet. Email confirmation can be configured for the clinic."
            },
            {
                "eyebrow": "RENDEVO",
                "headline": "A CLEARER NEXT STEP.",
                "body": "Want to explore it for your clinic? DM BOOKING.",
                "kind": "end",
                "voice": "Want to explore it for your clinic? DM BOOKING."
            }
        ],
        "caption": "Booking shouldn’t depend on catching someone at the right moment. RENDEVO gives clinics an online appointment request page and an admin view to follow incoming requests. Want to see how it could fit your clinic? DM BOOKING.\n\n#RENDEVO #ClinicBooking #OnlineAppointments #PatientExperience #AppointmentSystem #RENDEVOdz",
        "filename": "RENDEVO_EN_2026-11-16.mp4"
    }
}

CSS = r"""
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#07131c;color:#f5faf7;font-family:Arial,Helvetica,sans-serif}
.scene{width:1080px;height:1920px;position:relative;overflow:hidden;padding:150px 64px 170px;display:grid;grid-template-columns:545px 390px;column-gap:45px;align-items:center}
.scene.fr{background:radial-gradient(ellipse at 88% 12%,#155547 0%,transparent 42%),radial-gradient(ellipse at 4% 82%,#183b45 0%,transparent 40%),linear-gradient(145deg,#06131c,#10272f 60%,#07131c)}
.scene.en{background:radial-gradient(ellipse at 82% 14%,#d8edff 0%,transparent 43%),radial-gradient(ellipse at 8% 85%,#d5f1e8 0%,transparent 40%),linear-gradient(145deg,#f6fafc,#e9f1f5 60%,#f7fbfc);color:#102b40}
.scene:before{content:"";position:absolute;width:850px;height:850px;border:1px solid #8ee5c21c;border-radius:50%;right:-500px;top:360px;animation:orbit 36s linear infinite}
.scene.en:before{border-color:#387ca01c}
@keyframes orbit{to{transform:rotate(360deg)}}
@keyframes rise{from{opacity:0;transform:translateY(38px)}to{opacity:1;transform:translateY(0)}}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-15px)}}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.025)}}
@keyframes slide{from{opacity:0;transform:translateX(35px)}to{opacity:1;transform:translateX(0)}}
.brand{position:absolute;top:72px;left:68px;font-size:28px;font-weight:900;letter-spacing:7px;z-index:5}
.fr .brand{color:#f3fbf6}.brand b{color:#8ee5c2}.en .brand{color:#102b40}.en .brand b{color:#2476a5}
.counter{position:absolute;top:82px;right:68px;font-size:16px;letter-spacing:3px;color:#8ee5c2;z-index:5}
.en .counter{color:#2476a5}
.copy{position:relative;z-index:3;animation:rise .75s .12s both}
.eyebrow{font-size:18px;letter-spacing:3px;font-weight:800;color:#8ee5c2;line-height:1.35;margin-bottom:34px}
.en .eyebrow{color:#2476a5}
h1{font-size:76px;line-height:1.03;letter-spacing:-3.4px;margin:0 0 35px;font-weight:900;overflow-wrap:anywhere}
.en h1{font-size:72px;color:#102b40}
.bodycopy{font-size:33px;line-height:1.38;color:#bed0cf;margin:0;max-width:530px}
.en .bodycopy{color:#526b7b}
.rule{width:140px;height:4px;background:#8ee5c2;margin-top:42px}
.en .rule{background:#2476a5}
.visual{position:relative;z-index:2;animation:slide .8s .22s both}
.footer{position:absolute;bottom:75px;left:68px;right:68px;z-index:5;display:flex;justify-content:space-between;color:#77949a;font-size:15px;letter-spacing:3px}
.en .footer{color:#6f8795}
.card{border-radius:30px;box-shadow:0 35px 80px #0005;animation:float 5s ease-in-out infinite}
.desk{width:390px;background:#102d37;border:1px solid #45655f;padding:28px}
.deskhead{display:flex;justify-content:space-between;font-size:16px;color:#dcece6;letter-spacing:1.3px;margin-bottom:24px}
.deskhead span:last-child{color:#8ee5c2}
.task{padding:22px 17px;border-radius:16px;background:#173c43;margin-top:15px;display:flex;align-items:center;gap:13px;color:#e8f2ee;font-size:18px;line-height:1.25}
.bubble{width:15px;height:15px;flex:none;border-radius:50%;background:#8ee5c2;box-shadow:0 0 18px #8ee5c277}
.phone{width:350px;min-height:650px;border:9px solid #d8e6df;border-radius:48px;background:#f8fbf9;color:#183a31;padding:28px 22px;box-shadow:0 32px 75px #0007;transform:rotate(-2deg);animation:float 5.4s ease-in-out infinite}
.notch{width:100px;height:15px;border-radius:0 0 14px 14px;background:#d8e6df;margin:-28px auto 29px}
.screenbrand{font-size:15px;letter-spacing:3px;color:#53776b;font-weight:900}
.screenhead{font-size:27px;line-height:1.1;font-weight:900;margin:27px 0 23px}
.field{padding:18px 15px;margin:13px 0;border-radius:13px;border:1px solid #d8e4de;background:white;color:#71847b;font-size:17px}
.action{padding:18px;text-align:center;background:#145c4b;color:white;border-radius:13px;font-size:17px;font-weight:900;margin-top:21px}
.en .action{background:#216d99}
.panel{width:400px;background:#102d37;border:1px solid #476960;border-radius:25px;padding:27px;box-shadow:0 30px 70px #0007;animation:float 5.2s ease-in-out infinite}
.en .panel{background:#fff;border-color:#d4e0e7}
.paneltop{display:flex;justify-content:space-between;color:#e7f3ed;font-size:16px;letter-spacing:1.2px;margin-bottom:20px}
.en .paneltop{color:#18384b}
.paneltop span:last-child{color:#8ee5c2;font-size:12px}
.en .paneltop span:last-child{color:#2476a5}
.rowitem{display:flex;align-items:center;gap:12px;padding:19px 4px;border-top:1px solid #ffffff20;font-size:17px;color:#e3efea}
.en .rowitem{border-color:#e4ebef;color:#28485b}
.status{margin-left:auto;font-size:12px;color:#8ee5c2;background:#8ee5c21c;padding:8px 10px;border-radius:18px;white-space:nowrap}
.en .status{color:#2476a5;background:#e6f3fb}
.callcard{width:380px;background:#f8fbfd;border-radius:28px;padding:32px;color:#16374d;box-shadow:0 30px 70px #0005;animation:float 5s ease-in-out infinite}
.calltop{font-size:15px;letter-spacing:2px;color:#688393}
.callicon{width:140px;height:140px;border-radius:50%;background:#e5f0f7;margin:36px auto;display:grid;place-items:center;font-size:70px;color:#2878a7;animation:pulse 2.2s infinite}
.calltitle{text-align:center;font-size:28px;font-weight:900}
.callsub{text-align:center;color:#748b9a;font-size:16px;margin-top:12px}
.timepill{padding:17px;border-radius:13px;background:#eaf3f8;text-align:center;color:#2878a7;font-weight:800;margin-top:25px}
.endcard{width:390px;min-height:590px;border-radius:32px;background:#0c2935;border:1px solid #4e7d78;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:30px;box-shadow:0 32px 80px #0007;animation:float 5s ease-in-out infinite}
.endmark{font-size:110px;font-weight:900;color:#e7f5ee;letter-spacing:-8px}
.endmark span{color:#8ee5c2}
.en .endmark span{color:#78bfe7}
.endline{font-size:15px;letter-spacing:3px;color:#a9c7bf;margin-top:10px}
.endcta{background:#8ee5c2;color:#092a23;border-radius:15px;padding:20px 22px;margin-top:42px;font-size:16px;font-weight:900;text-align:center;width:100%}
.en .endcta{background:#78bfe7;color:#102b40}
"""

def run(cmd):
    subprocess.run(cmd, check=True)

def probe_duration(path):
    return float(subprocess.check_output([
        "ffprobe","-v","error","-show_entries","format=duration",
        "-of","default=noprint_wrappers=1:nokey=1",str(path)
    ],text=True).strip())

def stamp(seconds):
    ms=max(0,int(seconds*1000))
    return f"{ms//3600000:02d}:{(ms%3600000)//60000:02d}:{(ms%60000)//1000:02d},{ms%1000:03d}"

def split_caption(s, width=38):
    words=s.split()
    lines=[]; cur=""
    for word in words:
        trial=(cur+" "+word).strip()
        if len(trial)>width and cur:
            lines.append(cur); cur=word
        else: cur=trial
    if cur: lines.append(cur)
    if len(lines)>2:
        lines=[lines[0], " ".join(lines[1:])]
    return "\n".join(lines)

def visual_markup(kind, lang):
    if kind=="desk":
        return """<div class="card desk"><div class="deskhead"><span>ACCUEIL · CABINET</span><span>EN COURS</span></div><div class="task"><i class="bubble"></i><span>Appel entrant</span></div><div class="task"><i class="bubble"></i><span>Patient à accueillir</span></div><div class="task"><i class="bubble"></i><span>Demande à noter</span></div></div>"""
    if kind=="phone":
        return """<div class="phone"><div class="notch"></div><div class="screenbrand">RENDEVO</div><div class="screenhead">Prendre rendez-vous</div><div class="field">Service · Consultation</div><div class="field">Date · Choisir une date</div><div class="field">Horaire · Disponible</div><div class="action">ENVOYER LA DEMANDE</div></div>"""
    if kind=="dashboard":
        return """<div class="panel"><div class="paneltop"><span>ESPACE CABINET</span><span>● SUIVI</span></div><div class="rowitem"><i class="bubble"></i><span>Nouvelle demande</span><b class="status">Reçue</b></div><div class="rowitem"><i class="bubble"></i><span>Coordonnées patient</span><b class="status">Enregistrées</b></div><div class="rowitem"><i class="bubble"></i><span>Confirmation e-mail</span><b class="status">Configurable</b></div></div>"""
    if kind=="call":
        return """<div class="callcard"><div class="calltop">CLINIC · INCOMING CALL</div><div class="callicon">↗</div><div class="calltitle">CALL MISSED</div><div class="callsub">The front desk is helping someone else.</div><div class="timepill">A SECOND WAY TO REQUEST</div></div>"""
    if kind=="booking":
        return """<div class="phone"><div class="notch"></div><div class="screenbrand">RENDEVO</div><div class="screenhead">Book an appointment</div><div class="field">Service · Consultation</div><div class="field">Date · Select a date</div><div class="field">Time · Available slot</div><div class="action">SEND REQUEST</div></div>"""
    if kind=="admin":
        return """<div class="panel"><div class="paneltop"><span>CLINIC ADMIN</span><span>● INBOX</span></div><div class="rowitem"><i class="bubble"></i><span>New request</span><b class="status">Received</b></div><div class="rowitem"><i class="bubble"></i><span>Patient details</span><b class="status">Saved</b></div><div class="rowitem"><i class="bubble"></i><span>Email confirmation</span><b class="status">Configurable</b></div></div>"""
    return """<div class="endcard"><div class="endmark">RENDE<span>VO</span></div><div class="endline">BOOKING SYSTEMS</div><div class="endcta">DM RENDEVO</div></div>""" if lang=="fr" else """<div class="endcard"><div class="endmark">RENDE<span>VO</span></div><div class="endline">BOOKING SYSTEMS</div><div class="endcta">DM “BOOKING”</div></div>"""

def make_html(lang, scenes, durations):
    sections=[]
    for i,(scene,duration) in enumerate(zip(scenes,durations),1):
        sections.append(f"""
<section class="scene {lang}" data-duration="{duration:.3f}" data-camera="push 1.025">
  <div class="brand">RENDE<b>VO</b></div><div class="counter">{i:02d} / 04</div>
  <div class="copy"><div class="eyebrow">{scene['eyebrow']}</div><h1>{scene['headline']}</h1><p class="bodycopy">{scene['body']}</p><div class="rule"></div></div>
  <div class="visual">{visual_markup(scene['kind'],lang)}</div>
  <div class="footer"><span>{'SYSTÈME DE RÉSERVATION' if lang=='fr' else 'ONLINE APPOINTMENTS'}</span><span>RENDEVO · {i:02d}</span></div>
</section>""")
    html_doc=f"""<!doctype html><html lang="{lang}" data-width="1080" data-height="1920" data-fps="30"><head><meta charset="utf-8"><meta name="viewport" content="width=1080,height=1920"><title>RENDEVO {lang.upper()} Daily Reel</title><style>{CSS}</style></head><body><main data-sequence data-transition="fade 0.28">{''.join(sections)}</main></body></html>"""
    return html_doc

def make_music(path, duration):
    sr=24000
    n=int(sr*duration)
    chords=[(65.41,82.41,98.0,130.81),(55.0,73.42,87.31,110.0),(61.74,77.78,92.5,123.47),(58.27,73.42,87.31,116.54)]
    with wave.open(str(path),"wb") as wf:
        wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(sr)
        buf=bytearray()
        for i in range(n):
            t=i/sr
            chord=chords[min(3,int(t//5.5))]
            s=sum(math.sin(2*math.pi*f*t+j*.22) for j,f in enumerate(chord))/len(chord)
            fade=min(1.0,t/1.1,max(0.0,(duration-t)/1.5))
            val=int(max(-1,min(1,s*0.025*fade))*32767)
            buf.extend(struct.pack("<hh",val,val))
        wf.writeframes(buf)

def build(lang, cfg):
    seg_files=[]
    durations=[]
    rate=cfg["rate"]
    for i,scene in enumerate(cfg["scenes"],1):
        audio=OUT/f"{lang}_{i:02d}.mp3"
        run([str(ROOT.parents[1] / ".venv" / "bin" / "edge-tts"),"--voice",cfg["voice"],f"--rate={rate}","--text",scene["voice"],"--write-media",str(audio)])
        seg_files.append(audio)
        durations.append(probe_duration(audio))
    total_voice=sum(durations)
    if total_voice>26.0:
        raise RuntimeError(f"{lang} narration too long: {total_voice:.2f}s")
    scene_durations=[max(d+0.48,4.25) for d in durations]
    total=sum(scene_durations)
    if total>29.0:
        scene_durations=[x*28.5/total for x in scene_durations]
        total=sum(scene_durations)
    html_path=COMPS/f"{lang}.html"
    html_path.write_text(make_html(lang,cfg["scenes"],scene_durations),encoding="utf-8")
    voice_wav=OUT/f"{lang}_voice.wav"
    ff_inputs=sum((["-i",str(p)] for p in seg_files),[])
    filters=[]
    for idx,(spoken,scene_len) in enumerate(zip(durations,scene_durations)):
        pad=max(0.0,scene_len-spoken)+0.03
        filters.append(f"[{idx}:a]apad=pad_dur={pad:.3f},atrim=duration={scene_len:.3f},asetpts=PTS-STARTPTS[a{idx}]")
    concat_inputs="".join(f"[a{i}]" for i in range(len(seg_files)))
    filter_complex=";".join(filters)+f";{concat_inputs}concat=n={len(seg_files)}:v=0:a=1[a]"
    run(["ffmpeg","-y",*ff_inputs,"-filter_complex",filter_complex,"-map","[a]","-ar","48000","-ac","2","-c:a","pcm_s16le",str(voice_wav)])
    srt=[]; cursor=0.0
    for i,(scene,dur,sd) in enumerate(zip(cfg["scenes"],durations,scene_durations),1):
        srt.append(f"{i}\n{stamp(cursor)} --> {stamp(cursor+dur)}\n{split_caption(scene['voice'])}\n")
        cursor += sd
    srt_path=OUT/f"{lang}.srt"
    srt_path.write_text("\n".join(srt),encoding="utf-8")
    ass_path=OUT/f"{lang}.ass"
    def ass_time(value):
        centis=int(value*100)
        return f"{centis//360000}:{(centis%360000)//6000:02d}:{(centis%6000)//100:02d}.{centis%100:02d}"
    ass_lines=[
        "[Script Info]","ScriptType: v4.00+","PlayResX: 1080","PlayResY: 1920","WrapStyle: 2","ScaledBorderAndShadow: yes","",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: Default,DejaVu Sans,30,&H00FFFFFF,&H000000FF,&H00102028,&H90000000,-1,0,0,0,100,100,0,0,3,1.5,0,2,90,90,250,1","",
        "[Events]","Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
    ]
    cursor=0.0
    for scene,spoken,scene_len in zip(cfg["scenes"],durations,scene_durations):
        text=split_caption(scene["voice"]).replace("\n","\\N").replace("{","\\{").replace("}","\\}")
        ass_lines.append(f"Dialogue: 0,{ass_time(cursor)},{ass_time(cursor+spoken)},Default,,0,0,0,,{text}")
        cursor += scene_len
    ass_path.write_text("\n".join(ass_lines),encoding="utf-8")
    music=OUT/f"{lang}_music.wav"
    make_music(music,total)
    silent=OUT/f"{lang}_silent.mp4"
    run(["npx","givemotion","render",str(html_path),"-o",str(silent),"--quality","standard"])
    final=OUT/cfg["filename"]
    subtitle_filter=f"subtitles={ass_path}"
    run([
        "ffmpeg","-y","-i",str(silent),"-i",str(voice_wav),"-i",str(music),
        "-filter_complex","[1:a]volume=1.0[v];[2:a]volume=0.18[m];[v][m]amix=inputs=2:duration=longest:dropout_transition=1,apad=pad_dur=0.4[a]",
        "-map","0:v:0","-map","[a]","-vf",subtitle_filter,
        "-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-r","30",
        "-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",str(final)
    ])
    (OUT/f"caption_{lang}.txt").write_text(cfg["caption"],encoding="utf-8")
    meta=json.loads(subprocess.check_output([
        "ffprobe","-v","error","-show_entries","stream=codec_name,codec_type,width,height,r_frame_rate,sample_rate:format=duration",
        "-of","json",str(final)
    ],text=True))
    v=next(s for s in meta["streams"] if s["codec_type"]=="video")
    a=next(s for s in meta["streams"] if s["codec_type"]=="audio")
    dur=float(meta["format"]["duration"])
    assert v["codec_name"]=="h264" and v["width"]==1080 and v["height"]==1920
    assert a["codec_name"]=="aac" and 15<=dur<=30
    print(f"VERIFIED {final.name}: {dur:.2f}s, {v['width']}x{v['height']}, {v['codec_name']}, {a['codec_name']}, {final.stat().st_size} bytes")

for lang,cfg in REELS.items():
    build(lang,cfg)

plan = """# RENDEVO Daily Content — 16 November 2026

## Finished Reel 1 — French / Algeria
**Pillar:** receptionist workload and patient experience  
**Hook:** « À l’accueil, tout arrive en même temps. »  
**Format:** premium cinematic UI story, dark emerald palette, four animated scenes  
**CTA:** « Cabinet médical ? Écrivez RENDEVO en DM. »

Voiceover / subtitle sequence:
1. À l’accueil, le téléphone sonne pendant qu’un patient attend et qu’une demande doit être notée.
2. RENDEVO donne aux patients une page pour envoyer leur demande de rendez-vous en ligne.
3. Votre équipe retrouve les informations dans son tableau de suivi. Une confirmation par e-mail peut être configurée.
4. Cabinet médical ? Écrivez RENDEVO en message privé.

## Finished Reel 2 — English / International
**Pillar:** patient experience and missed-call alternative  
**Hook:** “Booking shouldn’t be a phone tag game.”  
**Format:** bright, fast UI-led story with a distinct visual system  
**CTA:** “Want to explore it for your clinic? DM BOOKING.”

Voiceover / subtitle sequence:
1. Booking shouldn't mean calling again and again just to request an appointment.
2. With RENDEVO, patients can open a clinic booking page, choose a service, date and available time, then send their request.
3. Your team follows incoming requests in an admin sheet. Email confirmation can be configured for the clinic.
4. Want to explore it for your clinic? DM BOOKING.

## Backup queue

### 1. French — WhatsApp messages are not an agenda
- **Hook:** « WhatsApp n’est pas un agenda. »
- **Format:** fast-paced split-screen mini-story
- **Scenes:** scattered chat bubbles → handwritten note → RENDEVO booking link opened from a message → admin tracking sheet
- **Language:** French
- **Caption:** « Les demandes peuvent arriver par plusieurs canaux. Un lien de réservation RENDEVO partagé dans vos messages peut orienter les patients vers un parcours plus clair. Il ne s’agit pas d’une intégration WhatsApp automatique. »
- **CTA:** « Écrivez RENDEVO en DM. »
- **Audience:** Algerian medical clinics

### 2. English — Two requests, one time slot
- **Hook:** “Two people. One appointment slot. Avoid the overlap.”
- **Format:** punchy kinetic typography + calendar UI
- **Scenes:** two request cards collide → occupied time is shown → available slots appear → clinic admin view
- **Language:** English
- **Caption:** “Manual scheduling can get messy. RENDEVO checks booked slots before showing availability in supported clinic setups.”
- **CTA:** “DM BOOKING.”
- **Audience:** international clinics; demonstrate only after checking the clinic configuration

### 3. French — The first impression starts online
- **Hook:** « Votre première impression commence avant l’accueil. »
- **Format:** cinematic brand film
- **Scenes:** clinic exterior/detail shots → branded mobile booking page → QR code/link placement → RENDEVO end card
- **Language:** French
- **Caption:** « Le parcours de réservation fait partie de l’accueil. Une page claire, adaptée à l’identité du cabinet, peut donner un premier contact plus professionnel. »
- **CTA:** « Demandez les options RENDEVO en DM. »
- **Audience:** Algerian clinics; salon/consultant variants are concepts requiring configuration and testing

## Accuracy notes
- The visuals show a representative clinic workflow, not a real customer account or testimonial.
- The booking page, available-slot selection, admin tracking sheet and email confirmations are RENDEVO capabilities; email confirmation depends on configuration.
- The English Reel is clinic-focused. It does not claim that all international sectors are already deployed.
- WhatsApp is shown only as a possible place to share a booking link, not as an automatic integration.
- Nothing is posted or messaged automatically.
"""
(ROOT/"CONTENT_PLAN.md").write_text(plan,encoding="utf-8")
for lang in ("fr","en"):
    (OUT/f"CONTENT_PLAN_{lang.upper()}.txt").write_text(plan,encoding="utf-8")
print("Daily source package and two verified renders created.")
