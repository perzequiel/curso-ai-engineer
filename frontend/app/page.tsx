import { PRList } from "@/components/pr-list"
import { LogoutButton } from "@/components/logout-button"

export default function Home() {
  return (
    <main className="min-h-screen bg-background">
      <div className="container mx-auto py-8 px-4">
        <div className="flex justify-end mb-2">
          <LogoutButton />
        </div>
        <PRList />
      </div>
    </main>
  )
}
