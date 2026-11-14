import math, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W,H,FPS,DURATION=854,480,8,600
OUT="dream-documentary.mp4"
font="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
bold="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def F(p,s):
    try:return ImageFont.truetype(p,s)
    except:return ImageFont.load_default()
T,B,S=F(bold,20),F(font,15),F(font,11)
chapters=[
("LE MYSTÈRE DES RÊVES","Chaque nuit, notre esprit fabrique des mondes. Nous pouvons voler, parler à des personnes absentes ou vivre des scènes impossibles. Pourtant, au réveil, ces histoires s’effacent souvent. Pourquoi notre cerveau fait-il cela ?"),
("LE SOMMEIL N’EST PAS UN ARRÊT","Dormir ne signifie pas que le cerveau s’éteint. Il traverse plusieurs phases qui se répètent pendant la nuit. Certaines sont profondes ; d’autres sont plus légères. L’activité cérébrale change constamment."),
("LA PHASE REM","Pendant le sommeil paradoxal, appelé REM, les yeux bougent rapidement sous les paupières. Le cerveau devient très actif, tandis que les muscles du corps sont fortement relâchés. Beaucoup de rêves vivants surviennent à ce moment."),
("D’OÙ VIENNENT LES RÊVES ?","Les rêves peuvent mélanger souvenirs, émotions, sensations et imagination. Le cerveau réactive certains fragments d’expérience et les assemble en une histoire. Ce récit n’est pas toujours logique."),
("POURQUOI LES OUBLIONS-NOUS ?","Se souvenir d’un rêve dépend du moment du réveil et de la façon dont le cerveau encode les souvenirs. Si nous nous réveillons au milieu d’un rêve, nous avons plus de chances de nous en rappeler. Ensuite, il peut disparaître."),
("CAUCHEMARS ET ÉMOTIONS","Les cauchemars sont des rêves très négatifs qui provoquent peur ou détresse. Le stress, certains événements difficiles et le manque de sommeil peuvent jouer un rôle. Un cauchemar occasionnel est courant."),
("RÊVER EN SACHANT QUE L’ON RÊVE","Dans un rêve lucide, la personne comprend qu’elle est en train de rêver. Certaines arrivent même à influencer le scénario. Ce phénomène est étudié en laboratoire grâce à des signaux oculaires convenus à l’avance."),
("COMMENT ÉTUDIER LES RÊVES ?","Les chercheurs observent l’activité cérébrale, les mouvements des yeux et le tonus musculaire pendant le sommeil. Ils réveillent parfois les volontaires pour recueillir leurs récits. Ces méthodes donnent des indices."),
("CE QUE LA SCIENCE IGNORE ENCORE","Il n’existe pas une explication unique et définitive de tous les rêves. Ils pourraient participer à la mémoire, au traitement des émotions ou à la simulation de situations. Ces pistes sont étudiées."),
("UNE DERNIÈRE QUESTION","Le rêve révèle un cerveau toujours actif, qui transforme nos expériences en images et en histoires. La prochaine fois que vous vous réveillerez après un rêve étrange, demandez-vous : que raconte-t-il de votre cerveau ?")]
def wrap(d,txt,font,maxw):
    out=[];cur=""
    for word in txt.split():
        test=(cur+" "+word).strip()
        if d.textbbox((0,0),test,font=font)[2]<=maxw:cur=test
        else:
            if cur:out.append(cur)
            cur=word
    if cur:out.append(cur)
    return out
def draw_brain(d,cx,cy,t):
    lobes=[(-32,-12,28),(-8,-25,31),(20,-18,29),(37,5,25),(10,17,30),(-22,13,27)]
    for i,(dx,dy,r) in enumerate(lobes):
        rr=int(r*(1+.05*math.sin(t*2+i)));x=cx+dx;y=cy+dy
        d.ellipse((x-rr,y-rr,x+rr,y+rr),fill=(38,90+10*i,145+5*i),outline=(120,215,230),width=2)
