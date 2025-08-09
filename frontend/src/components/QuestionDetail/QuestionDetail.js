import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import "./QuestionDetail.css";

const QuestionDetail = () => {
  const { id } = useParams();
  const [question, setQuestion] = useState(null);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState("");

  useEffect(() => {
    const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
    const supabaseKey = process.env.REACT_APP_SUPABASE_KEY;

    // Fetch the selected question
    fetch(`${supabaseUrl}/rest/v1/questions?id=eq.${id}&select=*`, {
      headers: {
        apikey: supabaseKey,
        Authorization: `Bearer ${supabaseKey}`,
      },
    })
      .then((res) => res.json())
      .then((data) => setQuestion(data[0]));

    // Fetch comments
    fetch(`${supabaseUrl}/rest/v1/comments?question_id=eq.${id}&select=*`, {
      headers: {
        apikey: supabaseKey,
        Authorization: `Bearer ${supabaseKey}`,
      },
    })
      .then((res) => res.json())
      .then((data) => setComments(data));
  }, [id]);

  const handleCommentSubmit = (e) => {
    e.preventDefault();

    const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
    const supabaseKey = process.env.REACT_APP_SUPABASE_KEY;

    fetch(`${supabaseUrl}/rest/v1/comments`, {
      method: "POST",
      headers: {
        apikey: supabaseKey,
        Authorization: `Bearer ${supabaseKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question_id: id,
        comment: newComment,
      }),
    }).then(() => {
      setComments((prev) => [...prev, { comment: newComment }]);
      setNewComment("");
    });
  };

  if (!question) return <p>Loading...</p>;

  return (
    <div className="question-detail-container">
      <h2>🧠 Question Details</h2>
      <p>
        <strong>Original:</strong> {question.content}
      </p>
      {/* <p><strong>Fake Score:</strong> {question.fake_score}</p> */}
      <p>
        <strong>AI Explanation:</strong> {question.explanation}
      </p>

      <div className="comments-section">
        <h3>💬 Comments</h3>
        {comments.map((c, idx) => (
          <p key={idx}>🗨 {c.comment}</p>
        ))}

        <form onSubmit={handleCommentSubmit}>
          <textarea
            rows="3"
            placeholder="Leave an anonymous comment..."
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            required
          />
          <br />
          <button type="submit">Post Comment</button>
        </form>
      </div>
    </div>
  );
};

export default QuestionDetail;
