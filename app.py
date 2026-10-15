import os, time, random, sqlite3, hmac, asyncio, datetime
import httpx, socketio
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

PAGE = """<!DOCTYPE html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>نور • منصة القرآن والبث المباشر</title>
<style>
:root{--g:#d4af37;--bg:#07140f;--c:rgba(255,255,255,.06);--t:#f3efe0}
*{box-sizing:border-box}html,body{margin:0}
body{font-family:'Segoe UI',Tahoma,Arial,sans-serif;color:var(--t);min-height:100vh;
background:radial-gradient(circle at 20% 0,#0f3d2b 0,transparent 50%),radial-gradient(circle at 90% 100%,#4a3a0a 0,transparent 45%),var(--bg);background-attachment:fixed}
body:before{content:"";position:fixed;inset:0;opacity:.07;pointer-events:none;
background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='60' height='60'%3E%3Cpath d='M30 4l6 14 14-6-6 14 14 6-14 6 6 14-14-6-6 14-6-14-14 6 6-14-14-6 14-6-6-14 14 6z' fill='none' stroke='%23d4af37'/%3E%3C/svg%3E")}
header{padding:16px;text-align:center;position:relative}
h1{margin:0;color:var(--g);font-size:26px}
.sub{opacity:.8;font-size:13px;margin-top:4px}
nav{display:flex;gap:6px;overflow-x:auto;padding:8px 10px;position:sticky;top:0;z-index:5;background:rgba(7,20,15,.9);backdrop-filter:blur(8px)}
nav button{flex:0 0 auto;white-space:nowrap}
button,select,input,textarea{font:inherit;color:var(--t);background:var(--c);border:1px solid rgba(212,175,55,.35);border-radius:10px;padding:9px 13px}
button{cursor:pointer}button.on,button.pri{background:var(--g);color:#1b1500;font-weight:700}
button.red{background:#c0392b;border-color:#c0392b}
main{max-width:900px;margin:auto;padding:12px}
section{display:none}section.on{display:block}
.card{background:var(--c);border:1px solid rgba(212,175,55,.25);border-radius:16px;padding:14px;margin:10px 0}
.row{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
video,canvas{width:100%;border-radius:12px;background:#000;max-height:60vh}
.badge{background:#c0392b;border-radius:8px;padding:2px 8px;font-size:12px}
#ayat{font-family:'Amiri','Traditional Arabic',serif;line-height:2.4;text-align:justify;font-size:26px;background:#fbf7e8;color:#111;border-radius:14px;padding:16px;margin-top:10px}
.n{color:var(--g);font-size:.7em;margin:0 4px}
#chatbox,#aiout{max-height:260px;overflow:auto}
.m{background:rgba(255,255,255,.08);border-radius:10px;padding:6px 10px;margin:5px 0}
#stage{overflow:hidden;height:55vh;background:#000;border-radius:12px;touch-action:none;position:relative}
#stage img{position:absolute;left:50%;top:50%;max-width:90%;max-height:90%;user-select:none;-webkit-user-drag:none}
.big{font-size:34px;color:var(--g)}
input,textarea,select{width:100%}
</style></head><body>
<header><h1>🕌 نور — القرآن والبث المباشر</h1><div class="sub"><span id="onl">0</span> متصل الآن • <span id="me"></span></div></header>
<nav id="nav"></nav><div id="ann" class="card" hidden style="margin:8px 12px;border-color:var(--g);text-align:center"></div>
<main>
<section id="s-live" class="on">
 <div class="card"><div class="row"><b>البث المباشر</b><span class="badge" id="lb" hidden>LIVE</span></div>
 <video id="v" autoplay playsinline controls></video><p id="lm" class="sub">لا يوجد بث حالياً.</p></div>
 <div class="card" id="pl" hidden><b id="pq"></b><div id="po"></div></div>
 <div class="card"><b>اسأل المشرف</b><div class="row"><input id="qi" maxlength="300" placeholder="سؤالك..." style="flex:1"><button id="qs">أرسل</button></div></div>
 <div class="card"><b>الدردشة</b><div id="chatbox"></div>
 <div class="row" style="margin-top:8px"><input id="ci" maxlength="300" placeholder="اكتب رسالة..." style="flex:1"><button class="pri" id="cs">إرسال</button></div></div>
</section>
<section id="s-q">
 <div class="card"><div class="row"><select id="sur" style="flex:1"></select><button id="fm">A-</button><button id="fp">A+</button></div>
 <audio id="au" controls style="width:100%;margin-top:8px"></audio><div id="ayat">جاري التحميل...</div></div>
</section>
<section id="s-i">
 <div class="card"><input type="file" id="fi" accept="image/*">
 <div class="row" style="margin:8px 0"><button id="zp">تكبير +</button><button id="zm">تصغير −</button><button id="rl">⟲ تدوير</button><button id="rr">⟳ تدوير</button><button id="fx">قلب</button><button id="rs">إعادة</button></div>
 <div id="stage"><img id="im" alt=""></div><p class="sub">اسحب بإصبعك للتحريك، وعجلة الماوس للتكبير.</p></div>
</section>
<section id="s-a">
 <div class="card"><b>مساعد الذكاء الاصطناعي</b><select id="am" style="margin:8px 0"><option value="">سؤال عام</option><option value="فسّر الآية: ">تفسير</option><option value="ما الحكم الشرعي في: ">فقه</option><option value="أعرب: ">إعراب</option></select><textarea id="aq" rows="3" placeholder="اسأل عن تفسير آية أو حكم أو فائدة..."></textarea>
 <button class="pri" id="ab" style="margin-top:8px">إرسال</button><div id="aiout"></div></div>
</section>
<section id="s-t">
 <div class="card" style="text-align:center"><div class="big" id="tc">0</div>
 <button class="pri" id="tb" style="font-size:22px;padding:18px 50px">سبّح</button> <button id="tr">تصفير</button></div>
 <div class="card"><b>مواقيت الصلاة</b> <button id="pt">حسب موقعي</button><div id="pto" class="sub"></div><div id="cd" style="font-size:20px;color:var(--g);margin-top:6px"></div></div>
 <div class="card"><b>آية اليوم</b><div id="da" style="font-size:22px;line-height:2;margin:6px 0"></div><button id="dn">آية أخرى</button></div>
 <div class="card"><b>التاريخ الهجري:</b> <span id="hj"></span></div>
</section>
<section id="s-d">
 <div class="card" id="lg"><b>دخول الأدمن</b><input type="password" id="pw" placeholder="كلمة السر" style="margin:8px 0"><button class="pri" id="pb">دخول</button></div>
 <div id="ad" hidden>
  <div class="card"><b>إعلان للجميع</b><div class="row"><input id="ani" placeholder="نص الإعلان" style="flex:1"><button class="pri" id="anb">نشر</button></div></div>
  <div class="card"><b>استطلاع</b><input id="pqi" placeholder="السؤال" style="margin:6px 0"><input id="poi" placeholder="الخيارات مفصولة بفاصلة: نعم, لا"><div class="row" style="margin-top:6px"><button class="pri" id="pnb">إنشاء</button><button id="pcb">إغلاق</button></div></div>
  <div class="card"><b>أسئلة الزوار</b><div id="inbox"></div></div>
  <div class="card"><b>الزيارات آخر 7 أيام</b><div id="hs" class="row" style="align-items:flex-end;height:90px;flex-wrap:nowrap"></div></div>
  <div class="card"><div class="row"><button class="pri" id="bs">▶ بدء البث</button><button class="red" id="be">■ إيقاف</button><button id="bm">🎤 كتم</button><button id="bv">📷 إيقاف الكاميرا</button><button id="bf">🔄 قلب الكاميرا</button></div>
  <video id="pv" autoplay playsinline muted style="margin-top:8px"></video></div>
  <div class="card row" style="justify-content:space-around;text-align:center">
   <div>المتصلون<div class="big" id="st1">0</div></div><div>الزيارات<div class="big" id="st2">0</div></div><div>الذروة<div class="big" id="st3">0</div></div></div>
  <div class="card"><b>قائمة المتصلين</b><div id="ul"></div></div>
 </div>
</section>
</main>
<script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>
<script>
const $=id=>document.getElementById(id),s=io();
const tabs=[['live','البث'],['q','القرآن'],['i','الصور'],['a','الذكاء'],['t','التسبيح والمواقيت'],['d','الأدمن']];
tabs.forEach(([k,n],i)=>{const b=document.createElement('button');b.textContent=n;if(!i)b.className='on';
 b.onclick=()=>{document.querySelectorAll('nav button').forEach(x=>x.className='');b.className='on';
 document.querySelectorAll('section').forEach(x=>x.className='');$('s-'+k).className='on'};$('nav').appendChild(b)});
// ---- socket / live
const cfg={iceServers:[{urls:'stun:stun.l.google.com:19302'}]};
s.on('online',n=>$('onl').textContent=n);
s.on('live',setLive);
function setLive(on){$('lb').hidden=!on;$('lm').textContent=on?'البث مباشر، جاري الاتصال...':'لا يوجد بث حالياً.';
 if(vpc){vpc.close();vpc=null;$('v').srcObject=null}
 if(on&&!stream)s.emit('watch')}
s.on('viewer',async id=>{if(!stream)return;const pc=new RTCPeerConnection(cfg);pcs[id]=pc;
 stream.getTracks().forEach(t=>pc.addTrack(t,stream));
 pc.onicecandidate=e=>e.candidate&&s.emit('signal',{to:id,data:{ice:e.candidate}});
 pc.onconnectionstatechange=()=>{if(['failed','closed','disconnected'].includes(pc.connectionState)){pc.close();delete pcs[id]}};
 await pc.setLocalDescription(await pc.createOffer());s.emit('signal',{to:id,data:{sdp:pc.localDescription}})});
s.on('signal',async({from,data})=>{try{
 if(data.sdp&&data.sdp.type==='offer'){vpc=new RTCPeerConnection(cfg);pend[from]=[];
  vpc.ontrack=e=>{$('v').srcObject=e.streams[0];$('lm').textContent='🔴 بث مباشر'};
  vpc.onicecandidate=e=>e.candidate&&s.emit('signal',{to:from,data:{ice:e.candidate}});
  await vpc.setRemoteDescription(data.sdp);await flush(vpc,from);
  await vpc.setLocalDescription(await vpc.createAnswer());s.emit('signal',{to:from,data:{sdp:vpc.localDescription}})}
 else if(data.sdp){const pc=pcs[from];if(pc){await pc.setRemoteDescription(data.sdp);await flush(pc,from)}}
 else if(data.ice){const pc=stream?pcs[from]:vpc;if(pc&&pc.remoteDescription)await pc.addIceCandidate(data.ice);else(pend[from]=pend[from]||[]).push(data.ice)}
}catch(e){console.warn(e)}});
async function flush(pc,id){for(const c of pend[id]||[])await pc.addIceCandidate(c);pend[id]=[]}
// chat
const addMsg=(n,t)=>{const d=document.createElement('div');d.className='m';const b=document.createElement('b');b.textContent=n+': ';d.append(b,document.createTextNode(t));$('chatbox').appendChild(d);$('chatbox').scrollTop=1e9};
s.on('chat',m=>addMsg(m.n,m.t));
$('cs').onclick=()=>{const v=$('ci').value.trim();if(v){s.emit('chat',v);$('ci').value=''}};
$('ci').onkeydown=e=>{if(e.key==='Enter')$('cs').click()};
// ---- admin
$('pb').onclick=()=>s.emit('admin',$('pw').value);
s.on('admin-ok',ok=>{$('ad').hidden=!ok;$('lg').hidden=ok;if(!ok)alert('كلمة السر خاطئة')});
let facing='user';
async function getMedia(){return navigator.mediaDevices.getUserMedia({video:{facingMode:facing},audio:true})}
$('bs').onclick=async()=>{try{if(!stream)stream=await getMedia();$('pv').srcObject=stream;s.emit('start')}catch(e){alert('تعذّر الوصول للكاميرا/المايك: '+e.message)}};
$('be').onclick=()=>{s.emit('stop');if(stream){stream.getTracks().forEach(t=>t.stop());stream=null}$('pv').srcObject=null;Object.values(pcs).forEach(p=>p.close());pcs={}};
$('bm').onclick=()=>{if(!stream)return;const t=stream.getAudioTracks()[0];t.enabled=!t.enabled;$('bm').textContent=t.enabled?'🎤 كتم':'🎤 تشغيل'};
$('bv').onclick=()=>{if(!stream)return;const t=stream.getVideoTracks()[0];t.enabled=!t.enabled;$('bv').textContent=t.enabled?'📷 إيقاف الكاميرا':'📷 تشغيل الكاميرا'};
$('bf').onclick=async()=>{if(!stream)return;try{facing=facing==='user'?'environment':'user';
 const n=await navigator.mediaDevices.getUserMedia({video:{facingMode:facing}});const nt=n.getVideoTracks()[0];
 stream.getVideoTracks()[0].stop();stream.removeTrack(stream.getVideoTracks()[0]);stream.addTrack(nt);
 Object.values(pcs).forEach(p=>{const sn=p.getSenders().find(x=>x.track&&x.track.kind==='video'||!x.track);sn&&sn.replaceTrack(nt)});$('pv').srcObject=stream}catch(e){alert(e.message)}};
s.on('stats',d=>{$('st1').textContent=d.online;$('st2').textContent=d.visits;$('st3').textContent=d.peak;
 $('ul').replaceChildren(...d.list.map(u=>{const x=document.createElement('div');x.className='m row';
  const t=document.createElement('span');t.style.flex='1';t.textContent=u.n+' — '+u.m+' د'+(u.mute?' 🔇':'');
  const a=document.createElement('button');a.textContent='كتم';a.onclick=()=>s.emit('mute',u.sid);
  const b=document.createElement('button');b.className='red';b.textContent='طرد';b.onclick=()=>s.emit('kick',u.sid);
  x.append(t,a,b);return x}));
 const mx=Math.max(1,...d.hist.map(z=>z.v));
 $('hs').replaceChildren(...d.hist.map(z=>{const c=document.createElement('div');c.style.cssText='flex:1;text-align:center;font-size:11px';
  c.innerHTML='<div style="background:var(--g);height:'+Math.round(z.v/mx*60)+'px;border-radius:4px"></div>';
  c.append(document.createTextNode(z.v),document.createElement('br'),document.createTextNode(z.d));return c}))});
s.on('ask',m=>{const d=document.createElement('div');d.className='m';d.textContent=m.n+': '+m.t;$('inbox').prepend(d)});
$('anb').onclick=()=>s.emit('announce',$('ani').value);
$('pnb').onclick=()=>s.emit('poll_new',{q:$('pqi').value,o:$('poi').value.split(/[,،]/)});
$('pcb').onclick=()=>s.emit('poll_close');
function showAnn(t){$('ann').hidden=!t;$('ann').textContent='📢 '+(t||'')}
s.on('ann',showAnn);
function renderPoll(p){$('pl').hidden=!p;if(!p)return;$('pq').textContent=p.q;
 $('po').replaceChildren(...p.o.map((o,i)=>{const b=document.createElement('button');b.style.cssText='display:block;width:100%;margin:5px 0';b.textContent=o+' — '+p.c[i];b.onclick=()=>s.emit('vote',i);return b}))}
s.on('poll',renderPoll);
$('qs').onclick=()=>{const v=$('qi').value.trim();if(v){s.emit('ask',v);$('qi').value='';alert('وصل سؤالك للمشرف')}};
// ---- Quran
let fs=26;const A='https://api.alquran.cloud/v1/';
(async()=>{try{const r=await(await fetch(A+'surah')).json();
 r.data.forEach(x=>{const o=document.createElement('option');o.value=x.number;o.textContent=x.number+'. '+x.name+' ('+x.numberOfAyahs+')';$('sur').appendChild(o)});
 const sv=localStorage.getItem('sur')||1;$('sur').value=sv;loadS(sv)}catch(e){$('ayat').textContent='تعذّر تحميل القرآن، تحقق من الاتصال.'}})();
async function loadS(n){$('ayat').textContent='جاري التحميل...';localStorage.setItem('sur',n);
 try{const r=await(await fetch(A+'surah/'+n+'/quran-uthmani')).json();const bs='بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ';
 $('ayat').replaceChildren(...r.data.ayahs.map(a=>{const sp=document.createElement('span');let t=a.text;
  if(a.numberInSurah===1&&n!=1&&t.startsWith(bs))t=t.slice(bs.length).trim();
  sp.append(document.createTextNode(t+' '));const m=document.createElement('span');m.className='n';m.textContent='﴿'+a.numberInSurah+'﴾ ';sp.appendChild(m);return sp}));
 $('au').src='https://cdn.islamic.network/quran/audio-surah/128/ar.alafasy/'+n+'.mp3'}catch(e){$('ayat').textContent='تعذّر تحميل السورة.'}}
$('sur').onchange=e=>loadS(e.target.value);
$('fp').onclick=()=>{fs=Math.min(60,fs+3);$('ayat').style.fontSize=fs+'px'};$('fm').onclick=()=>{fs=Math.max(16,fs-3);$('ayat').style.fontSize=fs+'px'};
// ---- Image tools
let z=1,r=0,fl=1,x=0,y=0;const im=$('im');
const up=()=>im.style.transform=`translate(calc(-50% + ${x}px),calc(-50% + ${y}px)) rotate(${r}deg) scale(${z*fl},${z})`;
$('fi').onchange=e=>{const f=e.target.files[0];if(f){im.src=URL.createObjectURL(f);z=1;r=0;fl=1;x=y=0;up()}};
$('zp').onclick=()=>{z=Math.min(8,z*1.25);up()};$('zm').onclick=()=>{z=Math.max(.2,z/1.25);up()};
$('rr').onclick=()=>{r+=90;up()};$('rl').onclick=()=>{r-=90;up()};$('fx').onclick=()=>{fl*=-1;up()};$('rs').onclick=()=>{z=1;r=0;fl=1;x=y=0;up()};
$('stage').onwheel=e=>{e.preventDefault();z=Math.min(8,Math.max(.2,z*(e.deltaY<0?1.1:.9)));up()};
let dr=null;$('stage').onpointerdown=e=>{dr=[e.clientX-x,e.clientY-y];$('stage').setPointerCapture(e.pointerId)};
$('stage').onpointermove=e=>{if(dr){x=e.clientX-dr[0];y=e.clientY-dr[1];up()}};$('stage').onpointerup=()=>dr=null;
// ---- AI
$('ab').onclick=async()=>{const q=$('aq').value.trim();if(!q)return;$('ab').disabled=true;
 const d=document.createElement('div');d.className='m';d.textContent='جاري التفكير...';$('aiout').prepend(d);
 try{const r=await fetch('/api/ai',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({q:$('am').value+q})});d.textContent=(await r.json()).a}
 catch(e){d.textContent='تعذّر الاتصال.'}$('ab').disabled=false};
// ---- tasbeeh / prayer / hijri
let tc=+localStorage.getItem('tc')||0;$('tc').textContent=tc;
$('tb').onclick=()=>{tc++;localStorage.setItem('tc',tc);$('tc').textContent=tc;navigator.vibrate&&navigator.vibrate(15)};
$('tr').onclick=()=>{tc=0;localStorage.setItem('tc',0);$('tc').textContent=0};
$('hj').textContent=new Intl.DateTimeFormat('ar-SA-u-ca-islamic-umalqura',{dateStyle:'full'}).format(new Date());
$('pt').onclick=()=>navigator.geolocation.getCurrentPosition(async p=>{try{
 const r=await(await fetch(`https://api.aladhan.com/v1/timings?latitude=${p.coords.latitude}&longitude=${p.coords.longitude}&method=4`)).json();
 const t=r.data.timings,n={Fajr:'الفجر',Dhuhr:'الظهر',Asr:'العصر',Maghrib:'المغرب',Isha:'العشاء'};
 $('pto').textContent=Object.keys(n).map(k=>n[k]+' '+t[k]).join(' • ');startCd(t,n)}catch(e){$('pto').textContent='تعذّر الجلب'}},()=>$('pto').textContent='لم يُسمح بالموقع');
let cdT=null;
function startCd(t,n){clearInterval(cdT);const ks=Object.keys(n);cdT=setInterval(()=>{const now=new Date();let best=null;
 for(const k of ks){const[h,m]=t[k].split(':').map(Number);const d=new Date(now);d.setHours(h,m,0,0);if(d>now&&(!best||d<best.d))best={k,d}}
 if(!best){const[h,m]=t.Fajr.split(':').map(Number);const d=new Date(now);d.setDate(d.getDate()+1);d.setHours(h,m,0,0);best={k:'Fajr',d}}
 const sec=Math.floor((best.d-now)/1000),p=v=>String(v).padStart(2,'0');
 $('cd').textContent='⏳ '+n[best.k]+' بعد '+p(Math.floor(sec/3600))+':'+p(Math.floor(sec%3600/60))+':'+p(sec%60)},1000)}
async function dayAyah(){try{const r=await(await fetch(A+'ayah/'+(1+Math.floor(Math.random()*6236))+'/quran-uthmani')).json();
 $('da').textContent=r.data.text+' ﴿'+r.data.numberInSurah+'﴾ — '+r.data.surah.name}catch(e){$('da').textContent='تعذّر التحميل'}}
$('dn').onclick=dayAyah;dayAyah();
</script></body></html>
"""

