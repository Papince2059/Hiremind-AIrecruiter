import React, { useState, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";

function InterviewCompleted() {
  const navigate = useNavigate();
  const location = useLocation();
  const [showAnalysis, setShowAnalysis] = useState(false);
  const [interviewData, setInterviewData] = useState(null);

  useEffect(() => {
    // Get interview data from navigation state
    if (location.state?.interviewData) {
      setInterviewData(location.state.interviewData);
    }
    
    // Show analysis after 3 seconds
    const timer = setTimeout(() => {
      setShowAnalysis(true);
    }, 3000);

    return () => clearTimeout(timer);
  }, [location.state]);

  if (showAnalysis && interviewData) {
    // Show the analysis page
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center p-6">
        <div className="bg-white rounded-lg shadow-lg p-6 max-w-4xl w-full">
          <h1 className="text-2xl font-semibold text-gray-800 mb-6 text-center">
            Candidate Analysis Report
          </h1>
          
          {/* Analysis content will be displayed here */}
          <div className="text-center py-8">
            <div className="text-green-600 text-6xl mb-4">✅</div>
            <h2 className="text-xl font-semibold text-gray-700 mb-2">
              Analysis Complete
            </h2>
            <p className="text-gray-600 mb-6">
              The candidate analysis has been generated and is available in the recruiter portal.
            </p>
            <div className="flex gap-4 justify-center">
              <button
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                onClick={() => navigate("/dashboard")}
              >
                Go to Dashboard
              </button>
              <button
                className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
                onClick={() => navigate("/completed-links")}
              >
                View Analysis
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Show the celebratory completion page
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-6">
      {/* Confetti animation */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden">
        {[...Array(30)].map((_, i) => (
          <div
            key={i}
            className="absolute animate-pulse"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 50}%`,
              backgroundColor: ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3'][Math.floor(Math.random() * 6)],
              width: `${Math.random() * 8 + 4}px`,
              height: `${Math.random() * 8 + 4}px`,
              borderRadius: Math.random() > 0.5 ? '50%' : '0%',
              animationDelay: `${Math.random() * 3}s`,
              animationDuration: `${3 + Math.random() * 2}s`,
              transform: `rotate(${Math.random() * 360}deg)`
            }}
          />
        ))}
      </div>

      {/* Main content */}
      <div className="bg-white rounded-xl shadow-xl p-8 max-w-md w-full text-center relative z-10">
        {/* Office illustration */}
        <div className="mb-6">
          <div className="w-32 h-24 mx-auto bg-gray-200 rounded-lg flex items-end justify-center relative">
            <div className="w-16 h-16 bg-blue-500 rounded-lg mb-2"></div>
            <div className="absolute -bottom-2 left-4 w-8 h-8 bg-yellow-500 rounded-full"></div>
            <div className="absolute -bottom-2 right-4 w-8 h-8 bg-pink-500 rounded-full"></div>
          </div>
        </div>

        {/* Title with confetti emoji */}
        <h1 className="text-3xl font-bold text-green-600 mb-2">
          Interview Completed 🎉
        </h1>

        {/* Message */}
        <p className="text-gray-600 mb-8">
          Thank you for completing the interview. Your responses have been successfully submitted!
        </p>

        {/* Button */}
        <button
          className="w-full bg-green-600 text-white py-3 px-6 rounded-lg hover:bg-green-700 transition-colors font-medium"
          onClick={() => setShowAnalysis(true)}
        >
          Go to Dashboard
        </button>
      </div>
    </div>
  );
}

export default InterviewCompleted;
