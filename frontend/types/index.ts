// User types
export interface User {
  id: string;
  email: string;
  name: string | null;
  created_at: string;
}

// Task types
export type TaskPriority = "high" | "medium" | "low";

export interface Task {
  id: number;
  user_id: string;
  title: string;
  description: string | null;
  completed: boolean;
  priority: TaskPriority;
  created_at: string;
  updated_at: string;
  tags: Tag[];
}

export interface TaskCreateInput {
  title: string;
  description?: string;
  priority: TaskPriority;
  tag_ids?: number[];
}

export interface TaskUpdateInput {
  title?: string;
  description?: string;
  completed?: boolean;
  priority?: TaskPriority;
  tag_ids?: number[];
}

// Tag types
export interface Tag {
  id: number;
  user_id: string;
  name: string;
}

export interface TagListResponse {
  tags: Tag[];
  total: number;
  page: number;
  per_page: number;
}

export interface TagAutocompleteResponse {
  suggestions: string[];
}

// API Response types
export interface TaskListResponse {
  tasks: Task[];
  total: number;
  page: number;
  per_page: number;
}

export interface ApiError {
  detail: string;
  error_code?: string;
}

// Form types
export interface SignUpFormData {
  email: string;
  password: string;
  confirmPassword: string;
  name: string;
}

export interface SignInFormData {
  email: string;
  password: string;
}

export interface TaskFormData {
  title: string;
  description: string;
  priority: TaskPriority;
  tags: number[];
}
