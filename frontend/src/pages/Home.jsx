import { useState, useRef } from "react"
import { useNavigate } from "react-router-dom"
import { createSession } from "../services/api"

function Home() {
    const [started, setStarted] = useState(false)
    const [problemText, setProblemText] = useState("")
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const navigate = useNavigate()
    const textareaRef = useRef(null)

    async function handleGo() {
        if (!problemText.trim()) return
        setLoading(true)
        setError(null)
        try {
            const session = await createSession(problemText)
            navigate(`/session/${session.session_id}`, {
                state: { firstQuestion: session.content, hintLevel: session.hint_level }
            })
        } catch (err) {
            setError("Something went wrong. Please try again.")
        } finally {
            setLoading(false)
        }
    }

    function handleKeyDown(e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault()
            handleGo()
        }
    }

    function handleInput(e) {
        setProblemText(e.target.value)
        const el = textareaRef.current
        el.style.height = "auto"
        el.style.height = Math.min(el.scrollHeight, 200) + "px"
    }

    return (
        <div className="home">
            <h1>Socra</h1>
            <p>The insight isn't handed to you. It's discovered - one question at a time.</p>

            {!started ? (
                <button className="start-btn" onClick={() => setStarted(true)}>
                    Start Session
                </button>
            ) : (
                <div className="problem-input">
                    <textarea
                        ref={textareaRef}
                        placeholder="Paste your Leetcode problem here..."
                        value={problemText}
                        onInput={handleInput}
                        onKeyDown={handleKeyDown}
                        autoFocus
                    />
                    <button className="go-btn" onClick={handleGo} disabled={loading}>
                        {loading ? "..." : "Go"}
                    </button>
                </div>
            )}

            {error && <p className="error">{error}</p>}
        </div>
    )
}

export default Home