import anvil.users
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.email
from datetime import datetime
import hashlib

def hash_password(password):
  """Hash a password using SHA-256"""
  return hashlib.sha256(password.encode()).hexdigest()

@anvil.server.callable
def create_user_account(name, email, password, role):
  try:
    user = anvil.users.signup_with_email(email, password)
    status = "pending" if role == "admin" else "approved"
    users_row = app_tables.users.get(email=email)
    users_row['role'] = role
    users_row['status'] = status
    users_row['name'] = name
    users_row['password_hash'] = hash_password(password)
    if role == "admin" and status == "pending":
      send_admin_approval_email(email, name)
    return {'success': True, 'message': 'Teacher account created! Log in now.' if role == "teacher" else 'Admin request sent. Check your email for approval instructions.'}
  except anvil.users.UserExists:
    return {'success': False, 'message': 'Email already registered.'}
  except Exception as err:
    return {'success': False, 'message': f'Signup failed: {str(err)}'}

@anvil.server.callable
def verify_login(email, password):
  """Verify login credentials against Users table"""
  try:
    users = app_tables.users.search(email=email)
    if not users:
      return {'success': False, 'message': 'Email not found.'}

    user_data = users[0]
    stored_hash = user_data['password_hash']
    entered_hash = hash_password(password)

    if stored_hash != entered_hash:
      return {'success': False, 'message': 'Incorrect email or password.'}

    role = user_data['role'] or 'teacher'
    status = user_data['status'] or 'pending'

    if role == 'admin' and status != 'approved':
      return {'success': False, 'message': 'Your admin account is pending approval.'}

    return {'success': True, 'role': role}
  except Exception as err:
    return {'success': False, 'message': f'Login error: {str(err)}'}

@anvil.server.callable
def send_admin_approval_email(email, name):
  try:
    anvil.email.send(
      to=email,
      subject="Admin Account Approval Request",
      html="<h2>Admin Account Request Received</h2><p>Hello " + name + ",</p><p>Your admin account request has been received and is pending approval.</p>"
    )
    return True
  except Exception as err:
    print(f"Email sending failed: {str(err)}")
    return False

@anvil.server.callable
def submit_issue(title, description, urgency, location_id, user_email):
  try:
    user_data = app_tables.users.search(email=user_email)[0]
    location = app_tables.location.get_by_id(location_id)
    app_tables.issues.add_row(
      title=title,
      description=description,
      urgency=urgency,
      status='open',
      created_by=user_data['name'],
      created_at=datetime.now(),
      last_updated=datetime.now(),
      reporter_email=user_email,
      location=location,
      assigned_to=None,
      resolved_at=None
    )
    send_issue_submitted_email(user_email, user_data['name'], title)
    return {'success': True, 'message': 'Issue submitted successfully!'}
  except Exception as err:
    return {'success': False, 'message': f'Failed to submit issue: {str(err)}'}

@anvil.server.callable
def send_issue_submitted_email(email, name, title):
  try:
    anvil.email.send(
      to=email,
      subject="Issue Received: " + title,
      html="<h2>Issue Submitted</h2><p>Hello " + name + ",</p><p>Your issue has been submitted.</p>"
    )
    return True
  except Exception as err:
    print(f"Email sending failed: {str(err)}")
    return False

@anvil.server.callable
def get_teacher_issues(user_email):
  try:
    issues = app_tables.issues.search(reporter_email=user_email)
    return [{'id': issue.get_id(), 'title': issue['title'], 'urgency': issue['urgency'], 'status': issue['status'], 'created_at': issue['created_at'], 'last_updated': issue['last_updated']} for issue in issues]
  except Exception as err:
    print(f"Error fetching issues: {str(err)}")
    return []

@anvil.server.callable
def get_all_issues(filters=None):
  try:
    all_issues = app_tables.issues.search()
    issues_list = [{'id': issue.get_id(), 'title': issue['title'], 'description': issue['description'], 'urgency': issue['urgency'], 'status': issue['status'], 'created_by': issue['created_by'], 'created_at': issue['created_at'], 'last_updated': issue['last_updated'], 'location': issue['location'], 'reporter_email': issue['reporter_email'], 'assigned_to': issue['assigned_to']} for issue in all_issues]
    if filters:
      if filters.get('urgency'):
        issues_list = [i for i in issues_list if i['urgency'] == filters['urgency']]
      if filters.get('status'):
        issues_list = [i for i in issues_list if i['status'] == filters['status']]
      if filters.get('search'):
        search_term = filters['search'].lower()
        issues_list = [i for i in issues_list if search_term in i['title'].lower() or search_term in i['description'].lower()]
    return issues_list
  except Exception as err:
    print(f"Error fetching issues: {str(err)}")
    return []

@anvil.server.callable
def get_pending_admins():
  try:
    pending_admins = app_tables.users.search(q.all_of(role='admin', status='pending'))
    return [{'email': admin['email'], 'name': admin['name'], 'signed_up': admin['signed_up']} for admin in pending_admins]
  except Exception as err:
    return []

@anvil.server.callable
def approve_admin_account(email):
  try:
    admin_row = app_tables.users.get(email=email)
    admin_row['status'] = 'approved'
    anvil.email.send(
      to=email,
      subject="Admin Account Approved!",
      html="<h2>Account Approved!</h2><p>Your admin account has been approved!</p>"
    )
    return {'success': True, 'message': 'Admin approved!'}
  except Exception as err:
    return {'success': False, 'message': str(err)}

@anvil.server.callable
def reject_admin_account(email):
  try:
    admin_row = app_tables.users.get(email=email)
    admin_row['status'] = 'rejected'
    anvil.email.send(
      to=email,
      subject="Admin Account Request - Rejected",
      html="<h2>Request Rejected</h2><p>Your admin account request has been rejected.</p>"
    )
    return {'success': True, 'message': 'Admin rejected'}
  except Exception as err:
    return {'success': False, 'message': str(err)}

@anvil.server.callable
def update_issue_status(issue_id, new_status, assigned_to=None):
  try:
    issue = app_tables.issues.get_by_id(issue_id)
    issue['status'] = new_status
    issue['last_updated'] = datetime.now()
    if assigned_to:
      issue['assigned_to'] = assigned_to
    if new_status == 'resolved':
      issue['resolved_at'] = datetime.now()
    send_status_update_email(issue['reporter_email'], issue['title'], new_status)
    return {'success': True, 'message': 'Issue updated!'}
  except Exception as err:
    return {'success': False, 'message': str(err)}

@anvil.server.callable
def send_status_update_email(email, title, new_status):
  try:
    anvil.email.send(
      to=email,
      subject="Issue Update: " + title,
      html="<h2>Issue Status Update</h2><p>Your issue status: " + new_status + "</p>"
    )
    return True
  except Exception as err:
    print(f"Email sending failed: {str(err)}")
    return False

@anvil.server.callable
def get_all_schools():
  try:
    schools = app_tables.school.search()
    return [(s.get_id(), s['school_name']) for s in schools]
  except Exception as err:
    return []

@anvil.server.callable
def get_locations_by_school(school_id):
  try:
    locations = app_tables.location.search(school=school_id)
    return [(l.get_id(), f"{l['branch']} - Floor {l['floor']}") for l in locations]
  except Exception as err:
    return []

@anvil.server.callable
def get_user_data(email):
  """Get user data from Users table"""
  try:
    user_data = app_tables.users.search(email=email)[0]
    return {
      'role': user_data['role'],
      'status': user_data['status']
    }
  except IndexError:
    return None