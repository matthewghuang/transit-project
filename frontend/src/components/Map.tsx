import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import { LatLngTuple } from "leaflet";
import { usePositions } from "../hooks/usePositions";
import { CSSProperties } from "react";

const position: LatLngTuple = [49.246292, -123.116226];

let Map: React.FC<{ className?: string; style?: CSSProperties }> = ({
  className,
  style,
}) => {
  const { data } = usePositions();

  console.log(data);

  return (
    <MapContainer
      center={position}
      zoom={13}
      scrollWheelZoom={false}
      className={className}
      style={style}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {data?.map((pos) => (
        <>
          <Marker
            key={pos._id}
            position={[
              pos.vehicle.position.latitude,
              pos.vehicle.position.longitude,
            ]}
          >
            <Popup key={pos._id}>
              {pos.vehicle.trip.route_name}
              Last Updated: {pos.timestamp}
            </Popup>
          </Marker>
        </>
      ))}
    </MapContainer>
  );
};

export { Map };
