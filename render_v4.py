import json, pathlib, subprocess, html, os, re

REELS = [
{
"slug":"01-phone-interruptions",
"voice":"Vous êtes en plein soin. Le téléphone sonne. La personne à l’accueil doit choisir entre répondre, accueillir quelqu’un ou terminer une tâche. Et le patient, lui, attend. RENDEVO ajoute une autre porte d’entrée : une page de réservation adaptée au téléphone. Le patient envoie sa demande, votre équipe retrouve les informations dans son suivi. Vous gardez le contact humain, sans dépendre uniquement des appels. Vous gérez un cabinet ? Écrivez-nous « RENDEVO ».",
"scenes":[
("LE PROBLÈME","En plein soin…","Le téléphone ne choisit jamais le bon moment.","ring"),
("CÔTÉ PATIENT","Une autre façon de réserver","Le patient envoie sa demande depuis son téléphone.","phone"),
("CÔTÉ CABINET","Tout est regroupé","Les informations arrivent dans le suivi du cabinet.","sheet"),
("RENDEVO","Gardez le contact humain","Cabinet médical ? Écrivez-nous « RENDEVO ».","cta")
]},
{
"slug":"02-missed-calls",
"voice":"Un patient appelle votre cabinet. Personne ne peut décrocher tout de suite. Il rappelle plus tard… ou il cherche ailleurs. Ce n’est pas un problème de qualité de soin : c’est un problème d’accès au rendez-vous. Avec RENDEVO, votre patient peut aussi envoyer sa demande en ligne, même quand l’accueil est occupé. Votre équipe la retrouve ensuite dans son tableau de suivi. Vous voulez proposer cette option à vos patients ? Écrivez-nous « RENDEVO ».",
"scenes":[
("APPEL MANQUÉ","Il n’a pas pu vous joindre","Un appel manqué peut devenir une demande perdue.","missed"),
("LE PATIENT","Il cherche une solution","Une page claire lui permet d’envoyer sa demande.","phone"),
("VOTRE ÉQUIPE","La demande reste visible","Retrouvez les informations dans un suivi centralisé.","inbox"),
("RENDEVO","Une autre porte d’entrée","Cabinet médical ? Écrivez-nous « RENDEVO ».","cta")
]},
{
"slug":"03-whatsapp-chaos",
"voice":"Une demande arrive sur WhatsApp. Une autre par téléphone. Une troisième est notée sur un papier. Et quand il faut retrouver le bon numéro ou la bonne date, tout le monde perd du temps. RENDEVO donne aux patients un parcours de demande en ligne et rassemble les informations dans un tableau de suivi. Pas de magie, juste une méthode plus claire pour traiter les demandes du cabinet. Vous voulez organiser vos réservations ? Envoyez « RENDEVO » en message privé.",
"scenes":[
("TOUT EST DISPERSÉ","WhatsApp. Appels. Papier.","Les demandes arrivent par plusieurs canaux.","chat"),
("LE RISQUE","Une info peut se perdre","Retrouver chaque détail devient compliqué.","notes"),
("LA SOLUTION","Un seul suivi","Les demandes en ligne sont regroupées au même endroit.","inbox"),
("RENDEVO","Moins de dispersion","Cabinet médical ? Envoyez « RENDEVO ».","cta")
]},
{
"slug":"04-after-hours",
"voice":"Il est vingt et une heures. Le cabinet est fermé, mais un patient pense à prendre rendez-vous. Il ne veut pas forcément attendre le lendemain pour envoyer sa demande. Avec RENDEVO, il peut ouvrir votre page et transmettre ses informations en ligne, même en dehors des horaires d’accueil. Votre équipe retrouve la demande à son retour et la traite selon votre organisation. Vos horaires ne changent pas. Le premier contact devient simplement plus pratique. Écrivez-nous « RENDEVO ».",
"scenes":[
("21:14","Le cabinet est fermé","Mais le patient pense déjà à son rendez-vous.","clock"),
("CÔTÉ PATIENT","Il envoie sa demande","La page reste accessible depuis son téléphone.","nightphone"),
("LE LENDEMAIN","Votre équipe la retrouve","Les informations attendent dans le tableau de suivi.","sheet"),
("RENDEVO","Disponible en ligne","Cabinet médical ? Écrivez-nous « RENDEVO ».","cta")
]},
{
"slug":"05-double-booking",
"voice":"Deux patients. Le même créneau. Et votre planning devient un casse-tête. Quand les disponibilités sont vérifiées à la main, une erreur peut arriver. RENDEVO contrôle les créneaux déjà occupés avant de présenter les horaires disponibles, selon les réglages du cabinet. Les demandes sont ensuite suivies dans un espace organisé. L’objectif n’est pas de remplacer votre équipe : c’est de lui donner un planning plus clair et de limiter les conflits. Vous voulez voir comment l’installation fonctionne ? Écrivez « RENDEVO ».",
"scenes":[
("LE CONFLIT","Deux demandes. Un horaire.","Un chevauchement suffit à désorganiser la journée.","conflict"),
("DISPONIBILITÉS","Les créneaux sont vérifiés","Les horaires occupés ne sont pas proposés.","calendar"),
("PLANNING","Une vue plus claire","Votre équipe suit les demandes au même endroit.","calendarclean"),
("RENDEVO","Moins de conflits","Cabinet médical ? Écrivez-nous « RENDEVO ».","cta")
]},
{
"slug":"06-reception-overload",
"voice":"À l’accueil, tout arrive en même temps : un patient devant le bureau, le téléphone, les horaires à vérifier, les coordonnées à noter. Votre secrétaire ne peut pas être partout à la fois. RENDEVO permet au patient d’envoyer sa demande en ligne et rassemble les informations pour le suivi. L’équipe garde le contrôle, mais une partie du parcours est déjà structurée. C’est un outil pour soutenir l’accueil, pas pour remplacer les personnes qui le font vivre. Écrivez-nous « RENDEVO ».",
"scenes":[
("À L’ACCUEIL","Tout arrive en même temps","Téléphone, patients, horaires, notes.","busy"),
("LE PARCOURS","Le patient remplit sa demande","Les informations sont saisies une seule fois.","journey"),
("LE SUIVI","Votre équipe garde la main","Les demandes sont visibles dans un tableau clair.","dashboard"),
("RENDEVO","L’accueil mieux organisé","Cabinet médical ? Écrivez-nous « RENDEVO ».","cta")
]},
{
"slug":"07-patient-journey",
"voice":"Imaginez votre patient sur son téléphone. Il veut choisir un service, trouver une date et envoyer ses coordonnées. Pas créer un compte compliqué. Pas chercher partout. RENDEVO propose un parcours mobile en étapes courtes, adapté à l’identité du cabinet. Une fois la demande envoyée, votre équipe retrouve les informations dans le suivi et peut la traiter. La prise de rendez-vous commence par une expérience simple. Vous gérez un cabinet ? Envoyez-nous « RENDEVO ».",
"scenes":[
("LE PATIENT","Il veut faire simple","Choisir un service, une date, puis envoyer sa demande.","journey"),
("SUR MOBILE","Des étapes courtes","Un écran à la fois, sans formulaire interminable.","mobile"),
("APRÈS L’ENVOI","La demande est transmise","Le cabinet retrouve les informations pour le suivi.","email"),
("RENDEVO","Un parcours plus clair","Cabinet médical ? Envoyez-nous « RENDEVO ».","cta")
]},
{
"slug":"08-lost-information",
"voice":"Le nom du patient est dans un message. La date est sur un papier. Le numéro est dans l’historique des appels. Retrouver une demande ne devrait pas devenir une enquête. RENDEVO rassemble les informations envoyées via la page de réservation dans un tableau de suivi. Votre équipe peut consulter les détails plus facilement et garder une trace organisée des demandes. Moins de recherche, plus de visibilité sur ce qui a été reçu. Pour équiper votre cabinet, écrivez-nous « RENDEVO ».",
"scenes":[
("OÙ EST L’INFO ?","Trois endroits différents","Message, papier, historique d’appel.","notes"),
("RECHERCHE","On perd du temps à retrouver","Les détails sont éparpillés entre plusieurs supports.","search"),
("SUIVI","Les demandes sont regroupées","Une vue claire pour retrouver les informations reçues.","sheet"),
("RENDEVO","Une trace plus organisée","Cabinet médical ? Écrivez-nous « RENDEVO ».","cta")
]},
{
"slug":"09-first-impression",
"voice":"Votre cabinet soigne son accueil, son espace et l’expérience des patients. Mais le premier contact se fait parfois sur un écran. Si la réservation est confuse, l’image de votre cabinet ne suit pas. RENDEVO crée une page personnalisée, adaptée au téléphone et à l’identité de votre établissement. Vous pouvez partager le lien sur vos réseaux ou l’ajouter à votre communication. Un parcours clair, cohérent avec votre cabinet. Vous souhaitez équiper votre établissement ? Écrivez « RENDEVO ».",
"scenes":[
("PREMIER CONTACT","Votre image commence en ligne","Le patient découvre votre cabinet sur son téléphone.","webpage"),
("PERSONNALISATION","Aux couleurs du cabinet","Une page claire, adaptée à votre identité.","brandpage"),
("PARTAGE","Un lien facile à diffuser","Ajoutez-le à votre bio, votre site ou vos supports.","link"),
("RENDEVO","Un accueil cohérent","Cabinet médical ? Écrivez-nous « RENDEVO ».","cta")
]},
{
"slug":"10-how-it-works",
"voice":"Concrètement, comment fonctionne RENDEVO ? Le patient ouvre la page personnalisée du cabinet. Il choisit le service, consulte les dates et les horaires disponibles, puis renseigne ses coordonnées. Sa demande est transmise au cabinet et apparaît dans le tableau de suivi. Selon la configuration, une confirmation est envoyée par e-mail. Votre équipe garde la visibilité sur les demandes et le planning. Vous voulez équiper votre cabinet ? Écrivez-nous « RENDEVO ».",
"scenes":[
("ÉTAPE 01","Le patient ouvre la page","Une page personnalisée au nom du cabinet.","webpage"),
("ÉTAPE 02","Il choisit un créneau","Les disponibilités sont affichées clairement.","calendar"),
("ÉTAPE 03","Il envoie ses coordonnées","Le parcours reste simple sur mobile.","mobile"),
("CÔTÉ CABINET","La demande est suivie","Les informations arrivent dans le tableau du cabinet.","dashboard")
]}
]

