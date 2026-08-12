import json, re, base64, time, secrets, random, requests, uuid, urllib.parse, hashlib, hmac

class InstaGram:
    def __init__(self, user, pas):
        self.user = user
        self.pas = pas
        self.host = random.choice(["i.instagram.com", "b.i.instagram.com"])
        self.bloks_version = "6a3cbff91965fad8f65457930cea7353a2020e5da081014807c72af8ff4e8334"
        self.user_agent = "Instagram 461.0.0.43.85 Android (31/12; 480dpi; 1080x2400; OnePlus; PJD110; marlin; qcom; en_US; 1001775661)"
        self.session = requests.Session()
        self.csrf_token = None
        self.device_id = self._device_id()
        self.family_device_id = self._family_device_id()
        self.machine_id = self._machine_id()

    def _headers(self, extra=None):
        headers = {
            'accept-language': 'en-US',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'ig-intended-user-id': '0',
            'priority': 'u=3',
            'x-bloks-is-layout-rtl': 'false',
            'x-bloks-prism-button-version': 'INDIGO_PRIMARY_BORDERED_SECONDARY',
            'x-bloks-prism-colors-enabled': 'true',
            'x-bloks-prism-extended-palette-gray': 'true',
            'x-bloks-prism-extended-palette-indigo': 'true',
            'x-bloks-prism-extended-palette-polish-enabled': 'true',
            'x-bloks-prism-extended-palette-red': 'true',
            'x-bloks-prism-extended-palette-rest-of-colors': 'true',
            'x-bloks-prism-font-enabled': 'true',
            'x-bloks-prism-indigo-link-version': '1',
            'x-bloks-version-id': self.bloks_version,
            'x-fb-client-ip': 'True',
            'x-fb-connection-type': 'WIFI',
            'x-fb-friendly-name': 'IgApi: bloks/async_action/com.bloks.www.bloks.caa.login.async.send_login_request/',
            'x-fb-network-properties': 'Wifi;Validated;',
            'x-fb-request-analytics-tags': '{"network_tags":{"product":"567067343352427","surface":"undefined","request_category":"api","purpose":"fetch","retry_attempt":"0"}}',
            'x-fb-server-cluster': 'True',
            'x-ig-android-id': 'android-' + secrets.token_hex(8),
            'x-ig-app-id': '567067343352427',
            'x-ig-app-locale': 'en_US',
            'x-ig-bandwidth-speed-kbps': str(random.randint(5000, 15000)) + '.000',
            'x-ig-bandwidth-totalbytes-b': str(random.randint(5000000, 20000000)),
            'x-ig-bandwidth-totaltime-ms': str(random.randint(1000, 5000)),
            'x-ig-capabilities': '3brTv10=',
            'x-ig-connection-type': 'WIFI',
            'x-ig-device-id': self.device_id,
            'x-ig-device-locale': 'en_US',
            'x-ig-family-device-id': self.family_device_id,
            'x-ig-is-foldable': 'false',
            'x-ig-mapped-locale': 'en_US',
            'x-ig-timezone-offset': str(random.choice([19800, 0, -18000, -25200, 3600])),
            'x-ig-www-claim': '0',
            'x-mid': self.machine_id,
            'x-meta-usdid': str(uuid.uuid4()) + '.1' + str(int(time.time())) + '.MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAE_qZAJ2CNnrKGXvlimSZ5h-FZ3Wq7nj__rx2MQi-lmLay3XEC3O0TKrrV-w_19Ft5unPiY1k43NSggixNYxw1Iw.MEUCIHldsNiJ-GkeKMTiw62tb9UmCc38TB2T9SwDSXFYo_BuAiEAhN_ZIIwlFgmx9zFaeIkgCaLikFo8SXmISB8v8qoeusU',
            'x-pigeon-rawclienttime': f'{time.time()}',
            'x-pigeon-session-id': 'UFS-' + str(uuid.uuid4()) + '-0',
            'x-tigon-is-retry': 'False',
            'user-agent': self.user_agent,
            'x-fb-appnetsession-nid': secrets.token_hex(16) + ',Wifi',
            'x-fb-appnetsession-sid': secrets.token_hex(16),
            'x-fb-conn-uuid-client': str(uuid.uuid4()).replace('-', ''),
            'x-fb-http-engine': 'Tigon/MNS/TCP',
            'x-fb-rmd': 'state=URL_ELIGIBLE',
            'x-fb-session-id': 'nid=' + secrets.token_urlsafe(12) + ';nc=1;fc=1;bc=0;',
            'x-fb-session-private': secrets.token_urlsafe(12),
        }
        
        if self.csrf_token:
            headers['x-csrftoken'] = self.csrf_token
            
        if extra:
            headers.update(extra)
            
        return headers

    def _bk_context(self):
        return json.dumps({
            "bloks_version": self.bloks_version,
            "styles_id": "instagram"
        }, separators=(',', ':'))

    def _device_id(self):
        return f"android-{str(uuid.uuid4().hex)[:16]}"

    def _machine_id(self):
        return str("a" + secrets.token_urlsafe(20))

    def _family_device_id(self):
        return str(uuid.uuid4())

    def _print_result(self, token, sessionid):
        print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Target    : {self.user}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Password  : {self.pas}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOKEN App : {token}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Sessionid : {sessionid}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 By : @rejerks
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

    def _extract_session(self, response):
        m = re.search(r'IG-Set-Authorization.*?IGT:\d+:([A-Za-z0-9+/=_-]+)', response)
        if m:
            token = m.group(1)
            padding = 4 - len(token) % 4
            if padding != 4:
                token += '=' * padding
            try:
                decoded = base64.b64decode(token).decode()
                s = re.search(r'"sessionid":"([^"]+)"', decoded)
                if s:
                    return token, s.group(1)
            except:
                pass
        return None, None

    def _sleep(self, seconds, message):
        print(f"[*] {message}")
        time.sleep(seconds)

    def _save_response(self, response, label):
        with open("response.txt", "a", encoding='utf-8') as f:
            f.write(f"\n{'='*80}\n[{label}]\n{'='*80}\n{response}\n")

    def _extract_context(self, response):
        patterns = [
            r'\(dkc\s+"([^"]*\|aplc)"',
            r'context_data["\']?\s*[:=]\s*["\']([^"\']*\|aplc)',
            r'([A-Za-z0-9_\-/+\|=]{100,}\|aplc)',
            r'"([^"]+\|aplc)"',
            r'([A-Za-z0-9_\-+=]{100,}\|aplc)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response, re.DOTALL)
            if match:
                context = match.group(1)
                context = context.replace('\\/', '/').replace('\\\\', '\\')
                return context
        return None

    def _get_2fa_methods(self, context):
        payload = {
            'params': json.dumps({
                "client_input_params": {
                    "auth_secure_device_id": "",
                    "accounts_list": [],
                    "has_whatsapp_installed": 0,
                    "family_device_id": self.family_device_id,
                    "machine_id": self.machine_id
                },
                "server_params": {
                    "use_open_instead_of_push": 0,
                    "context_data": context,
                    "INTERNAL__latency_qpl_marker_id": 36707139,
                    "INTERNAL__latency_qpl_instance_id": 1.84762981400001e14,
                    "device_id": self.device_id,
                    "use_close_instead_of_back": 0
                }
            }, separators=(',', ':')),
            'bk_client_context': self._bk_context(),
            'bloks_versioning_id': self.bloks_version
        }
        
        response = self.session.post(
            f"https://{self.host}/api/v1/bloks/async_action/com.bloks.www.ap.two_step_verification.entrypoint_async/",
            data=payload,
            headers=self._headers()
        ).text
        
        self._save_response(response, "2FA_ENTRYPOINT")
        return response

    def _handle_limbo_proactive(self, response, is_fallback=False):
        limbo_contx = self._extract_context(response)
        if not limbo_contx:
            print("[!] Could not extract limbo context")
            return False

        payload_limbo = {
            'params': json.dumps({
                "client_input_params": {
                    "aac": json.dumps({
                        "aac_init_timestamp": int(time.time()),
                        "aacjid": str(uuid.uuid4()),
                        "aaccs": secrets.token_urlsafe(32)
                    })
                },
                "server_params": {
                    "context_data": limbo_contx,
                    "show_close_button": 0,
                    "device_id": self.device_id,
                    "INTERNAL_INFRA_screen_id": "limbo_proactive",
                    "is_dismissable": 1
                }
            }, separators=(',', ':')),
            'bk_client_context': self._bk_context(),
            'bloks_versioning_id': self.bloks_version
        }

        print("[*] Sending limbo_proactive request...")
        host = "b.i.instagram.com" if is_fallback else self.host
        response_limbo = self.session.post(
            f"https://{host}/api/v1/bloks/apps/com.bloks.www.ap.two_step_verification.limbo_proactive/",
            data=payload_limbo,
            headers=self._headers()
        ).text
        
        self._save_response(response_limbo, "LIMBO_PROACTIVE")

        if '"status":"ok"' in response_limbo.replace("/", "").replace("\\", ""):
            print("[⚠] Device approval required!")
            print("[*] Check another device logged into this account and approve the login")
            input("[ * ] - Press ENTER after approving on another device: ")
            return "retry"
        return False

    def login(self):
        with open("response.txt", "w", encoding='utf-8') as f:
            f.write("[Login Session Start]\n")

        max_retries = 10
        retry_count = 0
        
        while retry_count < max_retries:
            payload = {
                'params': json.dumps({
                    "server_params": {
                        "device_id": self.device_id,
                        "server_login_source": "login",
                        "waterfall_id": str(uuid.uuid4()),
                        "machine_id": self.machine_id,
                        "from_native_screen": True,
                        "credential_type": "password",
                        "password": f"#PWD_INSTAGRAM:0:{str(int(time.time()))}:{self.pas}",
                        "try_num": "12",
                        "family_device_id": self.family_device_id,
                        "event_flow": "login_manual",
                        "event_step": "home_page",
                        "is_from_logged_in_switcher": False,
                        "contact_point": self.user
                    }
                }, separators=(',', ':')),
                'bk_client_context': self._bk_context(),
                'bloks_versioning_id': self.bloks_version
            }

            print(f"[*] Sending login request for {self.user}...")
            response = self.session.post(
                f"https://{self.host}/api/v1/bloks/async_action/com.bloks.www.bloks.caa.login.async.send_login_request/",
                data=payload,
                headers=self._headers()
            ).text

            response_clean = response.replace("/", "").replace("\\", "")
            self._save_response(response_clean, "LOGIN_REQUEST")

            token, sessionid = self._extract_session(response_clean)

            if token:
                self._print_result(token, sessionid)
                return True

            if "limbo_proactive" in response:
                self._save_response(response, "LIMBO_RESPONSE")
                self._sleep(3, "Waiting 3 seconds before limbo_proactive request...")
                result = self._handle_limbo_proactive(response, False)
                if result == "retry":
                    retry_count += 1
                    continue
                return result

            if "two_step_verification" in response:
                self._save_response(response, "2FA_RESPONSE")
                result = self._handle_2fa_direct(response)
                if result == "retry":
                    retry_count += 1
                    continue
                return result

            if "password" in response.lower() and ("incorrect" in response.lower() or "wrong" in response.lower()):
                print("Username or password miss Match")
                return False

            if "invalid" in response.lower() or "error" in response.lower():
                print(f"[!] Error: Check response.txt for details")
                return False

            if "challenge" in response.lower() or "checkpoint" in response.lower():
                print("[!] Challenge required. Check response.txt for details")
                return False

            print("[!] Unknown response. Check response.txt for details")
            return False
        
        print("[!] Max retries exceeded")
        return False

    def _handle_2fa_direct(self, response):
        self._sleep(3, "Waiting 3 seconds before 2FA entrypoint...")

        contx = self._extract_context(response)
        if not contx:
            print("[!] Could not extract context from response")
            return False

        print("[*] Requesting 2FA methods...")
        response2 = self._get_2fa_methods(contx)
        response2_clean = response2.replace("/", "").replace("\\", "")
        
        if "limbo_proactive" in response2:
            print("[*] Limbo proactive required...")
            return self._handle_limbo_proactive(response2, True)

        if "two_step_verification" not in response2_clean:
            print("[!] Unexpected 2FA response")
            return False

        contx2 = self._extract_context(response2_clean)
        if not contx2:
            print("[!] Could not extract 2FA context")
            return False

        self._sleep(2, "Waiting for code entry...")
        
        code_entry_payload = {
            'params': json.dumps({
                "server_params": {
                    "context_data": contx2,
                    "show_close_button": 0,
                    "device_id": self.device_id,
                    "INTERNAL_INFRA_screen_id": "generic_code_entry"
                }
            }, separators=(',', ':')),
            'bk_client_context': self._bk_context(),
            'bloks_versioning_id': self.bloks_version
        }

        print("[*] Loading code entry screen...")
        response3 = self.session.post(
            f"https://{self.host}/api/v1/bloks/apps/com.bloks.www.ap.two_step_verification.code_entry/",
            data=code_entry_payload,
            headers=self._headers()
        ).text

        response3_clean = response3.replace("/", "").replace("\\", "")
        self._save_response(response3_clean, "CODE_ENTRY_SCREEN")

        contx3 = self._extract_context(response3_clean)
        if not contx3:
            print("[!] Could not extract code entry context")
            return False

        print("[*] Enter 2FA code from your authenticator app or SMS")
        code = input("[ * ] - Enter The Code : ")

        verify_payload = {
            'params': json.dumps({
                "client_input_params": {
                    "auth_secure_device_id": "",
                    "code": code,
                    "family_device_id": self.family_device_id,
                    "device_id": self.device_id,
                    "machine_id": self.machine_id
                },
                "server_params": {
                    "context_data": contx3,
                    "INTERNAL__latency_qpl_marker_id": 36707139,
                    "INTERNAL__latency_qpl_instance_id": 1.847912435E14,
                    "device_id": self.device_id
                }
            }, separators=(',', ':')),
            'bk_client_context': self._bk_context(),
            'bloks_versioning_id': self.bloks_version
        }

        print("[*] Verifying the entered code...")
        response4 = self.session.post(
            f"https://{self.host}/api/v1/bloks/async_action/com.bloks.www.ap.two_step_verification.code_entry_async/",
            data=verify_payload,
            headers=self._headers()
        ).text

        response4_clean = response4.replace("/", "").replace("\\", "")
        self._save_response(response4_clean, "CODE_VERIFICATION")
        
        token, sessionid = self._extract_session(response4_clean)

        if token:
            self._print_result(token, sessionid)
            return True
        
        print("[!] Invalid code or verification failed")
        return False

user_or_email = input("Enter username or email: ")
password = input("Enter password: ")
InstaGram(user_or_email, password).login()