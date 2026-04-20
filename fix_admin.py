from app import app, db, User
from werkzeug.security import generate_password_hash

def fix_admin():
    with app.app_context():
        # Ensure tables exist
        db.create_all()
        
        username = "er.tushar07@gmail.com"
        password = "889763"
        
        user = User.query.filter_by(username=username).first()
        if user:
            print(f"Update: User {username} exists. Updating password.")
            user.password_hash = generate_password_hash(password)
        else:
            print(f"Creating User {username}...")
            hashed_pw = generate_password_hash(password)
            new_admin = User(username=username, password_hash=hashed_pw)
            db.session.add(new_admin)
            
        db.session.commit()
        print(f"[+] Admin account updated/created successfully!")

if __name__ == '__main__':
    fix_admin()
