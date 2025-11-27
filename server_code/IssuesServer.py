import anvil
from anvil.tables import app_tables
import datetime

@anvil.server. callable
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

@anvil.server.callable
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
      created_at=datetime. datetime.now()
    )
    return {'success': True, 'message': 'Issue submitted successfully'}
  except Exception as e:
    print(f"Error: {e}")
    return {'success': False, 'message': str(e)}

@anvil. server.callable
def get_all_issues():
  """Get all issues for admin dashboard"""
  try:
    return list(app_tables.issues. search())
  except Exception as e:
    print(f"Error: {e}")
    return []