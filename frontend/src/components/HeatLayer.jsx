import {useEffect} from "react";
import {useMap} from "react-leaflet";
import L from "leaflet";
import "leaflet.heat";
export default function HeatLayer({points}){
  const map=useMap();
  useEffect(()=>{
    if(!points?.length) return;
    const layer=L.heatLayer(points.map(p=>[p.lat,p.lng,p.intensity||1]),{radius:28,blur:20,maxZoom:17}).addTo(map);
    return()=>map.removeLayer(layer);
  },[map,points]);
  return null;
}
