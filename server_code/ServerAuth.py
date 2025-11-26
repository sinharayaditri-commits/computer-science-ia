import anvil
import anvil.users
from anvil.tables import app_tables

@anvil.server.callable
def create_user_account(name, email, password, role):

  # 1. Create the Anvil user
  user = anvil.users.signup_with_email(email, password)

  # 2. Add profile entry
  app_tables.user_profiles.add_row(
    anvil_user=user,
    name=name,
    email=email,
    role=role,
    status="pending" if role == "admin" else "approved"
  )

  return user