PW = os.getenv("ADMIN_PASSWORD", "change-me")
BASE = os.path.dirname(os.path.abspath(__file__))
db = sqlite3.connect(os.getenv("DB_PATH", os.path.join(BASE, "noor.db")), check_same_thread=False)
db.execute("create table if not exists days(d text primary key, v integer default 0)")
db.commit()

def hit():
    d = datetime.date.today().isoformat()
    db.execute("insert into days(d,v) values(?,1) on conflict(d) do update set v=v+1", (d,))
    db.commit()

def hist():
    rows = db.execute("select d,v from days order by d desc limit 7").fetchall()
    return [{"d": r[0][5:], "v": r[1]} for r in rows][::-1]

def total():
    return db.execute("select coalesce(sum(v),0) from days").fetchone()[0]

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
api = FastAPI()
users, admins, ai_last = {}, set(), {}
S = {"bc": None, "ann": "", "poll": None, "peak": 0, "loop": False}
SYS = ("أنت مساعد إسلامي يجيب بالعربية بإيجاز وأدب، ويعتمد على القرآن والسنة الصحيحة "
       "وأقوال أهل العلم المعتبرين. في الفتاوى الشخصية انصح بسؤال عالم موثوق.")

class Q(BaseModel):
    q: str

@api.post("/api/ai")
async def ai(b: Q, request: Request):
    q, ip, now = b.q.strip()[:1500], request.client.host, time.time()
    if not q:
        return {"a": "اكتب سؤالك أولاً."}
    if now - ai_last.get(ip, 0) < 3:
        return {"a": "انتظر ثوانٍ ثم أعد المحاولة."}
    ai_last[ip] = now
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        return {"a": "لم يُضبط ANTHROPIC_API_KEY في السيرفر."}
    try:
        async with httpx.AsyncClient(timeout=60) as c:
            r = await c.post("https://api.anthropic.com/v1/messages",
                headers={"x-api-key": key, "anthropic-version": "2023-06-01"},
                json={"model": os.getenv("MODEL", "claude-sonnet-5-5"), "max_tokens": 900,
                      "system": SYS, "messages": [{"role": "user", "content": q}]})
        d = r.json()
        return {"a": (d.get("content") or [{}])[0].get("text", "تعذر الرد الآن.")}
    except Exception:
        return {"a": "خطأ في الاتصال بالذكاء الاصطناعي."}

