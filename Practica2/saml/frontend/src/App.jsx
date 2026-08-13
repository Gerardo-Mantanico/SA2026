import React, { useState, useEffect } from 'react';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8001';

function App() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Pedir los datos de sesion al backend SAML
    fetch(`${BACKEND_URL}/api/profile`, { credentials: 'include' })
      .then((res) => {
        if (res.status === 401) {
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
    // Redirige al login SAML de la app
    window.location.href = `${BACKEND_URL}/login`;
  };

  const handleLogout = () => {
    // Redirige para borrar sesion SAML
    window.location.href = `${BACKEND_URL}/logout`;
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-[#070c15] via-[#0b0f19] to-[#1e293b]">
        <div className="relative">
          <div className="w-16 h-16 border-4 border-cyan-500/30 border-t-cyan-500 rounded-full animate-spin"></div>
          <div className="absolute inset-0 flex items-center justify-center text-xs font-semibold text-cyan-400">SAML</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#070c15] via-[#090d16] to-[#0f172a] flex flex-col items-center justify-center p-4">
      {/* Fondo con luces difuminadas */}
      <div className="absolute top-1/4 left-1/3 w-96 h-96 bg-cyan-600/10 rounded-full filter blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-1/4 right-1/3 w-96 h-96 bg-blue-600/10 rounded-full filter blur-[120px] pointer-events-none"></div>

      <div className="w-full max-w-2xl relative z-10 my-8">
        {/* Titulo */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-xs font-medium text-cyan-400 mb-3 animate-pulse">
            <span className="w-2 h-2 rounded-full bg-cyan-400"></span>
            SAML 2.0 Service Provider (SP)
          </div>
          <h1 className="text-4xl font-extrabold tracking-tight text-white sm:text-5xl">
            Protocolo <span className="bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">SAML 2.0</span>
          </h1>
          <p className="mt-3 text-sm text-gray-400 max-w-md mx-auto">
            Demostración de federación empresarial y Single Sign-On (SSO) con Keycloak.
          </p>
        </div>

        {/* Tarjeta principal */}
        <div className="bg-slate-900/60 backdrop-blur-xl border border-slate-800/80 shadow-2xl rounded-2xl p-8 relative overflow-hidden">
          {/* Borde brillante superior */}
          <div className="absolute top-0 inset-x-0 h-[2px] bg-gradient-to-r from-transparent via-cyan-500/50 to-transparent"></div>

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
            <div className="text-center py-6 max-w-md mx-auto">
              <div className="w-20 h-20 bg-slate-850/50 border border-slate-700/50 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-inner">
                <svg className="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"/>
                </svg>
              </div>

              <div className="mb-8">
                <h3 className="text-lg font-semibold text-white">Sin autenticar</h3>
                <p className="text-sm text-gray-400 mt-1">
                  Tu sesión no está activa. Por favor, inicia sesión para acceder a tu perfil protegido por SAML.
                </p>
              </div>

              <button
                onClick={handleLogin}
                className="w-full inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-50 hover:to-blue-500 text-white font-semibold text-sm transition-all transform hover:scale-[1.01] shadow-lg shadow-cyan-500/20 active:scale-[0.99] cursor-pointer"
              >
                <svg className="w-4 h-4 text-white animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"/>
                </svg>
                Iniciar sesión con Keycloak (SAML)
              </button>
            </div>
          ) : (
            /* SI ESTA LOGUEADO */
            <div>
              <div className="flex items-center justify-between border-b border-slate-800 pb-6 mb-6">
                <div className="flex items-center gap-3">
                  <div className="w-12 h-12 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center">
                    <svg className="w-6 h-6 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-white">Sesión Activa</h3>
                    <p className="text-xs text-cyan-400 flex items-center gap-1 font-medium">
                      <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-ping"></span>
                      Autenticado vía SAML SP
                    </p>
                  </div>
                </div>
                
                <span className="text-[10px] uppercase tracking-wider font-semibold px-2.5 py-1 rounded bg-cyan-500/10 border border-cyan-500/20 text-cyan-400">
                  SAML Assertion: ✓ Procesada
                </span>
              </div>

              {/* Contenedor de datos y metadatos */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                {/* Datos del usuario */}
                <div className="space-y-4">
                  <div className="text-xs text-gray-500 uppercase tracking-widest font-semibold">Atributos del Usuario</div>
                  
                  <div className="space-y-3">
                    <div className="p-3 rounded-xl bg-slate-850 border border-slate-800 flex flex-col justify-center">
                      <span className="text-[10px] text-gray-400 uppercase">Nombre</span>
                      <span className="text-sm font-semibold text-white mt-0.5">{profile.user.name}</span>
                    </div>

                    <div className="p-3 rounded-xl bg-slate-850 border border-slate-800 flex flex-col justify-center">
                      <span className="text-[10px] text-gray-400 uppercase">Username</span>
                      <span className="text-sm font-mono font-semibold text-cyan-400 mt-0.5">{profile.user.username}</span>
                    </div>

                    <div className="p-3 rounded-xl bg-slate-850 border border-slate-800 flex flex-col justify-center">
                      <span className="text-[10px] text-gray-400 uppercase">Email</span>
                      <span className="text-sm font-semibold text-white mt-0.5">{profile.user.email}</span>
                    </div>
                  </div>
                </div>

                {/* Detalles de la Assertion SAML */}
                <div className="space-y-4">
                  <div className="text-xs text-gray-500 uppercase tracking-widest font-semibold">Metadata de la Assertion</div>
                  
                  <div className="space-y-3">
                    <div className="p-3 rounded-xl bg-slate-850 border border-slate-800 flex flex-col justify-center">
                      <span className="text-[10px] text-gray-400 uppercase">Subject NameID</span>
                      <span className="text-xs font-mono font-semibold text-white mt-0.5 truncate" title={profile.assertion.subject_name_id}>
                        {profile.assertion.subject_name_id}
                      </span>
                    </div>

                    <div className="p-3 rounded-xl bg-slate-850 border border-slate-800 flex flex-col justify-center">
                      <span className="text-[10px] text-gray-400 uppercase">Issuer (Emisor IdP)</span>
                      <span className="text-xs font-mono font-semibold text-gray-300 mt-0.5 truncate" title={profile.assertion.issuer}>
                        {profile.assertion.issuer}
                      </span>
                    </div>

                    <div className="p-3 rounded-xl bg-slate-850 border border-slate-800 flex flex-col justify-center">
                      <span className="text-[10px] text-gray-400 uppercase">Validez de la Assertion</span>
                      <div className="text-[10px] text-gray-300 mt-1 space-y-0.5">
                        <p><span className="text-gray-500">NotBefore:</span> {profile.assertion.not_before}</p>
                        <p><span className="text-gray-500">NotOnOrAfter:</span> {profile.assertion.not_on_or_after}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Boton para salir */}
              <div className="flex gap-4">
                <button
                  onClick={handleLogout}
                  className="flex-1 inline-flex items-center justify-center gap-2 px-6 py-3.5 rounded-xl bg-slate-800 border border-slate-700/60 hover:bg-slate-700/80 text-gray-200 font-semibold text-sm transition-all transform hover:scale-[1.01] active:scale-[0.99] cursor-pointer"
                >
                  <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
                  </svg>
                  Cerrar sesión (SLO)
                </button>
              </div>
            </div>
          )}
        </div>

        {/* Enlace metadatos */}
        <div className="text-center mt-6 flex justify-center gap-4 text-xs font-mono">
          <a
            href={`${BACKEND_URL}/saml/metadata`}
            target="_blank"
            rel="noopener noreferrer"
            className="text-cyan-400 hover:text-cyan-300 underline"
          >
            Ver SP Metadata XML (público)
          </a>
          <span className="text-gray-600">|</span>
          <span className="text-gray-500">Endpoint Protegido: /api/profile</span>
        </div>
      </div>
    </div>
  );
}

export default App;
