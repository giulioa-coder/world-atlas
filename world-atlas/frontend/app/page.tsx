'use client'

import React, { useEffect, useState } from 'react'
import Link from 'next/link'
import { useWorldStore } from '@/stores/worldStore'
import { Button } from '@/components/ui/button'
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '@/components/ui/card'
import { Globe, Plus, Loader2, Map, Book, Users } from 'lucide-react'

export default function HomePage() {
  const { worlds, fetchWorlds, isLoading, error } = useWorldStore()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
    fetchWorlds()
  }, [fetchWorlds])

  if (!mounted) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Globe className="h-8 w-8 text-primary" />
              <div>
                <h1 className="text-2xl font-bold">World Atlas</h1>
                <p className="text-sm text-muted-foreground">Build your fictional worlds</p>
              </div>
            </div>
            <Link href="/new">
              <Button>
                <Plus className="mr-2 h-4 w-4" />
                Create World
              </Button>
            </Link>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {error && (
          <div className="mb-6 p-4 bg-destructive/10 border border-destructive rounded-lg text-destructive">
            {error}
          </div>
        )}

        {isLoading ? (
          <div className="flex justify-center py-12">
            <Loader2 className="h-8 w-8 animate-spin" />
          </div>
        ) : worlds.length === 0 ? (
          <div className="text-center py-12">
            <Globe className="mx-auto h-16 w-16 text-muted-foreground mb-4" />
            <h2 className="text-2xl font-semibold mb-2">No worlds yet</h2>
            <p className="text-muted-foreground mb-6">Create your first fictional world to get started</p>
            <Link href="/new">
              <Button size="lg">
                <Plus className="mr-2 h-4 w-4" />
                Create Your First World
              </Button>
            </Link>
          </div>
        ) : (
          <>
            <div className="mb-6">
              <h2 className="text-2xl font-semibold mb-2">Your Worlds</h2>
              <p className="text-muted-foreground">Manage and explore your created worlds</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {worlds.map((world) => (
                <Card key={world.id} className="hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-primary/10 rounded-lg">
                          <Globe className="h-6 w-6 text-primary" />
                        </div>
                        <div>
                          <CardTitle className="text-xl">{world.name}</CardTitle>
                          {world.genre && (
                            <p className="text-sm text-muted-foreground">{world.genre}</p>
                          )}
                        </div>
                      </div>
                      {world.is_demo && (
                        <span className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full">
                          Demo
                        </span>
                      )}
                    </div>
                  </CardHeader>
                  <CardContent>
                    {world.description && (
                      <CardDescription className="mb-4 line-clamp-2">
                        {world.description}
                      </CardDescription>
                    )}
                    
                    <div className="flex items-center gap-4 text-sm text-muted-foreground mb-4">
                      <div className="flex items-center gap-1">
                        <Map className="h-4 w-4" />
                        <span>Locations</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <Book className="h-4 w-4" />
                        <span>Manuscripts</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <Users className="h-4 w-4" />
                        <span>Characters</span>
                      </div>
                    </div>

                    <Link href={`/worlds/${world.id}`}>
                      <Button className="w-full">
                        Open World
                      </Button>
                    </Link>
                  </CardContent>
                </Card>
              ))}
            </div>
          </>
        )}
      </main>
    </div>
  )
}
