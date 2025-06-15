import React, { useState } from 'react';
import axios from 'axios';
import './senti.css';

function Form() {
  const [text, setText] = useState('');
  const [sentiment, setSentiment] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const onSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setSentiment(null);
    setError(null);
    try {
      const { data } = await axios.post('/api/v1/analyze', { text });
      console.log(data);
      
      setSentiment(data.sentiment);
      setLoading(false);
    } catch (error) {
      console.log(error);
      setError('Error analyzing sentiment. Please try again.');
      setLoading(false);
    }
  };

  return (
    <div className='sentiment-analyzer'>
      <h1 className='title'>Sentiment Analyser</h1>
      <form onSubmit={onSubmit} className='form'>
        <label htmlFor='text-input'>Enter your text:</label>
        <textarea
          id='text-input'
          className='textarea'
          rows='10'
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder='Enter your text'
        />
        <button
          type='submit'
          className='button'
          disabled={loading || text.trim() === ''}
        >
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
      </form>
      {error && <div className='error'>{error}</div>}
      {sentiment && (
        <div className={`result ${sentiment.toLowerCase()}`}>
          <h2>Sentiment Result:</h2>
          <p>{sentiment}</p>
        </div>
      )}
    </div>
  );
}

export default Form;