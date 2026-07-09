function formatTime(timestamp) {
    if (!timestamp) return null
    return new Date(timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
}

function MessageBubble({ role, content, timestamp }) {
    const time = formatTime(timestamp)

    return (
        <div className={`message ${role}`}>
            <span className="sender">{role === "coach" ? "Socra" : "You"}</span>
            <div className="bubble">{content}</div>
            {time && <span className="timestamp">{time}</span>}
        </div>
    )
}

export default MessageBubble