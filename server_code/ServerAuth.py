# server_modules/ServerAuth.py
import anvil.users
from anvil.tables import app_tables
import anvil.server
import anvil.email
from datetime import datetime
import hashlib
import anvil.tables.query as q

# Utilities
def _normalize_email(email):
  if email is None:
    return None
  return str(email).strip().lower()

def hash_password(password: str) -> str:
  if not password:
    return None
  return hashlib.sha256(str(password).encode("utf-8")).hexdigest()

# Account creation & login
@anvil.server.callable
def create_user_account(name, email, password, role="teacher"):
  try:
    email_n = _normalize_email(email)
    if not email_n:
      return {'success': False, 'message': 'Email is required.'}
    if not password:
      return {'success': False, 'message': 'Password is required.'}

    # Try create Anvil auth user (non-fatal)
    try:
      anvil.users.signup_with_email(email_n, password)
    except Exception:
      pass

    # Ensure users table row exists
    try:
      user_row = app_tables.users.get(email=email_n)
    except Exception:
      user_row = None

    if user_row is None:
      try:
        user_row = app_tables.users.add_row(email=email_n)
      except Exception as e:
        print(f"create_user_account: failed to add users row: {e}")
        return {'success': False, 'message': 'Internal error creating user row.'}

    user_row['name'] = name
    user_row['role'] = role
    user_row['status'] = "pending" if role == "admin" else "approved"
    user_row['password_hash'] = hash_password(password)
    try:
      user_row['signed_up'] = datetime.now()
    except Exception:
      pass

    if role == "admin" and user_row.get('status') == 'pending':
      send_admin_approval_email(email_n, name)

    return {'success': True, 'message': 'Account created or updated.'}
  except Exception as err:
    print(f"create_user_account exception: {err}")
    return {'success': False, 'message': f'Signup failed: {err}'}

@anvil.server.callable
def verify_login(email, password):
  try:
    email_n = _normalize_email(email)
    if not email_n:
      return {'success': False, 'message': 'Please enter an email.'}
    if password is None:
      return {'success': False, 'message': 'Please enter a password.'}

    try:
      user_row = app_tables.users.get(email=email_n)
    except Exception:
      user_row = None

    if not user_row:
      return {'success': False, 'message': 'Email not found.'}

    stored_hash = user_row.get('password_hash')
    if not stored_hash:
      return {'success': False, 'message': 'Account has no password set. Please reset password.'}

    entered_hash = hash_password(password)
    if entered_hash != stored_hash:
      return {'success': False, 'message': 'Incorrect email or password.'}

    role = user_row.get('role') or 'teacher'
    status = user_row.get('status') or 'approved'
    if role == 'admin' and status != 'approved':
      return {'success': False, 'message': 'Your admin account is pending approval.'}

    return {'success': True, 'role': role}
  except Exception as err:
    print(f"verify_login exception: {err}")
    return {'success': False, 'message': f'Login error: {err}'}

# Debug helpers (temporary)
@anvil.server.callable
def debug_get_user(email):
  try:
    email_n = _normalize_email(email)
    if not email_n:
      return {'found': False}
    try:
      row = app_tables.users.get(email=email_n)
    except Exception:
      print("debug_get_user: users table missing or error getting row.")
      return {'found': False}
    if not row:
      return {'found': False}
    return {
      'found': True,
      'email': row.get('email'),
      'name': row.get('name'),
      'password_hash': row.get('password_hash'),
      'password_field': row.get('password'),
      'role': row.get('role'),
      'status': row.get('status'),
      'signed_up': row.get('signed_up')
    }
  except Exception as e:
    print(f"debug_get_user exception: {e}")
    return {'error': str(e)}

@anvil.server.callable
def verify_login_debug(email, password):
  try:
    email_n = _normalize_email(email)
    if not email_n:
      return {'success': False, 'message': 'Email required.'}
    try:
      user = app_tables.users.get(email=email_n)
    except Exception:
      user = None
    if not user:
      print(f"verify_login_debug: no user row for {email_n}")
      return {'success': False, 'message': 'Email not found.'}

    stored_hash = user.get('password_hash')
    plain_pw = user.get('password')

    if stored_hash:
      entered_hash = hash_password(password)
      print(f"verify_login_debug: comparing hashes for {email_n} stored={stored_hash} entered={entered_hash}")
      if entered_hash == stored_hash:
        return {'success': True, 'role': user.get('role', 'teacher')}
      else:
        return {'success': False, 'message': 'Incorrect email or password.'}

    if plain_pw is not None:
      print(f"verify_login_debug: comparing plain password for {email_n}")
      if str(plain_pw) == str(password):
        return {'success': True, 'role': user.get('role', 'teacher')}
      else:
        return {'success': False, 'message': 'Incorrect email or password.'}

    print(f"verify_login_debug: no password data for {email_n}")
    return {'success': False, 'message': 'Account has no password set.'}
  except Exception as e:
    print(f"verify_login_debug exception: {e}")
    return {'success': False, 'message': f'Login error: {e}'}