def pub():
    p = S["poll"]
    return {"q": p["q"], "o": p["o"], "c": p["c"]} if p else None

async def to_admins(ev, data):
    for a in list(admins):
        await sio.emit(ev, data, to=a)

def is_admin(sid):
    return sid in admins

async def loop():
    while True:
        await asyncio.sleep(2)
    admins:
            now = time.time()
            lst = [{"sid": k, "n": u["n"], "m": int((now - u["t"]) / 60), "mute": u["mute"]} for k, u in users.items()]
            await to_admins("stats", {"online": len(users), "visits": total(), "peak": S["peak"],
                                      "live": S["bc"] is not None, "list": lst, "hist": hist()})

@sio.event
async def connect(sid, environ, auth=None):
    n = "زائر_%d" % random.randint(100, 999)
    users[sid] = {"n": n, "t": time.time(), "mute": False, "last": 0}
    hit()
    S["peak"] = max(S["peak"], len(users))
    await sio.emit("hello", {"name": n, "live": S["bc"] is not None, "ann": S["ann"], "poll": pub()}, to=sid)
    await sio.emit("online", len(users))
    if not S["loop"]:
        S["loop"] = True
        asyncio.create_task(loop())

@sio.event
async def disconnect(sid, *a):
    users.pop(sid, None)
    admins.discard(sid)
    if S["bc"] == sid:
        S["bc"] = None
        await sio.emit("live", False)
    await sio.emit("online", len(users))

