"use client";

import { TaskItem } from "./task-item";
import { Card, CardContent } from "@/components/ui/card";
import type { Task, Tag } from "@/types";

interface TaskListProps {
  tasks: Task[];
  isLoading: boolean;
  searchQuery: string;
  filterStatus: "all" | "active" | "completed";
  onToggleComplete: (taskId: number) => Promise<void>;
  onDelete: (taskId: number) => Promise<void>;
  onEdit: (task: Task) => void;
}

export function TaskList({
  tasks,
  isLoading,
  searchQuery,
  filterStatus,
  onToggleComplete,
  onDelete,
  onEdit,
}: TaskListProps) {
  if (isLoading) {
    return (
      <div className="flex justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (tasks.length === 0) {
    let message = "No tasks yet. Create your first task above!";
    if (searchQuery) {
      message = "No tasks match your search";
    } else if (filterStatus === "completed") {
      message = "No completed tasks";
    } else if (filterStatus === "active") {
      message = "No active tasks";
    }

    return (
      <Card>
        <CardContent className="py-12 text-center">
          <p className="text-gray-500 dark:text-gray-400">{message}</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onToggleComplete={onToggleComplete}
          onDelete={onDelete}
          onEdit={onEdit}
        />
      ))}
    </div>
  );
}
