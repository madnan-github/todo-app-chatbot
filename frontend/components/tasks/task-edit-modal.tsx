"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { TagInput } from "./tag-input";
import { useTags } from "@/hooks/useTags";
import type { Task, Tag } from "@/types";

interface TaskEditModalProps {
  task: Task | null;
  isOpen: boolean;
  onClose: () => void;
  onSave: (taskId: number, data: Partial<Task> & { tag_ids?: number[] }) => Promise<void>;
  availableTags: Tag[];
}

export function TaskEditModal({ task, isOpen, onClose, onSave, availableTags: initialTags }: TaskEditModalProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState<"high" | "medium" | "low">("medium");
  const [selectedTags, setSelectedTags] = useState<Tag[]>([]);
  const [isSaving, setIsSaving] = useState(false);

  const { tags, fetchTags, createTag, isLoading: isTagsLoading } = useTags();

  // Load all tags for the modal
  useEffect(() => {
    if (isOpen) {
      fetchTags({ per_page: 100 });
    }
  }, [isOpen, fetchTags]);

  // Combine initial availableTags with loaded tags
  const allTags = tags.length > 0 ? tags : initialTags;

  useEffect(() => {
    if (task) {
      setTitle(task.title);
      setDescription(task.description || "");
      setPriority(task.priority);
      setSelectedTags(task.tags || []);
    }
  }, [task]);

  if (!isOpen || !task) return null;

  const handleSave = async () => {
    if (!title.trim()) return;

    setIsSaving(true);
    try {
      await onSave(task.id, {
        title,
        description,
        priority,
        tag_ids: selectedTags.map((t) => t.id),
      });
      onClose();
    } finally {
      setIsSaving(false);
    }
  };

  const handleCreateTag = async (name: string): Promise<Tag> => {
    return createTag(name);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="w-full max-w-md rounded-lg bg-white p-6 shadow-xl dark:bg-gray-800">
        <h2 className="mb-4 text-lg font-semibold text-gray-900 dark:text-white">
          Edit Task
        </h2>

        <div className="space-y-4">
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">
              Title
            </label>
            <Input
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Task title"
              maxLength={200}
            />
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">
              Description
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Task description (optional)"
              className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm placeholder:text-gray-400 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white"
              rows={3}
              maxLength={1000}
            />
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">
              Priority
            </label>
            <Select
              value={priority}
              onChange={(e) => setPriority(e.target.value as "high" | "medium" | "low")}
              options={[
                { value: "high", label: "High" },
                { value: "medium", label: "Medium" },
                { value: "low", label: "Low" },
              ]}
            />
          </div>

          {/* T129: Tag input in TaskEditModal */}
          <TagInput
            selectedTags={selectedTags}
            onTagsChange={setSelectedTags}
            availableTags={allTags}
            onCreateTag={handleCreateTag}
            isLoading={isTagsLoading}
          />
        </div>

        <div className="mt-6 flex justify-end gap-2">
          <Button variant="outline" onClick={onClose} disabled={isSaving}>
            Cancel
          </Button>
          <Button onClick={handleSave} disabled={isSaving || !title.trim()}>
            {isSaving ? "Saving..." : "Save Changes"}
          </Button>
        </div>
      </div>
    </div>
  );
}
