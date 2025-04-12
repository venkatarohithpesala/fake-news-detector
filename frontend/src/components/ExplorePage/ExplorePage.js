import React, { useEffect, useState } from 'react';
import './ExplorePage.css'; // Import the CSS file
import { useNavigate } from 'react-router-dom';

const ExplorePage = () => {
    const [questions, setQuestions] = useState([]);
    const navigate = useNavigate();


    useEffect(() => {
        const supabaseUrl = process.env.REACT_APP_SUPABASE_URL;
        const supabaseKey = process.env.REACT_APP_SUPABASE_KEY;

        fetch(`${supabaseUrl}/rest/v1/questions?select=*`, {
            headers: {
                apikey: supabaseKey,
                Authorization: `Bearer ${supabaseKey}`
            }
        })
            .then(res => res.json())
            .then(data => setQuestions(data))
            .catch(err => console.error("Failed to fetch questions:", err));
    }, []);



    return (
        <div className="explore-container">
            <h2>Previously Asked Questions</h2>
            {questions.length === 0 ? (
                <p>Loading questions...</p>
            ) : (
                <ul style={{ listStyle: 'none', padding: 0 }}>
                    {questions.map(q => (
                        <li
                            key={q.id}
                            className="question-card"
                            onClick={() => navigate(`/question/${q.id}`)}
                            style={{ cursor: 'pointer' }}
                        >
                            <p className="question-title">🗒 {q.content.slice(0, 100)}...</p>
                            <p className="question-date">📅 {new Date(q.created_at).toLocaleString()}</p>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default ExplorePage;
