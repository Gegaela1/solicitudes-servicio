/* La sesión vive únicamente en memoria. Nunca usar localStorage para el JWT. */
let token = null;
let me = null;
const view = document.querySelector('#view');
const nav = document.querySelector('#nav');
const feedback = document.querySelector('#feedback');
const pages = {};
function el(tag, text, attrs={}) {
  const n = document.createElement(tag);
  if (text !== null && text !== undefined) n.textContent = text;
  for (const [k,v] of Object.entries(attrs)) n.setAttribute(k,v);
  return n;
}
function message(text, error=false) { feedback.textContent=text; feedback.className=error?'error':'success'; }
async function api(path, method='GET', data) {
  const r = await fetch('/api/v1'+path,{method,headers:{'Content-Type':'application/json',...(token?{Authorization:'Bearer '+token}:{})},body:data===undefined?undefined:JSON.stringify(data),signal:AbortSignal.timeout(15000)});
  let d; try { d=await r.json(); } catch { throw new Error('Respuesta no disponible'); }
  if (!r.ok) {
    if(r.status===401 && token) { token=null; me=null; navigation(); loginPage(); }
    const text = Array.isArray(d.detail)?d.detail.map(e=>e.loc.slice(1).join('.')+': '+e.msg).join('\n'):d.detail;
    throw new Error(text || 'No se pudo completar la operación');
  }
  return d;
}
async function run(action) { try { await action(); } catch(e) { message(e.name==='TimeoutError'?'Tiempo de espera agotado. Intenta nuevamente.':e.message,true); } }
function button(text,action,parent=view) { const b=el('button',text,{type:'button'}); b.onclick=()=>run(async()=>{ b.disabled=true; try { await action(); } finally {b.disabled=false;} }); parent.append(b); return b; }
function form(title,fields,submit,caption='Guardar') {
  const f=el('form'); f.append(el('h2',title));
  for(const field of fields) {
    const label=el('label',field.label); const id='f-'+field.name;
    label.htmlFor=id;
    const input=el(field.type==='textarea'?'textarea':field.options?'select':'input',null,{id,name:field.name});
    if(field.options) for(const [value,text] of field.options) {const o=el('option',text,{value}); input.append(o);}
    else if(field.type!=='textarea') input.type=field.type||'text';
    if(field.required!==false) input.required=true;
    if(field.min) input.minLength=field.min;
    if(field.max) input.maxLength=field.max;
    if(field.value!==undefined && field.value!==null) input.value=field.value;
    label.append(input,el('span','',{class:'field-error',id:id+'-error'}));
    input.setAttribute('aria-describedby',id+'-error');
    f.append(label);
  }
  const b=el('button',caption,{type:'submit'}); f.append(b);
  f.onsubmit=e=>{ e.preventDefault(); run(async()=>{ b.disabled=true; message('Procesando…'); try { await submit(Object.fromEntries(new FormData(f))); } finally {b.disabled=false;} }); };
  view.append(f); return f;
}
function clear(title) {view.replaceChildren(); if(title) view.append(el('h1',title)); message('');}
function has(role) {return me?.roles.includes(role);}
function navigation() {
  nav.replaceChildren();
  if(!me) return;
  for(const [name,page] of Object.entries(pages)) if(page.allow()) button(name,page.show,nav);
  button('Contraseña',passwordPage,nav);
  button('Salir',()=>{token=null;me=null;navigation();loginPage();},nav);
}
function loginPage() {
  clear('Acceso');
  form('Iniciar sesión',[{name:'correo',label:'Correo',type:'email'},{name:'contrasena',label:'Contraseña',type:'password',max:128}],async d=>{
    const r=await api('/auth/token','POST',d); token=r.access_token; me=await api('/usuarios/me'); navigation(); clear('Bienvenida, '+me.nombre); message('Sesión iniciada.');
  },'Entrar');
  if(typeof registerPage==='function') button('Crear cuenta solicitante',registerPage);
}
function passwordPage(){clear('Seguridad'); form('Cambiar contraseña',[{name:'actual',label:'Contraseña actual',type:'password'},{name:'nueva',label:'Nueva contraseña (12–128)',type:'password',min:12,max:128}],async d=>{await api('/usuarios/me/contrasena','POST',d);token=null;me=null;navigation();loginPage();message('Contraseña cambiada. Inicia sesión nuevamente.');});}
loginPage();
