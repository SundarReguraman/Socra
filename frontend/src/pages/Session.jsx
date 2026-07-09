import { useState, useEffect, useRef } from "react"
import { useParams, useLocation } from "react-router-dom"
import { sendMessage } from "../services/api"
import MessageBubble from "../components/MessageBubble"

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
                content: location.state.firstQuestion
            }])
        }
    },[])

    useEffect(() => {
        bottomRef.current?.scrollIntoView({behavior: "smooth"})

    }, [messages])

    async function handleSend() {
        if (loading || !input.trim()) return

        const studentMessage = { role: "student", content: input }
        setMessages(prev => [...prev, studentMessage])
        setInput("")
        setLoading(true)

        try{
            const response = await sendMessage(id, input)
            setMessages(prev => [...prev, {
                role: "coach",
                content: response.content
            }])
        } catch (err){
            setMessages(prev => [...prev, {
                role: "coach",
                content: "Something went wrong. Please try again."
            }])

        } finally {
            setLoading(false)
        }
    }

    function handleKeyDown(e) {
        if (loading) return

        if (e.key == "Enter" && !e.shiftKey) {
            e.preventDefault()
            handleSend()
        }
    }

    return (
        <div className = "session">
            <div className="chat-window">
                {messages.map((msg, index) => (
                    <MessageBubble key = {index} role={msg.role} content= {msg.content} />
                ))}
                {loading && <div className = "loading"> Socra is thinking...</div>}
            <div ref = {bottomRef} />
        </div>

        <div className = "input-area">
            <textarea
                value = {input}
                onChange = {(e) => setInput(e.target.value)}
                onKeyDown = {handleKeyDown}
                placeholder = "Type your response..."
                rows = {3}
                disabled = {loading}
            />
            <button onClick = {handleSend} disabled = {loading}>
                {loading ? "..." : "Send"}
            </button>
        </div>
    </div>
    )
}
        
export default Session