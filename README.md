# CMS Application API

This is a RESTful API for a CMS (Content Management System) application. It provides CRUD operations for managing users, posts/blogs, and likes.

## Features

- User Management: Create, read, update, and delete users.
- Post/Blog Management: Create, read, update, and delete posts/blogs.
- Like Management: Create, read, update, and delete likes.
- Access Control:
  - Public and private posts/blogs: Any user can access the GET API for public posts/blogs. Only the owner can access private posts/blogs.
  - PUT and DELETE API access restricted to the owner of the post/blog.
- Retrieve Number of Likes: The GET all post/blog API also returns the number of likes for each post/blog.
- Single Query: Retrieval of both the post/blog and its likes is completed within a single query.

## Technologies Used

- Python
- Django (Web framework)
- Django REST Framework (API framework)
- sqlite (Database)

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/DK-SAINI/cms_project.git
   ```
2. Navigate to the project directory:
	
	```bash
	cd cms_project
	```

3. Create and activate a virtual environment:
	
	```bash
	python3 -m venv env
	source env/bin/activate
	```

4. Install the dependencies:
	
	```bash
	pip install -r requirments.txt
	```
5. Apply database migrations:

	```bash
	python manage.py migrate
	```
6. Run the development server:
	
	```bash
	python manage.py runserver
	```
7. The API is now accessible at `http://localhost:8000`.


## API Documentation

The API documentation and endpoints can be found in the [API documentation file](https://documenter.getpostman.com/view/22783737/2s93m4Xhax).
