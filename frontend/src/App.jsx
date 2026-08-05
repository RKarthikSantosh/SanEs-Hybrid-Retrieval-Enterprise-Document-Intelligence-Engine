import { useEffect, useState } from 'react'

function App() {
  const [health, setHealth] = useState('Loading backend status...')

  useEffect(() => {
    const controller = new AbortController()

    async function loadHealth() {
      try {
        const response = await fetch('http://127.0.0.1:8000/health', {
          signal: controller.signal,
        })

        if (!response.ok) {
          throw new Error(`Request failed with status ${response.status}`)
        }

        const data = await response.json()
        setHealth(`Backend response: ${JSON.stringify(data)}`)
      } catch (error) {
        if (error.name !== 'AbortError') {
          setHealth(`Backend request failed: ${error.message}`)
        }
      }
    }

    loadHealth()

    return () => controller.abort()
  }, [])

  return (
    <main className="min-h-screen bg-slate-950 text-slate-50">
      <div className="mx-auto flex min-h-screen max-w-4xl items-center justify-center px-6 py-16">
        <section className="w-full rounded-3xl border border-white/10 bg-white/5 p-8 shadow-2xl shadow-cyan-950/20 backdrop-blur">
          <p className="mb-4 text-sm uppercase tracking-[0.35em] text-cyan-300">
            Hybrid Retrieval Enterprise Document Intelligence Engine
          </p>
          <h1 className="text-4xl font-semibold tracking-tight text-white sm:text-5xl">
            Hybrid Retrieval Enterprise Document Intelligence Engine
          </h1>
          <p className="mt-6 text-lg leading-8 text-slate-300">
            {health}
          </p>
        </section>
      </div>
    </main>
  )
}

export default App
