import anvil.users
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.email

@anvil.server.callable
def create_user_account(name, email, password, role):
  # 1. Create the actual Anvil user
  user = anvil.users.signup_with_email(email, password)
  # 2. Get the UID (string)
  uid = user.get_id()

  # 3. Add profile row to user_profiles
  app_tables.user_profiles.add_row(,          # store UID as text
    name=name,
    email=email,
    role=role,
    status="pending" if role == "admin" else "approved"
  )

  return uid
