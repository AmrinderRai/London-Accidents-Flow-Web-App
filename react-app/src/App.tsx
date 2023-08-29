import "./App.css";
import "leaflet/dist/leaflet.css"
import { MapContainer, TileLayer } from 'react-leaflet'
import ControlPanel from './ControlPanel.tsx'



function App() {

  return (
    <div>
    <MapContainer center={[51.505, -0.09]} zoom={13}>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="http://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png'.png"
      />
    </MapContainer>
    <ControlPanel /> 
    </div>
    // Sidebar component here??? 
  )
}

export default App
