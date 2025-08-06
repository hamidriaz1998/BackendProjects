import requests

BASE_URL = "http://localhost:8000"


def test_api():
    print("🚀 Testing Blogging API")
    print("=" * 50)

    # Test root endpoint
    print("1. Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

    # Test health endpoint
    print("2. Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

    # Test Categories CRUD
    print("3. Testing Categories CRUD...")

    # Create categories
    categories = ["Technology", "Travel", "Food"]
    created_categories = []

    for cat_name in categories:
        response = requests.post(f"{BASE_URL}/categories/", json={"name": cat_name})
        print(f"Created category '{cat_name}': {response.status_code}")
        if response.status_code == 200:
            created_categories.append(response.json())

    # Get all categories
    response = requests.get(f"{BASE_URL}/categories/")
    print(f"Get all categories: {response.status_code}")
    print(f"Categories count: {len(response.json())}")
    print()

    # Test Tags CRUD
    print("4. Testing Tags CRUD...")

    # Create tags
    tags = ["python", "fastapi", "web-development", "tutorial"]
    created_tags = []

    for tag_name in tags:
        response = requests.post(f"{BASE_URL}/tags/", json={"name": tag_name})
        print(f"Created tag '{tag_name}': {response.status_code}")
        if response.status_code == 200:
            created_tags.append(response.json())

    # Get all tags
    response = requests.get(f"{BASE_URL}/tags/")
    print(f"Get all tags: {response.status_code}")
    print(f"Tags count: {len(response.json())}")
    print()

    # Test Posts CRUD
    print("5. Testing Posts CRUD...")

    # Create posts
    posts_data = [
        {
            "title": "Getting Started with FastAPI",
            "content": "FastAPI is a modern, fast web framework for building APIs with Python 3.7+.",
            "category": "Technology",
            "tags": ["python", "fastapi", "tutorial"],
        },
        {
            "title": "My Trip to Japan",
            "content": "An amazing journey through the land of the rising sun.",
            "category": "Travel",
            "tags": ["travel", "japan"],
        },
        {
            "title": "Best Italian Restaurants",
            "content": "A guide to the finest Italian cuisine in the city.",
            "category": "Food",
            "tags": ["food", "italian"],
        },
    ]

    created_posts = []
    for post_data in posts_data:
        response = requests.post(f"{BASE_URL}/posts/", json=post_data)
        print(f"Created post '{post_data['title']}': {response.status_code}")
        if response.status_code == 200:
            created_posts.append(response.json())

    # Get all posts
    response = requests.get(f"{BASE_URL}/posts/")
    print(f"Get all posts: {response.status_code}")
    print(f"Posts count: {len(response.json())}")
    print()

    # Test individual operations
    if created_posts:
        post_id = created_posts[0]["id"]

        # Get single post
        response = requests.get(f"{BASE_URL}/posts/{post_id}")
        print(f"Get post {post_id}: {response.status_code}")

        # Update post
        update_data = {
            "title": "Getting Started with FastAPI - Updated",
            "content": "FastAPI is a modern, fast web framework for building APIs with Python 3.7+. This is an updated version.",
            "tags": ["python", "fastapi", "web-development"],
        }
        response = requests.put(f"{BASE_URL}/posts/{post_id}", json=update_data)
        print(f"Update post {post_id}: {response.status_code}")

    if created_categories:
        cat_id = created_categories[0]["id"]
        # Get posts by category
        response = requests.get(f"{BASE_URL}/posts/category/{cat_id}")
        print(f"Get posts by category {cat_id}: {response.status_code}")
        print(f"Posts in category: {len(response.json())}")

    if created_tags:
        tag_id = created_tags[0]["id"]
        # Get posts by tag
        response = requests.get(f"{BASE_URL}/posts/tag/{tag_id}")
        print(f"Get posts by tag {tag_id}: {response.status_code}")
        print(f"Posts with tag: {len(response.json())}")

    print()
    print("✅ API Testing Complete!")
    print("Check your FastAPI docs at: http://localhost:8000/docs")


def test_error_cases():
    print("\n🔍 Testing Error Cases")
    print("=" * 30)

    # Test non-existent post
    response = requests.get(f"{BASE_URL}/posts/999")
    print(
        f"Get non-existent post: {response.status_code} - {response.json().get('detail', 'No error message')}"
    )

    # Test duplicate category
    response = requests.post(f"{BASE_URL}/categories/", json={"name": "Technology"})
    print(
        f"Create duplicate category: {response.status_code} - {response.json().get('detail', 'No error message')}"
    )

    # Test duplicate tag
    response = requests.post(f"{BASE_URL}/tags/", json={"name": "python"})
    print(
        f"Create duplicate tag: {response.status_code} - {response.json().get('detail', 'No error message')}"
    )


if __name__ == "__main__":
    try:
        test_api()
        test_error_cases()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API server.")
        print("Please make sure the server is running on http://localhost:8000")
        print("Run: python -m app.main")
    except Exception as e:
        print(f"❌ Error during testing: {e}")
