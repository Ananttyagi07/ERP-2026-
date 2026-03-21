"""
Security Utility Functions
IP detection, device fingerprinting, geolocation, etc.
"""
import hashlib
import user_agents
from datetime import datetime, timedelta
from ipware import get_client_ip as ipware_get_client_ip
def get_client_ip(request):
    """
    Get client IP address from request
    Handles proxies and load balancers
    """
    client_ip, is_routable = ipware_get_client_ip(request)
    return client_ip or '127.0.0.1'


def get_user_agent(request):
    """Get full user agent string"""
    return request.META.get('HTTP_USER_AGENT', '')


def detect_device_type(request):
    """
    Detect device type: mobile, tablet, desktop, bot
    """
    ua_string = get_user_agent(request)
    ua = user_agents.parse(ua_string)

    if ua.is_mobile:
        return 'mobile'
    elif ua.is_tablet:
        return 'tablet'
    elif ua.is_bot:
        return 'bot'
    else:
        return 'desktop'


def get_device_name(request):
    """
    Get human-readable device name
    Examples: "Chrome on Windows", "Safari on iPhone"
    """
    ua_string = get_user_agent(request)
    ua = user_agents.parse(ua_string)

    browser = ua.browser.family
    os = ua.os.family

    if ua.is_mobile:
        device = ua.device.family
        return f"{browser} on {device}"
    else:
        return f"{browser} on {os}"


def get_device_details(request):
    """
    Get detailed device information
    """
    ua_string = get_user_agent(request)
    ua = user_agents.parse(ua_string)

    return {
        'type': detect_device_type(request),
        'brand': ua.device.brand or '',
        'model': ua.device.model or '',
        'name': get_device_name(request),
        'browser': {
            'family': ua.browser.family,
            'version': ua.browser.version_string,
        },
        'os': {
            'family': ua.os.family,
            'version': ua.os.version_string,
        },
        'is_mobile': ua.is_mobile,
        'is_tablet': ua.is_tablet,
        'is_pc': ua.is_pc,
        'is_bot': ua.is_bot,
    }


def generate_device_fingerprint(request):
    """
    Generate unique device fingerprint
    Combines IP, User-Agent, and other headers
    """
    components = [
        get_client_ip(request),
        get_user_agent(request),
        request.META.get('HTTP_ACCEPT_LANGUAGE', ''),
        request.META.get('HTTP_ACCEPT_ENCODING', ''),
    ]

    fingerprint_string = '|'.join(components)
    return hashlib.sha256(fingerprint_string.encode()).hexdigest()


