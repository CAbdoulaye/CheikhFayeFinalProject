from flask import Flask, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from db import create_tables, register_user, login_user, add_review, get_reviews_by_movie

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


moviesDict = {
    "Titanic" : {
        "link" : "titanic",
        "description" : "The RMS Titanic, a British passenger liner, met a tragic fate on April 15, 1912. During its maiden voyage from Southampton to New York, the ship struck an iceberg in the North Atlantic Ocean and sank. The disaster resulted in the loss of over 1,500 lives. Despite being equipped with advanced safety features for its time, inadequate lifeboat capacity and a lack of efficient communication contributed to the high casualty toll. The sinking of the Titanic remains one of the most infamous maritime disasters in history, prompting improvements in maritime safety regulations and capturing the public's imagination for decades to come."
    },
    "Jaws" : {
        "link" : "jaws",
        "description" : "Jaws is a 1975 thriller film directed by Steven Spielberg. Based on Peter Benchley's novel, it follows Police Chief Martin Brody (Roy Scheider), marine biologist Matt Hooper (Richard Dreyfuss), and shark hunter Quint (Robert Shaw) as they attempt to hunt down a great white shark that is terrorizing the fictional resort town of Amity Island. The film became a blockbuster and is known for its suspenseful atmosphere and the iconic music score composed by John Williams. Jaws not only defined the summer blockbuster but also instilled a fear of sharks in popular culture, leaving a lasting impact on cinema."
    },
    "Avatar" : {
        "link" : "avatar",
        "description" : "Avatar is a 2009 science fiction film directed by James Cameron. Set in the mid-22nd century on the fictional moon Pandora, the story follows Jake Sully (played by Sam Worthington), a paralyzed former Marine who becomes an Avatar operator. Avatars are genetically engineered human-Na'vi hybrids used to interact with the indigenous Na'vi people on Pandora. As Jake infiltrates the Na'vi community, he finds himself torn between loyalty to humanity and empathy for the Na'vi. The film is known for its groundbreaking visual effects, 3D technology, and immersive world-building. Avatar became the highest-grossing film of all time until it was surpassed by Avengers: Endgame in 2019."
    },
    "Avengers" : {
        "link" : "avengers",
        "description" : "Avatar is a 2009 science fiction film directed by James Cameron. Set in the mid-22nd century on the fictional moon Pandora, the story follows Jake Sully (played by Sam Worthington), a paralyzed former Marine who becomes an Avatar operator. Avatars are genetically engineered human-Na'vi hybrids used to interact with the indigenous Na'vi people on Pandora. As Jake infiltrates the Na'vi community, he finds himself torn between loyalty to humanity and empathy for the Na'vi. The film is known for its groundbreaking visual effects, 3D technology, and immersive world-building. Avatar became the highest-grossing film of all time until it was surpassed by Avengers: Endgame in 2019."
    },
    "Home Alone" : {
        "link" : "homeAlone",
        "description" : "Avatar is a 2009 science fiction film directed by James Cameron. Set in the mid-22nd century on the fictional moon Pandora, the story follows Jake Sully (played by Sam Worthington), a paralyzed former Marine who becomes an Avatar operator. Avatars are genetically engineered human-Na'vi hybrids used to interact with the indigenous Na'vi people on Pandora. As Jake infiltrates the Na'vi community, he finds himself torn between loyalty to humanity and empathy for the Na'vi. The film is known for its groundbreaking visual effects, 3D technology, and immersive world-building. Avatar became the highest-grossing film of all time until it was surpassed by Avengers: Endgame in 2019."
    },
    "Jurassic Park" : {
        "link" : "jurassicPark",
        "description" : "Avatar is a 2009 science fiction film directed by James Cameron. Set in the mid-22nd century on the fictional moon Pandora, the story follows Jake Sully (played by Sam Worthington), a paralyzed former Marine who becomes an Avatar operator. Avatars are genetically engineered human-Na'vi hybrids used to interact with the indigenous Na'vi people on Pandora. As Jake infiltrates the Na'vi community, he finds himself torn between loyalty to humanity and empathy for the Na'vi. The film is known for its groundbreaking visual effects, 3D technology, and immersive world-building. Avatar became the highest-grossing film of all time until it was surpassed by Avengers: Endgame in 2019."
    },
    "Lion King" : {
        "link" : "lionKing",
        "description" : "Avatar is a 2009 science fiction film directed by James Cameron. Set in the mid-22nd century on the fictional moon Pandora, the story follows Jake Sully (played by Sam Worthington), a paralyzed former Marine who becomes an Avatar operator. Avatars are genetically engineered human-Na'vi hybrids used to interact with the indigenous Na'vi people on Pandora. As Jake infiltrates the Na'vi community, he finds himself torn between loyalty to humanity and empathy for the Na'vi. The film is known for its groundbreaking visual effects, 3D technology, and immersive world-building. Avatar became the highest-grossing film of all time until it was surpassed by Avengers: Endgame in 2019."
    },
    "Shrek" : {
        "link" : "shrek",
        "description" : "Avatar is a 2009 science fiction film directed by James Cameron. Set in the mid-22nd century on the fictional moon Pandora, the story follows Jake Sully (played by Sam Worthington), a paralyzed former Marine who becomes an Avatar operator. Avatars are genetically engineered human-Na'vi hybrids used to interact with the indigenous Na'vi people on Pandora. As Jake infiltrates the Na'vi community, he finds himself torn between loyalty to humanity and empathy for the Na'vi. The film is known for its groundbreaking visual effects, 3D technology, and immersive world-building. Avatar became the highest-grossing film of all time until it was surpassed by Avengers: Endgame in 2019."
    },
    "Star Wars" : {
        "link" : "starWars",
        "description" : "Avatar is a 2009 science fiction film directed by James Cameron. Set in the mid-22nd century on the fictional moon Pandora, the story follows Jake Sully (played by Sam Worthington), a paralyzed former Marine who becomes an Avatar operator. Avatars are genetically engineered human-Na'vi hybrids used to interact with the indigenous Na'vi people on Pandora. As Jake infiltrates the Na'vi community, he finds himself torn between loyalty to humanity and empathy for the Na'vi. The film is known for its groundbreaking visual effects, 3D technology, and immersive world-building. Avatar became the highest-grossing film of all time until it was surpassed by Avengers: Endgame in 2019."
    },
    "The Dark Knight" : {
        "link" : "theDarkKnight",
        "description" : "Avatar is a 2009 science fiction film directed by James Cameron. Set in the mid-22nd century on the fictional moon Pandora, the story follows Jake Sully (played by Sam Worthington), a paralyzed former Marine who becomes an Avatar operator. Avatars are genetically engineered human-Na'vi hybrids used to interact with the indigenous Na'vi people on Pandora. As Jake infiltrates the Na'vi community, he finds himself torn between loyalty to humanity and empathy for the Na'vi. The film is known for its groundbreaking visual effects, 3D technology, and immersive world-building. Avatar became the highest-grossing film of all time until it was surpassed by Avengers: Endgame in 2019."
    },
    "Jurassic World" : {
        "link" : "jurassicWorld",
        "description" : "Avatar is a 2009 science fiction film directed by James Cameron. Set in the mid-22nd century on the fictional moon Pandora, the story follows Jake Sully (played by Sam Worthington), a paralyzed former Marine who becomes an Avatar operator. Avatars are genetically engineered human-Na'vi hybrids used to interact with the indigenous Na'vi people on Pandora. As Jake infiltrates the Na'vi community, he finds himself torn between loyalty to humanity and empathy for the Na'vi. The film is known for its groundbreaking visual effects, 3D technology, and immersive world-building. Avatar became the highest-grossing film of all time until it was surpassed by Avengers: Endgame in 2019."
    }
}


