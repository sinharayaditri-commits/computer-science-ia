import anvil
import anvil.users
from anvil.tables import app_tables
import datetime

@anvil.server.callable
def create_user_account(name, email, password, role):
  """Create a new user account with profile"""
  try:
    user = anvil.users.signup_with_email(email, password)
    user_row = app_tables.users.get(email=email)
    user_row['name'] = name
    user_row['role'] = role
    user_row['status'] = "pending" if role == "admin" else "approved"
    return {'success': True, 'message': 'Account created'}
  except Exception as e:
    print(f"Error creating account: {e}")
    return {'success': False, 'message': str(e)}

@anvil.server.callable
def get_user_profile(email):
  """Get user profile - SERVER SIDE"""
  try:
    user = app_tables.users.get(email=email)
    return {
      'email': user['email'],
      'name': user['name'],
      'role': user['role'],
      'status': user['status']
    }
  except Exception as e:
    print(f"Error getting profile: {e}")
    return None

@anvil.server.callable
def get_teacher_issues(email):
  """Get all issues created by a specific teacher"""
  try:
    print(f"SERVER DEBUG: Looking for issues with reporter_email: {email}")
    issues = list(app_tables.issues.search(reporter_email=email))
    print(f"SERVER DEBUG: Found {len(issues)} issues for teacher")
    return issues
  except Exception as e:
    print(f"SERVER ERROR: {e}")
    import traceback
    traceback.print_exc()
    return []

@anvil.server. callable
def submit_issue(title, description, urgency, location_id, reporter_email):
  """Submit a new issue"""
  try:
    app_tables. issues.add_row(
      title=title,
      description=description,
      urgency=urgency,
      location=location_id,
      reporter_email=reporter_email,
      status="open",
      created_at=datetime.datetime.now()
    )
    return {'success': True, 'message': 'Issue submitted successfully'}
  except Exception as e:
    print(f"Error: {e}")
    return {'success': False, 'message': str(e)}

@anvil.server.callable
def get_all_issues():
  """Get all issues for admin dashboard"""
  try:
    return list(app_tables.issues.search())
  except Exception as e:
    print(f"Error: {e}")
    return []

@anvil.server.callable
def get_all_schools():
  """Get list of schools for dropdown"""
  try:
    print(f"SERVER DEBUG: get_all_schools called")
    schools = app_tables.school.search()
    print(f"SERVER DEBUG: Found {len(schools)} schools")
    result = [(school['school_name'], school) for school in schools]
    print(f"SERVER DEBUG: Returning {len(result)} schools")
    return result
  except Exception as e:
    print(f"SERVER ERROR in get_all_schools: {e}")
    return []

@anvil.server.callable
def get_locations_by_school(school_row):
  """Get locations for selected school"""
  try:
    print(f"SERVER DEBUG: get_locations_by_school called")
    locations = app_tables. location.search(school=school_row)
    print(f"SERVER DEBUG: Found {len(locations)} locations")
    result = [(f"Floor {location['floor']} - {location['room']}", location) for location in locations]
    print(f"SERVER DEBUG: Returning: {result}")
    return result
  except Exception as e:
    print(f"SERVER ERROR in get_locations_by_school: {e}")
    return []

@anvil.server.callable
def get_pending_admins():
  """Get pending admin approvals"""
  try:
    return list(app_tables.users. search(role="admin", status="pending"))
  except Exception as e:
    return []

@anvil.server. callable
def approve_admin_account(email):
  """Approve admin account"""
  try:
    user = app_tables.users.get(email=email)
    user['status'] = "approved"
    return {'success': True, 'message': 'Admin approved'}
  except Exception as e:
    return {'success': False, 'message': str(e)}

@anvil.server.callable
def reject_admin_account(email):
  """Reject admin account"""
  try:
    user = app_tables.users.get(email=email)
    user. delete()
    return {'success': True, 'message': 'Admin rejected'}
  except Exception as e:
    return {'success': False, 'message': str(e)}