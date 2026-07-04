const BASE_URL = "http://localhost:8000"

export async function createSession(problemText) {
    const response = await fetch('${BASE_URL}/v1/session', {
        method: "POST",
        headers:  {
            "Content-Type" : "application/json"
        },
        body: JSON.stringfy({
            problem_text: problemText
        })
        
    })

    if (!response.ok) {
        throw new Error('Fail to create session: ${response.status}')
    }

    return await response.json()
}

export async function sendMessage(sessionId, content) {
    const response = await fetch('${BASE_URL}/v1/session/${sessionId}/message', {
        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringfy({
            content: content
        })
    })

    if (!response.ok) {
        throw new Error('Failed to send message: ${response.status}')
    }

    return await response.json()
}

export async function getSession(sessionId) {
    const response = await fetch('${BASE_URL}/v1/session/${sessionId}', {
        method: "GET",

        headers:{
            "Content-Type": "application/json"
        }
    })

    if(!response.ok){
        throw new Error('Failed to get session: ${response.status}')
    }

    return await response.json()
}



