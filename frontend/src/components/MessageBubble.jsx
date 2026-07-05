function MessageBubble({ role, content }) {
    return (
        <div className={'message ${role}'}>
            <span className="sender"> {role === "coach" ? "Socra" : "You"} </span>
            <p>{content}</p>
        </div>
    )
}

export default MessageBubble
