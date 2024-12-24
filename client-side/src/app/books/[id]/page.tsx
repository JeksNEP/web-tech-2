"use client"
import { useRouter } from "next/navigation"

export default async function BookPage({params}) {
    const paramsResolved = await params

    console.log(paramsResolved)

    return (<div>
        Book Page
    </div>)
}
