import { ChangeEvent, useState } from "react";
import { usePositions } from "../hooks/usePositions";
import { useFilterStore } from "../stores/filterStore";
import { useCallback } from "react";

const FilterEntry: React.FC<{ routeName: string; checked: boolean }> = ({
  routeName,
  checked,
}) => {
  const { addFilter, removeFilter } = useFilterStore();

  const handleCheckbox = useCallback((event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.checked) {
      addFilter(routeName);
    } else {
      removeFilter(routeName);
    }
  }, []);

  return (
    <li>
      <input
        type="checkbox"
        name={routeName}
        checked={checked}
        onChange={handleCheckbox}
      />
      {routeName}
    </li>
  );
};

export const FilterTable: React.FC<{}> = ({}) => {
  const { data } = usePositions();
  const { filters, addFilter, clearFilters } = useFilterStore();

  const routeNames = new Set<string>();
  data?.forEach((pde) => {
    routeNames.add(pde.vehicle.trip.route_name);
  });
  filters.forEach((filter) => routeNames.add(filter));

  const handleSelectAll = useCallback(
    () => routeNames.forEach((val) => addFilter(val)),
    [routeNames, addFilter]
  );

  return (
    <>
      <button onClick={handleSelectAll}>Select All</button>
      <button onClick={clearFilters}>Clear All</button>
      <ul>
        {Array.from(routeNames)
          .sort()
          .map((routeName) => (
            <FilterEntry
              key={routeName}
              routeName={routeName}
              checked={filters.includes(routeName)}
            ></FilterEntry>
          ))}
      </ul>
    </>
  );
};
