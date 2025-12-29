"use client";

import { useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Select } from "@/components/ui/select";

interface TaskSortProps {
  sortBy: "created_at" | "updated_at" | "title" | "priority";
  sortOrder: "asc" | "desc";
  onSortChange: (sortBy: "created_at" | "updated_at" | "title" | "priority") => void;
  onOrderChange: (order: "asc" | "desc") => void;
  isLoading?: boolean;
}

export function TaskSort({
  sortBy,
  sortOrder,
  onSortChange,
  onOrderChange,
  isLoading = false,
}: TaskSortProps) {
  const handleSortChange = useCallback(
    (e: React.ChangeEvent<HTMLSelectElement>) => {
      onSortChange(e.target.value as "created_at" | "updated_at" | "title" | "priority");
    },
    [onSortChange]
  );

  const toggleOrder = useCallback(() => {
    onOrderChange(sortOrder === "asc" ? "desc" : "asc");
  }, [sortOrder, onOrderChange]);

  return (
    <div className="flex items-center gap-2">
      <span className="text-sm text-gray-500 dark:text-gray-400">Sort by:</span>

      {/* Sort by dropdown (T160, T164) */}
      <Select
        value={sortBy}
        onChange={handleSortChange}
        options={[
          { value: "created_at", label: "Created Date" },
          { value: "updated_at", label: "Updated Date" },
          { value: "title", label: "Title" },
          { value: "priority", label: "Priority" },
        ]}
        disabled={isLoading}
        className="w-36"
      />

      {/* Sort order toggle (T161, T165) */}
      <Button
        variant="outline"
        size="sm"
        onClick={toggleOrder}
        disabled={isLoading}
        className="px-2"
        title={`Sort ${sortOrder === "asc" ? "descending" : "ascending"}`}
      >
        {sortOrder === "asc" ? (
          <svg
            className="h-4 w-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12"
            />
          </svg>
        ) : (
          <svg
            className="h-4 w-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M3 4h13M3 8h9m-9 4h9m5-4v12m0 0l-4-4m4 4l4-4"
            />
          </svg>
        )}
      </Button>
    </div>
  );
}
