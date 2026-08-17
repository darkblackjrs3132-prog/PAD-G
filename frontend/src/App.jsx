import {useEffect,useState} from "react";
import {api,buildParams} from "./api";
import Filtros from "./components/Filtros";
import MapaDelitos from "./components/MapaDelitos";
import Estadisticas from "./components/Estadisticas";
import DetalleIncidente from "./components/DetalleIncidente";

const VACIOS={fecha_inicio:"",fecha_fin:"",delito:"",alcaldia:""};

export default function App(){
 const [filtros,setFiltros]=useState(VACIOS),[alcaldias,setAlcaldias]=useState([]),[delitos,setDelitos]=useState([]);
 const [geojson,setGeojson]=useState({type:"FeatureCollection",features:[]}),[heatPoints,setHeatPoints]=useState([]),[stats,setStats]=useState(null);
 const [seleccionado,setSeleccionado]=useState(null),[modoHeatmap,setModoHeatmap]=useState(false),[loading,setLoading]=useState(false),[error,setError]=useState("");

 async function cargar(f=filtros){
   setLoading(true);setError("");setSeleccionado(null);const params=buildParams(f);
   try{
     const [inc,est,heat]=await Promise.all([api.get("/incidentes",{params}),api.get("/estadisticas",{params}),api.get("/heatmap",{params})]);
     setGeojson(inc.data);setStats(est.data);setHeatPoints(heat.data);
   }catch(e){setError(e?.response?.data?.detail||"No fue posible consultar PAD-G.");}
   finally{setLoading(false);}
 }

 useEffect(()=>{
   Promise.all([api.get("/alcaldias"),api.get("/tipos-delito")]).then(([a,d])=>{setAlcaldias(a.data);setDelitos(d.data)}).catch(()=>setError("No se pudieron cargar los catálogos."));
   cargar(VACIOS);
 },[]);

 function limpiar(){setFiltros(VACIOS);setModoHeatmap(false);cargar(VACIOS)}

 return <main className="shell">
   <header className="hero"><div><p className="eyebrow">Plataforma de Análisis Delictivo Geoespacial</p><h1>PAD-G</h1><p>Visualización interactiva de incidencia delictiva en la Ciudad de México.</p></div><button className={modoHeatmap?"mode":"secondary"} onClick={()=>setModoHeatmap(v=>!v)}>{modoHeatmap?"Ver marcadores":"Ver mapa de calor"}</button></header>
   <Filtros filtros={filtros} setFiltros={setFiltros} alcaldias={alcaldias} delitos={delitos} onAplicar={()=>cargar(filtros)} onLimpiar={limpiar} loading={loading}/>
   {error&&<div className="error">{String(error)}</div>}
   <section className="content"><MapaDelitos geojson={geojson} heatPoints={heatPoints} modoHeatmap={modoHeatmap} setSeleccionado={setSeleccionado}/><DetalleIncidente incidente={seleccionado} onClose={()=>setSeleccionado(null)}/></section>
   {!loading&&geojson.features.length===0&&<div className="panel empty">No se encontraron delitos con los parámetros seleccionados.</div>}
   <Estadisticas stats={stats}/>
 </main>
}
