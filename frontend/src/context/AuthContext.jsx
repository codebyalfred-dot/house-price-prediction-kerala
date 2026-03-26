import { createContext, useContext, useEffect, useState } from "react";

import { api } from "../api/client";

const AuthContext = createContext(null);
const TOKEN_KEY = "kerala-house-price-token";
const USER_KEY = "kerala-house-price-user";

function readStoredUser() {
  const rawUser = localStorage.getItem(USER_KEY);
  if (!rawUser) {
    return null;
  }

  try {
    return JSON.parse(rawUser);
  } catch {
    localStorage.removeItem(USER_KEY);
    return null;
  }
}

export function AuthProvider({ children }) {
  const [token, setToken] = useState(() => localStorage.getItem(TOKEN_KEY));
  const [user, setUser] = useState(readStoredUser);
  const [isLoading, setIsLoading] = useState(Boolean(token));

  useEffect(() => {
    let isMounted = true;

    async function refreshProfile() {
      if (!token) {
        setIsLoading(false);
        return;
      }

      try {
        const profile = await api.getMe(token);
        if (!isMounted) {
          return;
        }
        setUser(profile);
        localStorage.setItem(USER_KEY, JSON.stringify(profile));
      } catch {
        if (!isMounted) {
          return;
        }
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(USER_KEY);
        setToken(null);
        setUser(null);
      } finally {
        if (isMounted) {
          setIsLoading(false);
        }
      }
    }

    refreshProfile();

    return () => {
      isMounted = false;
    };
  }, [token]);

  async function login(credentials) {
    const response = await api.login(credentials);
    setToken(response.access_token);
    setUser(response.user);
    localStorage.setItem(TOKEN_KEY, response.access_token);
    localStorage.setItem(USER_KEY, JSON.stringify(response.user));
    return response;
  }

  async function signup(payload) {
    const response = await api.signup(payload);
    setToken(response.access_token);
    setUser(response.user);
    localStorage.setItem(TOKEN_KEY, response.access_token);
    localStorage.setItem(USER_KEY, JSON.stringify(response.user));
    return response;
  }

  function logout() {
    setToken(null);
    setUser(null);
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
  }

  return (
    <AuthContext.Provider value={{ token, user, isLoading, login, signup, logout, isAuthenticated: Boolean(token) }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider.");
  }
  return context;
}
