import { useState } from "react"

const EMPTY_PULL = { player: "", parallel: "" }

function BreakForm({ onSubmit, loading }) {
  const [box, setBox] = useState("")
  const [costGbp, setCostGbp] = useState("")
  const [pulls, setPulls] = useState([{ ...EMPTY_PULL }])

  function addPull() {
    setPulls([...pulls, { ...EMPTY_PULL }])
  }

  function removePull(index) {
    setPulls(pulls.filter((_, i) => i !== index))
  }

  function updatePull(index, field, value) {
    const updated = [...pulls]
    updated[index][field] = value
    setPulls(updated)
  }

  function handleSubmit() {
    if (!box || !costGbp || pulls.some(p => !p.player)) return
    onSubmit({ box, cost_gbp: parseFloat(costGbp), pulls })
  }

  return (
    <div className="card form-card">
      <h2>Break Details</h2>

      <div className="field">
        <label>Box / Set</label>
        <input
          type="text"
          placeholder="e.g. Topps Chrome UEFA 2023"
          value={box}
          onChange={e => setBox(e.target.value)}
        />
      </div>

      <div className="field">
        <label>Box Cost (£)</label>
        <input
          type="number"
          placeholder="e.g. 85"
          value={costGbp}
          onChange={e => setCostGbp(e.target.value)}
        />
      </div>

      <div className="pulls-section">
        <h3>Pulls</h3>
        {pulls.map((pull, index) => (
          <div key={index} className="pull-row">
            <input
              type="text"
              placeholder="Player name"
              value={pull.player}
              onChange={e => updatePull(index, "player", e.target.value)}
            />
            <input
              type="text"
              placeholder="Parallel e.g. Gold Refractor /50"
              value={pull.parallel}
              onChange={e => updatePull(index, "parallel", e.target.value)}
            />
            {pulls.length > 1 && (
              <button className="remove-btn" onClick={() => removePull(index)}>✕</button>
            )}
          </div>
        ))}
        <button className="add-btn" onClick={addPull}>+ Add Pull</button>
      </div>

      <button
        className="submit-btn"
        onClick={handleSubmit}
        disabled={loading}
      >
        {loading ? "Analysing..." : "Run Analysis"}
      </button>
    </div>
  )
}

export default BreakForm