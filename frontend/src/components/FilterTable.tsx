import { ChangeEvent, useCallback } from "react";
import { usePositions } from "../hooks/usePositions";
import { useFilterStore } from "../stores/filterStore";

const FilterEntry: React.FC<{ routeName: string; checked: boolean }> = ({
  routeName,
  checked,
}) => {
  const { addFilter, removeFilter } = useFilterStore();

  const handleCheckbox = useCallback(
    (event: ChangeEvent<HTMLInputElement>) => {
      if (event.target.checked) {
        addFilter(routeName);
      } else {
        removeFilter(routeName);
      }
    },
    [routeName, addFilter, removeFilter]
  );

  return (
    <li className="filter-item" onClick={() => (checked ? removeFilter(routeName) : addFilter(routeName))}>
      <input
        type="checkbox"
        id={`filter-${routeName}`}
        name={routeName}
        checked={checked}
        onChange={handleCheckbox}
        onClick={(e) => e.stopPropagation()}
      />
      <label htmlFor={`filter-${routeName}`}>{routeName}</label>
    </li>
  );
};

export const FilterTable: React.FC<{}> = () => {
  const { data } = usePositions();
  const { filters, addFilter, clearFilters } = useFilterStore();

  const routeNames = new Set<string>();
  data?.forEach((pde) => {
    routeNames.add(pde.trip.routeId);
  });
  filters.forEach((filter) => routeNames.add(filter));

  const sortedRouteNames = Array.from(routeNames).sort();

  const handleSelectAll = useCallback(
    () => sortedRouteNames.forEach((val) => addFilter(val)),
    [sortedRouteNames, addFilter]
  );

  return (
    <>
      <div className="filter-header">
        <h2 style={{ fontSize: "1rem", marginBottom: "0.75rem", fontWeight: 600 }}>Route Filters</h2>
        <div className="filter-controls">
          <button className="btn btn-primary" onClick={handleSelectAll}>
            Select All
          </button>
          <button className="btn" onClick={clearFilters}>
            Clear
          </button>
        </div>
      </div>
      <ul className="filter-list">
        {sortedRouteNames.map((routeName) => (
          <FilterEntry
            key={routeName}
            routeName={routeName}
            checked={filters.includes(routeName)}
          />
        ))}
      </ul>
    </>
  );
};
