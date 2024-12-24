export const dynamic = 'force-static'

export async function Get() {
    
    const data = {data: "hello"}

    return Response.json({ data })

    
}