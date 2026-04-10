import { MapContainer, TileLayer, Marker, CircleMarker, Popup } from "react-leaflet";
import L, { LatLngTuple } from "leaflet";
import { usePositions } from "../hooks/usePositions";
import { useStops } from "../hooks/useStops";
import { CSSProperties, useMemo, lazy, Suspense } from "react";
import { useFilterStore } from "../stores/filterStore";

const DelayDistributionChart = lazy(() => import("./DelayDistributionChart"));

const centerPosition: LatLngTuple = [49.246292, -123.116226];

// Custom stop icon — red pin that stands out from vehicles
const stopIcon = new L.DivIcon({
  className: "",
  html: `<div style="
    width: 28px; height: 28px;
    background: #d32f2f;
    border: 3px solid #fff;
    border-radius: 50% 50% 50% 0;
    transform: rotate(-45deg);
    box-shadow: 0 2px 6px rgba(0,0,0,0.4);
  "></div>`,
  iconSize: [28, 28],
  iconAnchor: [14, 28],
  popupAnchor: [0, -28],
});

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

      {/* Render Vehicles as small translucent dots */}
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
                Route: {pos.trip.routeId}
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

      {/* Render Stops as prominent red markers with delay distributions */}
      {stops?.map((stop) => (
        <Marker 
          key={`stop-${stop.id}`}
          position={[stop.latitude, stop.longitude] as LatLngTuple}
          icon={stopIcon}
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
                Observations: {stop.observation_count}

                <Suspense fallback={<div>Loading chart...</div>}>
                  <DelayDistributionChart stopId={stop.id} />
                </Suspense>
              </div>
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};


export { Map };
