import anvil
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime

# Add this right after imports at the top of ServerAuth.py
print("=== CHECKING AVAILABLE TABLES ===")
print(dir(app_tables))
print("=================================")

@anvil.server.callable
def test_tables():
  """Test if we can access ANY table"""
  try:
    print("=" * 50)
    print("TEST: Checking what tables are available...")
    print("=" * 50)

    print(f"app_tables type: {type(app_tables)}")

    # Test each table
    print("\n--- Testing users table ---")
    try:
      users = list(app_tables. users.search())
      print(f"✓ users table works!  Got {len(users)} users")
    except Exception as e:
      print(f"✗ users table failed: {e}")

    print("\n--- Testing issues table ---")
    try:
      issues = list(app_tables.issues.search())
      print(f"✓ issues table works! Got {len(issues)} issues")
    except Exception as e:
      print(f"✗ issues table failed: {e}")

    print("\n--- Testing location table ---")
    try:
      locations = list(app_tables.location.search())
      print(f"✓ location table works! Got {len(locations)} locations")
    except Exception as e:
      print(f"✗ location table failed: {e}")

    print("\n--- Testing school table ---")
    try:
      schools = list(app_tables. school.search())
      print(f"✓ school table works! Got {len(schools)} schools")
    except Exception as e:
      print(f"✗ school table failed: {e}")

    print("=" * 50)
    return {'success': True, 'message': 'Tests completed - check console'}

  except Exception as e:
    print(f"MAJOR ERROR: {e}")
    import traceback
    traceback.print_exc()
    return {'success': False, 'message': str(e)}


@anvil.server.callable
def test_issues_table():
  """Simple test to check issues table"""
  try:
    count = len(list(app_tables.issues.search()))
    return f"SUCCESS: Found {count} issues in table"
  except Exception as e:
    return f"ERROR: {e}"


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


@anvil. server.callable
def get_user_profile(email):
  """Get user profile - SERVER SIDE"""
  try:
    user = app_tables.users. get(email=email)
    if user:
      return {
        'email': user['email'],
        'name': user['name'],
        'role': user['role'],
        'status': user['status']
      }
    return None
  except Exception as e:
    print(f"Error getting profile: {e}")
    return None


@anvil.server. callable
def get_teacher_issues(email):
  """Get all issues created by a specific teacher"""
  try:
    print(f"SERVER DEBUG: Looking for issues with reporter_email: {email}")

    # Search directly by reporter_email
    issues = app_tables.issues. search(reporter_email=email)

    # Convert to list of dictionaries for the DataGrid
    result = []
    for issue in issues:
      # Handle location - it's a linked row, so we need to extract the room name
      location_text = ''
      if issue['location']:
        try:
          location_text = issue['location']['room']
        except:
          location_text = str(issue['location'])

          # Handle assigned_to - it's a linked row
      assigned_to_text = ''
      if issue['assigned_to']:
        try:
          assigned_to_text = issue['assigned_to']['email'] if issue['assigned_to'] else ''
        except:
          assigned_to_text = str(issue['assigned_to'])

          # Handle created_by - it's a linked row
      created_by_text = ''
      if issue['created_by']:
        try:
          created_by_text = issue['created_by']['email'] if issue['created_by'] else ''
        except:
          created_by_text = str(issue['created_by'])

      result.append({
        'title': issue['title'] or '',
        'description': issue['description'] or '',
        'urgency': issue['urgency'] or '',
        'status': issue['status'] or '',
        'assigned_to': assigned_to_text,
        'created_by': created_by_text,
        'created_at': issue['created_at'],
        'resolved_at': issue['resolved_at'],
        'location': location_text,
        'reporter_email': issue['reporter_email'] or '',
        'last_updated': issue['last_updated']
      })

      print(f"SERVER DEBUG: Found {len(result)} issues for {email}")
      return result

  except Exception as e:
    print(f"SERVER ERROR: {e}")
    import traceback
    traceback.print_exc()
    return []


@anvil.server.callable
def get_all_issues():
  """Get all issues for admin dashboard"""
  try:
    issues = app_tables.issues. search()

    result = []
    for issue in issues:
      location_text = ''
      if issue['location']:
        try:
          location_text = issue['location']['room']
        except:
          location_text = str(issue['location'])

      assigned_to_text = ''
      if issue['assigned_to']:
        try:
          assigned_to_text = issue['assigned_to']['email']
        except:
          assigned_to_text = str(issue['assigned_to'])

      created_by_text = ''
      if issue['created_by']:
        try:
          created_by_text = issue['created_by']['email']
        except:
          created_by_text = str(issue['created_by'])

      result.append({
        'title': issue['title'] or '',
        'description': issue['description'] or '',
        'urgency': issue['urgency'] or '',
        'status': issue['status'] or '',
        'assigned_to': assigned_to_text,
        'created_by': created_by_text,
        'created_at': issue['created_at'],
        'resolved_at': issue['resolved_at'],
        'location': location_text,
        'reporter_email': issue['reporter_email'] or '',
        'last_updated': issue['last_updated']
      })

    return result
  except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    return []


@anvil. server.callable
def submit_issue(title, description, urgency, location_id, reporter_email):
  """Submit a new issue"""
  try:
    app_tables.issues.add_row(
      title=title,
      description=description,
      urgency=urgency,
      location=location_id,
      reporter_email=reporter_email,
      status="open",
      created_at=datetime.datetime.now(),
      last_updated=datetime. datetime.now()
    )
    return {'success': True, 'message': 'Issue submitted successfully'}
  except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    return {'success': False, 'message': str(e)}


@anvil.server.callable
def get_all_schools():
  """Get list of schools for dropdown"""
  try:
    print(f"SERVER DEBUG: get_all_schools called")
    schools = app_tables.school.search()
    result = [(school['school_name'], school) for school in schools]
    print(f"SERVER DEBUG: Returning {len(result)} schools")
    return result
  except Exception as e:
    print(f"SERVER ERROR in get_all_schools: {e}")
    return []


@anvil. server.callable
def get_locations_by_school(school_row):
  """Get locations for selected school"""
  try:
    print(f"SERVER DEBUG: get_locations_by_school called")
    locations = app_tables.location.search(school=school_row)
    result = [(f"Floor {location['floor']} - {location['room']}", location) for location in locations]
    print(f"SERVER DEBUG: Returning: {result}")
    return result
  except Exception as e:
    print(f"SERVER ERROR in get_locations_by_school: {e}")
    return []


@anvil. server.callable
def get_pending_admins():
  """Get pending admin approvals"""
  try:
    admins = app_tables.users. search(role="admin", status="pending")
    result = []
    for admin in admins:
      result.append({
        'email': admin['email'],
        'name': admin['name'],
        'role': admin['role'],
        'status': admin['status']
      })
    return result
  except Exception as e:
    print(f"Error: {e}")
    return []


@anvil.server.callable
def approve_admin_account(email):
  """Approve admin account"""
  try:
    user = app_tables.users.get(email=email)
    if user:
      user['status'] = "approved"
      return {'success': True, 'message': 'Admin approved'}
    return {'success': False, 'message': 'User not found'}
  except Exception as e:
    return {'success': False, 'message': str(e)}


@anvil.server.callable
def reject_admin_account(email):
  """Reject admin account"""
  try:
    user = app_tables.users.get(email=email)
    if user:
      user. delete()
      return {'success': True, 'message': 'Admin rejected'}
    return {'success': False, 'message': 'User not found'}
  except Exception as e:
    return {'success': False, 'message': str(e)}