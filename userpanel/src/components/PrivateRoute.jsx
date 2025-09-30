import React, { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";

const PrivateRoute = ({ element }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(null); // null = loading
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simple localStorage check for demo authentication
    const isLoggedIn = localStorage.getItem('isAuthenticated') === 'true';
    setIsAuthenticated(isLoggedIn);
    setLoading(false);
  }, []);

  if (loading) return <div className="flex items-center justify-center min-h-screen">Loading...</div>;

  return isAuthenticated ? element : <Navigate to="/login" />;
};

export default PrivateRoute;
