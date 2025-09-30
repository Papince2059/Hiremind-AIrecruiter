import React from "react";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const navigate = useNavigate();

  const handleLogin = async (provider) => {
    try {
      // For now, we'll use a simple mock authentication
      // In production, this would integrate with actual OAuth2 providers
      console.log(`Logging in with ${provider}...`);
      
      // Set authentication flag in localStorage
      localStorage.setItem('isAuthenticated', 'true');
      localStorage.setItem('userProvider', provider);
      
      console.log('Authentication set, redirecting to dashboard...');
      
      // Direct redirect to dashboard
      window.location.href = '/dashboard';
    } catch (error) {
      console.error("Login error:", error);
      alert("Login failed. Please try again.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-sm bg-white p-8 rounded-2xl shadow-xl space-y-6 text-center">
        <h1 className="text-3xl font-bold text-gray-800">Login</h1>
        <p className="text-gray-600 text-sm">
          Click any button to continue (Mock Authentication)
        </p>

        <button
          onClick={() => handleLogin("google")}
          className="w-full bg-red-500 hover:bg-red-600 text-white py-2 px-4 rounded-lg transition-colors"
        >
          Continue with Google
        </button>

        <button
          onClick={() => handleLogin("github")}
          className="w-full bg-gray-800 hover:bg-black text-white py-2 px-4 rounded-lg transition-colors"
        >
          Continue with GitHub
        </button>
        
        <div className="mt-4 p-2 bg-gray-100 rounded text-xs">
          <p>Debug: Check browser console for login messages</p>
          <p>Current auth status: {localStorage.getItem('isAuthenticated') || 'Not set'}</p>
        </div>
      </div>
    </div>
  );
};

export default Login;
