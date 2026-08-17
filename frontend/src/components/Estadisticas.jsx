export default function Estadisticas({stats}){if(!stats)return null;return <section className="stats">
 <div className="stat"><span>Total</span><b>{stats.total_incidentes}</b></div><div className="stat"><span>Promedio diario</span><b>{stats.promedio_diario}</b></div><div className="stat"><span>Delito más frecuente</span><b>{stats.delito_mas_frecuente||"N/D"}</b></div><div className="stat"><span>Alcaldía con más registros</span><b>{stats.alcaldia_mayor_incidencia||"N/D"}</b></div>
 <div className="panel list"><h3>Por delito</h3>{stats.por_delito.map(x=><div key={x.delito}><span>{x.delito}</span><b>{x.total}</b></div>)}</div><div className="panel list"><h3>Por alcaldía</h3>{stats.por_alcaldia.map(x=><div key={x.alcaldia}><span>{x.alcaldia}</span><b>{x.total}</b></div>)}</div>
 </section>}