CSS = r"""
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#07131b;color:#f4f8f6;font-family:Arial,Helvetica,sans-serif}
.scene{width:1080px;height:1920px;position:relative;overflow:hidden;padding:150px 68px 150px 70px;display:grid;grid-template-columns:650px 270px;column-gap:24px;align-items:center;background:radial-gradient(ellipse at 20% 45%,#173e3a 0%,transparent 48%),radial-gradient(ellipse at 82% 15%,#16354b 0%,transparent 40%),linear-gradient(145deg,#06121a,#10232c 58%,#08151d)}
.scene:before{content:"";position:absolute;width:900px;height:900px;border:1px solid #9ce7c51c;border-radius:50%;left:-500px;top:480px;animation:orbit 34s linear infinite}
.scene:after{content:"";position:absolute;width:520px;height:520px;border:1px solid #9ce7c51c;border-radius:50%;right:-330px;bottom:220px}
@keyframes orbit{to{transform:rotate(360deg)}}
@keyframes enter{from{opacity:0;transform:translateY(28px) scale(.985)}to{opacity:1;transform:translateY(0) scale(1)}}
@keyframes glide{from{opacity:0;transform:translateX(-42px)}to{opacity:1;transform:translateX(0)}}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
@keyframes pulse{0%,100%{box-shadow:0 0 0 0 #8ee5c200}50%{box-shadow:0 0 0 15px #8ee5c51a}}
@keyframes sweep{0%{transform:translateX(-120%)}100%{transform:translateX(160%)}}
@keyframes ring{0%,100%{transform:scale(1);opacity:.7}50%{transform:scale(1.12);opacity:1}}
.brand{position:absolute;top:72px;left:72px;font-size:25px;font-weight:900;letter-spacing:6px;z-index:5;color:#eaf5f0}
.brand b{color:#8ee5c2}
.counter{position:absolute;top:75px;right:72px;font-size:17px;letter-spacing:3px;color:#8ee5c2;z-index:5}
.stage{position:relative;width:650px;height:900px;display:flex;align-items:center;justify-content:center;z-index:2;animation:enter .9s cubic-bezier(.2,.8,.2,1) both}
.copy{position:relative;width:270px;z-index:3;padding:24px 18px 24px 22px;border-left:2px solid #8ee5c2;background:linear-gradient(90deg,#0c2029e8,#0c2029a8);border-radius:0 18px 18px 0;animation:enter .75s .18s cubic-bezier(.2,.8,.2,1) both}
.kicker{font-size:14px;letter-spacing:2.5px;color:#8ee5c2;font-weight:800;margin-bottom:17px;line-height:1.35}
.copy h2{font-size:29px;line-height:1.13;letter-spacing:-.7px;margin:0 0 14px;font-weight:800;overflow-wrap:anywhere}
.copy p{font-size:17px;line-height:1.48;color:#b7c9c9;margin:0}
.brand,.counter,.copy,.stage{isolation:isolate}
.footer{position:absolute;bottom:72px;left:72px;right:72px;z-index:5;display:flex;justify-content:space-between;color:#6f8991;font-size:14px;letter-spacing:2.4px}
.phone{width:430px;height:760px;border:9px solid #dce8e2;border-radius:52px;background:#f7faf8;color:#18312c;padding:32px 25px;box-shadow:0 35px 95px #0008;position:relative;transform:rotate(-2deg);animation:float 5s ease-in-out infinite}
.notch{width:105px;height:17px;border-radius:0 0 14px 14px;background:#dce8e2;margin:-32px auto 30px}
.screenbrand{font-size:16px;letter-spacing:3px;color:#4e6e63;font-weight:800}
.screenhead{font-size:29px;line-height:1.1;font-weight:850;margin:28px 0 24px}
.field{padding:20px 16px;margin:14px 0;border-radius:13px;border:1px solid #dbe5e0;background:white;color:#71837d;font-size:18px}
.action{padding:19px;text-align:center;background:#145c4b;color:white;border-radius:13px;font-size:18px;font-weight:800;margin-top:22px}
.toast{position:absolute;right:-25px;top:180px;background:#fff;color:#20332e;border-radius:18px;padding:21px 24px;width:290px;box-shadow:0 20px 55px #0007;animation:glide .8s .25s both}
.toast small{font-size:13px;color:#75877f;letter-spacing:1px}
.toast strong{display:block;font-size:20px;margin-top:9px}
.panel{width:570px;background:#102b34;border:1px solid #41615c;border-radius:26px;padding:28px;box-shadow:0 28px 75px #0007;animation:float 5.5s ease-in-out infinite}
.paneltop{display:flex;justify-content:space-between;align-items:center;color:#dcebe5;font-size:18px;letter-spacing:1.5px;margin-bottom:22px}
.paneltop span:last-child{color:#8ee5c2;font-size:13px}
.item{display:flex;align-items:center;gap:15px;padding:19px 6px;border-top:1px solid #ffffff19;font-size:19px;color:#dce9e4}
.dot{width:12px;height:12px;flex:none;border-radius:50%;background:#8ee5c2;box-shadow:0 0 16px #8ee5c277}
.status{margin-left:auto;font-size:13px;color:#8ee5c2;background:#8ee5c21c;padding:8px 11px;border-radius:20px}
.chatstack{width:540px;display:flex;flex-direction:column;gap:22px;transform:rotate(-2deg);animation:float 5s ease-in-out infinite}
.bubble{padding:23px 26px;border-radius:22px;max-width:430px;font-size:19px;line-height:1.35;box-shadow:0 20px 45px #0005}
.bubble.left{background:#f6faf7;color:#203a33;align-self:flex-start;border-bottom-left-radius:5px}
.bubble.right{background:#1a6957;color:white;align-self:flex-end;border-bottom-right-radius:5px}
.clock{width:480px;height:480px;border:18px solid #8ee5c2;border-radius:50%;position:relative;display:grid;place-items:center;box-shadow:0 0 75px #8ee5c233;animation:pulse 3s infinite}
.clock:before{content:"";position:absolute;width:12px;height:160px;background:#e7f3ed;left:50%;top:80px;transform:translateX(-50%) rotate(35deg);transform-origin:bottom;border-radius:10px}
.clock:after{content:"";position:absolute;width:12px;height:120px;background:#8ee5c2;left:50%;top:120px;transform:translateX(-50%) rotate(125deg);transform-origin:bottom;border-radius:10px}
.clocklabel{font-size:64px;font-weight:900;letter-spacing:-2px;margin-top:160px}
.calendar{width:570px;background:#f7faf8;color:#1a332d;border-radius:26px;padding:30px;box-shadow:0 28px 75px #0008;transform:rotate(-1deg)}
.calhead{display:flex;justify-content:space-between;font-size:22px;font-weight:800;margin-bottom:22px}
.days{display:grid;grid-template-columns:repeat(7,1fr);gap:9px}
.day{padding:16px 0;text-align:center;border-radius:10px;background:#eaf0ed;color:#5c7069;font-size:17px}
.day.active{background:#17614e;color:#fff;animation:pulse 2s infinite}
.day.busy{background:#f5d9d4;color:#b85c51;text-decoration:line-through}
.slots{display:flex;gap:10px;flex-wrap:wrap;margin-top:22px}
.slot{padding:12px 15px;border:1px solid #9ab9aa;border-radius:10px;color:#1a614c;font-size:16px}
.conflict{width:570px;position:relative;height:520px}
.appointment{position:absolute;width:360px;padding:25px;border-radius:22px;background:#f8fbf9;color:#20362f;box-shadow:0 22px 65px #0007;font-size:19px}
.appointment.one{top:65px;left:15px;transform:rotate(-5deg)}
.appointment.two{top:235px;right:0;transform:rotate(4deg);border:3px solid #db7668}
.cross{position:absolute;top:205px;left:255px;width:75px;height:75px;border-radius:50%;background:#d75e54;color:white;font-size:48px;display:grid;place-items:center;z-index:2;box-shadow:0 0 30px #d75e5488}
.taskstack{display:flex;flex-direction:column;gap:16px;width:540px}
.task{padding:24px;border-radius:18px;background:#f7faf8;color:#223932;font-size:20px;display:flex;gap:18px;align-items:center;box-shadow:0 15px 40px #0005}
.task i{width:38px;height:38px;border-radius:12px;background:#d9f1e5;display:grid;place-items:center;color:#17614e;font-style:normal;font-weight:900}
.journey{width:550px;background:#102a34;border:1px solid #46665e;border-radius:25px;padding:35px;box-shadow:0 28px 70px #0007}
.step{display:flex;align-items:center;gap:20px;padding:24px 0;border-bottom:1px solid #ffffff1a;font-size:20px;color:#e1eee8}
.step:last-child{border:0}
.stepnum{width:42px;height:42px;display:grid;place-items:center;border-radius:50%;background:#8ee5c2;color:#0b3026;font-weight:900}
.paper{width:490px;display:flex;flex-direction:column;gap:20px;transform:rotate(-3deg)}
.note{background:#f6f1df;color:#3a433b;padding:23px 27px;border-radius:8px;box-shadow:0 20px 40px #0006;font-size:20px}
.note:nth-child(2){margin-left:70px;transform:rotate(3deg)}
.note:nth-child(3){margin-left:25px;transform:rotate(-1deg)}
.searchbar{width:540px;background:#f7faf8;color:#30463f;border-radius:18px;padding:22px 25px;font-size:19px;box-shadow:0 22px 60px #0007}
.browser{width:570px;background:#f7faf8;color:#17332a;border-radius:22px;overflow:hidden;box-shadow:0 30px 75px #0008;transform:rotate(-1deg)}
.browserbar{height:48px;background:#e4ece7;display:flex;align-items:center;gap:8px;padding:0 18px}
.browserbar i{width:10px;height:10px;border-radius:50%;background:#a7b8ae}
.heroimg{height:300px;background:linear-gradient(135deg,#d9ede3,#aacdbd);padding:35px;display:flex;flex-direction:column;justify-content:flex-end}
.heroimg strong{font-size:30px;color:#194536}
.browserbody{padding:25px}
.browserbody .action{margin-top:15px}
.linkcard{width:510px;padding:30px;border-radius:25px;background:#f7faf8;color:#1d382f;box-shadow:0 25px 70px #0007;text-align:center}
.linkicon{width:90px;height:90px;border-radius:25px;background:#d8f1e4;color:#17614e;display:grid;place-items:center;font-size:42px;margin:0 auto 20px}
.flow{display:flex;flex-direction:column;gap:18px;width:540px}
.flowstep{display:flex;align-items:center;gap:18px;background:#112e37;border:1px solid #42665d;padding:20px 24px;border-radius:17px;color:#e7f2ec;font-size:19px;box-shadow:0 15px 40px #0005}
.flowstep b{width:38px;height:38px;border-radius:50%;background:#8ee5c2;color:#0b3026;display:grid;place-items:center}
.mail{width:530px;background:#f7faf8;color:#203b32;border-radius:24px;padding:32px;box-shadow:0 25px 65px #0007;text-align:center}
.mailcheck{font-size:65px;color:#17855f;margin:18px}
.mailtitle{font-size:25px;font-weight:900}
.mailcopy{font-size:17px;color:#71837b;margin-top:14px}
.brandpage{width:550px;padding:35px;border-radius:25px;background:#102b34;border:1px solid #41665b;box-shadow:0 25px 70px #0007}
.brandpage h3{font-size:30px;margin:20px 0;color:#f1f7f4}
.brandpage p{font-size:18px;color:#b6ccc4;line-height:1.5}
.brandpage .action{background:#8ee5c2;color:#10352a}
.ctavisual{width:560px;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:26px}
.ctalogo{font-size:58px;font-weight:900;letter-spacing:12px;color:#edf8f2}
.ctalogo b{color:#8ee5c2}
.ctaline{width:140px;height:3px;background:#8ee5c2;box-shadow:0 0 22px #8ee5c2}
.ctasmall{font-size:18px;letter-spacing:3px;color:#b8ccc4}
"""

