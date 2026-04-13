import React, { useState } from 'react';
import axios from 'axios';
import { Lock, User, Loader2, Eye, EyeOff } from 'lucide-react';

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

export function LoginScreen({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username || !password) { setError('Vul gebruikersnaam en wachtwoord in'); return; }
    setLoading(true);
    setError('');
    try {
      const res = await axios.post(`${API}/auth/login`, { username, password }, { withCredentials: true });
      localStorage.setItem('recra_token', res.data.token);
      localStorage.setItem('recra_user', JSON.stringify(res.data));
      onLogin(res.data);
    } catch (err) {
      const detail = err.response?.data?.detail;
      setError(typeof detail === 'string' ? detail : 'Inloggen mislukt');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#244628] flex items-center justify-center p-4" data-testid="login-screen">
      <div className="w-full max-w-sm">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="text-3xl font-bold text-white tracking-[6px]">RECRA</div>
          <div className="text-[#70C26C] text-xs tracking-[4px] mt-1">SOLUTIONS</div>
          <div className="w-12 h-0.5 bg-[#70C26C] mx-auto mt-4" />
        </div>

        {/* Login card */}
        <form onSubmit={handleSubmit} className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6 space-y-4" data-testid="login-form">
          <div className="text-center">
            <div className="w-12 h-12 bg-[#70C26C]/15 rounded-xl flex items-center justify-center mx-auto mb-3">
              <Lock size={22} className="text-[#70C26C]" />
            </div>
            <h1 className="text-white text-base font-bold">Inloggen</h1>
            <p className="text-white/40 text-xs mt-1">Voer uw gegevens in om toegang te krijgen</p>
          </div>

          {error && (
            <div className="bg-red-500/10 border border-red-500/20 text-red-300 text-xs rounded-lg px-3 py-2.5 text-center" data-testid="login-error">
              {error}
            </div>
          )}

          <div>
            <label className="text-[10px] text-white/40 uppercase tracking-wider block mb-1.5">Gebruikersnaam</label>
            <div className="relative">
              <User size={15} className="absolute left-3 top-2.5 text-white/25" />
              <input
                value={username}
                onChange={e => setUsername(e.target.value)}
                placeholder="Gebruikersnaam"
                autoComplete="username"
                className="w-full text-sm bg-white/5 border border-white/10 rounded-xl pl-10 pr-3 py-2.5 text-white placeholder-white/20 focus:outline-none focus:border-[#70C26C]/50 transition-colors"
                data-testid="login-username"
              />
            </div>
          </div>

          <div>
            <label className="text-[10px] text-white/40 uppercase tracking-wider block mb-1.5">Wachtwoord</label>
            <div className="relative">
              <Lock size={15} className="absolute left-3 top-2.5 text-white/25" />
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={e => setPassword(e.target.value)}
                placeholder="Wachtwoord"
                autoComplete="current-password"
                className="w-full text-sm bg-white/5 border border-white/10 rounded-xl pl-10 pr-10 py-2.5 text-white placeholder-white/20 focus:outline-none focus:border-[#70C26C]/50 transition-colors"
                data-testid="login-password"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-2.5 text-white/25 hover:text-white/50"
                data-testid="toggle-password"
              >
                {showPassword ? <EyeOff size={15} /> : <Eye size={15} />}
              </button>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 text-sm font-bold bg-[#70C26C] text-[#244628] rounded-xl py-3 hover:bg-[#5fb35b] disabled:opacity-50 transition-all mt-2"
            data-testid="login-submit"
          >
            {loading ? <><Loader2 size={16} className="animate-spin" /> Inloggen...</> : 'Inloggen'}
          </button>
        </form>

        <p className="text-center text-white/20 text-[10px] mt-6">
          Powered by Pleisureworld x RECRA Solutions
        </p>
      </div>
    </div>
  );
}
