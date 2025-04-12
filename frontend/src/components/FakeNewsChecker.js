import React, { useState } from "react";
import "./FakeNewsChecker.css";

const FakeNewsChecker = () => {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    setError("");

    try {
      const response = await fetch("http://localhost:5000/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      const data = await response.json();

      if (response.ok) {
        setResult(data);
      } else {
        setError(data.error || "Something went wrong");
      }
    } catch (err) {
      setError("Server not reachable");
    }

    setLoading(false);
  };

  return (
    <div className="container">

      <form onSubmit={handleSubmit} className="form">
        <textarea
          className="textarea"
          placeholder="Ask a question or paste a news headline..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          required
        />
        <button type="submit" className="button" disabled={loading}>
          {loading ? "Checking..." : "Check Now"}
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      {result && (
        <div className="resultBox">
          <h3>🤖 AI Opinion</h3>
          <p>{result.explanation}</p>
        </div>
      )}
    </div>
  );
};

export default FakeNewsChecker;
