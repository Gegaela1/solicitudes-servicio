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
function identityFields(data={}) {return [{name:'nombre',label:'Nombre',min:2,max:120,value:data.nombre},{name:'documento',label:'Documento',min:3,max:30,value:data.documento},{name:'correo',label:'Correo',type:'email',max:254,value:data.correo}];}
function registerPage(){clear('Cuenta solicitante');form('Registro',[...identityFields(),{name:'contrasena',label:'Contraseña (12–128 caracteres)',type:'password',min:12,max:128}],async d=>{await api('/auth/registro','POST',d);loginPage();message('Cuenta creada. Ya puedes ingresar.');},'Crear cuenta');button('Volver al acceso',loginPage);}
loginPage();
async function staffPage(page=1){clear('Administración de personal');message('Cargando…');const data=await api('/usuarios?page='+page);message('');if(!data.items.length)view.append(el('p','Sin cuentas.'));for(const u of data.items){const row=el('article');row.append(el('h2',u.nombre),el('p',u.correo+' · '+u.roles.join(', ')+' · '+(u.activo?'Activa':'Inactiva')));button('Editar permisos',()=>staffEdit(u),row);view.append(row);}pagination(data,staffPage);form('Crear cuenta',[...identityFields(),{name:'contrasena',label:'Contraseña inicial',type:'password',min:12,max:128},{name:'roles',label:'Roles (separados por coma)',value:'atencion'}],async d=>{d.roles=d.roles.split(',').map(x=>x.trim());await api('/usuarios','POST',d);await staffPage();message('Cuenta creada. Comunica la contraseña por un canal privado.');});}
function staffEdit(u){clear('Permisos de '+u.nombre);form('Actualizar',[{name:'roles',label:'Roles separados por coma',value:u.roles.join(',')},{name:'activo',label:'Cuenta',options:[['true','Activa'],['false','Inactiva']],value:String(u.activo)}],async d=>{d.roles=d.roles.split(',').map(x=>x.trim());d.activo=d.activo==='true';await api('/usuarios/'+u.id+'/roles','PUT',d);if(u.id===me.id){token=null;me=null;navigation();loginPage();message('Permisos actualizados. Inicia sesión.');}else{await staffPage();message('Cuenta actualizada.');}});}
function pagination(data,load){const p=el('p','Página '+data.page+' · '+data.total+' resultados');view.append(p);if(data.page>1)button('Anterior',()=>load(data.page-1),p);if(data.page*data.size<data.total)button('Siguiente',()=>load(data.page+1),p);}
pages['Personal']={allow:()=>has('coordinacion'),show:staffPage};
async function newCasePage(){clear('Nueva solicitud');const services=await api('/servicios');form('Datos presentados',[...identityFields(me),{name:'servicio_id',label:'Servicio',options:services.filter(s=>s.activo).map(s=>[s.id,s.nombre])},{name:'asunto',label:'Asunto',min:5,max:150},{name:'descripcion',label:'Descripción',type:'textarea',min:20,max:5000}],async d=>{d.servicio_id=Number(d.servicio_id);const c=await api('/solicitudes','POST',d);clear('Solicitud registrada');view.append(el('h2',c.radicado),el('p',c.asunto),el('p','Estado: '+c.estado));message('Solicitud guardada. Conserva tu radicado.');});}
pages['Nueva solicitud']={allow:()=>has('solicitante'),show:newCasePage};
const detailWidgets=[];
const stateNames=['registrada','en_revision','pendiente_informacion','aceptada','asignada','en_atencion','finalizada','rechazada','cancelada','cerrada_duplicidad'];
let listFilters={};
function colombia(value){return value?new Intl.DateTimeFormat('es-CO',{dateStyle:'medium',timeStyle:'short',timeZone:'America/Bogota'}).format(new Date(value)):'Sin definir';}
function filterFields(){return [{name:'estado',label:'Estado',options:[['','Todos'],...stateNames.map(x=>[x,x])],required:false},{name:'responsable_id',label:'ID responsable',type:'number',required:false},{name:'servicio_id',label:'ID servicio',type:'number',required:false},{name:'prioridad',label:'Prioridad',options:[['','Todas'],['baja','Baja'],['normal','Normal'],['alta','Alta']],required:false},{name:'desde',label:'Registro desde (Colombia)',type:'date',required:false},{name:'hasta',label:'Registro hasta (inclusive)',type:'date',required:false},{name:'radicado',label:'Radicado',required:false}].map(f=>({...f,value:listFilters[f.name]||''}));}
function queryFilters(data){return Object.fromEntries(Object.entries(data).filter(([k,v])=>v!==''&&v!==null));}
async function casesPage(page=1){clear(has('atencion')||has('coordinacion')?'Bandeja de solicitudes':'Mis solicitudes');form('Filtros',filterFields(),async d=>{listFilters=queryFilters(d);await casesPage();},'Filtrar');message('Cargando…');const data=await api('/solicitudes?'+new URLSearchParams({...listFilters,page}));message('');caseTable(data.items);pagination(data,casesPage);}
function caseTable(items){if(!items.length){view.append(el('p','No hay solicitudes con estos filtros.'));return;}const table=el('table');const tr=el('tr');for(const t of ['Radicado','Asunto','Estado','Prioridad','Acción'])tr.append(el('th',t,{scope:'col'}));table.append(tr);for(const c of items){const row=el('tr');for(const t of [c.radicado,c.asunto,c.estado,c.prioridad])row.append(el('td',t));const td=el('td');button('Ver detalle',()=>caseDetail(c.id),td);row.append(td);table.append(row);}view.append(table);}
async function caseDetail(id){clear('Detalle de solicitud');message('Cargando…');const c=await api('/solicitudes/'+id);message('');view.append(el('h2',c.radicado));for(const [label,value] of [['Asunto',c.asunto],['Estado',c.estado],['Nombre presentado',c.nombre],['Documento',c.documento],['Correo presentado',c.correo],['Servicio (ID)',c.servicio_id],['Responsable (ID)',c.responsable_id||'Sin asignar'],['Descripción',c.descripcion],['Prioridad',c.prioridad],['Registro',colombia(c.creada_en)],['Vencimiento',colombia(c.vencimiento)],['Vencida',c.vencida?'Sí':'No'],['Duración total (horas)',c.duracion_total_horas.toFixed(2)],['Duración ciclo vigente (horas)',c.duracion_ciclo_horas?.toFixed(2)]]){const p=el('p',null,{class:'text'});p.append(el('strong',label+': '),document.createTextNode(String(value??'Sin datos')));view.append(p);}for(const widget of detailWidgets)await widget(c);button('Volver a la bandeja',casesPage);}
pages['Solicitudes']={allow:()=>true,show:casesPage};
async function historyBlock(c,page=1){const data=await api('/solicitudes/'+c.id+'/historial?page='+page);view.append(el('h2','Historial'));for(const i of data.items){const a=el('article');a.append(el('strong',colombia(i.creada_en)+' · '+i.tipo+(i.interna?' · Interna':'')),el('p',i.detalle,{class:'text'}));if(i.rectifica_id)a.append(el('small','Rectifica intervención '+i.rectifica_id));view.append(a);}if(!data.items.length)view.append(el('p','Sin intervenciones visibles.'));if(data.page*data.size<data.total)button('Más historial',()=>historyBlock(c,page+1));}
detailWidgets.push(async c=>{await historyBlock(c);if((has('coordinacion')||((has('atencion'))&&c.responsable_id===me.id))&&['registrada','en_revision','pendiente_informacion','aceptada','asignada','en_atencion'].includes(c.estado)){form('Añadir intervención',[{name:'detalle',label:'Detalle',type:'textarea',max:5000},{name:'interna',label:'Visibilidad',options:[['true','Interna'],['false','Visible al solicitante']]},{name:'rectifica_id',label:'ID de nota a rectificar (opcional)',type:'number',required:false}],async d=>{d.interna=d.interna==='true';d.rectifica_id=d.rectifica_id?Number(d.rectifica_id):null;await api('/solicitudes/'+c.id+'/intervenciones','POST',{...d,version:c.version});await caseDetail(c.id);message('Intervención registrada.');});}});
async function caseAction(c,action,data={}){await api('/solicitudes/'+c.id+'/'+action,'POST',{version:c.version,...data});await caseDetail(c.id);message('Acción registrada.');}
detailWidgets.push(async c=>{if(has('atencion')||has('coordinacion')){if(c.estado==='registrada')button('Iniciar revisión',()=>caseAction(c,'revision'));if(c.estado==='en_revision'){button('Aceptar solicitud',()=>caseAction(c,'aceptacion'));form('Rechazar por improcedencia',[{name:'motivo',label:'Motivo del rechazo',type:'textarea',min:10,max:2000}],async d=>{if(confirm('¿Rechazar esta solicitud?'))await caseAction(c,'rechazo',d);},'Rechazar');}}});
detailWidgets.push(async c=>{if(has('coordinacion')&&(['aceptada'].includes(c.estado)||(c.responsable_id&&['registrada','en_revision','pendiente_informacion','asignada','en_atencion'].includes(c.estado)))){const data=await api('/usuarios?size=100');form(c.responsable_id?'Reasignar responsable':'Asignar responsable',[{name:'responsable_id',label:'Responsable activo',options:data.items.filter(u=>u.activo&&u.roles.some(r=>['atencion','coordinacion'].includes(r))).map(u=>[u.id,u.nombre+' ('+u.correo+')'])},{name:'motivo',label:'Motivo',min:10,max:2000,type:'textarea'}],async d=>{d.responsable_id=Number(d.responsable_id);await api('/solicitudes/'+c.id+'/responsable','PUT',{...d,version:c.version});await caseDetail(c.id);message('Responsable actualizado.');});}});
detailWidgets.push(async c=>{if((has('atencion')||has('coordinacion'))&&c.responsable_id===me.id){if(c.estado==='asignada')button('Iniciar atención',()=>caseAction(c,'inicio-atencion'));if(c.estado==='en_atencion')form('Finalizar atención',[{name:'respuesta',label:'Respuesta al solicitante',type:'textarea',min:10,max:5000},{name:'resultado',label:'Resultado de lo realizado',type:'textarea',min:5,max:2000}],async d=>{if(confirm('¿Finalizar este caso con la respuesta indicada?'))await caseAction(c,'finalizacion',d);},'Finalizar');}});
detailWidgets.push(async c=>{if(c.estado==='finalizada'){const r=await api('/solicitudes/'+c.id+'/resultado');view.append(el('h2','Respuesta y finalización'),el('p',r.respuesta,{class:'text'}),el('p','Resultado: '+r.resultado,{class:'text'}),el('p','Finalizada: '+colombia(r.finalizada_en)));}});
detailWidgets.push(async c=>{if((c.estado==='en_revision'&&(has('atencion')||has('coordinacion')))||(c.estado==='en_atencion'&&c.responsable_id===me.id&&(has('atencion')||has('coordinacion')))){form('Pedir información adicional',[{name:'pregunta',label:'Pregunta (sin adjuntos)',type:'textarea',min:10,max:2000}],d=>caseAction(c,'requerimientos',d),'Solicitar información');}const data=await api('/solicitudes/'+c.id+'/requerimientos');if(data.items.length)view.append(el('h2','Requerimientos de información'));for(const r of data.items){view.append(el('p',r.pregunta,{class:'text'}),el('p',r.respuesta||'Sin respuesta',{class:'text'}));if(!r.cerrado_en&&c.solicitante_id===me.id&&c.estado==='pendiente_informacion')form('Responder requerimiento',[{name:'respuesta',label:'Respuesta (solo texto)',type:'textarea',min:1,max:5000}],async d=>{await api('/requerimientos/'+r.id+'/respuesta','POST',{...d,version:c.version});await caseDetail(c.id);message('Información enviada.');},'Enviar información');}});
detailWidgets.push(async c=>{const personal=c.solicitante_id===me.id&&c.estado==='registrada';const admin=has('coordinacion')&&['registrada','en_revision','pendiente_informacion','aceptada','asignada','en_atencion'].includes(c.estado);if(personal||admin)button('Corregir datos',async()=>{clear('Corregir solicitud '+c.radicado);const services=await api('/servicios');const fields=[...identityFields(c),{name:'servicio_id',label:'Servicio',options:services.filter(s=>s.activo).map(s=>[s.id,s.nombre]),value:c.servicio_id},{name:'asunto',label:'Asunto',min:5,max:150,value:c.asunto},{name:'descripcion',label:'Descripción',type:'textarea',min:20,max:5000,value:c.descripcion}];if(!personal)fields.push({name:'motivo',label:'Motivo administrativo',type:'textarea',min:10,max:2000});form('Datos presentados',fields,async d=>{d.servicio_id=Number(d.servicio_id);await api('/solicitudes/'+c.id,'PATCH',{...d,version:c.version});await caseDetail(c.id);message('Corrección registrada.');});});});
detailWidgets.push(async c=>{if(c.solicitante_id===me.id&&c.estado==='registrada')form('Cancelar solicitud',[{name:'motivo',label:'Motivo de cancelación',type:'textarea',min:10,max:2000}],async d=>{if(confirm('¿Cancelar esta solicitud? Esta versión no permite reabrir solicitudes canceladas.'))await caseAction(c,'cancelacion',d);},'Cancelar solicitud');});
detailWidgets.push(async c=>{const data=await api('/solicitudes/'+c.id+'/reaperturas');const pending=data.items.find(r=>r.estado==='pendiente');if(c.estado==='finalizada'&&c.solicitante_id===me.id&&!pending)form('Solicitar reapertura',[{name:'motivo',label:'Motivo',type:'textarea',min:10,max:2000}],d=>caseAction(c,'reaperturas',d),'Solicitar reapertura');for(const r of data.items){view.append(el('h2','Reapertura: '+r.estado),el('p',r.motivo,{class:'text'}));if(r.motivo_decision)view.append(el('p','Decisión: '+r.motivo_decision,{class:'text'}));if(has('coordinacion')&&r.estado==='pendiente')form('Resolver petición',[{name:'aprobar',label:'Decisión',options:[['true','Aprobar'],['false','Rechazar']]},{name:'motivo',label:'Motivo de decisión',type:'textarea',min:10,max:2000}],async d=>{d.aprobar=d.aprobar==='true';if(confirm('¿Registrar esta decisión de reapertura?')){await api('/reaperturas/'+r.id+'/decision','POST',{...d,version:c.version});await caseDetail(c.id);message('Decisión registrada.');}},'Resolver');}});
detailWidgets.push(async c=>{if(has('coordinacion')&&['registrada','en_revision','pendiente_informacion','aceptada','asignada','en_atencion'].includes(c.estado))form('Cerrar por duplicidad',[{name:'original_id',label:'ID del caso original del mismo propietario',type:'number'},{name:'motivo',label:'Justificación',type:'textarea',min:10,max:2000}],async d=>{d.original_id=Number(d.original_id);if(confirm('¿Cerrar como duplicado y cerrar requerimientos pendientes?'))await caseAction(c,'duplicidad',d);},'Cerrar duplicado');});
async function servicesPage(){clear('Prioridades y plazos');view.append(el('p','Política de demostración: horas calendario; las esperas no pausan el plazo. Los cambios solo afectan nuevas solicitudes.'));const services=await api('/servicios');for(const s of services){form(s.nombre,[{name:'prioridad',label:'Prioridad predeterminada',options:[['baja','Baja'],['normal','Normal'],['alta','Alta']],value:s.prioridad},{name:'plazo_horas',label:'Plazo en horas (1–8760; vacío = sin definir)',type:'number',required:false,value:s.plazo_horas}],async d=>{d.plazo_horas=d.plazo_horas===''?null:Number(d.plazo_horas);await api('/servicios/'+s.id+'/configuracion','PATCH',d);message('Configuración guardada para nuevas solicitudes.');});}}
pages['Servicios']={allow:()=>has('coordinacion'),show:servicesPage};
async function reportPage(page=1){clear('Consolidado de coordinación');form('Filtros combinables',filterFields(),async d=>{listFilters=queryFilters(d);await reportPage();},'Consultar');message('Cargando…');const data=await api('/reportes/solicitudes?'+new URLSearchParams({...listFilters,page}));message('');view.append(el('h2','Resumen con los mismos filtros del listado'));for(const [label,value] of [['Total',data.total],['Pendientes activos',data.pendientes_activos],['Vencidas',data.vencidas],['Resolución promedio por ciclo finalizado (horas)',data.promedio_resolucion_horas===null?'Sin datos':data.promedio_resolucion_horas.toFixed(2)]])view.append(el('p',label+': '+value));for(const [group,counts]of Object.entries(data.conteos)){view.append(el('h3','Conteos por '+group));if(!Object.keys(counts).length)view.append(el('p','Sin datos'));for(const [name,count]of Object.entries(counts))view.append(el('p',name+': '+count));}caseTable(data.items);pagination(data,reportPage);}
pages['Consolidado']={allow:()=>has('coordinacion'),show:reportPage};
