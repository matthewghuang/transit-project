import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { LatLngTuple } from "leaflet";
import { usePositions } from "../hooks/usePositions";
import { CSSProperties, useMemo, lazy, Suspense } from "react";
import { useFilterStore } from "../stores/filterStore";

const DelayDistributionChart = lazy(() => import("./DelayDistributionChart"));

const centerPosition: LatLngTuple = [49.246292, -123.116226];

// Mock stops for Phase 1 gap closure (would ideally come from API)
const MOCK_STOPS = [
  { id: "50001", name: "Main St at E 10th Ave", position: [49.2624, -123.1012] as LatLngTuple },
  { id: "50002", name: "Granville St at W 10th Ave", position: [49.2630, -123.1388] as LatLngTuple },
  { id: "50003", name: "Commercial Dr at E 1st Ave", position: [49.2705, -123.0696] as LatLngTuple },
];

const Map: React.FC<{ className?: string; style?: CSSProperties }> = ({
  className,
  style,
}) => {
  const { data } = usePositions();
  const { filters, selectedStopId, setSelectedStopId } = useFilterStore();

  const filteredData = useMemo(() => {
    let result = data;
    
    if (filters.length > 0) {
      result = result?.filter((pde) =>
        filters.includes(pde.vehicle.trip.route_name)
      );
    }

    if (selectedStopId) {
      // Highlight vehicles approaching the selected stop
      // This logic will be refined as more data becomes available
    }

    return result;
  }, [data, filters, selectedStopId]);

  return (
    <MapContainer
      center={centerPosition}
      zoom={13}
      scrollWheelZoom={true}
      className={className}
      style={style}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {/* Render Stops */}
      {MOCK_STOPS.map((stop) => (
        <Marker 
          key={stop.id} 
          position={stop.position}
          eventHandlers={{
            click: () => setSelectedStopId(stop.id),
          }}
        >
          <Popup>
            <div style={{ padding: "4px" }}>
              <strong style={{ fontSize: "1.1em", display: "block", marginBottom: "4px" }}>
                Stop: {stop.name}
              </strong>
              <div style={{ color: "#666", fontSize: "0.9em" }}>
                Stop ID: {stop.id}<br />
                
                {/* Real-time Arrival Info for Selected Stop */}
                <div style={{ marginTop: "8px", borderTop: "1px solid #eee", paddingTop: "8px" }}>
                  <strong>Next Arrivals:</strong>
                  {data?.filter(pos => pos.vehicle.next_stop_id === stop.id).length === 0 ? (
                    <div style={{ marginTop: "4px", fontStyle: "italic" }}>No vehicles approaching</div>
                  ) : (
                    data?.filter(pos => pos.vehicle.next_stop_id === stop.id).map(pos => (
                      <div key={pos._id} style={{ marginTop: "4px" }}>
                        <span style={{ fontWeight: "bold" }}>{pos.vehicle.trip.route_name}</span>: 
                        <span style={{ 
                          marginLeft: "4px",
                          color: (pos.vehicle.delay_seconds || 0) > 60 ? "#d32f2f" : "#2e7d32"
                        }}>
                          {(pos.vehicle.delay_seconds || 0) > 60 
                            ? `${Math.round(pos.vehicle.delay_seconds! / 60)}m delay` 
                            : "On time"}
                        </span>
                      </div>
                    ))
                  )}
                </div>

                <Suspense fallback={<div>Loading chart...</div>}>
                  <DelayDistributionChart stopId={stop.id} />
                </Suspense>
              </div>
            </div>
          </Popup>
        </Marker>
      ))}

      {/* Render Vehicles */}
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
