"""
Comprehensive API tests for World Atlas backend.
Run with: python test_api.py
"""

from fastapi.testclient import TestClient
from app.main import app

def run_tests():
    client = TestClient(app, raise_server_exceptions=False)
    
    print("=" * 60)
    print("TEST COMPLETI BACKEND WORLD ATLAS")
    print("=" * 60)
    
    # Test 1: Health endpoint
    response = client.get('/health')
    assert response.status_code == 200, f"Health check failed: {response.status_code}"
    print('✅ 1. Health endpoint funziona')
    
    # Test 2: Create World
    response = client.post('/api/v1/worlds/', json={'name': 'Test World', 'genre': 'fantasy'})
    assert response.status_code == 201, f"Create world failed: {response.status_code}"
    world = response.json()
    world_id = world['id']
    print(f'✅ 2. Creato mondo: {world["name"]}')
    
    # Test 3: Get World
    response = client.get(f'/api/v1/worlds/{world_id}/')
    assert response.status_code == 200, f"Get world failed: {response.status_code}"
    print('✅ 3. Lettura mondo funziona')
    
    # Test 4: Update World
    response = client.put(f'/api/v1/worlds/{world_id}/', json={'name': 'Updated World'})
    assert response.status_code == 200, f"Update world failed: {response.status_code}"
    print('✅ 4. Aggiornamento mondo funziona')
    
    # Test 5: Create Location
    response = client.post(f'/api/v1/locations/worlds/{world_id}/', json={
        'name': 'Test City',
        'location_type': 'city',
        'latitude': 45.0,
        'longitude': 10.0
    })
    assert response.status_code == 201, f"Create location failed: {response.status_code}"
    location = response.json()
    location_id = location['id']
    print(f'✅ 5. Creata località: {location["name"]}')
    
    # Test 6: List Locations
    response = client.get(f'/api/v1/locations/worlds/{world_id}/')
    assert response.status_code == 200, f"List locations failed: {response.status_code}"
    print('✅ 6. Lista località funziona')
    
    # Test 7: Update Location
    response = client.put(f'/api/v1/locations/{location_id}', json={
        'name': 'Updated City',
        'description': 'Test description'
    })
    assert response.status_code == 200, f"Update location failed: {response.status_code}"
    print('✅ 7. Aggiornamento località funziona')
    
    # Test 8: Delete Location
    response = client.delete(f'/api/v1/locations/{location_id}')
    assert response.status_code == 204, f"Delete location failed: {response.status_code}"
    print('✅ 8. Eliminazione località funziona')
    
    # Test 9: Create Manuscript (stub)
    response = client.post(f'/api/v1/worlds/{world_id}/manuscripts/', json={
        'title': 'Test Manuscript',
        'file_type': 'txt'
    })
    assert response.status_code == 201, f"Create manuscript failed: {response.status_code}"
    print('✅ 9. Creato manoscritto (stub)')
    
    # Test 10: Create Character
    response = client.post(f'/api/v1/worlds/{world_id}/characters/', json={
        'name': 'Test Character'
    })
    assert response.status_code == 201, f"Create character failed: {response.status_code}"
    print('✅ 10. Creato personaggio')
    
    # Test 11: Delete World
    response = client.delete(f'/api/v1/worlds/{world_id}/')
    assert response.status_code == 204, f"Delete world failed: {response.status_code}"
    print('✅ 11. Eliminazione mondo funziona')
    
    print("\n" + "=" * 60)
    print("✅✅✅ TUTTI I 11 TEST API SONO PASSATI ✅✅✅")
    print("=" * 60)
    return True

if __name__ == "__main__":
    try:
        run_tests()
    except AssertionError as e:
        print(f"\n❌ TEST FALLITO: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ ERRORE IMPREVISTO: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
