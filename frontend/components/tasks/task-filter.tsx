"use client";

import { useState, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Select } from "@/components/ui/select";
import type { Tag } from "@/types";

interface TaskFilterProps {
  // Status filter
  statusFilter: "all" | "active" | "completed";
  onStatusChange: (value: "all" | "active" | "completed") => void;

  // Priority filter
  selectedPriorities: string[];
  onPriorityChange: (priorities: string[]) => void;

  // Tag filter
  selectedTags: number[];
  onTagChange: (tags: number[]) => void;
  availableTags: Tag[];

  // Actions
  onClearFilters: () => void;
  isLoading?: boolean;
}

export function TaskFilter({
  statusFilter,
  onStatusChange,
  selectedPriorities,
  onPriorityChange,
  selectedTags,
  onTagChange,
  availableTags,
  onClearFilters,
  isLoading = false,
}: TaskFilterProps) {
  const [showAdvanced, setShowAdvanced] = useState(false);

  const activeFilterCount =
    (statusFilter !== "all" ? 1 : 0) +
    selectedPriorities.length +
    selectedTags.length;

  const togglePriority = (priority: string) => {
    if (selectedPriorities.includes(priority)) {
      onPriorityChange(selectedPriorities.filter((p) => p !== priority));
    } else {
      onPriorityChange([...selectedPriorities, priority]);
    }
  };

  const toggleTag = (tagId: number) => {
    if (selectedTags.includes(tagId)) {
      onTagChange(selectedTags.filter((id) => id !== tagId));
    } else {
      onTagChange([...selectedTags, tagId]);
    }
  };

  const handleClear = useCallback(() => {
    onStatusChange("all");
    onPriorityChange([]);
    onTagChange([]);
    onClearFilters();
  }, [onStatusChange, onPriorityChange, onTagChange, onClearFilters]);

  return (
    <div className="space-y-3">
      {/* Basic filters row */}
      <div className="flex flex-wrap items-center gap-3">
        {/* Status filter dropdown (T150) */}
        <Select
          value={statusFilter}
          onChange={(e) =>
            onStatusChange(e.target.value as "all" | "active" | "completed")
          }
          options={[
            { value: "all", label: "All Status" },
            { value: "active", label: "Active" },
            { value: "completed", label: "Completed" },
          ]}
          disabled={isLoading}
        />

        {/* Toggle advanced filters */}
        <Button
          variant="outline"
          size="sm"
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="relative"
        >
          Filters
          {activeFilterCount > 0 && !showAdvanced && (
            <span className="absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full bg-blue-600 text-[10px] text-white">
              {activeFilterCount}
            </span>
          )}
        </Button>

        {/* Clear filters button (T154) */}
        {activeFilterCount > 0 && (
          <Button variant="ghost" size="sm" onClick={handleClear}>
            Clear all
          </Button>
        )}
      </div>

      {/* Advanced filters panel */}
      {showAdvanced && (
        <div className="rounded-lg border border-gray-200 bg-white p-4 dark:border-gray-700 dark:bg-gray-800">
          <div className="grid gap-4 sm:grid-cols-2">
            {/* Priority filter (T151) */}
            <div>
              <label className="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">
                Priority
              </label>
              <div className="flex flex-wrap gap-2">
                {["high", "medium", "low"].map((priority) => (
                  <button
                    key={priority}
                    type="button"
                    onClick={() => togglePriority(priority)}
                    className={`rounded-full px-3 py-1 text-sm transition-colors ${
                      selectedPriorities.includes(priority)
                        ? "bg-blue-600 text-white"
                        : "bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-300"
                    }`}
                    disabled={isLoading}
                  >
                    {priority.charAt(0).toUpperCase() + priority.slice(1)}
                  </button>
                ))}
              </div>
            </div>

            {/* Tag filter (T152) */}
            <div>
              <label className="mb-2 block text-sm font-medium text-gray-700 dark:text-gray-300">
                Tags
              </label>
              {availableTags.length > 0 ? (
                <div className="flex flex-wrap gap-2 max-h-32 overflow-y-auto">
                  {availableTags.map((tag) => (
                    <button
                      key={tag.id}
                      type="button"
                      onClick={() => toggleTag(tag.id)}
                      className={`rounded-full px-3 py-1 text-sm transition-colors ${
                        selectedTags.includes(tag.id)
                          ? "bg-blue-600 text-white"
                          : "bg-gray-100 text-gray-700 hover:bg-gray-200 dark:bg-gray-700 dark:text-gray-300"
                      }`}
                      disabled={isLoading}
                    >
                      {tag.name}
                    </button>
                  ))}
                </div>
              ) : (
                <p className="text-sm text-gray-500">No tags available</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
