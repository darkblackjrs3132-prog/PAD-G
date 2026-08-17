export default function Filtros({filtros,setFiltros,alcaldias,delitos,onAplicar,onLimpiar,loading}){
  const set=(k,v)=>setFiltros(p=>({...p,[k]:v}));
  return <section className="panel filters">
    <div><label>Fecha inicial</label><input type="date" value={filtros.fecha_inicio} onChange={e=>set("fecha_inicio",e.target.value)}/></div>
    <div><label>Fecha final</label><input type="date" value={filtros.fecha_fin} onChange={e=>set("fecha_fin",e.target.value)}/></div>
    <div><label>Tipo de delito</label><select value={filtros.delito} onChange={e=>set("delito",e.target.value)}><option value="">Todos</option>{delitos.map(x=><option key={x}>{x}</option>)}</select></div>
    <div><label>Alcaldía</label><select value={filtros.alcaldia} onChange={e=>set("alcaldia",e.target.value)}><option value="">Todas</option>{alcaldias.map(x=><option key={x}>{x}</option>)}</select></div>
    <div className="actions"><button onClick={onAplicar} disabled={loading}>{loading?"Consultando...":"Aplicar filtros"}</button><button className="secondary" onClick={onLimpiar}>Limpiar</button></div>
  </section>
}
