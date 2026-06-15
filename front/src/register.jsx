import React, { useState } from "react";
import { sanitizeInput, isValidUsername, isValidPassword } from "./sanitizes";


function Register({ switchToLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  function getStrength(pwd) {
    let score = 0;
    if (pwd.length >= 8) score++;
    if (pwd.length >= 12) score++;
    if (/[A-Z]/.test(pwd)) score++;
    if (/[0-9]/.test(pwd)) score++;
    return score;
  }

  const strength = getStrength(password);

  const strengthConfig = {
    0: { label: "", color: "bg-slate-200" },
    1: { label: "Weak", color: "bg-red-400" },
    2: { label: "Fair", color: "bg-amber-400" },
    3: { label: "Good", color: "bg-indigo-400" },
    4: { label: "Strong", color: "bg-emerald-500" },
  };


  async function register() {
    setError("");

    const cleanUsername = sanitizeInput(username);
    const cleanPassword = sanitizeInput(password);

    if (!cleanUsername || !cleanPassword) {
      setError("Fill in all fields");
      return;
    }
    if (!isValidUsername(cleanUsername)) {
      setError("Username must have only alphanumeric, - and _");
      return;
    }
    if (!isValidPassword(cleanPassword)) {
      setError("Password must have at least 8 charachters");
      return;
    }

    const res = await fetch("http://127.0.0.1:8000/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username, password }),
    });

    const data = await res.json();

    if (!res.ok) {
      alert(data.detail || "Register failed");
      return;
    }

    setSuccess(true);
    setUsername("");
    setPassword("");
  }

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center px-4">
      <div className="w-full max-w-sm bg-white rounded-xl border border-slate-200 p-8">

        {/*BRAND*/}
        <div className="flex items-center gap-2 mb-6">
          <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white text-sm">
            ▦
          </div>
          <span className="text-sm font-medium text-slate-800">Inventory</span>
        </div>

        <h1 className="text-lg font-medium text-slate-900 mb-1">Create account</h1>
        <p className="text-sm text-slate-500 mb-6">Start managing your inventory</p>

        {/*SUCCESS MESSAGE*/}
        {success && (
          <div className="flex items-center gap-2 bg-emerald-50 border border-emerald-200 text-emerald-700 text-sm rounded-lg px-3 py-2 mb-4">
            <span>✓</span>
            <span>Account created! You can now <button onClick={switchToLogin} className="font-medium underline">sign in</button>.</span>
          </div>
        )}

        {/*USERNAME FIELD*/}
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

        {/*PASSWORD FIELD/STRENGTH BAR*/}
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
              onKeyDown={(e) => { if (e.key === "Enter") register(); }}
              className="w-full h-10 pl-9 pr-3 text-sm border border-slate-200 rounded-lg bg-slate-50 text-slate-900 focus:outline-none focus:border-indigo-400 focus:bg-white"
            />
          </div>

          {/*STRENGTH BAR*/}
          {password.length > 0 && (
            <div className="mt-1">
              <div className="flex gap-1">
                {[1, 2, 3, 4].map((seg) => (
                  <div
                    key={seg}
                    className={`h-1 flex-1 rounded-full transition-colors ${
                      seg <= strength
                        ? strengthConfig[strength].color
                        : "bg-slate-200"
                    }`}
                  />
                ))}
              </div>
              {/* Label δεξιά */}
              <p className={`text-xs mt-1 text-right ${
                strength <= 1 ? "text-red-400" :
                strength === 2 ? "text-amber-400" :
                strength === 3 ? "text-indigo-400" :
                "text-emerald-500"
              }`}>
                {strengthConfig[strength].label}
              </p>
            </div>
          )}
        </div>

        {/*ERROR MESSAGE*/}
        {error && (
          <p className="text-xs text-red-600 mb-4 flex items-center gap-1">
            <span>⚠</span> {error}
          </p>
        )}

        <button
          onClick={register}
          className="w-full h-10 mt-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium rounded-lg transition-colors"
        >
          Create account
        </button>

        <div className="border-t border-slate-100 mt-5 pt-5 text-center">
          <p className="text-sm text-slate-500">
            Already have an account?{" "}
            <button
              onClick={switchToLogin}
              className="text-indigo-600 font-medium hover:underline"
            >
              Sign in
            </button>
          </p>
        </div>

      </div>
    </div>
  );
}

export default Register;
