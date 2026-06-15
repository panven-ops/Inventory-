import React, { useState } from "react";
import { useAuth } from "./AuthContext";
import Login from "./login";
import Register from "./register";
import Items from "./Items";
import { useItems } from "./useItems";

function App() {

  const { accessToken, refreshToken, setAccessToken, logout } = useAuth();
  const [mode, setMode] = useState("login");

  const itemsLogic = useItems();

  if (!accessToken) {
    return (
      <div>
        {mode === "login" ? (
          <Login switchToRegister={() => setMode("register")} />
        ) : (
          <Register switchToLogin={() => setMode("login")} />
        )}
      </div>
    );
  }

  if (accessToken && !itemsLogic) return null;

  return <Items {...itemsLogic}accessToken={accessToken}refreshToken={refreshToken}setAccessToken={setAccessToken}logout={logout}/>;
}

export default App;
