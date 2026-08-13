import React, { useState, useEffect } from 'react';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

function App() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Pedir los datos de sesion al backend
    fetch(`${BACKEND_URL}/api/profile`, { credentials: 'include' })
      .then((res) => {
        if (res.status === 401) {
          // No hay sesion iniciada
          setProfile(null);
          setLoading(false);
          return null;
        }
        if (!res.ok) {
          throw new Error(`Error ${res.status}: No se pudo verificar la sesión.`);
        }
        return res.json();
      })
      .then((data) => {
        if (data) {
          setProfile(data);
        }
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const handleLogin = () => {
    // Redirige al backend para iniciar login
    window.location.href = `${BACKEND_URL}/login`;
  };

  const handleLogout = () => {
    // Redirige al backend para desloguear
    window.location.href = `${BACKEND_URL}/logout`;
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#0b0f19] via-[#111827] to-[#1e1b4b]">
        <div className="relative">
          <div className="w-16 h-16 border-4 border-violet-500/30 border-t-violet-500 rounded-full animate-spin"></div>
          <div className="absolute inset-0 flex items-center justify-center text-xs font-semibold text-violet-400">OIDC</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0b0f19] via-[#0f172a] to-[#1e1b4b] flex flex-col items-center justify-center p-4">
      {/* Fondo con luces de colores */}
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-violet-600/10 rounded-full filter blur-[100px] pointer-events-none"></div>
      <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-indigo-600/10 rounded-full filter blur-[100px] pointer-events-none"></div>

      <div className="w-full max-w-lg relative z-10">
        {/* Titulo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-violet-500/10 border border-violet-500/20 text-xs font-medium text-violet-400 mb-3 animate-pulse">
            <span className="w-2 h-2 rounded-full bg-violet-400"></span>
            OAuth 2.0 + OpenID Connect (OIDC)
          </div>
          <h1 className="text-4xl font-extrabold tracking-tight text-white sm:text-5xl">
            Protocolo <span className="bg-gradient-to-r from-violet-400 to-indigo-400 bg-clip-text text-transparent">OIDC</span>
          </h1>
          <p className="mt-3 text-sm text-gray-400 max-w-md mx-auto">
            Demostración de delegación de identidad y Single Sign-On (SSO) con Keycloak.
          </p>
        </div>

        {/* Tarjeta principal */}
        <div className="bg-slate-900/60 backdrop-blur-xl border border-slate-800/80 shadow-2xl rounded-2xl p-8 overflow-hidden relative">
          {/* Linea brillante en el borde */}
          <div className="absolute top-0 inset-x-0 h-[2px] bg-gradient-to-r from-transparent via-violet-500/50 to-transparent"></div>

          {error && (
            <div className="mb-6 p-4 rounded-lg bg-red-950/40 border border-red-500/30 text-red-300 text-xs flex gap-2">
              <svg className="w-4 h-4 shrink-0 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
              </svg>
              <span>{error}</span>
            </div>
          )}

          {!profile ? (
            /* SI NO ESTA LOGUEADO */
            <div className="text-center py-6">
              <div className="w-20 h-20 bg-slate-800/50 border border-slate-700/50 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-inner">
                <svg className="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                </svg>
              </div>

              <div className="mb-8">
                <h3 className="text-lg font-semibold text-white">Sin autenticar</h3>
                <p className="text-sm text-gray-400 mt-1">
                  Tu sesión no está activa. Por favor, inicia sesión para acceder a tu perfil protegido.
                </p>
              </div>

              <button
                onClick={handleLogin}
                className="w-full inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 text-white font-semibold text-sm transition-all transform hover:scale-[1.01] shadow-lg shadow-violet-500/20 active:scale-[0.99] cursor-pointer"
              >
                <svg className="w-4 h-4 text-white animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"/>
                </svg>
                Iniciar sesión con Keycloak
              </button>
            </div>
          ) : (
            /* SI ESTA LOGUEADO */
            <div>
              <div className="flex items-center justify-between border-b border-slate-800 pb-6 mb-6">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-xl bg-violet-500/10 border border-violet-500/20 flex items-center justify-center">
                    <svg className="w-6 h-6 text-violet-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-white">Sesión Activa</h3>
                    <p className="text-xs text-emerald-400 flex items-center gap-1 font-medium">
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span>
                      Autenticado vía OIDC
                    </p>
                  </div>
                </div>
                
                <div className="text-right">
                  <span className="text-[10px] uppercase tracking-wider font-semibold px-2.5 py-1 rounded bg-emerald-500/10 border border-emerald-500/20 text-emerald-400">
                    Access Token: ✓ Disponible
                  </span>
                </div>
              </div>

              {/* Mostrar datos del usuario (claims) */}
              <div className="space-y-4 mb-8">
                <div className="text-xs text-gray-500 uppercase tracking-widest font-semibold">Datos del Usuario (Claims ID Token)</div>
                
                <div className="grid grid-cols-1 gap-3">
                  <div className="p-3.5 rounded-xl bg-slate-800/30 border border-slate-800/80 flex items-center justify-between">
                    <span className="text-xs text-gray-400">Nombre completo</span>
                    <span className="text-sm font-semibold text-white">{profile.user.name}</span>
                  </div>

                  <div className="p-3.5 rounded-xl bg-slate-800/30 border border-slate-800/80 flex items-center justify-between">
                    <span className="text-xs text-gray-400">Username</span>
                    <span className="text-sm font-mono font-semibold text-violet-400">{profile.user.username}</span>
                  </div>

                  <div className="p-3.5 rounded-xl bg-slate-800/30 border border-slate-800/80 flex items-center justify-between">
                    <span className="text-xs text-gray-400">Correo electrónico</span>
                    <span className="text-sm font-semibold text-white">{profile.user.email}</span>
                  </div>
                </div>
              </div>

              {/* Boton para salir */}
              <button
                onClick={handleLogout}
                className="w-full inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl bg-slate-800 border border-slate-700/60 hover:bg-slate-700/80 text-gray-200 font-semibold text-sm transition-all transform hover:scale-[1.01] active:scale-[0.99] cursor-pointer"
              >
                <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
                </svg>
                Cerrar sesión (Logout)
              </button>
            </div>
          )}
        </div>

        <p className="text-center mt-6 text-[11px] text-gray-500 font-mono">
          Endpoint Protegido: <span className="text-violet-400">/api/profile</span>
        </p>
      </div>
    </div>
  );
}

export default App;
