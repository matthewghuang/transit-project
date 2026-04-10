import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";
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
    if (!data || filters.length === 0) return [];
    
    return data.filter((pde) =>
      filters.includes(pde.trip.routeName)
    );
  }, [data, filters]);

  const filteredStops = useMemo(() => {
    if (!stops || filters.length === 0) return [];
    
    return stops.filter((stop) => 
      stop.routes.some((route) => filters.includes(route))
    );
  }, [stops, filters]);

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

      {/* Render Vehicles as small translucent blue dots */}
      {filteredData?.map((pos) => (
        <CircleMarker
          key={pos.id}
          center={[pos.position.latitude, pos.position.longitude]}
          radius={5}
          pathOptions={{
            color: "#1565c0",
            fillColor: "#42a5f5",
            fillOpacity: 0.6,
            weight: 1,
          }}
        >
          <Popup>
            <div style={{ padding: "4px" }}>
              <strong style={{ fontSize: "1.1em", display: "block", marginBottom: "4px" }}>
                Route: {pos.trip.routeName}
              </strong>
              <div style={{ color: "#666", fontSize: "0.9em" }}>
                Vehicle ID: {pos.id}<br />
                Trip: {pos.trip.tripId}<br />
                Last Update: {pos.timestamp ? new Date(pos.timestamp).toLocaleString() : "N/A"}
              </div>
            </div>
          </Popup>
        </CircleMarker>
      ))}

      {/* Render Stops as red circles with delay distribution popups */}
      {filteredStops?.map((stop) => (
        <CircleMarker
          key={`stop-${stop.id}`}
          center={[stop.latitude, stop.longitude]}
          radius={7}
          pathOptions={{
            color: "#b71c1c",
            fillColor: "#d32f2f",
            fillOpacity: 0.7,
            weight: 2,
          }}
          eventHandlers={{
            click: () => setSelectedStopId(stop.id),
          }}
        >
          <Popup>
            <div style={{ padding: "4px", minWidth: "280px" }}>
              <strong style={{ fontSize: "1.1em", display: "block", marginBottom: "4px" }}>
                {stop.name}
              </strong>
              <div style={{ color: "#666", fontSize: "0.9em" }}>
                Stop ID: {stop.id}<br />
                Routes: {stop.routes.join(", ")}<br />
                Observations: {stop.observation_count}

                <Suspense fallback={<div>Loading chart...</div>}>
                  <DelayDistributionChart stopId={stop.id} />
                </Suspense>
              </div>
            </div>
          </Popup>
        </CircleMarker>
      ))}
    </MapContainer>
  );
};


export { Map };
