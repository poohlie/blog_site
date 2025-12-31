from flask import Flask, render_template, request, redirect, url_for
from models import db, Post

app = Flask(__name__)
# Configure the SQLite database, relative to the app instance folder
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

# --- Routes ---

@app.route('/')
def index():
    """Display the list of all blog posts."""
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    """Display a single blog post."""
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=['GET', 'POST'])
def create():
    """Handle creating new blog posts (simple admin route)."""
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title, content=content)

        try:
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return 'There was an issue adding your post.'
    else:
        # GET request: show the creation form
        return render_template('create.html')

# --- Initial Setup ---

def create_db():
    """
    Function to create the database file and tables.
    Run this once before the first run.
    """
    with app.app_context():
        db.create_all()
        # Optional: Add a sample post
        if not Post.query.first():
            from datetime import datetime
            sample_post = Post(
                title='Hello World - The Digital Rain',
                content="""
                Welcome to the digital realm. This blog uses a minimalist, Matrix-inspired theme, 
                designed for clarity amidst the code. Look closely at the screen... do you see the code?
                """,
                date_posted=datetime.now()
            )
            db.session.add(sample_post)
            db.session.commit()
            print("Database created and sample post added.")

if __name__ == '__main__':
    # You would typically run create_db() once in a separate setup script,
    # but for simplicity, we'll call it here before running the app.
    create_db()
    app.run(debug=True)