import {useEffect} from "react";
import {MapContainer,TileLayer,CircleMarker,Popup,useMap} from "react-leaflet";
import HeatLayer from "./HeatLayer";
function Ajustar({geojson}){const map=useMap();useEffect(()=>{const c=geojson?.features?.map(f=>[f.geometry.coordinates[1],f.geometry.coordinates[0]]);if(c?.length)map.fitBounds(c,{padding:[30,30],maxZoom:14});},[geojson,map]);return null;}
export default function MapaDelitos({geojson,heatPoints,modoHeatmap,setSeleccionado}){
 return <div className="map-card"><MapContainer center={[19.4326,-99.1332]} zoom={11} className="map" scrollWheelZoom>
  <TileLayer attribution="&copy; OpenStreetMap contributors" url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/><Ajustar geojson={geojson}/>
  {modoHeatmap?<HeatLayer points={heatPoints}/>:geojson.features.map(f=>{const [lng,lat]=f.geometry.coordinates,p=f.properties;return <CircleMarker key={p.id} center={[lat,lng]} radius={7} pathOptions={{weight:2,fillOpacity:.75}} eventHandlers={{click:()=>setSeleccionado({...p,lat,lng})}}><Popup><b>{p.delito}</b><br/>{p.alcaldia}<br/>{p.colonia}<br/>{p.fecha}</Popup></CircleMarker>})}
 </MapContainer></div>
}
