"use client";

import type { SignUpFormData, SignInFormData } from "@/types";
import { useState, useEffect, useCallback, createContext, useContext, ReactNode } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Types for our auth context
interface User {
  id: string;
  email: string;
  name: string;
  image?: string;
}

interface Session {
  token: string;
  user: User;
}

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  signIn: (data: SignInFormData) => Promise<void>;
  signUp: (data: SignUpFormData) => Promise<void>;
  signOut: () => Promise<void>;
}

// Create auth context
const AuthContext = createContext<AuthContextType | null>(null);

// Helper to get/set token from localStorage
const getStoredToken = (): string | null => {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("auth_token");
};

const setStoredToken = (token: string | null) => {
  if (typeof window === "undefined") return;
  if (token) {
    localStorage.setItem("auth_token", token);
  } else {
    localStorage.removeItem("auth_token");
  }
};

const getStoredUser = (): User | null => {
  if (typeof window === "undefined") return null;
  const userStr = localStorage.getItem("auth_user");
  if (!userStr) return null;
  try {
    return JSON.parse(userStr);
  } catch {
    return null;
  }
};

const setStoredUser = (user: User | null) => {
  if (typeof window === "undefined") return;
  if (user) {
    localStorage.setItem("auth_user", JSON.stringify(user));
  } else {
    localStorage.removeItem("auth_user");
  }
};

// Provider component
export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Load session from localStorage on mount
  useEffect(() => {
    const storedToken = getStoredToken();
    const storedUser = getStoredUser();
    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(storedUser);
    }
    setIsLoading(false);
  }, []);

  const signInWithEmail = useCallback(async (data: SignInFormData) => {
    setError(null);
    setIsLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/v1/sign-in/email`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: data.email, password: data.password }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || "Sign in failed");
      }

      const result = await response.json();
      console.log("Sign in result:", result);

      if (result.user && result.session?.token) {
        setUser(result.user as User);
        setToken(result.session.token);
        setStoredToken(result.session.token);
        setStoredUser(result.user as User);
      }
    } catch (err: any) {
      setError(err.message || "Sign in failed");
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const signUpWithEmail = useCallback(async (data: SignUpFormData) => {
    setError(null);
    setIsLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/v1/sign-up/email`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: data.email, password: data.password, name: data.name }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || "Sign up failed");
      }

      const result = await response.json();
      console.log("Sign up result:", result);

      if (result.user && result.session?.token) {
        setUser(result.user as User);
        setToken(result.session.token);
        setStoredToken(result.session.token);
        setStoredUser(result.user as User);
      }
    } catch (err: any) {
      setError(err.message || "Sign up failed");
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const logout = useCallback(async () => {
    setError(null);
    setIsLoading(true);
    try {
      // Clear local state and storage
      setUser(null);
      setToken(null);
      setStoredToken(null);
      setStoredUser(null);
    } catch (err: any) {
      setError(err.message || "Sign out failed");
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!user && !!token,
        isLoading,
        error,
        signIn: signInWithEmail,
        signUp: signUpWithEmail,
        signOut: logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

// Hook to use auth context
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
