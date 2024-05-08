## ConnectX: Your Social Media Hub with PostgreSQL Database

This project implements a basic social media platform with functionalities such as user authentication, posting, commenting, liking, and friending.

### Files

- **main.py**: Entry point of the application. Orchestrates the execution of other Python files based on user requirements.
- **signIn.py**: Handles user authentication, allowing existing users to log in.
- **signUp.py**: Enables users to create new accounts by providing necessary information.
- **profile_page.py**: Manages user profile-related functionalities such as viewing posts and interacting with friends.
- **public_page.py**: Handles functionalities related to public content, including viewing and interacting with posts.
- **post_page.py**: Manages posting, liking, commenting, and sharing functionalities.

### Folders

- **src**: Contains all the Python files implementing the functionalities of the social media platform.
- **database**: Contains SQL files for database schema definition and data population.

### Dependencies

- **Python 3.x**
- **psycopg2** (for PostgreSQL database interaction)

### Database Setup

1. Clone the repository to your local machine.
2. Set up the database using PostgreSQL's command-line interface (`psql`):
   - Open a terminal or command prompt.
   - Navigate to the directory containing the SQL files (`populate.sql`) in the `database` folder of the cloned repository.
   - Log in to your PostgreSQL server using the `psql` command and provide necessary authentication credentials:
     ```
     psql -U your_username -h your_host_address
     ```
     Replace `your_username` and `your_host_address` with your PostgreSQL username and host address, respectively.
   - Once logged in, run the SQL script to create the database schema and populate it with initial data:
     ```
     \i populate.sql
     ```
     This script defines the database schema and automatically calls `populate-data.sql` to insert initial data into the tables.
3. After setting up the database, run `main.py` to start the social media platform.
4. Follow the prompts and instructions provided by `main.py` to navigate through different functionalities.

### Contributors

- Sanchi Sujith Kumar
- Pilli Hamsini
- Palaparthi Revanth
- Sahitya Chinta

### Demo Video

[Watch Demo Video](https://youtu.be/Ongxgm564SI)