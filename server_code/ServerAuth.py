import anvil.server
import anvil.users

@anvil.server.callable
def get_current_user_role():
  user = anvil.users.get_user()
  if user:
    return user['role']
  return None
