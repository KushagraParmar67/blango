from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class AnonSustainedThrottle(AnonRateThrottle):
  scope = "anon_sustained"

class AnonBrustThrottle(AnonRateThrottle):
  scope = "anon_brust"

class UserSustainedThrottle(UserRateThrottle):
  scope = "user_sustained"

class UserBrustThrottle(UserRateThrottle):
  scope = "user_brust"