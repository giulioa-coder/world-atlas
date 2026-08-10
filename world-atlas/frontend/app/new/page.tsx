'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useWorldStore } from '@/stores/worldStore';
import { ArrowLeft, Loader2 } from 'lucide-react';

export default function NewWorldPage() {
  const router = useRouter();
  const { createWorld, isLoading } = useWorldStore();
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    genre: '',
  });
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    
    if (!formData.name.trim()) {
      setError('World name is required');
      return;
    }

    try {
      const world = await createWorld({
        name: formData.name,
        description: formData.description || undefined,
        genre: formData.genre || undefined,
      });
      router.push(`/worlds/${world.id}`);
    } catch (err: any) {
      setError(err.message || 'Failed to create world');
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto px-4 py-4 flex items-center gap-4">
          <Link href="/">
            <button className="p-2 hover:bg-accent rounded-md">
              <ArrowLeft className="h-5 w-5" />
            </button>
          </Link>
          <h1 className="text-xl font-bold">Create New World</h1>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 max-w-2xl">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="name" className="block text-sm font-medium mb-2">
              World Name *
            </label>
            <input
              id="name"
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className="w-full px-3 py-2 border rounded-md bg-background focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="e.g., Middle-earth, Westeros, Elarion"
              disabled={isLoading}
            />
          </div>

          <div>
            <label htmlFor="genre" className="block text-sm font-medium mb-2">
              Genre
            </label>
            <select
              id="genre"
              value={formData.genre}
              onChange={(e) => setFormData({ ...formData, genre: e.target.value })}
              className="w-full px-3 py-2 border rounded-md bg-background focus:outline-none focus:ring-2 focus:ring-primary"
              disabled={isLoading}
            >
              <option value="">Select a genre</option>
              <option value="fantasy">Fantasy</option>
              <option value="science_fiction">Science Fiction</option>
              <option value="historical_fiction">Historical Fiction</option>
              <option value="realistic_fiction">Realistic Fiction</option>
              <option value="alternate_history">Alternate History</option>
              <option value="mystery_thriller">Mystery/Thriller</option>
              <option value="post_apocalyptic">Post-Apocalyptic</option>
              <option value="other">Other</option>
            </select>
          </div>

          <div>
            <label htmlFor="description" className="block text-sm font-medium mb-2">
              Description
            </label>
            <textarea
              id="description"
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              className="w-full px-3 py-2 border rounded-md bg-background focus:outline-none focus:ring-2 focus:ring-primary min-h-[120px]"
              placeholder="Describe your world..."
              disabled={isLoading}
            />
          </div>

          {error && (
            <div className="p-3 bg-destructive/10 text-destructive rounded-md text-sm">
              {error}
            </div>
          )}

          <div className="flex gap-4 pt-4">
            <Link href="/">
              <button
                type="button"
                className="px-4 py-2 border rounded-md hover:bg-accent"
                disabled={isLoading}
              >
                Cancel
              </button>
            </Link>
            <button
              type="submit"
              className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 disabled:opacity-50 flex items-center gap-2"
              disabled={isLoading}
            >
              {isLoading && <Loader2 className="h-4 w-4 animate-spin" />}
              Create World
            </button>
          </div>
        </form>
      </main>
    </div>
  );
}
