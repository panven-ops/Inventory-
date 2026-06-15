import React, { useState } from "react";
import { useAuth } from "./AuthContext";
import { sanitizeInput, isValidUsername, isValidPassword } from "./sanitizes";

function Login({ switchToRegister }) {
  const { login } = useAuth();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleLogin() {

    setError("");

    const cleanUsername = sanitizeInput(username);
    const cleanPassword = sanitizeInput(password);

    if (!cleanUsername || !cleanPassword) {
      setError("Fill in every field");
      return;
    }
    if (!isValidUsername(cleanUsername)) {
      setError("Username accepts only alphanumeric characters, _ and -");
      return;
    }
    if (!isValidPassword(cleanPassword)) {
      setError("Password must have at least 8 characters");
      return;
    }

    const res = await fetch("http://127.0.0.1:8000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    const data = await res.json();

    if (!res.ok) {
      alert(data.detail);
      return;
    }

    login(data);
  }

   return (

    <div className="min-h-screen bg-slate-50 flex items-center justify-center px-4">
      <div className="w-full max-w-sm bg-white rounded-xl border border-slate-200 p-8">
        <div className="flex items-center gap-2 mb-6">
          <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white text-sm">
            ▦
          </div>
          <span className="text-sm font-medium text-slate-800">Inventory</span>
        </div>

        {/* TITLE */}
        <h1 className="text-lg font-medium text-slate-900 mb-1">Welcome back</h1>
        <p className="text-sm text-slate-500 mb-6">Sign in to your account</p>

        {/*USERNAME FIELD
            */}
        <div className="flex flex-col gap-1 mb-4">
          <label className="text-xs font-medium text-slate-500 uppercase tracking-wide">
            Username
          </label>
          <div className="relative">
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm">👤</span>
            <input
              placeholder="your_username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full h-10 pl-9 pr-3 text-sm border border-slate-200 rounded-lg bg-slate-50 text-slate-900 focus:outline-none focus:border-indigo-400 focus:bg-white"
            />
          </div>
        </div>

        {/*PASSWORD FIELD*/}
        <div className="flex flex-col gap-1 mb-2">
          <label className="text-xs font-medium text-slate-500 uppercase tracking-wide">
            Password
          </label>
          <div className="relative">
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm">🔒</span>
            <input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              onKeyDown={(e) => { if (e.key === "Enter") handleLogin(); }}
              className="w-full h-10 pl-9 pr-3 text-sm border border-slate-200 rounded-lg bg-slate-50 text-slate-900 focus:outline-none focus:border-indigo-400 focus:bg-white"
            />
          </div>
        </div>

        {/*ERROR MESSAGE*/}
        {error && (
          <p className="text-xs text-red-600 mb-4 flex items-center gap-1">
            <span>⚠</span> {error}
          </p>
        )}

        {/*SUBMIT BUTTON*/}
        <button
          onClick={handleLogin}
          className="w-full h-10 mt-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium rounded-lg transition-colors"
        >
          Sign in
        </button>

        {/*DIVIDER + SWITCH*/}
        <div className="border-t border-slate-100 mt-5 pt-5 text-center">
          <p className="text-sm text-slate-500">
            No account?{" "}
            <button
              onClick={switchToRegister}
              className="text-indigo-600 font-medium hover:underline"
            >
              Create one
            </button>
          </p>
        </div>

      </div>
    </div>
  );
}

export default Login;