def get_geolocation(ip_address):
    """
    Get geolocation from IP address using GeoIP2
    Returns: dict with country, city, coordinates
    """
    if ip_address in ['127.0.0.1', 'localhost', '::1']:
        return {
            'country': 'Local',
            'country_code': 'LC',
            'city': 'Localhost',
            'region': '',
            'latitude': None,
            'longitude': None,
        }

    try:
        import geoip2.database
        from django.conf import settings
        import os

        # Try to use GeoLite2 database if available
        geoip_path = getattr(settings, 'GEOIP_PATH', None)
        if not geoip_path:
            # Default path
            geoip_path = os.path.join(settings.BASE_DIR, 'geoip')

        city_db_path = os.path.join(geoip_path, 'GeoLite2-City.mmdb')

        if os.path.exists(city_db_path):
            with geoip2.database.Reader(city_db_path) as reader:
                response = reader.city(ip_address)

                return {
                    'country': response.country.name or '',
                    'country_code': response.country.iso_code or '',
                    'city': response.city.name or '',
                    'region': response.subdivisions.most_specific.name if response.subdivisions else '',
                    'latitude': float(response.location.latitude) if response.location.latitude else None,
                    'longitude': float(response.location.longitude) if response.location.longitude else None,
                }
    except Exception as e:
        # Fallback: try ip-api.com (free, no key required, 45 req/min limit)
        try:
            import requests
            response = requests.get(
                f'http://ip-api.com/json/{ip_address}',
                timeout=2
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return {
                        'country': data.get('country', ''),
                        'country_code': data.get('countryCode', ''),
                        'city': data.get('city', ''),
                        'region': data.get('regionName', ''),
                        'latitude': data.get('lat'),
                        'longitude': data.get('lon'),
                    }
        except:
            pass

    # If all fails, return empty geolocation
    return {
        'country': '',
        'country_code': '',
        'city': '',
        'region': '',
        'latitude': None,
        'longitude': None,
    }


def calculate_trust_score(user, request):
    """
    Calculate trust score for a login attempt (0-100)
    Higher score = more trustworthy
    """
    score = 50  # Start neutral

    # Check if IP is known
    from apps.authentication.models_security import UserSession
    known_ips = UserSession.objects.filter(
        user=user,
        status='active'
    ).values_list('ip_address', flat=True).distinct()

    ip = get_client_ip(request)

    if ip in known_ips:
        score += 20  # Known IP

    # Check if device fingerprint is known
    fingerprint = generate_device_fingerprint(request)
    known_fingerprints = UserSession.objects.filter(
        user=user,
        device_fingerprint=fingerprint
    ).exists()

    if known_fingerprints:
        score += 15  # Known device

    # Check if location is known
    geo = get_geolocation(ip)
    known_countries = UserSession.objects.filter(
        user=user,
        country_code=geo['country_code']
    ).exists()

    if known_countries:
        score += 10  # Known country

    # Check recent failed login attempts
    from apps.authentication.models_security import SecurityAuditLog
    recent_failures = SecurityAuditLog.objects.filter(
        user=user,
        event_type='login_failed',
        created_at__gte=datetime.now() - timedelta(hours=24)
    ).count()

    if recent_failures > 0:
        score -= recent_failures * 5  # Deduct for failed attempts

    # Check time of day (unusual hours = lower score)
    from datetime import datetime
    hour = datetime.now().hour
    if hour < 6 or hour > 23:
        score -= 10  # Login at unusual hours

    # Ensure score is between 0 and 100
    return max(0, min(100, score))


def detect_suspicious_login(user, request):
    """
    Detect if login attempt is suspicious
    Returns: bool
    """
    trust_score = calculate_trust_score(user, request)

    # Suspicious if trust score is very low
    if trust_score < 30:
        return True

    # Check for rapid location changes
    from apps.authentication.models_security import UserSession
    last_session = UserSession.objects.filter(
        user=user
    ).order_by('-created_at').first()

    if last_session:
        geo = get_geolocation(get_client_ip(request))
        last_geo = {'country_code': last_session.country_code}

        # If country changed in last 1 hour, suspicious
        time_diff = (datetime.now() - last_session.created_at).total_seconds()
        if (geo['country_code'] != last_geo['country_code'] and
            geo['country_code'] and last_geo['country_code'] and
            time_diff < 3600):
            return True

    return False


def is_ip_blocked(ip_address):
    """
    Check if IP is in blocklist
    Can be extended to check against threat intelligence feeds
    """
    # TODO: Implement IP blocklist
    # For now, just check against known malicious IPs
    blocked_ips = [
        # Add known malicious IPs here
    ]

    return ip_address in blocked_ips


def should_require_mfa(user, request):
    """
    Determine if MFA should be required for this login
    """
    from apps.authentication.models_security import UserMFA

    try:
        mfa = user.mfa
        if not mfa.is_enabled:
            return False

        # Always require MFA if enforced
        if mfa.is_enforced:
            return True

        # Check if device is trusted
        fingerprint = generate_device_fingerprint(request)
        if mfa.is_device_trusted(fingerprint):
            return False

        # Check trust score
        trust_score = calculate_trust_score(user, request)
        if trust_score < 50:
            return True  # Low trust = require MFA

        # Check if suspicious
        if detect_suspicious_login(user, request):
            return True

        return False

    except UserMFA.DoesNotExist:
        return False


def send_otp_sms(phone_number, code):
    """
    Send OTP via SMS
    TODO: Integrate with SMS provider (Twilio, AWS SNS, etc.)
    """
    # For development, just log it
    print(f"[SMS OTP] Sending code {code} to {phone_number}")

    # In production, use SMS provider:
    # from twilio.rest import Client
    # client = Client(account_sid, auth_token)
    # message = client.messages.create(
    #     body=f"Your verification code is: {code}",
    #     from_='+1234567890',
    #     to=phone_number
    # )

    return True


def send_otp_email(email, code):
    """
    Send OTP via email
    """
    from django.core.mail import send_mail
    from django.conf import settings

    subject = 'Your Verification Code'
    message = f"""
    Your verification code is: {code}

    This code will expire in 10 minutes.

    If you didn't request this code, please ignore this email.
    """

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"[Email OTP] Error sending: {e}")
        return False
