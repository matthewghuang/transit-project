import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import { LatLngTuple } from "leaflet";
import { usePositions } from "../hooks/usePositions";
import { useStops } from "../hooks/useStops";
import { CSSProperties, useMemo, lazy, Suspense } from "react";
import { useFilterStore } from "../stores/filterStore";

const DelayDistributionChart = lazy(() => import("./DelayDistributionChart"));

const centerPosition: LatLngTuple = [49.246292, -123.116226];

const Map: React.FC<{ className?: string; style?: CSSProperties }> = ({
  className,
  style,
}) => {
  const { data } = usePositions();
  const { data: stops } = useStops();
  const { filters, selectedStopId, setSelectedStopId } = useFilterStore();

  const filteredData = useMemo(() => {
    let result = data;
    
    if (filters.length > 0) {
      result = result?.filter((pde) =>
        filters.includes(pde.trip.routeId)
      );
    }

    return result;
  }, [data, filters]);

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

      {/* Render Stops with delay data */}
      {stops?.map((stop) => (
        <Marker 
          key={stop.id} 
          position={[stop.latitude, stop.longitude] as LatLngTuple}
          eventHandlers={{
            click: () => setSelectedStopId(stop.id),
          }}
        >
          <Popup>
            <div style={{ padding: "4px", minWidth: "280px" }}>
              <strong style={{ fontSize: "1.1em", display: "block", marginBottom: "4px" }}>
                Stop: {stop.name}
              </strong>
              <div style={{ color: "#666", fontSize: "0.9em" }}>
                Stop ID: {stop.id}<br />
                Observations: {stop.observation_count}

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
          key={pos.id}
          position={[
            pos.position.latitude,
            pos.position.longitude,
          ]}
        >
          <Popup>
            <div style={{ padding: "4px" }}>
              <strong style={{ fontSize: "1.1em", display: "block", marginBottom: "4px" }}>
                Route: {pos.trip.routeId}
              </strong>
              <div style={{ color: "#666", fontSize: "0.9em" }}>
                Vehicle ID: {pos.id}<br />
                Trip: {pos.trip.tripId}<br />
                Last Update: {pos.timestamp ? new Date(pos.timestamp).toLocaleString() : "N/A"}
              </div>
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};


export { Map };