@sio.event
async def admin(sid, pw):
    ok = hmac.compare_digest(str(pw).encode(), PW.encode())
    if ok:
        admins.add(sid)
    await sio.emit("admin-ok", ok, to=sid)

@sio.event
async def start(sid):
    if is_admin(sid):
        S["bc"] = sid
        await sio.emit("live", True)

@sio.event
async def stop(sid):
    if S["bc"] == sid:
        S["bc"] = None
        await sio.emit("live", False)

@sio.event
async def watch(sid):
    if S["bc"] and S["bc"] != sid:
        await sio.emit("viewer", sid, to=S["bc"])

@sio.event
async def signal(sid, m):
    to = m.get("to") if isinstance(m, dict) else None
    if isinstance(to, str) and (to == S["bc"] or sid == S["bc"]):
        await sio.emit("signal", {"from": sid, "data": m.get("data")}, to=to)

@sio.event
async def chat(sid, t):
    u, t, now = users.get(sid), str(t or "").strip()[:300], time.time()
    if not u or not t or u["mute"] or now - u["last"] < 1:
        return
    u["last"] = now
    await sio.emit("chat", {"n": u["n"], "t": t})

@sio.event
async def ask(sid, t):
    u, t = users.get(sid), str(t or "").strip()[:300]
    if u and t:
        await to_admins("ask", {"n": u["n"], "t": t})

