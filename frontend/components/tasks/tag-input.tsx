"use client";

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import type { Tag } from "@/types";

interface TagInputProps {
  selectedTags: Tag[];
  onTagsChange: (tags: Tag[]) => void;
  availableTags: Tag[];
  onCreateTag?: (name: string) => Promise<Tag>;
  isLoading?: boolean;
}

export function TagInput({
  selectedTags,
  onTagsChange,
  availableTags,
  onCreateTag,
  isLoading = false,
}: TagInputProps) {
  const [inputValue, setInputValue] = useState("");
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const wrapperRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Filter suggestions based on input
    if (inputValue.trim()) {
      const filtered = availableTags
        .filter(
          (tag) =>
            tag.name.toLowerCase().includes(inputValue.toLowerCase()) &&
            !selectedTags.some((t) => t.id === tag.id)
        )
        .map((tag) => tag.name)
        .slice(0, 5);
      setSuggestions(filtered);
      setShowSuggestions(filtered.length > 0);
    } else {
      setSuggestions([]);
      setShowSuggestions(false);
    }
  }, [inputValue, availableTags, selectedTags]);

  useEffect(() => {
    // Close suggestions when clicking outside
    const handleClickOutside = (event: MouseEvent) => {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target as Node)) {
        setShowSuggestions(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleKeyDown = async (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      e.preventDefault();
      if (inputValue.trim() && onCreateTag) {
        await addNewTag(inputValue.trim());
      } else if (suggestions.length > 0) {
        selectSuggestion(suggestions[0]);
      }
    } else if (e.key === "Escape") {
      setShowSuggestions(false);
    } else if (e.key === "Backspace" && !inputValue && selectedTags.length > 0) {
      removeTag(selectedTags[selectedTags.length - 1]);
    }
  };

  const selectSuggestion = (name: string) => {
    const tag = availableTags.find((t) => t.name.toLowerCase() === name.toLowerCase());
    if (tag && !selectedTags.some((t) => t.id === tag.id)) {
      onTagsChange([...selectedTags, tag]);
    }
    setInputValue("");
    setShowSuggestions(false);
    inputRef.current?.focus();
  };

  const addNewTag = async (name: string) => {
    if (!onCreateTag) return;

    setIsCreating(true);
    try {
      const newTag = await onCreateTag(name);
      if (!selectedTags.some((t) => t.id === newTag.id)) {
        onTagsChange([...selectedTags, newTag]);
      }
      setInputValue("");
      setShowSuggestions(false);
    } finally {
      setIsCreating(false);
    }
  };

  const removeTag = (tagToRemove: Tag) => {
    onTagsChange(selectedTags.filter((t) => t.id !== tagToRemove.id));
  };

  const addTag = (tag: Tag) => {
    if (!selectedTags.some((t) => t.id === tag.id)) {
      onTagsChange([...selectedTags, tag]);
    }
    setInputValue("");
    setShowSuggestions(false);
  };

  return (
    <div ref={wrapperRef} className="relative">
      <label className="mb-1 block text-sm font-medium text-gray-700 dark:text-gray-300">
        Tags
      </label>

      {/* Selected tags */}
      <div className="mb-2 flex flex-wrap gap-2">
        {selectedTags.map((tag) => (
          <span
            key={tag.id}
            className="inline-flex items-center gap-1 rounded-full bg-blue-100 px-3 py-1 text-sm text-blue-800 dark:bg-blue-900 dark:text-blue-200"
          >
            {tag.name}
            <button
              type="button"
              onClick={() => removeTag(tag)}
              className="ml-1 rounded-full p-0.5 hover:bg-blue-200 dark:hover:bg-blue-800"
              disabled={isLoading}
            >
              <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </span>
        ))}
      </div>

      {/* Input field */}
      <div className="relative">
        <input
          ref={inputRef}
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          onFocus={() => suggestions.length > 0 && setShowSuggestions(true)}
          placeholder="Type a tag and press Enter"
          className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm placeholder:text-gray-400 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-700 dark:text-white dark:placeholder:text-gray-400"
          disabled={isLoading || isCreating}
        />

        {/* Suggestions dropdown */}
        {showSuggestions && (
          <div className="absolute z-10 mt-1 w-full rounded-md border border-gray-300 bg-white py-1 shadow-lg dark:border-gray-600 dark:bg-gray-800">
            {suggestions.map((name, index) => (
              <button
                key={index}
                type="button"
                onClick={() => selectSuggestion(name)}
                className="w-full px-3 py-2 text-left text-sm hover:bg-gray-100 dark:hover:bg-gray-700"
              >
                {name}
              </button>
            ))}
            {onCreateTag && inputValue.trim() && (
              <button
                type="button"
                onClick={() => addNewTag(inputValue.trim())}
                className="w-full border-t border-gray-200 px-3 py-2 text-left text-sm text-blue-600 hover:bg-gray-100 dark:border-gray-700 dark:hover:bg-gray-700"
              >
                + Create "{inputValue.trim()}"
              </button>
            )}
          </div>
        )}
      </div>

      {/* Available tags quick add */}
      {availableTags.filter((t) => !selectedTags.some((st) => st.id === t.id)).length > 0 && (
        <div className="mt-2 flex flex-wrap gap-1">
          <span className="text-xs text-gray-500">Quick add:</span>
          {availableTags
            .filter((t) => !selectedTags.some((st) => st.id === t.id))
            .slice(0, 5)
            .map((tag) => (
              <button
                key={tag.id}
                type="button"
                onClick={() => addTag(tag)}
                className="rounded-full border border-gray-300 px-2 py-0.5 text-xs hover:bg-gray-100 dark:border-gray-600 dark:hover:bg-gray-700"
              >
                {tag.name}
              </button>
            ))}
        </div>
      )}
    </div>
  );
}