def frame(i):
    t=i/FPS; ch=min(9,int(t//60)); sec=t-ch*60; heading,copy=chapters[ch]
    im=Image.new("RGB",(W,H),(7,17,39));d=ImageDraw.Draw(im)
    d.rectangle((0,0,300,H),fill=(12,25,49));d.rectangle((0,0,6,H),fill=(44,190,204))
    d.text((24,22),"SCIENCE / SOMMEIL / CERVEAU",font=S,fill=(90,205,220))
    y=58
    for line in wrap(d,heading,T,250):d.text((24,y),line,font=T,fill=(245,248,252));y+=26
    d.line((24,116,270,116),fill=(48,102,137),width=2);y=136
    for line in wrap(d,copy,B,246):d.text((24,y),line,font=B,fill=(211,224,237));y+=23
    d.text((24,425),f"CHAPITRE {ch+1:02d} / 10",font=S,fill=(94,206,219))
    d.rectangle((24,447,270,452),fill=(35,57,82));d.rectangle((24,447,24+int(246*sec/60),452),fill=(55,200,211))
    cx,cy=570,230
    for k in range(65):
        x=310+(k*79+int(t*(2+k%5)))%530; yy=(k*43+13*k%71)%470
        d.ellipse((x-1,yy-1,x+1,yy+1),fill=(38,75,112))
    if ch in (0,8,9):
        for j in range(8):
            r=42+j*22+int(5*math.sin(sec+j))
            d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=(48+8*j,110+8*j,175+5*j),width=2)
        for j in range(12):
            a=sec*.25+j*math.tau/12;x=cx+int(math.cos(a)*145);yy=cy+int(math.sin(a)*95)
            d.ellipse((x-5,yy-5,x+5,yy+5),fill=(112,220,226))
    elif ch in (1,2,7):draw_brain(d,cx,cy,sec)
    elif ch==3:
        for j in range(8):
            a=sec*.2+j*math.tau/8;x=cx+int(math.cos(a)*140);yy=cy+int(math.sin(a)*90)
            d.rounded_rectangle((x-27,yy-22,x+27,yy+22),radius=8,fill=(55+8*j,100,155),outline=(145,215,230),width=2)
        d.ellipse((cx-42,cy-42,cx+42,cy+42),fill=(25,60,108),outline=(130,220,230),width=3);d.text((cx-10,cy-24),"?",font=F(bold,40),fill="white")
    elif ch==4:
        for j in range(120):
            a=j*2.4+sec*.2;r=(j*2.3+sec*5)%175;x=cx+math.cos(a)*r;yy=cy+math.sin(a)*r*.62
            d.ellipse((x-2,yy-2,x+2,yy+2),fill=(65,130,190))
    elif ch==5:
        for j in range(7):
            r=30+j*22+int(7*math.sin(sec+j));d.ellipse((cx-r,cy-r,cx+r,cy+r),outline=(170,65+8*j,105+8*j),width=3)
        d.polygon([(cx,cy-55),(cx+15,cy-10),(cx+50,cy-10),(cx+20,cy+12),(cx+32,cy+52),(cx,cy+25),(cx-32,cy+52),(cx-20,cy+12),(cx-50,cy-10),(cx-15,cy-10)],fill=(210,85,115))
    else:
        d.ellipse((cx-150,cy-75,cx+150,cy+75),outline=(110,205,225),width=5);d.ellipse((cx-55,cy-55,cx+55,cy+55),fill=(35,95,145),outline=(170,225,235),width=3)
        rr=22+int(5*math.sin(sec*2));d.ellipse((cx-rr,cy-rr,cx+rr,cy+rr),fill=(225,190,115))
    d.rounded_rectangle((320,18,460,47),radius=10,fill=(16,47,75),outline=(50,125,155));d.text((334,27),f"CHAPITRE {ch+1:02d}",font=S,fill=(180,225,235))
    d.text((790,25),f"{int(t//60):02d}:{int(t%60):02d}",font=S,fill=(170,195,215))
    return np.asarray(im)
sr=22050;t=np.arange(sr*DURATION)/sr
audio=.018*np.sin(2*np.pi*110*t)+.012*np.sin(2*np.pi*164.81*t)+.008*np.sin(2*np.pi*220*t)
audio*=np.minimum(1,t/4)*np.minimum(1,(DURATION-t)/5)
for k in range(1,10):
    env=np.exp(-.5*((t-k*60)/1.3)**2);audio+=.018*env*np.sin(2*np.pi*440*(t-k*60))
audio=np.clip(audio,-.09,.09)
with wave.open("ambience.wav","wb") as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((audio*32767).astype(np.int16).tobytes())
cmd=["ffmpeg","-y","-loglevel","error","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i","ambience.wav","-c:v","libx264","-preset","ultrafast","-crf","25","-pix_fmt","yuv420p","-c:a","aac","-b:a","128k","-shortest",OUT]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
for i in range(FPS*DURATION):p.stdin.write(frame(i).tobytes())
p.stdin.close()
if p.wait()!=0:raise SystemExit("FFmpeg render failed")
print("Rendered",OUT)
