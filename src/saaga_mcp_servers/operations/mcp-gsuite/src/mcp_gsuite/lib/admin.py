#!/usr/bin/env python3
"""
Google Workspace User Onboarding Script

This script automates the process of creating new users in Google Workspace,
including user creation, license assignment, and group membership.
"""

import json
import logging
from typing import Dict, List, Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class GoogleWorkspaceOnboarding:
    """Handles Google Workspace user onboarding operations."""
    
    def __init__(self, service_account_file: str, delegated_email: str):
        """
        Initialize the Google Workspace onboarding client.
        
        Args:
            service_account_file: Path to the service account JSON file
            delegated_email: Email of the admin user to impersonate
        """
        self.scopes = [
            'https://www.googleapis.com/auth/admin.directory.user',
            'https://www.googleapis.com/auth/admin.directory.group',
            'https://www.googleapis.com/auth/apps.licensing'
        ]
        
        # Create credentials with domain-wide delegation
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file,
            scopes=self.scopes,
            subject=delegated_email
        )
        
        # Build service objects
        self.directory_service = build('admin', 'directory_v1', credentials=credentials)
        self.licensing_service = build('licensing', 'v1', credentials=credentials)
    
    def create_user(self, user_data: Dict) -> Dict:
        """
        Create a new user in Google Workspace.
        
        Args:
            user_data: Dictionary containing user information
                Required fields:
                - primaryEmail: User's email address
                - password: Initial password (minimum 8 characters)
                - firstName: User's first name
                - lastName: User's last name
                Optional fields:
                - orgUnitPath: Organizational unit path (default: '/')
                - recoveryEmail: Recovery email address
                - recoveryPhone: Recovery phone number
                - department: Department name
                - title: Job title
                - manager: Manager's email
                - phone: Work phone number
                - address: Work address
        
        Returns:
            Created user object
        """
        # Prepare user body
        user_body = {
            'primaryEmail': user_data['primaryEmail'],
            'password': user_data['password'],
            'name': {
                'givenName': user_data['firstName'],
                'familyName': user_data['lastName']
            },
            'changePasswordAtNextLogin': True,
            'orgUnitPath': user_data.get('orgUnitPath', '/')
        }
        
        # Add optional fields if provided
        if 'recoveryEmail' in user_data:
            user_body['recoveryEmail'] = user_data['recoveryEmail']
        
        if 'recoveryPhone' in user_data:
            user_body['recoveryPhone'] = user_data['recoveryPhone']
        
        # Add custom schema fields if provided
        custom_schemas = {}
        
        if 'department' in user_data:
            user_body['organizations'] = [{
                'department': user_data['department'],
                'primary': True
            }]
        
        if 'title' in user_data:
            if 'organizations' not in user_body:
                user_body['organizations'] = [{'primary': True}]
            user_body['organizations'][0]['title'] = user_data['title']
        
        if 'manager' in user_data:
            user_body['relations'] = [{
                'value': user_data['manager'],
                'type': 'manager'
            }]
        
        if 'phone' in user_data:
            user_body['phones'] = [{
                'value': user_data['phone'],
                'type': 'work',
                'primary': True
            }]
        
        if 'address' in user_data:
            user_body['addresses'] = [{
                'type': 'work',
                'formatted': user_data['address'],
                'primary': True
            }]
        
        try:
            user = self.directory_service.users().insert(body=user_body).execute()
            logger.info(f"Successfully created user: {user['primaryEmail']}")
            return user
        except HttpError as e:
            logger.error(f"Failed to create user: {e}")
            raise
    
    def assign_license(self, user_email: str, sku_id: str = 'Google-Apps-For-Business') -> Dict:
        """
        Assign a license to a user.
        
        Common SKU IDs:
        - Google-Apps-For-Business: Google Workspace Business Starter
        - Google-Apps-Unlimited: Google Workspace Business Standard
        - Google-Apps-For-Postini: Google Workspace Business Plus
        - 1010020020: Google Workspace Enterprise Standard
        - 1010020025: Google Workspace Enterprise Plus
        
        Args:
            user_email: Email address of the user
            sku_id: License SKU ID
        
        Returns:
            License assignment response
        """
        license_body = {
            'userId': user_email
        }
        
        try:
            response = self.licensing_service.licenseAssignments().insert(
                productId='Google-Apps',
                skuId=sku_id,
                body=license_body
            ).execute()
            logger.info(f"Successfully assigned license to: {user_email}")
            return response
        except HttpError as e:
            logger.error(f"Failed to assign license: {e}")
            raise
    
    def add_to_groups(self, user_email: str, group_emails: List[str]) -> None:
        """
        Add user to one or more groups.
        
        Args:
            user_email: Email address of the user
            group_emails: List of group email addresses
        """
        member_body = {
            'email': user_email,
            'role': 'MEMBER'
        }
        
        for group_email in group_emails:
            try:
                self.directory_service.members().insert(
                    groupKey=group_email,
                    body=member_body
                ).execute()
                logger.info(f"Added {user_email} to group: {group_email}")
            except HttpError as e:
                logger.error(f"Failed to add user to group {group_email}: {e}")
    
    def setup_email_forwarding(self, user_email: str, forward_to: str) -> None:
        """
        Set up email forwarding for a user (requires Gmail API).
        Note: This is a placeholder - full implementation requires Gmail API setup.
        """
        logger.info(f"Email forwarding setup would forward {user_email} to {forward_to}")
        # Implementation would require Gmail API and additional scopes
    
    def onboard_user(self, user_data: Dict, license_sku: Optional[str] = None, 
                     groups: Optional[List[str]] = None) -> Dict:
        """
        Complete onboarding process for a new user.
        
        Args:
            user_data: User information dictionary
            license_sku: License SKU to assign (optional)
            groups: List of group emails to add user to (optional)
        
        Returns:
            Dictionary with onboarding results
        """
        results = {
            'success': False,
            'user': None,
            'license': None,
            'groups': [],
            'errors': []
        }
        
        try:
            # Step 1: Create user
            user = self.create_user(user_data)
            results['user'] = user
            
            # Step 2: Assign license (if specified)
            if license_sku:
                license_result = self.assign_license(user['primaryEmail'], license_sku)
                results['license'] = license_result
            
            # Step 3: Add to groups (if specified)
            if groups:
                self.add_to_groups(user['primaryEmail'], groups)
                results['groups'] = groups
            
            results['success'] = True
            logger.info(f"Successfully onboarded user: {user['primaryEmail']}")
            
        except Exception as e:
            results['errors'].append(str(e))
            logger.error(f"Onboarding failed: {e}")
        
        return results


