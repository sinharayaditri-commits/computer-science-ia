@anvil.server.callable
def create_user_account(name, email, password, role):
  from anvil.tables import app_tables

  # 1. Create the Anvil user
  user = anvil.users.signup_with_email(email, password)

  # 2. Check if row already exists for this anvil_user
  existing = app_tables.users.get(anvil_user=user)
  if existing:
    # update instead of creating duplicates
    existing['name'] = name
    existing['role'] = role
    existing['status'] = "pending" if role == "admin" else "approved"
    return existing.get_id()

    # 3. Create new row (NO email column here!)
  row = app_tables.users.add_row(
    anvil_user=user,
    name=name,
    role=role,
    status="pending" if role == "admin" else "approved"
  )

  return row.get_id()