def visual(kind):
    templates = {
    "ring": '<div class="panel"><div class="paneltop"><span>ACCUEIL · CABINET</span><span>MAINTENANT</span></div><div class="item"><span class="dot"></span>Consultation en cours</div><div class="item"><span class="dot" style="background:#df8c67"></span>Téléphone qui sonne <span class="status">APPEL</span></div><div class="item"><span class="dot"></span>Patient à accueillir</div><div class="toast"><small>APPEL ENTRANT</small><strong>Cabinet médical</strong></div></div>',
    "phone": '<div class="phone"><div class="notch"></div><div class="screenbrand">CABINET · RENDEZ-VOUS</div><div class="screenhead">Prendre rendez-vous</div><div class="field">Choisir un service</div><div class="field">Date souhaitée</div><div class="field">Vos coordonnées</div><div class="action">Envoyer ma demande →</div></div>',
    "sheet": '<div class="panel"><div class="paneltop"><span>RENDEVO · SUIVI</span><span>DEMANDES</span></div><div class="item"><span class="dot"></span>Consultation · 09:00 <span class="status">Reçue</span></div><div class="item"><span class="dot"></span>Contrôle · 10:30 <span class="status">Reçue</span></div><div class="item"><span class="dot"></span>Suivi · 11:15 <span class="status">Reçue</span></div></div>',
    "missed": '<div class="phone"><div class="notch"></div><div class="screenbrand">TÉLÉPHONE</div><div style="text-align:center;margin:90px 0 25px;font-size:72px;color:#d86d60">◉</div><div class="screenhead" style="text-align:center">Appel manqué</div><div style="text-align:center;color:#71837d;font-size:19px">Cabinet · 10:42</div><div class="action">Rappeler</div><div class="toast"><small>AUTRE OPTION</small><strong>Envoyer une demande en ligne</strong></div></div>',
    "inbox": '<div class="panel"><div class="paneltop"><span>DEMANDES REÇUES</span><span>AUJOURD’HUI</span></div><div class="item"><span class="dot"></span>Patient · Consultation <span class="status">Nouveau</span></div><div class="item"><span class="dot"></span>Patient · Contrôle <span class="status">Nouveau</span></div><div class="item"><span class="dot"></span>Patient · Suivi <span class="status">Nouveau</span></div></div>',
    "chat": '<div class="chatstack"><div class="bubble left">Bonjour, je voudrais un rendez-vous.</div><div class="bubble right">Pour quel service ?</div><div class="bubble left">Est-ce que mardi est possible ?</div><div class="bubble right">Je vérifie le planning…</div></div>',
    "notes": '<div class="paper"><div class="note">Nom : Mme A. · Appel du matin</div><div class="note">Date souhaitée : jeudi ?</div><div class="note">Numéro reçu sur WhatsApp…</div></div>',
    "clock": '<div class="clock"><div class="clocklabel">21:14</div></div>',
    "nightphone": '<div class="phone"><div class="notch"></div><div class="screenbrand">RENDEVO · EN LIGNE</div><div class="screenhead">Votre demande, à tout moment.</div><div class="field">Service souhaité</div><div class="field">Date préférée</div><div class="field">Téléphone</div><div class="action">Envoyer →</div></div>',
    "conflict": '<div class="conflict"><div class="appointment one"><small>10:30 · CONSULTATION</small><h3>Patient A</h3><span>Créneau réservé</span></div><div class="cross">×</div><div class="appointment two"><small>10:30 · CONSULTATION</small><h3>Patient B</h3><span>Conflit de planning</span></div></div>',
    "calendar": '<div class="calendar"><div class="calhead"><span>JUIN</span><span>Disponibilités</span></div><div class="days">'+''.join(f'<div class="day {"busy" if n in [17,20,23] else "active" if n==18 else ""}">{n}</div>' for n in range(15,29))+'</div><div class="slots"><span class="slot">09:00</span><span class="slot">09:15</span><span class="slot">10:30</span></div></div>',
    "calendarclean": '<div class="calendar"><div class="calhead"><span>PLANNING DU JOUR</span><span style="color:#16805b">✓</span></div><div class="item" style="color:#234238;border-color:#dce7e1"><span class="dot"></span>09:00 · Consultation</div><div class="item" style="color:#234238;border-color:#dce7e1"><span class="dot"></span>10:30 · Contrôle</div><div class="item" style="color:#234238;border-color:#dce7e1"><span class="dot"></span>11:15 · Suivi</div></div>',
    "busy": '<div class="taskstack"><div class="task"><i>☎</i>Répondre au téléphone</div><div class="task"><i>＋</i>Accueillir un patient</div><div class="task"><i>◷</i>Vérifier les horaires</div><div class="task"><i>✎</i>Noter une demande</div></div>',
    "journey": '<div class="journey"><div class="paneltop"><span>PARCOURS PATIENT</span><span>3 ÉTAPES</span></div><div class="step"><span class="stepnum">1</span>Choisir un service</div><div class="step"><span class="stepnum">2</span>Sélectionner une date</div><div class="step"><span class="stepnum">3</span>Envoyer ses coordonnées</div></div>',
    "mobile": '<div class="phone"><div class="notch"></div><div class="screenbrand">ÉTAPE 2 SUR 5</div><div class="screenhead">Choisissez une date</div><div class="calendar" style="width:100%;padding:14px;box-shadow:none"><div class="days">'+''.join(f'<div class="day {"active" if n==18 else ""}">{n}</div>' for n in range(15,29))+'</div></div><div class="field">10:30</div><div class="action">Continuer →</div></div>',
    "email": '<div class="mail"><div style="font-size:15px;color:#71837b">RENDEVO · E-MAIL</div><div class="mailcheck">✓</div><div class="mailtitle">Demande enregistrée</div><div class="mailcopy">Les informations ont bien été transmises au cabinet.</div></div>',
    "search": '<div class="searchbar">⌕ &nbsp; Rechercher une demande…<div class="item" style="color:#29463c;border-color:#dce7e1;margin-top:20px"><span class="dot"></span>Patient · 09:30</div><div class="item" style="color:#29463c;border-color:#dce7e1"><span class="dot"></span>Patient · 10:15</div></div>',
    "webpage": '<div class="browser"><div class="browserbar"><i></i><i></i><i></i></div><div class="heroimg"><strong>Votre cabinet, plus accessible.</strong></div><div class="browserbody"><div class="screenbrand">CABINET MÉDICAL</div><div class="screenhead">Bienvenue dans votre espace rendez-vous.</div><div class="action">Prendre rendez-vous →</div></div></div>',
    "brandpage": '<div class="brandpage"><div class="screenbrand">VOTRE CABINET</div><h3>Une page à votre image.</h3><p>Vos couleurs, vos services, vos horaires et un parcours clair pour vos patients.</p><div class="action">Réserver en ligne →</div></div>',
    "link": '<div class="linkcard"><div class="linkicon">↗</div><div style="font-size:24px;font-weight:900">Votre lien de réservation</div><div style="font-size:17px;color:#6e8179;margin-top:15px">À partager sur Instagram, votre site ou par QR code.</div><div class="action">rendevo.dz / cabinet</div></div>',
    "flow": '<div class="flow"><div class="flowstep"><b>1</b>Page personnalisée</div><div class="flowstep"><b>2</b>Choix du service et du créneau</div><div class="flowstep"><b>3</b>Coordonnées du patient</div><div class="flowstep"><b>4</b>Suivi côté cabinet</div></div>',
    "dashboard": '<div class="panel"><div class="paneltop"><span>ESPACE CABINET</span><span>VUE DU JOUR</span></div><div class="item"><span class="dot"></span>Demande reçue <span class="status">À traiter</span></div><div class="item"><span class="dot"></span>Créneau sélectionné <span class="status">Visible</span></div><div class="item"><span class="dot"></span>Coordonnées patient <span class="status">Enregistrées</span></div></div>',
    "cta": '<div class="ctavisual"><div class="ctalogo">RENDE<b>VO</b></div><div class="ctal ine"></div><div class="ctasmall">RÉSERVATION · SUIVI · ORGANISATION</div></div>'
    }
    return templates.get(kind, templates["phone"])

