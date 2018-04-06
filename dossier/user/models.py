# -*- coding: utf-8 -*-
from flask_ldapconn import LDAPConn
from flask_ldapconn.entry import LDAPEntry
from flask_ldapconn.attribute import LDAPAttribute as Attribute


from flask_login import UserMixin

from dossier import app

class User(LDAPEntry, UserMixin):
    _ldap = LDAPConn(app)

    base_dn = app.config['LDAP_USER_BASEDN']
    object_classes = ['inetOrgPerson']

    name = Attribute('displayName')
    email = Attribute('mail')
    userid = Attribute('uid')
    avatar = Attribute('jpegPhoto')
    last_name = Attribute('sn')
    first_name = Attribute('givenName')
    title = Attribute('title')
    locked = Attribute('nsaccountlock')
    email_alias = Attribute('mailalternateaddress')
    subject_pronoun = Attribute('subjectPronoun')
    object_pronoun = Attribute('objectPronoun')

    def check_password(self, password):
        if self.password is None:
            return False
        return self._ldap.authenticate(self.dn, password)


    # ================================================================
    # Class methods

    @classmethod
    def authenticate(cls, login, password):
        user = User.query.filter('userid: {}'.format(login)).first()

        if user:
            authenticated = user.check_password(password)
        else:
            authenticated = False

        return user, authenticated

    """@classmethod
    def search(cls, keywords):
        criteria = []
        for keyword in keywords.split():
            keyword = '%' + keyword + '%'
            criteria.append(db.or_(
                User.name.ilike(keyword),
                User.email.ilike(keyword),
            ))
        q = reduce(db.and_, criteria)
        return cls.query.filter(q)"""

    @classmethod
    def get_by_id(cls, user_id):
        return User.query.filter('userid: {}'.format(user_id)).first()

    """def check_name(self, name):
        return User.query.filter(db.and_(
            User.name == name, User.email != self.id)).count() == 0"""

class TOTPToken(LDAPEntry):
    base_dn = app.config['LDAP_OTP_BASEDN']
    object_classes = ['ipatokentotp']

    owner = Attribute('ipatokenowner')
    algorithm = Attribute('ipatokenOTPalgorithm')
    digits = Attribute('ipatokenOTPdigits')
    key = Attribute('ipatokenOTPkey')
    clock_offset = Attribute('ipatokenTOTPclockOffset')
    time_step = Attribute('ipatokenTOTPtimeStep')
