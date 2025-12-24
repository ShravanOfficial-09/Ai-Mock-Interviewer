console.log("JavaScript Loaded!");

let currentQuestion = "Tell me about your technical strengths.";

window.onload = () => {
  document.getElementById("register-btn").addEventListener("click", registerUser);
  document.getElementById("login-btn").addEventListener("click", loginUser);
  document.getElementById("logout-btn").addEventListener("click", logoutUser);
  document.getElementById("upload-resume-btn").addEventListener("click", uploadResume);
  document.getElementById("generate-question-btn").addEventListener("click", generateQuestion);
  document.getElementById("submit-response-btn").addEventListener("click", submitInterviewResponse);
  document.getElementById("next-question-btn").addEventListener("click", nextQuestion);
  document.getElementById("start-voice-btn").addEventListener("click", startVoiceRecognition);
};

// Register User
async function registerUser() {
  const username = document.getElementById("username").value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!username || !email || !password) {
    alert("Please fill all registration fields.");
    return;
  }

  const res = await fetch("http://127.0.0.1:8000/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email, password }),
  });

  const result = await res.json();
  document.getElementById("register-message").innerText = result.message || result.detail || "Registration failed.";
}

// Login User
async function loginUser() {
  const email = document.getElementById("login-email").value.trim();
  const password = document.getElementById("login-password").value.trim();

  if (!email || !password) {
    alert("Please fill all login fields.");
    return;
  }

  const res = await fetch("http://127.0.0.1:8000/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  const result = await res.json();
  document.getElementById("login-message").innerText = result.message || result.detail || "Login failed.";
}

// Logout User
function logoutUser() {
  alert("Logout successful!");
  document.getElementById("logout-message").innerText = "Logged out.";
}

// Upload Resume
async function uploadResume() {
  const fileInput = document.getElementById("resume-file");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select a resume file.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch("http://127.0.0.1:8000/upload-resume/", {
      method: "POST",
      body: formData,
    });

    const result = await res.json();

    if (res.ok) {
      document.getElementById("resume-message").innerText = `📄 Uploaded: ${file.name}`;

      const question = result.question || "❌ No question generated.";
      const skills = result.skills || [];

      currentQuestion = question;

      document.getElementById("question-text").innerHTML = `<strong>Q:</strong> ${question}`;
      document.getElementById("generated-question").innerText = `🛠️ Skills: ${skills.join(", ") || "None found."}`;

      console.log("Extracted Skills:", skills);
    } else {
      throw new Error(result.detail || "Resume processing failed.");
    }
  } catch (error) {
    console.error("Resume upload error:", error);
    alert("❌ Resume upload failed. Try again.");
    document.getElementById("resume-message").innerText = "❌ Upload failed.";
  }
}

// Generate Question
async function generateQuestion() {
  const domain = document.getElementById("language-select").value;
  const difficulty = document.getElementById("difficulty-select").value;

  try {
    const res = await fetch(`http://127.0.0.1:8000/generate-question/?domain=${domain}&difficulty=${difficulty}`);
    const result = await res.json();

    const question = result?.question || "❌ Failed to generate question. Please try again.";

    document.getElementById("generated-question").innerText = `👉 ${question}`;
    document.getElementById("question-text").innerHTML = `<strong>Q:</strong> ${question}`;
    currentQuestion = question;
  } catch (error) {
    console.error("Error fetching question:", error);
    document.getElementById("generated-question").innerText = "❌ Error generating question.";
    document.getElementById("question-text").innerHTML = `<strong>Q:</strong> Please try again later.`;
    currentQuestion = "";
  }
}

// Submit Interview Response
async function submitInterviewResponse() {
  const candidate_name = document.getElementById("candidate-name").value.trim();
  const response = document.getElementById("candidate-response").value.trim();

  if (!candidate_name || !response) {
    alert("Please enter name and response.");
    return;
  }

  const res = await fetch("http://127.0.0.1:8000/process_response/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ candidate_name, response }),
  });

  const result = await res.json();

  if (res.ok) {
    document.getElementById("response-message").innerText =
      `✅ Submitted!\nScore: ${result.data.score}%\nFeedback: ${result.data.feedback}`;
  } else {
    alert(result.detail || "❌ Submission failed.");
  }
}

// Next Question
function nextQuestion() {
  generateQuestion();
  document.getElementById("candidate-response").value = "";
  document.getElementById("response-message").innerText = "";
}

// Voice Recognition
function startVoiceRecognition() {
  if (!("webkitSpeechRecognition" in window)) {
    alert("Speech Recognition not supported in your browser!");
    return;
  }

  const recognition = new webkitSpeechRecognition();
  recognition.lang = "en-US";
  recognition.start();

  recognition.onresult = function (event) {
    const transcript = event.results[0][0].transcript;
    document.getElementById("candidate-response").value = transcript;
  };

  recognition.onerror = function (event) {
    console.error("Voice recognition error:", event.error);
    alert("Voice recognition error occurred.");
  };
}

