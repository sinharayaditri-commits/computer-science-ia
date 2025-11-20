import anvil.users
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.email
from datetime import datetime

@anvil.server.callable
def create_user_account(name, email, password, role):
  """
    Create a new user account and set their role.
    Teachers auto-approve, Admins require approval.
    """
  try:
    # 1. Create the Anvil user account
    user = anvil.users.signup_with_email(email, password)
    uid = user.get_id()

    # 2. Determine initial status
    status = "pending" if role == "admin" else "approved"

    # 3. Update Users table with role and status
    users_row = app_tables.users.get(email=email)
    users_row['role'] = role
    users_row['status'] = status

    # 4. If admin and pending, send approval email
    if role == "admin" and status == "pending":
      send_admin_approval_email(email, name, uid)

    return {
      'success': True,
      'message': 'Teacher account created! Log in now.' if role == "teacher" 
      else 'Admin request sent. Check your email for approval instructions.'
    }

  except anvil.users.UserExists:
    return {'success': False, 'message': 'Email already registered.'}
  except Exception as err:
    return {'success': False, 'message': f'Signup failed: {str(err)}'}


@anvil.server.callable
def send_admin_approval_email(email, name, uid):
  """Send approval email to admins"""
  approval_link = f"https://your-app.anvil.app/admin/approve?uid={uid}"

  anvil.email.send(
    to=email,
    subject="Admin Account Approval Required",
    html=f"""
        <h2>Admin Account Approval</h2>
        <p>Hello {name},</p>
        <p>Your admin account request is pending approval from the system administrator.</p>
        <p>Once approved, you'll be able to log in and access the admin dashboard.</p>
        <p><strong>Status:</strong> Pending</p>
        <br>
        <p>This is an automated message. Please do not reply.</p>
        """
  )


@anvil.server.callable
def approve_admin_account(uid):
  """Approve a pending admin account"""
  try:
    user_row = app_tables.users.search(q.ilike(app_tables.users.email, '%'))

    for row in user_row:
      if row.user.get_id() == uid:
        row['status'] = 'approved'

        # Send approval email
        anvil.email.send(
          to=row['email'],
          subject="Admin Account Approved! ✅",
          html="""
                    <h2>Account Approved</h2>
                    <p>Your admin account has been approved!</p>
                    <p>You can now log in at the admin portal.</p>
                    """
        )
        return {'success': True, 'message': 'Admin approved!'}

    return {'success': False, 'message': 'User not found'}
  except Exception as err:
    return {'success': False, 'message': str(err)}


@anvil.server.callable
def reject_admin_account(uid):
  """Reject a pending admin account"""
  try:
    user_row = app_tables.users.search(q.ilike(app_tables.users.email, '%'))

    for row in user_row:
      if row.user.get_id() == uid:
        row['status'] = 'rejected'

        # Send rejection email
        anvil.email.send(
          to=row['email'],
          subject="Admin Account Request Rejected",
          html="""
                    <h2>Request Rejected</h2>
                    <p>Your admin account request has been rejected.</p>
                    <p>Contact your system administrator for more information.</p>
                    """
        )
        return {'success': True, 'message': 'Admin rejected'}

    return {'success': False, 'message': 'User not found'}
  except Exception as err:
    return {'success': False, 'message': str(err)}


@anvil.server.callable
def get_pending_admins():
  """Get all pending admin accounts (for admin dashboard)"""
  try:
    pending_admins = app_tables.users.search(
      q.all_of(
        role='admin',
        status='pending'
      )
    )
    return [
      {
        'uid': admin.user.get_id(),
        'name': admin['name'],
        'email': admin['email'],
        'signed_up': admin['signed_up']
      }
      for admin in pending_admins
    ]
  except Exception as err:
    return []


@anvil.server.callable
def get_all_issues():
  """Get all submitted issues (for admin dashboard)"""
  try:
    issues = app_tables.issues.search()
    return [
      {
        'id': issue.get_id(),
        'title': issue['title'],
        'description': issue['description'],
        'urgency': issue['urgency'],
        'status': issue['status'],
        'created_by': issue['created_by'],
        'created_at': issue['created_at'],
        'location': issue['location'],
        'reporter_email': issue['reporter_email']
      }
      for issue in issues
    ]
  except Exception as err:
    return []


@anvil.server.callable
def submit_issue(title, description, urgency, class_name, floor, room, location_id):
  """Submit a new issue (for teachers)"""
  try:
    user = anvil.users.get_user()

    app_tables.issues.add_row(
      title=title,
      description=description,
      urgency=urgency,
      status='open',
      created_by=user['name'],
      created_at=datetime.now(),
      reporter_email=user['email'],
      location=app_tables.location.get_by_id(location_id),
      assigned_to=None,
      resolved_at=None
    )

    return {'success': True, 'message': 'Issue submitted successfully!'}
  except Exception as err:
    return {'success': False, 'message': f'Failed to submit issue: {str(err)}'}


@anvil.server.callable
def update_issue_status(issue_id, new_status):
  """Update issue status (for admin)"""
  try:
    issue = app_tables.issues.get_by_id(issue_id)
    issue['status'] = new_status
    if new_status == 'resolved':
      issue['resolved_at'] = datetime.now()
    return {'success': True, 'message': 'Issue updated!'}
  except Exception as err:
    return {'success': False, 'message': str(err)}