def run(cmd):
    subprocess.run(cmd, check=True)

pathlib.Path("compositions").mkdir(exist_ok=True)
pathlib.Path("out").mkdir(exist_ok=True)
for idx, reel in enumerate(REELS, 1):
    slug = reel["slug"]
    text_path = pathlib.Path("compositions", slug + ".txt")
    text_path.write_text(reel["voice"], encoding="utf-8")
    run([".venv/bin/edge-tts","--voice","fr-FR-VivienneMultilingualNeural","--rate=-2%","--file",str(text_path),"--write-media",f"out/{slug}-voice.mp3"])
    duration = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",f"out/{slug}-voice.mp3"]).decode().strip())
    scene_duration = max(5.0, duration / len(reel["scenes"]) + 0.35)
    blocks = []
    for j, (kicker, title, detail, kind) in enumerate(reel["scenes"]):
        blocks.append(
            f'<section class="scene" data-duration="{scene_duration:.3f}" data-camera="push 1.025">'
            f'<div class="brand">RENDE<b>VO</b></div><div class="counter">{idx:02d} / 10</div>'
            f'<div class="stage">{visual(kind)}</div>'
            f'<aside class="copy"><div class="kicker">{html.escape(kicker)}</div>'
            f'<h2>{html.escape(title)}</h2><p>{html.escape(detail)}</p></aside>'
            f'<div class="footer"><span>LE RENDEZ-VOUS, PLUS SIMPLE</span><span>RENDEVO.DZ</span></div>'
            f'</section>'
        )
    page = '<!doctype html><html lang="fr" data-width="1080" data-height="1920" data-fps="30"><head><meta charset="utf-8"><style>'+CSS+'</style></head><body><main data-sequence data-transition="fade 0.7">'+''.join(blocks)+'</main></body></html>'
    pathlib.Path("compositions", slug + ".html").write_text(page, encoding="utf-8")
    print(f"Rendering {slug} | voice {duration:.1f}s")
    run(["npx","givemotion","render",f"compositions/{slug}.html","-o",f"out/{slug}-silent.mp4","--quality","standard"])
    run(["ffmpeg","-y","-i",f"out/{slug}-silent.mp4","-i",f"out/{slug}-voice.mp3","-map","0:v:0","-map","1:a:0","-c:v","libx264","-preset","fast","-crf","19","-c:a","aac","-b:a","192k","-shortest",f"out/{slug}.mp4"])
    pathlib.Path(f"out/{slug}-silent.mp4").unlink()
    pathlib.Path(f"out/{slug}-voice.mp3").unlink()
    print(f"Finished {slug}")

files = sorted(pathlib.Path("out").glob("*.mp4"))
assert len(files) == 10, f"Expected 10 videos, got {len(files)}"
for f in files:
    d = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1:nokey=1",str(f)]).decode().strip())
    assert d >= 24, f"{f} too short: {d}"
    print(f"{f.name}: {d:.1f}s")
