import ReactMarkdown from "react-markdown"

function ResultsPanel({ result, loading }) {
  if (loading) {
    return (
      <div className="card results-card loading">
        <div className="spinner" />
        <p>Agent is researching your pulls...</p>
      </div>
    )
  }

  if (!result) {
    return (
      <div className="card results-card empty">
        <p>Your ROI breakdown will appear here</p>
      </div>
    )
  }

  return (
    <div className="card results-card">
      <h2>Analysis</h2>
      <div className="result-content">
        <ReactMarkdown>{result}</ReactMarkdown>
      </div>
    </div>
  )
}

export default ResultsPanel