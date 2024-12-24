import {NextRequest,NextResponse} from "next/server"

export async function GET(req: NextRequest){
    return proxyRequest(req);
}

export async function POST(req: NextRequest){
    return proxyRequest(req);
}

export async function PUT(req: NextRequest){
    return proxyRequest(req);
}


export async function DELETE(req: NextRequest){
    return proxyRequest(req);
}

async function proxyRequest(req: NextRequest){
    const targetUrl = `http://localhost:8000/${req.nextUrl.pathname.split("/").slice(2).join("/")}`
    try {
        const response = await fetch(targetUrl, {
            method: req.method,
            body: req.body,
            headers: {
                host: "http://localhost:8000/"
            }
        })
        
        const data = await response.json()
        return new NextResponse(JSON.stringify(data), {status: response.status})

    } catch(e){
        console.error("Proxing error", e)
        return new NextResponse("Server error", {status: 500})
    }
}