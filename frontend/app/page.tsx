import { PRList } from "@/components/pr-list"

export default function Home() {
  return (
    <main className="min-h-screen bg-background">
      <div className="container mx-auto py-8 px-4">
        <PRList />
      </div>
    </main>
  )
}
