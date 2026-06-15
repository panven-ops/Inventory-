import React, { createContext, useState, useContext, useEffect } from "react";

const AuthContext = createContext();

export function AuthProvider({ children }) {

  console.log("AUTH CONTEXT EXECUTED");


  const [accessToken, setAccessToken] = useState("");
  const [refreshToken, setRefreshToken] = useState("");

  useEffect(() => {
    const a = localStorage.getItem("access_token");
    const r = localStorage.getItem("refresh_token");

    if (a) setAccessToken(a);
    if (r) setRefreshToken(r);
  }, []);

  const login = (tokens) => {
    setAccessToken(tokens.access_token);
    setRefreshToken(tokens.refresh_token);

    localStorage.setItem("access_token", tokens.access_token);
    localStorage.setItem("refresh_token", tokens.refresh_token);
  };

  const logout = () => {
    setAccessToken("");
    setRefreshToken("");

    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
  };

  return (
    <AuthContext.Provider value={{ accessToken, refreshToken, login, logout, setAccessToken }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
