import { useState } from "react"
import BreakForm from "./components/BreakForm"
import ResultsPanel from "./components/ResultsPanel"
import "./App.css"

function App() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  async function handleSubmit(breakData) {
    setLoading(true)
    setResult(null)

    try {
      const response = await fetch("http://127.0.0.1:8000/analyse", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(breakData)
      })
      const data = await response.json()
      setResult(data.result)
    } catch (err) {
      setResult("❌ Error connecting to backend. Is uvicorn running?")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header>
        <h1>🃏 JB Cards — Box Break ROI Analyst</h1>
        <p>Enter your pulls and get an instant ROI breakdown</p>
      </header>
      <main>
        <BreakForm onSubmit={handleSubmit} loading={loading} />
        <ResultsPanel result={result} loading={loading} />
      </main>
    </div>
  )
}

export default App