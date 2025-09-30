import React, { useState, useEffect, useRef } from "react";
import {
  useParams,
  useLocation,
  useSearchParams,
  useNavigate,
} from "react-router-dom";
import Vapi from "@vapi-ai/web";
import ErrorBoundary from "../components/ErrorBoundary";
import AlertConfirmation from "../components/AlertConfirmation";
import { toast } from "react-toastify";

function InterviewRoom() {
  const { id } = useParams();
  const [searchParams] = useSearchParams();
  const location = useLocation();
  const navigate = useNavigate();
  const vapiRef = useRef(null);
  const startTimeRef = useRef(null);
  const [isInterviewStarted, setIsInterviewStarted] = useState(false);
  const [questions, setQuestions] = useState([]);
  const [userName, setUserName] = useState(
    location.state?.userName || searchParams.get("name") || "Candidate"
  );
  const [jobTitle, setJobTitle] = useState("Interview");
  const [duration, setDuration] = useState("15 Min");
  const [isLoading, setIsLoading] = useState(true);
  const [time, setTime] = useState("00:00:00");
  const [activeUser, setActiveUser] = useState(true);
  const [conversation, setConversation] = useState([]);
  const conversationRef = useRef([]);
  const [feedback, setFeedback] = useState(null);

  useEffect(() => {
    console.log("InterviewRoom useEffect triggered");
    console.log("Location state:", location.state);
    console.log("Interview ID:", id);
    
    setIsLoading(true);
    const initialInfo = location.state?.interviewInfo || location.state;
    if (initialInfo && initialInfo.interviewData) {
      console.log("Using navigation state interviewInfo:", initialInfo);
      setUserName(initialInfo.userName || userName);
      setQuestions(initialInfo.interviewData.questionList || []);
      setJobTitle(initialInfo.interviewData.jobTitle || "Interview");
      setDuration(initialInfo.interviewData.duration || "15 Min");
      setIsLoading(false);
    } else {
      console.log("No navigation state, fetching data for id:", id);
      fetch(`http://localhost:8080/api/interviews/${id}`, {
        method: "GET",
        credentials: "include",
        headers: { "Content-Type": "application/json" },
      })
        .then((res) => {
          if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
          return res.json();
        })
        .then((data) => {
          console.log("API Response in InterviewRoom:", data);
          
          // Better question parsing
          let parsedQuestions = [];
          try {
            if (data.questions) {
              const questionsData = JSON.parse(data.questions);
              if (questionsData.question && Array.isArray(questionsData.question)) {
                parsedQuestions = questionsData.question.map(q => q.text || q.question || q).filter(q => q);
              }
            }
          } catch (e) {
            console.log("Could not parse questions JSON, using fallback");
          }
          
          // Fallback questions if parsing failed
          if (parsedQuestions.length === 0) {
            parsedQuestions = [
              `What is your experience with ${data.job_title || data.jobTitle || 'this role'}?`,
              `Describe a challenging project you worked on related to ${data.job_title || data.jobTitle || 'this field'}.`,
              `How do you stay updated with the latest trends in ${data.job_title || data.jobTitle || 'this field'}?`,
              `What tools and technologies do you use for ${data.job_title || data.jobTitle || 'this role'}?`,
              `Tell me about a time you had to learn a new technology.`
            ];
          }
          
          console.log("Final parsed questions:", parsedQuestions);
          setQuestions(parsedQuestions);
          setJobTitle(data.job_title || data.jobTitle || "Interview");
          setDuration(data.duration || "15 Min");
          setIsLoading(false);
        })
        .catch((err) => {
          console.error("Error fetching interview data:", err.message);
          setQuestions([
            `What is your experience with ${jobTitle}?`,
            `Describe a challenging project you worked on.`,
            `How do you stay updated with the latest trends?`,
            `What tools and technologies do you use?`,
            `Tell me about a time you had to learn a new technology.`
          ]);
          setIsLoading(false);
        });
    }

    const timer = setInterval(() => {
      if (isInterviewStarted && startTimeRef.current) {
        const elapsed = Math.floor((Date.now() - startTimeRef.current) / 1000);
        const hours = String(Math.floor(elapsed / 3600)).padStart(2, "0");
        const minutes = String(Math.floor((elapsed % 3600) / 60)).padStart(
          2,
          "0"
        );
        const seconds = String(elapsed % 60).padStart(2, "0");
        setTime(`${hours}:${minutes}:${seconds}`);
      } else if (!isInterviewStarted) {
        setTime("00:00:00");
      }
    }, 1000);

    const vapi =
      vapiRef.current || new Vapi("710b92d8-20aa-4191-b966-795efe3d816d");
    vapiRef.current = vapi;

    vapi.on("call-start", () => {
      console.log("Call started");
      setIsInterviewStarted(true);
      startTimeRef.current = Date.now();
      toast("Call Connected...");
    });
    vapi.on("call-end", () => {
      console.log("Call has ended.");
      toast("Interview Ended");
      GenerateFeedback();
    });
    vapi.on("speech-start", () => {
      console.log("Assistant speech has started.");
      setActiveUser(false);
      toast("Assistant speaking...");
    });
    vapi.on("speech-end", () => {
      console.log("Assistant speech has ended.");
      setActiveUser(true);
      toast("Your turn to speak...");
    });
    vapi.on("message", (message) => {
      if (message?.conversation) {
        console.log("Message received:", message.conversation);
        setConversation(message.conversation);
        conversationRef.current = message.conversation;
      } else {
        console.warn("Received undefined conversation!");
      }
    });

    vapi.on("error", (error) => {
      console.error("Vapi error:", error);
      if (error.message && error.message.includes("Invalid Key")) {
        toast.error("Voice service API key is invalid. Please contact support.");
      } else if (error.message && error.message.includes("Unauthorized")) {
        toast.error("Voice service authentication failed. Please contact support.");
      } else {
        toast.error(`Voice service error: ${error.message || 'Unknown error'}`);
      }
    });

    return () => clearInterval(timer);
  }, [id, location.state, userName]);

  const startInterview = async () => {
    console.log("Start interview clicked!");
    console.log("Vapi ref:", vapiRef.current);
    console.log("Is interview started:", isInterviewStarted);
    console.log("Questions:", questions);
    
    if (vapiRef.current && !isInterviewStarted) {
      if (questions.length === 0) {
        console.error("Cannot start interview: No questions available");
        toast.error("No questions available.");
        return;
      }

      // Check microphone permission first
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        console.log("Microphone access granted");
        stream.getTracks().forEach(track => track.stop()); // Stop the test stream
        toast.success("Microphone access confirmed!");
      } catch (error) {
        console.error("Microphone access denied:", error);
        toast.error("Microphone access is required for the interview. Please allow microphone access and try again.");
        return;
      }

      // Add fallback questions if none available
      const finalQuestions = questions.length > 0 ? questions : [
        `What is your experience with ${jobTitle}?`,
        `Describe a challenging project you worked on.`,
        `How do you stay updated with the latest trends?`,
        `What tools and technologies do you use?`,
        `Tell me about a time you had to learn a new technology.`
      ];

      const assistantOptions = {
        name: "AI Recruiter",
        firstMessage: `Hi ${userName}, how are you? Ready for your interview on ${jobTitle}?`,
        transcriber: {
          provider: "deepgram",
          model: "nova-2",
          language: "en-US",
        },
        voice: { provider: "playht", voiceId: "jennifer" },
        model: {
          provider: "openai",
          model: "gpt-4",
          messages: [
            {
              role: "system",
              content: `
            You are an AI voice assistant conducting interviews for a ${jobTitle} position.
            Begin with a friendly introduction. Ask one question at a time from: ${finalQuestions
              .map((q, i) => `${i + 1}. ${typeof q === 'string' ? q : q.text || q.question || 'No question text'}`)
              .join("\n")}.
            Offer hints if needed, provide feedback, and wrap up after 5-7 questions.
            Keep it natural, engaging, and focused on ${jobTitle}.
          `.trim(),
            },
          ],
        },
      };

      console.log("Questions being used in interview:", finalQuestions);
      console.log("Job title:", jobTitle);
      console.log(
        "Assistant Options with questions:",
        JSON.stringify(assistantOptions, null, 2)
      );
      
      // Add error handling and user feedback
      toast.info("Starting interview... Connecting to voice service...");
      
      vapiRef.current.start(assistantOptions).catch((error) => {
        console.error("Vapi start error:", error);
        
        // Check for specific error types
        if (error.message && error.message.includes("Invalid Key")) {
          toast.error("Voice service configuration issue. The voice service API key is invalid. Please contact support.");
        } else if (error.message && error.message.includes("Unauthorized")) {
          toast.error("Voice service authentication failed. Please contact support.");
        } else if (error.message && error.message.includes("Permission")) {
          toast.error("Microphone permission denied. Please allow microphone access and try again.");
        } else {
          toast.error(`Failed to start interview: ${error.message || 'Unknown error'}`);
        }
        
        // Show additional help
        setTimeout(() => {
          toast.info("Tip: Check browser console for detailed error information.");
        }, 2000);
      });
    } else {
      console.error("Cannot start interview:", {
        vapiRef: !!vapiRef.current,
        isInterviewStarted,
        questions: questions.length
      });
      toast.error("Cannot start interview. Please check your microphone permissions.");
    }
  };

  const stopInterview = () => {
    if (vapiRef.current) {
      vapiRef.current.stop();
      console.log("Interview stopped");
      setIsInterviewStarted(false);
      startTimeRef.current = null;
      toast("Interview Ended.");
    }
  };

  const GenerateFeedback = () => {
    const conv = conversationRef.current;

    if (conv.length > 0) {
      console.log("Generating feedback with conversation:", conv);
      GenerateFeedbackForm(conv);
    } else {
      console.warn("No conversation data available for feedback.");
      toast.warn("No conversation data to generate feedback.");
      navigate("/completed", {
        state: {
          interviewData: {
            id: id,
            jobTitle: jobTitle,
            userName: userName,
            duration: time
          }
        }
      });
    }
  };

  const GenerateFeedbackForm = (conv) => {
    console.log("Opening feedback form with:", conv);
    const payload = {
      interviewId: id,
      userName: userName,
      conversation: conv,
      duration: time,
    };
    console.log("Sending payload:", JSON.stringify(payload, null, 2));
    fetch(`http://localhost:8080/api/interviews/${id}/feedback`, {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
        return res.json();
      })
      .then((data) => {
        setFeedback(data.feedback);
        toast.success("Feedback submitted!");
        navigate("/completed", {
          state: {
            interviewData: {
              id: id,
              jobTitle: jobTitle,
              userName: userName,
              duration: time,
              feedback: data.feedback
            }
          }
        });
      })
      .catch((err) => {
        console.error("Error submitting feedback:", err.message);
        toast.error("Failed to submit feedback.");
        navigate("/completed", {
          state: {
            interviewData: {
              id: id,
              jobTitle: jobTitle,
              userName: userName,
              duration: time
            }
          }
        });
      });
  };

  if (isLoading) return <div className="p-6 text-center">Loading...</div>;

  return (
    <ErrorBoundary>
      <div className="h-screen bg-gray-100 flex flex-col items-center justify-start p-4">
        <div className="w-full flex justify-between items-center mb-6">
          <h1 className="text-xl font-semibold text-gray-800">
            AI Interview Session
          </h1>
          <div className="flex items-center gap-2 text-gray-600 text-sm font-medium">
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              viewBox="0 0 24 24"
            >
              <path d="M12 6v6l4 2" />
            </svg>
            <span>{time}</span>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-6 w-full max-w-4xl mb-8">
          <div className="bg-white rounded-lg shadow-md flex flex-col items-center justify-center p-8 h-64">
            <div className="relative">
              {!activeUser && (
                <span className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 rounded-full bg-blue-500 opacity-75 animate-ping w-16 h-16" />
              )}
              <img
                src="https://randomuser.me/api/portraits/women/44.jpg"
                alt="AI Recruiter"
                className="w-16 h-16 rounded-full object-cover z-10"
              />
            </div>
            <p className="text-gray-700 font-medium mt-2">AI Recruiter</p>
          </div>

          <div className="bg-white rounded-lg shadow-md flex flex-col items-center justify-center p-8 h-64">
            <div className="relative">
              {activeUser && (
                <span className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 rounded-full bg-green-500 opacity-75 animate-ping w-16 h-16" />
              )}
              <div className="w-16 h-16 rounded-full bg-blue-600 text-white flex items-center justify-center text-2xl z-10">
                {userName.charAt(0).toUpperCase()}
              </div>
            </div>
            <p className="text-gray-700 font-medium mt-2">{userName}</p>
          </div>
        </div>

        <div className="flex gap-4">
          {!isInterviewStarted ? (
            <button
              onClick={startInterview}
              className="bg-gray-700 hover:bg-gray-800 text-white rounded-full p-3"
            >
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                viewBox="0 0 24 24"
              >
                <path d="M12 4v16m8-8H4" />
              </svg>
            </button>
          ) : (
            <AlertConfirmation stopInterview={stopInterview}>
              <button className="bg-red-600 hover:bg-red-700 text-white rounded-full p-3">
                <svg
                  className="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  viewBox="0 0 24 24"
                >
                  <path d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </AlertConfirmation>
          )}
        </div>
        
        {/* Debug Information */}
        <div className="mt-4 p-4 bg-gray-50 rounded-lg text-sm">
          <p><strong>Debug Info:</strong></p>
          <p>Questions loaded: {questions.length}</p>
          <p>Job Title: {jobTitle}</p>
          <p>User Name: {userName}</p>
          <p>Vapi Ready: {vapiRef.current ? 'Yes' : 'No'}</p>
          <p>Interview Started: {isInterviewStarted ? 'Yes' : 'No'}</p>
          <p>Microphone Permission: {navigator.permissions ? 'Check console' : 'Not available'}</p>
          <div className="mt-2 p-2 bg-yellow-50 border border-yellow-200 rounded">
            <p className="text-xs text-yellow-800">
              <strong>Note:</strong> If the interview doesn't start, check the browser console for errors. 
              The voice service may require a valid API key. Microphone permission is required.
            </p>
          </div>
          <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded">
            <p className="text-xs text-red-800">
              <strong>Known Issue:</strong> The Vapi API key is invalid. Voice interviews won't work until a valid key is provided.
            </p>
          </div>
        </div>

        <p className="text-sm text-gray-500 mt-2">
          {isInterviewStarted
            ? "Interview in Progress..."
            : "Click Start to begin"}
        </p>
      </div>
    </ErrorBoundary>
  );
}

export default InterviewRoom;
