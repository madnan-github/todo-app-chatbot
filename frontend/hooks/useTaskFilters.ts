"use client";

import { useState, useEffect, useCallback } from "react";

interface TaskFilters {
  // Search
  search: string;

  // Status
  status: "all" | "active" | "completed";

  // Priority (multiple selection)
  priorities: string[];

  // Tags (multiple selection)
  tags: number[];

  // Sorting
  sortBy: "created_at" | "updated_at" | "title" | "priority";
  sortOrder: "asc" | "desc";
}

const STORAGE_KEY = "taskflow-filters";

const defaultFilters: TaskFilters = {
  search: "",
  status: "all",
  priorities: [],
  tags: [],
  sortBy: "created_at",
  sortOrder: "desc",
};

export function useTaskFilters() {
  const [filters, setFilters] = useState<TaskFilters>(defaultFilters);
  const [isInitialized, setIsInitialized] = useState(false);

  // Load from localStorage on mount (T167a)
  useEffect(() => {
    if (typeof window !== "undefined") {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        try {
          const parsed = JSON.parse(saved);
          setFilters({ ...defaultFilters, ...parsed });
        } catch {
          setFilters(defaultFilters);
        }
      }
      setIsInitialized(true);
    }
  }, []);

  // Save to localStorage on change
  useEffect(() => {
    if (isInitialized && typeof window !== "undefined") {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(filters));
    }
  }, [filters, isInitialized]);

  // Update functions
  const setSearch = useCallback((search: string) => {
    setFilters((prev) => ({ ...prev, search }));
  }, []);

  const setStatus = useCallback((status: "all" | "active" | "completed") => {
    setFilters((prev) => ({ ...prev, status }));
  }, []);

  const setPriorities = useCallback((priorities: string[]) => {
    setFilters((prev) => ({ ...prev, priorities }));
  }, []);

  const togglePriority = useCallback((priority: string) => {
    setFilters((prev) => ({
      ...prev,
      priorities: prev.priorities.includes(priority)
        ? prev.priorities.filter((p) => p !== priority)
        : [...prev.priorities, priority],
    }));
  }, []);

  const setTags = useCallback((tags: number[]) => {
    setFilters((prev) => ({ ...prev, tags }));
  }, []);

  const toggleTag = useCallback((tagId: number) => {
    setFilters((prev) => ({
      ...prev,
      tags: prev.tags.includes(tagId)
        ? prev.tags.filter((t) => t !== tagId)
        : [...prev.tags, tagId],
    }));
  }, []);

  const setSortBy = useCallback(
    (sortBy: "created_at" | "updated_at" | "title" | "priority") => {
      setFilters((prev) => ({ ...prev, sortBy }));
    },
    []
  );

  const setSortOrder = useCallback((sortOrder: "asc" | "desc") => {
    setFilters((prev) => ({ ...prev, sortOrder }));
  }, []);

  const toggleSortOrder = useCallback(() => {
    setFilters((prev) => ({
      ...prev,
      sortOrder: prev.sortOrder === "asc" ? "desc" : "asc",
    }));
  }, []);

  const clearFilters = useCallback(() => {
    setFilters((prev) => ({
      ...prev,
      search: "",
      status: "all",
      priorities: [],
      tags: [],
    }));
  }, []);

  const resetAll = useCallback(() => {
    setFilters(defaultFilters);
  }, []);

  // Get active filter count
  const activeFilterCount =
    (filters.status !== "all" ? 1 : 0) +
    filters.priorities.length +
    filters.tags.length +
    (filters.search ? 1 : 0);

  return {
    filters,
    setFilters,
    isInitialized,

    // Search
    search: filters.search,
    setSearch,

    // Status
    status: filters.status,
    setStatus,

    // Priorities
    priorities: filters.priorities,
    setPriorities,
    togglePriority,

    // Tags
    tags: filters.tags,
    setTags,
    toggleTag,

    // Sorting
    sortBy: filters.sortBy,
    sortOrder: filters.sortOrder,
    setSortBy,
    setSortOrder,
    toggleSortOrder,

    // Actions
    clearFilters,
    resetAll,
    activeFilterCount,
  };
}
