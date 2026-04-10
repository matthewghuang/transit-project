import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { LatLngTuple } from "leaflet";
import { usePositions } from "../hooks/usePositions";
import { CSSProperties } from "react";
import { useFilterStore } from "../stores/filterStore";

const position: LatLngTuple = [49.246292, -123.116226];

const Map: React.FC<{ className?: string; style?: CSSProperties }> = ({
  className,
  style,
}) => {
  const { data } = usePositions();
  const { filters } = useFilterStore();

  const filteredData = data?.filter((pde) =>
    filters.includes(pde.vehicle.trip.route_name)
  );

  return (
    <MapContainer
      center={position}
      zoom={13}
      scrollWheelZoom={true}
      className={className}
      style={style}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {filteredData?.map((pos) => (
        <Marker
          key={pos._id}
          position={[
            pos.vehicle.position.latitude,
            pos.vehicle.position.longitude,
          ]}
        >
          <Popup>
            <div style={{ padding: "4px" }}>
              <strong style={{ fontSize: "1.1em", display: "block", marginBottom: "4px" }}>
                Route: {pos.vehicle.trip.route_name}
              </strong>
              <div style={{ color: "#666", fontSize: "0.9em" }}>
                Vehicle ID: {pos.vehicle.vehicle.id}<br />
                {pos.vehicle.delay_seconds !== undefined && (
                  <div style={{
                    color: pos.vehicle.delay_seconds > 0 ? "#d32f2f" : pos.vehicle.delay_seconds < 0 ? "#2e7d32" : "#666",
                    fontWeight: "bold",
                    marginTop: "2px"
                  }}>
                    {pos.vehicle.delay_seconds > 0 
                      ? `${Math.round(pos.vehicle.delay_seconds / 60)} minutes late` 
                      : pos.vehicle.delay_seconds < 0 
                        ? `${Math.round(Math.abs(pos.vehicle.delay_seconds) / 60)} minutes early` 
                        : "On time"}
                  </div>
                )}
                Last Update: {pos.vehicle.timestamp? new Date(Number(pos.vehicle.timestamp) * 1000).toLocaleString() : "N/A"}
              </div>
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};

export { Map };