@anvil.server.callable
def force_set_password_hash(email, new_plain_password):
  try:
    email_n = _normalize_email(email)
    if not email_n:
      return {'success': False, 'message': 'Email required.'}
    try:
      row = app_tables.users.get(email=email_n)
    except Exception:
      row = None
    if not row:
      return {'success': False, 'message': 'User not found.'}
    row['password_hash'] = hash_password(new_plain_password)
    return {'success': True}
  except Exception as e:
    print(f"force_set_password_hash exception: {e}")
    return {'success': False, 'message': str(e)}

# Issue + lookups (robust)
@anvil.server.callable
def submit_issue(title, description, urgency, location_id, user_email):
  try:
    if not user_email:
      return {'success': False, 'message': 'User email required.'}
    email_n = _normalize_email(user_email)
    try:
      user_row = app_tables.users.get(email=email_n)
    except Exception:
      user_row = None
    if not user_row:
      return {'success': False, 'message': 'User not found.'}

    location = None
    if location_id:
      try:
        location = app_tables.location.get_by_id(location_id)
      except Exception as e:
        print(f"submit_issue: location lookup failed: {e}")
        location = None

    try:
      app_tables.issues.add_row(
        title=title,
        description=description,
        urgency=urgency,
        status='open',
        created_by=user_row.get('name'),
        created_at=datetime.now(),
        last_updated=datetime.now(),
        reporter_email=email_n,
        location=location,
        assigned_to=None,
        resolved_at=None
      )
    except Exception as e:
      print(f"submit_issue: failed to add issue row: {e}")
      return {'success': False, 'message': 'Failed to save issue (check issues table).'}

    send_issue_submitted_email(email_n, user_row.get('name'), title)
    return {'success': True, 'message': 'Issue submitted successfully!'}
  except Exception as err:
    print(f"submit_issue exception: {err}")
    return {'success': False, 'message': f'Failed to submit issue: {err}'}

@anvil.server.callable
def get_teacher_issues(user_email):
  try:
    if not user_email:
      return []
    email_n = _normalize_email(user_email)
    try:
      rows = app_tables.issues.search(reporter_email=email_n)
    except Exception:
      print("get_teacher_issues: issues table missing or search error.")
      return []
    return [{
      'id': r.get_id(),
      'title': r.get('title'),
      'urgency': r.get('urgency'),
      'status': r.get('status'),
      'created_at': r.get('created_at'),
      'last_updated': r.get('last_updated')
    } for r in rows]
  except Exception as e:
    print(f"get_teacher_issues exception: {e}")
    return []

# Simple school/location helpers
@anvil.server.callable
def get_all_schools():
  try:
    rows = app_tables.school.search()
    return [(r.get_id(), r.get('school_name')) for r in rows]
  except Exception as e:
    print(f"get_all_schools exception: {e}")
    return []

@anvil.server.callable
def get_locations_by_school(school_id):
  try:
    if not school_id:
      return []
    rows = app_tables.location.search(school=school_id)
    out = []
    for r in rows:
      branch = r.get('branch') or ''
      floor = r.get('floor') or ''
      label = f"{branch} - Floor {floor}" if branch or floor else str(r.get_id())
      out.append((r.get_id(), label))
    return out
  except Exception as e:
    print(f"get_locations_by_school exception: {e}")
    return []

# Emails & admin helpers (internal)
def send_admin_approval_email(email, name):
  try:
    anvil.email.send(to=email, subject="Admin Account Approval Request",
                     html=f"<h2>Admin Account Request Received</h2><p>Hello {name},</p><p>Your admin request is pending approval.</p>")
  except Exception as e:
    print(f"send_admin_approval_email error: {e}")

def send_issue_submitted_email(email, name, title):
  try:
    anvil.email.send(to=email, subject="Issue Received: " + (title or ''), html=f"<p>Hello {name or ''}, your issue was received.</p>")
  except Exception as e:
    print(f"send_issue_submitted_email error: {e}")

@anvil.server.callable
def get_user_data(email):
  try:
    email_n = _normalize_email(email)
    if not email_n:
      return None
    try:
      row = app_tables.users.get(email=email_n)
    except Exception:
      row = None
    if not row:
      return None
    return {'role': row.get('role'), 'status': row.get('status'), 'name': row.get('name')}
  except Exception as e:
    print(f"get_user_data exception: {e}")
    return None