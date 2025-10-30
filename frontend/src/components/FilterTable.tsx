import { useState } from "react";
import { usePositions } from "../hooks/usePositions";
import { useFilterStore } from "../stores/filterStore";

const FilterEntry: React.FC<{ routeName: string }> = ({ routeName }) => {
  const { addFilter, removeFilter } = useFilterStore();

  return (
    <li>
      <input type="checkbox" name={routeName} />
      {routeName}
    </li>
  );
};

export const FilterTable: React.FC<{}> = ({}) => {
  const { data } = usePositions();

  const routeNames = new Set<string>();
  data?.forEach((pde) => {
    routeNames.add(pde.vehicle.trip.route_name);
  });

  return (
    <>
      <ul>
        {Array.from(routeNames).map((routeName) => (
          <FilterEntry key={routeName} routeName={routeName}></FilterEntry>
        ))}
      </ul>
    </>
  );
};