# Form functions
def validate_registration_form(username, email, password, confirm_password):
    if not username or not email or not password or not confirm_password:
        flash('All fields are required.', 'danger')
        return False

    if password != confirm_password:
        flash('Passwords do not match.', 'danger')
        return False

    # Add more validation as needed

    return True


def validate_login_form(username, password):
    if not username or not password:
        flash('All fields are required.', 'danger')
        return False

    # Add more validation as needed

    return True


def validate_review_form(movie_title, review_text):
    if not movie_title or not review_text:
        flash('All fields are required.', 'danger')
        return False

    # Add more validation as needed

    return True

# ... (your other code)


# Routes for user authentication
# Routes for user authentication
# Routes for user authentication
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in request.cookies:
        return redirect(url_for('index'))

    if request.method == 'POST':
        form = (
            request.form['username'],
            request.form['email'],
            request.form['password'],
            request.form['confirm_password']  # Include the confirm_password field
        )

        if validate_registration_form(*form):
            # Update the function call to pass all four parameters
            result = register_user(form[0], form[1], form[2], form[3])

            if result:
                flash('Registration successful! You can now log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('Registration failed. Username or email already exists.', 'danger')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in request.cookies:
        return redirect(url_for('index'))

    if request.method == 'POST':
        form = (
            request.form['username'],
            request.form['password']
        )

        if validate_login_form(*form):
            user = login_user(*form)

            if user:
                flash('Login successful!', 'success')
                response = redirect(url_for('index'))
                response.set_cookie('user_id', str(user[0]))
                return response
            else:
                flash('Login failed. Check your username and password.', 'danger')

    return render_template('login.html')


# Route for adding reviews
# Route for adding reviews
@app.route('/add_review/<movie_title>', methods=['GET', 'POST'])
def add_review_route(movie_title):
    if 'user_id' not in request.cookies:
        flash('You need to log in to add a review.', 'danger')
        return redirect(url_for('login'))

    user_id = int(request.cookies.get('user_id'))

    if request.method == 'POST':
        form = (
            movie_title,  # Pass the movie_title from the URL
            request.form['review_text']
        )

        if validate_review_form(*form):
            add_review(user_id, *form)
            flash('Review added successfully!', 'success')
            return redirect(url_for('index'))

    return render_template('add_review.html', movie_title=movie_title)


@app.route('/logout')
def logout():
    # Clear the user_id cookie to log the user out
    response = redirect(url_for('index'))
    response.delete_cookie('user_id')
    flash('Logout successful!', 'success')
    return response


@app.route('/')
def index():
    return render_template('index.html')  # Adjust the template name as needed

# ... (your other code)


@app.route('/movies')
def movie_list():
    return render_template('movie_list.html')


# Route for displaying reviews for a specific movie
@app.route('/movie/<movie_title>')
def movie_reviews(movie_title):
    # Fetch reviews for the specified movie from the database
    reviews = get_reviews_by_movie(movie_title)
    reviews = [review[0] for review in reviews]
    print("name")
    print(movie_title)
    info = moviesDict[movie_title]
    image_link = info["link"]
    print(image_link)
    movie_description = info["description"]
    arr = [movie_title, image_link, movie_description, reviews]
    return render_template('movie_reviews.html', arr=arr)

if __name__ == '__main__':
    create_tables()  # Ensure that the database tables are created before running the app
    app.run(debug=True)

