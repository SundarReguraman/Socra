import { useState, useEffect, useRef } from "react"
import { useParams, useLocation } from "react-router-dom"
import { sendMessage } from "../services/api"
import MessageBubble from "../components/MessageBubble"
import TypingIndicator from "../components/TypingIndicator"

function Session() {
    const { id } = useParams()
    const location = useLocation()
    const [messages, setMessages] = useState([])
    const [input, setInput] = useState("")
    const [loading, setLoading] = useState(false)
    const bottomRef = useRef(null)

    useEffect(() => {
        if (location.state?.firstQuestion) {
            setMessages([{
                role: "coach",
                content: location.state.firstQuestion,
                timestamp: Date.now()
            }])
        }
    }, [])

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth" })
    }, [messages, loading])

    async function handleSend() {
        if (!input.trim()) return

        const studentMessage = { role: "student", content: input, timestamp: Date.now() }
        setMessages(prev => [...prev, studentMessage])
        setInput("")
        setLoading(true)

        try {
            const response = await sendMessage(id, input)
            setMessages(prev => [...prev, {
                role: "coach",
                content: response.content,
                timestamp: Date.now()
            }])
        } catch (err) {
            setMessages(prev => [...prev, {
                role: "coach",
                content: "Something went wrong. Please try again.",
                timestamp: Date.now()
            }])
        } finally {
            setLoading(false)
        }
    }

    function handleKeyDown(e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault()
            handleSend()
        }
    }

    return (
        <div className="session">
            <div className="chat-window">
                {messages.map((msg, index) => (
                    <MessageBubble
                        key={index}
                        role={msg.role}
                        content={msg.content}
                        timestamp={msg.timestamp}
                    />
                ))}
                {loading && <TypingIndicator />}
                <div ref={bottomRef} />
            </div>

            <div className="input-area">
                <textarea
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Type your response..."
                    rows={1}
                    disabled={loading}
                />
                <button onClick={handleSend} disabled={loading}>
                    {loading ? "..." : "Send"}
                </button>
            </div>
        </div>
    )
}

export default Session