import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import FakeNewsChecker from './components/FakeNewsChecker/FakeNewsChecker';
import ExplorePage from './components/ExplorePage/ExplorePage';
import QuestionDetail
 from './components/QuestionDetail/QuestionDetail';
function App() {
  return (
    <Router>
      <div style={{ padding: '2rem' }}>
        {/* <h2>📰 Fake News Detector</h2> */}
        <Routes>
          <Route path="/" element={<FakeNewsChecker />} />
          <Route path="/explore" element={<ExplorePage />} />
          <Route path="/question/:id" element={<QuestionDetail />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
