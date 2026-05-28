"use client"

import { useRouter } from "next/navigation"
import { LogOut } from "lucide-react"
import { Button } from "@/components/ui/button"

export function LogoutButton() {
  const router = useRouter()

  function onLogout() {
    document.cookie = "auth=; path=/; max-age=0; samesite=lax"
    router.replace("/login")
  }

  return (
    <Button variant="ghost" size="sm" onClick={onLogout}>
      <LogOut className="h-4 w-4 mr-2" />
      Salir
    </Button>
  )
}
