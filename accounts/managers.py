from accounts.utils import get_username_from_email
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email: str, password=None, username=None):
        """ Creation a new user (different from User.objects.create() method)
        
        Args:
            email (str): Email address
            password (str, optional): Password. Defaults to None.
            username (str, optional): Username. Defaults to None.
        
        Raises:
            ValueError: no email provided
            ValueError: provided email already exists
        
        Returns:
            (User): Created user
        """
        
        if not email:
            raise ValueError(_("Veuillez fournir une adresse mail s'il vous plaît!"))
        
        if self.filter(email=str(email).lower()).exists():
            raise ValueError(_("Email déjà en cours d'utilisation"))
        
        user = self.model(email=self.normalize_email(email))
        
        user.is_active = True # or False, then you should send an activation link to user
        user.set_password(password)
        user.save(using=self._db)
        
        # Get username from email address if not provided
        if not username or username is None:
            username = get_username_from_email(email=email)
        
        # check if username already exists
        if self.filter(username=str(username).lower()).exists():
            username = f"{username}{user.pk}" # append self.pk to make a difference
        
        user.username = username
        user.save()
        return user
    
    
    def create_superuser(self, email: str, password=None, username=None):
        """ Creation a new superuser (an admin)
        
        Args:
            email (str): Email address
            password (str, optional): Password. Defaults to None.
            username (str, optional): Username. Defaults to None.
        
        Returns:
            (User): Created superuser
        """
        user = self.create_user(email=self.normalize_email(email), password=password, username=username)
        user.is_active = True # just to make sure (was already defined in self.create_user())
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
