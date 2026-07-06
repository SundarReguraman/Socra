import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { createSession } from "../services/api"

function Home() {
    const [problemText, setProblemText] = useState("")
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const navigate = useNavigate()

    async function handleStart() {
        if(!problemText.trim()) return 

        setLoading(true)
        setError(null)

        try {
            const session = await createSession(problemText)
            navigate(`/session/${session.session_id}`, {
                state:{
                    firstQuestion: session.content,
                    hintLevel: session.hint_level
                }
            })
        } catch (err) {
            setError("Something went wrong. Please try again.")

        } finally{
            setLoading(false)
        }
    }

    return (
        <div className = "home">
            <h1>Socra</h1>
            <p>The insight isn't handed to you. It's discovered - one question at a time.</p>

            <textarea
                placeholder = "Paste your Leetcode problem here..."
                value = {problemText}
                onChange={(e) => setProblemText(e.target.value)}
                rows = {10}
            />

            {error && <p className = "error">{error}</p>}

            <button onClick = {handleStart} disabled = {loading}>
                {loading ? "Starting..." : "Start Session"}
            </button>

        </div>
    )
}
export default Home