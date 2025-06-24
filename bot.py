from aiohttp import (
    ClientResponseError,
    ClientSession,
    ClientTimeout
)
from aiohttp_socks import ProxyConnector
from eth_account.messages import encode_defunct
from eth_utils import to_hex
from eth_account import Account
from datetime import datetime, timezone
from colorama import *
import asyncio, random, time, json, os, pytz

wib = pytz.timezone('Asia/Jakarta')

USER_AGENT = [
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
  "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0"
]

class Sixpence:
    def __init__(self) -> None:
        self.BASE_API = "https://us-central1-openoracle-de73b.cloudfunctions.net/backend_apis/api/service"
        self.BASE_HEADERS = {}
        self.WSS_HEADERS = {}
        self.ref_code = "T4HWGQ" # U can change it with yours.
        self.proxies = []
        self.proxy_index = 0
        self.account_proxies = {}
        self.access_tokens = {}
        self.wss_tokens = {}
        self.exp_time = {}
        self.nonce = {}

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "\n" + "═" * 60)
        print(Fore.GREEN + Style.BRIGHT + "    ⚡ Sixpence Automation BOT  ⚡")
        print(Fore.CYAN + Style.BRIGHT + "    ────────────────────────────────")
        print(Fore.YELLOW + Style.BRIGHT + "    🧠 Project    : Sixpence - Automation Bot")
        print(Fore.YELLOW + Style.BRIGHT + "    🧑‍💻 Author     : YetiDAO")
        print(Fore.YELLOW + Style.BRIGHT + "    🌐 Status     : Running & Monitoring...")
        print(Fore.CYAN + Style.BRIGHT + "    ────────────────────────────────")
        print(Fore.MAGENTA + Style.BRIGHT + "    🧬 Powered by Cryptodai3 × YetiDAO | Buddy v1.0 🚀")
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "═" * 60 + "\n")

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    
    def load_accounts(self):
        filename = "tokens.json"
        try:
            if not os.path.exists(filename):
                self.log(f"{Fore.RED}File {filename} Not Found.{Style.RESET_ALL}")
                return

            with open(filename, 'r') as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                return []
        except json.JSONDecodeError:
            return []
    
    async def load_proxies(self, use_proxy_choice: int):
        filename = "proxy.txt"
        try:
            if use_proxy_choice == 1:
                async with ClientSession(timeout=ClientTimeout(total=30)) as session:
                    async with session.get("https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text") as response:
                        response.raise_for_status()
                        content = await response.text()
                        with open(filename, 'w') as f:
                            f.write(content)
                        self.proxies = [line.strip() for line in content.splitlines() if line.strip()]
            else:
                if not os.path.exists(filename):
                    self.log(f"{Fore.RED + Style.BRIGHT}File {filename} Not Found.{Style.RESET_ALL}")
                    return
                with open(filename, 'r') as f:
                    self.proxies = [line.strip() for line in f.read().splitlines() if line.strip()]
            
            if not self.proxies:
                self.log(f"{Fore.RED + Style.BRIGHT}No Proxies Found.{Style.RESET_ALL}")
                return

            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Proxies Total  : {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(self.proxies)}{Style.RESET_ALL}"
            )
        
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}Failed To Load Proxies: {e}{Style.RESET_ALL}")
            self.proxies = []

    def check_proxy_schemes(self, proxies):
        schemes = ["http://", "https://", "socks4://", "socks5://"]
        if any(proxies.startswith(scheme) for scheme in schemes):
            return proxies
        return f"http://{proxies}"

    def get_next_proxy_for_account(self, email):
        if email not in self.account_proxies:
            if not self.proxies:
                return None
            proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
            self.account_proxies[email] = proxy
            self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return self.account_proxies[email]

    def rotate_proxy_for_account(self, email):
        if not self.proxies:
            return None
        proxy = self.check_proxy_schemes(self.proxies[self.proxy_index])
        self.account_proxies[email] = proxy
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        return proxy
    
    def generate_address(self, account: str):
        try:
            account = Account.from_key(account)
            address = account.address
            
            return address
        except Exception as e:
            return None
        
    def mask_account(self, account):
        try:
            mask_account = account[:6] + '*' * 6 + account[-6:]
            return mask_account 
        except Exception as e:
            return None
    
    def generate_payload(self, account: str, address: str, type=None):
        try:
            issued_at = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
            message = f"bcakokeeafaehcajfkajcpbdkfnoahlh wants you to sign in with your Ethereum account:\n{address}\n\nBy signing, you are proving you own this wallet and logging in. This does not initiate a transaction or cost any fees.\n\nURI: chrome-extension://bcakokeeafaehcajfkajcpbdkfnoahlh\nVersion: 1\nChain ID: 42000\nNonce: {self.nonce[address]}\nIssued At: {issued_at}"
            encoded_message = encode_defunct(text=message)
            signed_message = Account.sign_message(encoded_message, private_key=account)
            signature = to_hex(signed_message.signature)

            payload = {
                "message":message, 
                "signature":signature
            }

            if type == "websocket":
                payload = {
                    "userId": address,
                    "message":message, 
                    "signature":signature
                }
            
            return payload
        except Exception as e:
            raise Exception(f"Generate Req Payload Failed: {str(e)}")

    def print_message(self, account, proxy, color, message):
        self.log(
            f"{Fore.CYAN + Style.BRIGHT}[ Account:{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} {self.mask_account(account)} {Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT}-{Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT} Proxy: {Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT}{proxy}{Style.RESET_ALL}"
            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}Status:{Style.RESET_ALL}"
            f"{color + Style.BRIGHT} {message} {Style.RESET_ALL}"
            f"{Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}"
        )

    def print_question(self):
        while True:
            try:
                print(f"{Fore.WHITE + Style.BRIGHT}1. Run With Free Proxyscrape Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}2. Run With Private Proxy{Style.RESET_ALL}")
                print(f"{Fore.WHITE + Style.BRIGHT}3. Run Without Proxy{Style.RESET_ALL}")
                choose = int(input(f"{Fore.BLUE + Style.BRIGHT}Choose [1/2/3] -> {Style.RESET_ALL}").strip())

                if choose in [1, 2, 3]:
                    proxy_type = (
                        "With Free Proxyscrape" if choose == 1 else 
                        "With Private" if choose == 2 else 
                        "Without"
                    )
                    print(f"{Fore.GREEN + Style.BRIGHT}Run {proxy_type} Proxy Selected.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Please enter either 1, 2 or 3.{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter a number (1, 2 or 3).{Style.RESET_ALL}")

        rotate = False
        if choose in [1, 2]:
            while True:
                rotate = input(f"{Fore.BLUE + Style.BRIGHT}Rotate Invalid Proxy? [y/n] -> {Style.RESET_ALL}").strip()

                if rotate in ["y", "n"]:
                    rotate = rotate == "y"
                    break
                else:
                    print(f"{Fore.RED + Style.BRIGHT}Invalid input. Enter 'y' or 'n'.{Style.RESET_ALL}")

        return choose, rotate
    
    async def check_connection(self, address: str, proxy=None):
        connector = ProxyConnector.from_url(proxy) if proxy else None
        try:
            async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                async with session.post(url="http://ip-api.com/json") as response:
                    response.raise_for_status()
                    return await response.json()
        except (Exception, ClientResponseError) as e:
            self.print_message(address, proxy, Fore.RED, f"Connection Not 200 OK: {Fore.YELLOW+Style.BRIGHT}{str(e)}{Style.RESET_ALL}")
            return None
    
    async def get_nonce(self, address: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/{address}/nonce?"
        headers = self.BASE_HEADERS[address].copy()
        headers["Authorization"] = "Bearer null"
        headers["Content-Type"] = "application/json"
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(address, proxy, Fore.RED, f"GET Nonce Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}{Style.RESET_ALL}")

        return None
    
    async def user_login(self, account: str, address: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/login"
        data = json.dumps(self.generate_payload(account, address))
        headers = self.BASE_HEADERS[address].copy()
        headers["Authorization"] = "Bearer null"
        headers["Content-Length"] = str(len(data))
        headers["Content-Type"] = "application/json"
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(address, proxy, Fore.RED, f"Login Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}{Style.RESET_ALL}")

        return None
    
    async def user_info(self, account: str, address: str, use_proxy: bool, rotate_proxy: bool, proxy=None, retries=5):
        url = f"{self.BASE_API}/userInfo?"
        headers = self.BASE_HEADERS[address].copy()
        headers["Authorization"] = f"Bearer {self.access_tokens[address]}"
        headers["Content-Type"] = "application/json"
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers, ssl=False) as response:
                        if response.status == 401:
                            await self.process_user_login(account, address, use_proxy, rotate_proxy)
                            headers["Authorization"] = f"Bearer {self.access_tokens[address]}"
                            continue
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(address, proxy, Fore.RED, f"GET Earning Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}{Style.RESET_ALL}")

        return None
    
    async def bind_invite(self, address: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/inviteBind"
        data = json.dumps({"inviteCode":self.ref_code})
        headers = self.BASE_HEADERS[address].copy()
        headers["Authorization"] = f"Bearer {self.access_tokens[address]}"
        headers["Content-Length"] = str(len(data))
        headers["Content-Type"] = "application/json"
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(address, proxy, Fore.RED, f"Bind Invite Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}{Style.RESET_ALL}")

        return None
    
    async def egg_info(self, address: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/getEggInfo?"
        headers = self.BASE_HEADERS[address].copy()
        headers["Authorization"] = f"Bearer {self.access_tokens[address]}"
        headers["Content-Type"] = "application/json"
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.get(url=url, headers=headers, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(address, proxy, Fore.RED, f"GET Egg Info Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}{Style.RESET_ALL}")

        return None
    
    async def register_companion(self, address: str, egg_id: str, proxy=None, retries=5):
        url = f"{self.BASE_API}/registerCompanion"
        data = json.dumps({"eggInfoId":egg_id, "name":"sixpenceai"})
        headers = self.BASE_HEADERS[address].copy()
        headers["Authorization"] = f"Bearer {self.access_tokens[address]}"
        headers["Content-Length"] = str(len(data))
        headers["Content-Type"] = "application/json"
        for attempt in range(retries):
            connector = ProxyConnector.from_url(proxy) if proxy else None
            try:
                async with ClientSession(connector=connector, timeout=ClientTimeout(total=60)) as session:
                    async with session.post(url=url, headers=headers, data=data, ssl=False) as response:
                        response.raise_for_status()
                        return await response.json()
            except (Exception, ClientResponseError) as e:
                if attempt < retries - 1:
                    await asyncio.sleep(5)
                    continue
                self.print_message(address, proxy, Fore.RED, f"Registering Companion Failed: {Fore.YELLOW+Style.BRIGHT}{str(e)}{Style.RESET_ALL}")

        return None

    async def process_check_connection(self, address: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None

            check = await self.check_connection(address, proxy)
            if check and check.get("status") == "success":
                return True
            
            if rotate_proxy:
                proxy = self.rotate_proxy_for_account(address)

            await asyncio.sleep(5)

    async def process_get_nonce(self, address: str, use_proxy: bool, rotate_proxy: bool):
        is_valid = await self.process_check_connection(address, use_proxy, rotate_proxy)
        if is_valid:
            while True:
                proxy = self.get_next_proxy_for_account(address) if use_proxy else None

                request = await self.get_nonce(address, proxy)
                if request and request.get("msg") == "ok":
                    self.nonce[address] = request["data"]["nonce"]
                    self.exp_time[address] = request["data"]["expireTime"]
                    return True

                await asyncio.sleep(5)

    async def process_user_login(self, account: str, address: str, use_proxy: bool, rotate_proxy: bool):
        requested = await self.process_get_nonce(address, use_proxy, rotate_proxy)
        if requested:
            while True:
                proxy = self.get_next_proxy_for_account(address) if use_proxy else None

                login = await self.user_login(account, address, proxy)
                if login and login.get("msg") == "success":
                    self.access_tokens[address] = login["data"]["token"]

                    self.print_message(address, proxy, Fore.GREEN, "Login Success")
                    return True

                await asyncio.sleep(5)

    async def process_register_companion(self, address: str, use_proxy: bool):
        proxy = self.get_next_proxy_for_account(address) if use_proxy else None

        egg = await self.egg_info(address, proxy)
        if egg and egg.get("msg") == "ok":
            egg_id = egg["data"][0]["id"]

            register = await self.register_companion(address, egg_id, proxy)
            if register:
                self.print_message(address, proxy, Fore.GREEN, "Companion Registered Successfully")

    async def process_get_earning(self, account: str, address: str, use_proxy: bool, rotate_proxy: bool):
        while True:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None

            user = await self.user_info(account, address, use_proxy, rotate_proxy, proxy)
            if user and user.get("msg") == "ok":
                current_points = user["data"]["point"]["currentPoints"]

                self.print_message(address, proxy, Fore.WHITE, f"Earning: {current_points} PTS")

                invited = user.get("data", {}).get("referral", {}).get("inviteCode", None)
                if invited is None:
                    await self.bind_invite(address, proxy)

                egg_info_id = user.get("data", {}).get("eggInfo", {}).get("eggInfoId", None)
                if egg_info_id is None:
                    await self.process_register_companion(address, use_proxy)

            await asyncio.sleep(60)

    async def connect_websocket(self, account: str, address: str, use_proxy: bool, rotate_proxy: bool):
        wss_url = "wss://ws.sixpence.ai/"
        connected = False

        while True:
            proxy = self.get_next_proxy_for_account(address) if use_proxy else None
            connector = ProxyConnector.from_url(proxy) if proxy else None
            session = ClientSession(connector=connector, timeout=ClientTimeout(total=300))
            try:
                async with session.ws_connect(wss_url, headers=self.WSS_HEADERS[address]) as wss:
                    
                    payload = {
                        "type": "extension_auth",
                        "data": self.generate_payload(account, address, "websocket")
                    }
                    await wss.send_json(payload)
                    self.print_message(address, proxy, Fore.GREEN, "Websocket Is Connected")
                    connected = True

                    if connected:
                        one_days_time = 24 * 60 * 60
                        reconnect_time = int(time.time()) + one_days_time

                        try:
                            response = await wss.receive_json()
                            if response.get("msg") == "auth success":
                                self.wss_tokens[address] = response["data"]["token"]

                                self.print_message(address, proxy, Fore.GREEN, "Authenticate Success")

                                while True:
                                    if int(time.time()) <= reconnect_time:
                                        payload = {
                                            "type": "extension_heartbeat",
                                            "token": self.wss_tokens[address],
                                            "address": address,
                                            "taskEnable": False
                                        }
                                        await wss.send_json(payload)
                                        self.print_message(address, proxy, Fore.BLUE, "Heartbeat Sent")
                                        await asyncio.sleep(30)

                                    else:
                                        raise Exception("Time to Reconnect")

                        except Exception as e:
                            self.print_message(address, proxy, Fore.YELLOW, f"Websocket Connection Closed: {Fore.RED + Style.BRIGHT}{str(e)}")
                            await asyncio.sleep(5)

                            if int(time.time()) > self.exp_time[address]:
                                await self.process_user_login(account, address, use_proxy, rotate_proxy)

                            connected = False
                            await asyncio.sleep(5)

            except Exception as e:
                self.print_message(address, proxy, Fore.RED, f"Websocket Not Connected: {Fore.YELLOW + Style.BRIGHT}{str(e)}")
                await asyncio.sleep(5)

            except asyncio.CancelledError:
                self.print_message(address, proxy, Fore.YELLOW, "Websocket Closed")
                break
            finally:
                await session.close()

    async def process_accounts(self, account: str, address: str, use_proxy: bool, rotate_proxy: bool):
        logined = await self.process_user_login(account, address, use_proxy, rotate_proxy)
        if logined:
            tasks = [
                asyncio.create_task(self.process_get_earning(account, address, use_proxy, rotate_proxy)),
                asyncio.create_task(self.connect_websocket(account, address, use_proxy, rotate_proxy))
            ]
            await asyncio.gather(*tasks)

    async def main(self):
        try:
            with open('accounts.txt', 'r') as file:
                accounts = [line.strip() for line in file if line.strip()]
            
            use_proxy_choice, rotate_proxy = self.print_question()

            use_proxy = False
            if use_proxy_choice in [1, 2]:
                use_proxy = True

            self.clear_terminal()
            self.welcome()
            self.log(
                f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT}{len(accounts)}{Style.RESET_ALL}"
            )

            if use_proxy:
                await self.load_proxies(use_proxy_choice)

            self.log(f"{Fore.CYAN + Style.BRIGHT}={Style.RESET_ALL}"*75)

            tasks = []
            for idx, account in enumerate(accounts, start=1):
                if account:
                    address = self.generate_address(account)

                    if not address:
                        self.log(
                            f"{Fore.CYAN + Style.BRIGHT}[ Account: {Style.RESET_ALL}"
                            f"{Fore.WHITE + Style.BRIGHT}{idx}{Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT} - {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}Status:{Style.RESET_ALL}"
                            f"{Fore.RED + Style.BRIGHT} Invalid Private Key or Library Version Not Supported {Style.RESET_ALL}"
                            f"{Fore.CYAN + Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                        continue

                    user_agent = random.choice(USER_AGENT)

                    self.WSS_HEADERS[address] = {
                        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
                        "Cache-Control": "no-cache",
                        "Connection": "Upgrade",
                        "Host": "ws.sixpence.ai",
                        "Origin": "chrome-extension://bcakokeeafaehcajfkajcpbdkfnoahlh",
                        "Pragma": "no-cache",
                        "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
                        "Sec-WebSocket-Key": "g0PDYtLWQOmaBE5upOBXew==",
                        "Sec-WebSocket-Version": "13",
                        "Upgrade": "websocket",
                        "User-Agent": user_agent
                    }

                    self.BASE_HEADERS[address] = {
                        "Accept": "application/json, text/plain, */*",
                        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
                        "Origin": "chrome-extension://bcakokeeafaehcajfkajcpbdkfnoahlh",
                        "Sec-Fetch-Dest": "empty",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Site": "none",
                        "Sec-Fetch-Storage-Access": "active",
                        "User-Agent": user_agent
                    }

                    tasks.append(asyncio.create_task(self.process_accounts(account, address, use_proxy, rotate_proxy)))

            await asyncio.gather(*tasks)

        except FileNotFoundError:
            self.log(f"{Fore.RED}File 'accounts.txt' Not Found.{Style.RESET_ALL}")
            return
        except Exception as e:
            self.log(f"{Fore.RED+Style.BRIGHT}Error: {e}{Style.RESET_ALL}")
            raise e

if __name__ == "__main__":
    try:
        bot = Sixpence()
        asyncio.run(bot.main())
    except KeyboardInterrupt:
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
            f"{Fore.RED + Style.BRIGHT}[ EXIT ] Sixpence - BOT{Style.RESET_ALL}                                       "                              
        )
