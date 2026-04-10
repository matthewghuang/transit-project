import { create } from "zustand";

type FilterState = {
  filters: string[];
  selectedStopId: string | null;
};

type FilterActions = {
  addFilter: (filter: string) => void;
  removeFilter: (filter: string) => void;
  clearFilters: () => void;
  setFilters: (newFilters: string[]) => void;
  setSelectedStopId: (id: string | null) => void;
};

type FilterStore = FilterState & FilterActions;

export const useFilterStore = create<FilterStore>((set) => ({
  // Initial State
  filters: [],
  selectedStopId: null,

  // Actions
  addFilter: (filterToAdd) =>
    set((state) => {
      // Prevent duplicates
      if (!state.filters.includes(filterToAdd)) {
        return { filters: [...state.filters, filterToAdd] };
      }
      return state;
    }),

  removeFilter: (filterToRemove) =>
    set((state) => ({
      filters: state.filters.filter((filter) => filter !== filterToRemove),
    })),

  clearFilters: () =>
    set(() => ({
      filters: [],
    })),

  setFilters: (newFilters) =>
    set(() => ({
      filters: newFilters,
    })),

  setSelectedStopId: (id) =>
    set(() => ({
      selectedStopId: id,
    })),
}));