@sio.event
async def announce(sid, t):
    if is_admin(sid):
        S["ann"] = str(t or "").strip()[:300]
        await sio.emit("ann", S["ann"])

@sio.event
async def kick(sid, target):
    if is_admin(sid) and target in users and target not in admins:
        await sio.disconnect(target)

@sio.event
async def mute(sid, target):
    if is_admin(sid) and target in users:
        users[target]["mute"] = not users[target]["mute"]

@sio.event
async def poll_new(sid, d):
    if not is_admin(sid):
        return
    o = [str(x).strip()[:60] for x in (d.get("o") or []) if str(x).strip()][:6]
    q = str(d.get("q", "")).strip()[:150]
    if q and len(o) >= 2:
        S["poll"] = {"q": q, "o": o, "c": [0] * len(o), "voted": set()}
        await sio.emit("poll", pub())

@sio.event
async def poll_close(sid):
    if is_admin(sid):
        S["poll"] = None
        await sio.emit("poll", None)

@sio.event
async def vote(sid, i):
    p = S["poll"]
    if p and sid not in p["voted"] and isinstance(i, int) and 0 <= i < len(p["o"]):
        p["voted"].add(sid)
        p["c"][i] += 1
        await sio.emit("poll", pub())

@api.get("/", response_class=HTMLResponse)
async def home():
    return PAGE

app = socketio.ASGIApp(sio, api)
  