def main():
    """Example usage of the GoogleWorkspaceOnboarding class."""
    
    # Configuration
    SERVICE_ACCOUNT_FILE = 'path/to/service-account-key.json'
    ADMIN_EMAIL = 'admin@yourdomain.com'
    
    # Initialize the onboarding client
    onboarding = GoogleWorkspaceOnboarding(SERVICE_ACCOUNT_FILE, ADMIN_EMAIL)
    
    # Example: Single user onboarding
    new_user = {
        'primaryEmail': 'john.doe@yourdomain.com',
        'password': 'TempPassword123!',  # User will be forced to change on first login
        'firstName': 'John',
        'lastName': 'Doe',
        'department': 'Engineering',
        'title': 'Software Engineer',
        'manager': 'jane.smith@yourdomain.com',
        'phone': '+1-555-123-4567',
        'recoveryEmail': 'john.doe.personal@gmail.com',
        'orgUnitPath': '/Engineering'
    }
    
    # Onboard the user with a Business Standard license and add to groups
    result = onboarding.onboard_user(
        user_data=new_user,
        license_sku='Google-Apps-Unlimited',
        groups=['engineering@yourdomain.com', 'all-staff@yourdomain.com']
    )
    
    if result['success']:
        print(f"✅ Successfully onboarded {new_user['primaryEmail']}")
    else:
        print(f"❌ Failed to onboard user. Errors: {result['errors']}")
    
    # Example: Bulk onboarding from CSV
    import csv
    
    def bulk_onboard_from_csv(csv_file: str):
        """Onboard multiple users from a CSV file."""
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_data = {
                    'primaryEmail': row['email'],
                    'password': row.get('password', 'TempPass123!'),
                    'firstName': row['firstName'],
                    'lastName': row['lastName'],
                    'department': row.get('department', ''),
                    'title': row.get('title', ''),
                    'manager': row.get('manager', ''),
                    'orgUnitPath': row.get('orgUnit', '/')
                }
                
                # Remove empty optional fields
                user_data = {k: v for k, v in user_data.items() if v}
                
                groups = [g.strip() for g in row.get('groups', '').split(',') if g.strip()]
                
                result = onboarding.onboard_user(
                    user_data=user_data,
                    license_sku=row.get('license', 'Google-Apps-For-Business'),
                    groups=groups if groups else None
                )
                
                status = "✅" if result['success'] else "❌"
                print(f"{status} {row['email']}")


if __name__ == '__main__':
    main()