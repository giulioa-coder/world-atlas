'use client';

import { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import { useWorldStore } from '@/stores/worldStore';
import { MapCanvas } from '@/components/map/MapCanvas';
import { ArrowLeft, Loader2, MapPin, Book, Users, Settings } from 'lucide-react';

export default function WorldDetailPage() {
  const params = useParams();
  const router = useRouter();
  const worldId = params.id as string;
  const { currentWorld, fetchWorld, fetchLocations, locations, isLoading } = useWorldStore();
  const [activeTab, setActiveTab] = useState<'map' | 'locations' | 'manuscripts' | 'characters'>('map');

  useEffect(() => {
    if (worldId) {
      fetchWorld(worldId);
      fetchLocations(worldId);
    }
  }, [worldId]);

  if (!currentWorld && isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
        <span className="ml-2">Loading world...</span>
      </div>
    );
  }

  if (!currentWorld) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>World not found</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Header */}
      <header className="border-b bg-card">
        <div className="container mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <Link href="/">
                <button className="p-2 hover:bg-accent rounded-md">
                  <ArrowLeft className="h-5 w-5" />
                </button>
              </Link>
              <div>
                <h1 className="text-xl font-bold">{currentWorld.name}</h1>
                <p className="text-sm text-muted-foreground">
                  {currentWorld.genre?.replace('_', ' ') || 'Unknown genre'} • {locations.length} locations
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setActiveTab('map')}
                className={`px-3 py-2 rounded-md flex items-center gap-2 ${activeTab === 'map' ? 'bg-primary text-primary-foreground' : 'hover:bg-accent'}`}
              >
                <MapPin className="h-4 w-4" />
                Map
              </button>
              <button
                onClick={() => setActiveTab('locations')}
                className={`px-3 py-2 rounded-md flex items-center gap-2 ${activeTab === 'locations' ? 'bg-primary text-primary-foreground' : 'hover:bg-accent'}`}
              >
                <MapPin className="h-4 w-4" />
                Locations
              </button>
              <button
                onClick={() => setActiveTab('manuscripts')}
                className={`px-3 py-2 rounded-md flex items-center gap-2 ${activeTab === 'manuscripts' ? 'bg-primary text-primary-foreground' : 'hover:bg-accent'}`}
              >
                <Book className="h-4 w-4" />
                Manuscripts
              </button>
              <button
                onClick={() => setActiveTab('characters')}
                className={`px-3 py-2 rounded-md flex items-center gap-2 ${activeTab === 'characters' ? 'bg-primary text-primary-foreground' : 'hover:bg-accent'}`}
              >
                <Users className="h-4 w-4" />
                Characters
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 overflow-hidden">
        {activeTab === 'map' && (
          <div className="h-full w-full">
            <MapCanvas worldId={worldId} />
          </div>
        )}
        
        {activeTab === 'locations' && (
          <div className="container mx-auto px-4 py-6">
            <h2 className="text-2xl font-bold mb-4">Locations</h2>
            {locations.length === 0 ? (
              <p className="text-muted-foreground">No locations yet. Add them from the map editor.</p>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {locations.map((loc) => (
                  <div key={loc.id} className="border rounded-lg p-4">
                    <h3 className="font-semibold">{loc.name}</h3>
                    <p className="text-sm text-muted-foreground">{loc.location_type.replace('_', ' ')}</p>
                    {loc.description && (
                      <p className="text-sm mt-2 line-clamp-2">{loc.description}</p>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'manuscripts' && (
          <div className="container mx-auto px-4 py-6">
            <h2 className="text-2xl font-bold mb-4">Manuscripts</h2>
            <p className="text-muted-foreground">Upload your manuscript to auto-generate locations and maps.</p>
          </div>
        )}

        {activeTab === 'characters' && (
          <div className="container mx-auto px-4 py-6">
            <h2 className="text-2xl font-bold mb-4">Characters</h2>
            <p className="text-muted-foreground">Track character journeys across your world.</p>
          </div>
        )}
      </main>
    </div>
  );
}
