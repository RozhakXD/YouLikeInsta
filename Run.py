#!/usr/bin/env python3
try:
    import requests, re, json, time, random, os
    from rich.console import Console
    from rich import print as Print
    from rich.panel import Panel
    from rich.columns import Columns
    from requests.exceptions import RequestException
except ModuleNotFoundError:
    print("Please install the required modules by running: pip install -r requirements.txt")
    exit()

KOIN, DUMP, SUDAH = {
    "COUNT": 0,
}, [], []

def Banner() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    Print(Panel(r"""[bold green]      __   _       __             ___                
     ( /  /       ( /   o  /     ( /          _/_    
      (__/ __ , ,  /   ,  /<  _   / _ _   (   /  __, 
       _/_(_)(_/_(/___/(_/ |_(/__/_/ / /_/_)_(__(_/(_
      //
     (/[bold red]  ●[bold white] Coded by Rozhak-XD[bold red] -[bold white] youlikehits.com
""", width=65, style="bold bright_white"))
    return None

class Login:

    def __init__(self) -> None:
        pass

    def Cookies(self) -> None:
        try:
            Banner()
            Print(Panel(f"[bold white]Silakan Untuk Memasukkan Cookies YoulikeHits dan Cookies Ins\ntagram, Anda Bisa\nMenggunakan \"[bold green],[bold white]\" Sebagai Pemisah Antara Kedua Cookies Ini!", width=65, style="bold bright_white", subtitle="[bold bright_white]╭────", subtitle_align="left", title="[bold bright_white]>> [Login Cookies] <<"))
            cookies = Console().input("[bold bright_white]   ╰─> ")
            if "," not in cookies:
                Print(Panel(f"[bold red]Maaf, Pemisah Cookies Yang Anda Masukkan Salah atau Tidak Ada. Silakan Coba Lagi!", width=65, style="bold bright_white", title="[bold bright_white]>> [Incorrect Separator] <<"))
                exit()
            else:
                cookies = cookies.split(",")
                cookies_youlikehits, cookies_instagram = cookies[0], cookies[1]
                with open('Penyimpanan/Cookie.json', 'w') as w:
                    w.write(
                        json.dumps(
                            {
                                "Youlikehits": cookies_youlikehits,
                                "Instagram": cookies_instagram
                            }, indent=4
                        )
                    )
                username_youlikehits, email_youlikehits, coin_youlikehits = self.Periksa_Cookies_Youlikehits(cookies_youlikehits)
                full_name_instagram, username_instagram = self.Periksa_Cookies_Instagram(cookies_instagram)
                Print(Panel(f"""[bold white]Username:[bold green] {username_youlikehits}
[bold white]Link:[bold red] https://www.instagram.com/{username_instagram}
[bold white]Koin:[bold yellow] {coin_youlikehits}""", width=65, style="bold bright_white", title="[bold bright_white]>> [Welcome] <<"))
                time.sleep(5.5)
                Features()
        except Exception as e:
            Print(Panel(f"[bold red]{str(e).title()}!", width=65, style="bold bright_white", title="[bold bright_white]>> [Error] <<"))
            exit()

    def Periksa_Cookies_Youlikehits(self, cookies_youlikehits: str) -> tuple:
        with requests.Session() as session:
            session.headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
                'Referer': 'https://www.youlikehits.com/stats.php',
                'Accept-Language': 'en-US,en;q=0.9',
                'Host': 'www.youlikehits.com',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
            }
            response = session.get('https://www.youlikehits.com/account.php', cookies={
                'Cookie': cookies_youlikehits
            })
            if 'id="usernameDiv"' in response.text:
                username_youlikehits = re.search(r'id="usernameDiv".*?><b>(.*?)</b>', response.text).group(1)
                email_youlikehits = re.search(r'My Email</b>: (.*?)<br>', response.text).group(1)
                coin_youlikehits = re.search(r'id="currentpoints".*?>(.*?)<', response.text).group(1)
                KOIN['COUNT'] = coin_youlikehits.replace(",", "")
                return (
                    username_youlikehits, email_youlikehits, coin_youlikehits
                )
            else:
                Print(Panel(f"[bold red]Maaf, Sepertinya Cookies Akun Youlikehits Anda Sudah Tidak Valid, Silakan Coba Perbarui Cookies Anda!", width=65, style="bold bright_white", title="[bold bright_white]>> [Invalid Cookies] <<"))
                time.sleep(5.5)
                self.Login()

    def Periksa_Cookies_Instagram(self, cookies_instagram: str) -> tuple:
        with requests.Session() as session:
            ds_user_id = re.search(r'ds_user_id=(\d+);', str(cookies_instagram)).group(1)
            session.headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'User-Agent': 'Instagram 215.0.0.27.359 Android (30/11; 320dpi; 720x1448; realme; RMX3201; RMX3201; mt6765; ru_RU; 337202351)',
                'Cookie': '{}'.format(cookies_instagram),
                'Accept-Language': 'en-US,en;q=0.9'
            }
            response = session.get('https://i.instagram.com/api/v1/users/{}/info/'.format(ds_user_id), allow_redirects=False, verify=True)
            if "full_name" in response.text:
                self.json_data = json.loads(response.text)
                full_name_instagram, username_instagram = self.json_data['user']['full_name'], self.json_data['user']['username']
                return (
                    full_name_instagram, username_instagram
                )
            else:
                Print(Panel(f"[bold red]Maaf, Sepertinya Cookies Akun Instagram Anda Sudah Tidak Valid, Silakan Coba Perbarui Cookies Anda!", width=65, style="bold bright_white", title="[bold bright_white]>> [Invalid Cookies] <<"))
                time.sleep(5.5)
                self.Login()

def Tambah_Konfigurasi(cookies_youlikehits: str, username: str) -> str:
    Hapus_Konfigurasi(cookies_youlikehits, username)
    with requests.Session() as session:
        session.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Referer': 'https://www.youlikehits.com/addinstagram.php',
            'Host': 'www.youlikehits.com',
        }
        params = {
            'rand': random.random(),
            'step': 'verify',
            'uname': username,
        }
        response = session.get('https://www.youlikehits.com/addinstagram.php', params=params, cookies={
            'Cookie': cookies_youlikehits
        })
        if 'Your Instagram is Private.' not in response.text:
            if 'We couldn\'t find the Instagram account you\'re trying to add' in response.text:
                Print(Panel(f"[bold red]Maaf, Sepertinya Username Instagram Yang Anda Masukkan Salah atau Tidak Ditemukan, Silakan Coba Lagi!", width=65, style="bold bright_white", title="[bold bright_white]>> [Incorrect Username] <<"))
                exit()
            elif 'Success!' in response.text:
                return "Success"
            elif 'This Instagram account is already connected to an account on YouLikeHits' in response.text:
                Print(Panel(f"[bold red]Maaf, Sepertinya Akun Instagram Yang Anda Miliki Sudah Terkai\nt Dengan Akun Youlikehits Lain!", width=65, style="bold bright_white", title="[bold bright_white]>> [Username Limits] <<"))
                exit()
            else:
                Print(Panel(f"[bold red]Maaf, Sepertinya Terjadi Kesalahan Saat Menambahkan Akun Inst\nagram Anda, Silakan Coba Lagi Nanti!", width=65, style="bold bright_white", title="[bold bright_white]>> [Error] <<"))
                exit()
        else:
            Print(Panel(f"[bold red]Maaf, Sepertinya Akun Instagram Anda Dalam Mode Private, Sila\nkan Beralih Ke Mode Publik!", width=65, style="bold bright_white", title="[bold bright_white]>> [Permission Missing] <<"))
            exit()

def Hapus_Konfigurasi(cookies_youlikehits: str, username: str) -> str:
    with requests.Session() as session:
        session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'Referer': 'https://www.youlikehits.com/addinstagram.php',
            'Accept-Language': 'en-US,en;q=0.9',
            'Host': 'www.youlikehits.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        }
        params = {
            'step': 'remove',
        }
        response = session.get('https://www.youlikehits.com/addinstagram.php', params=params, cookies={
            'Cookie': cookies_youlikehits
        })
        response2 = session.get('https://www.youlikehits.com/addinstagram.php', cookies={
            'Cookie': cookies_youlikehits
        })
        if 'Adding your Instagram to YouLikeHits' in response2.text:
            return "Success"
        else:
            return "Mistakes"

def Tukarkan_Follower(cookies_youlikehits: str, payout: int) -> str:
    with requests.Session() as session:
        session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'Referer': 'https://www.youlikehits.com/addinstagram.php',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': '*/*',
            'Host': 'www.youlikehits.com',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        params = {
            'payout': payout, # Payout 20 / 30
            'step': 'payout',
            'rand': random.random(),
        }
        response = session.get('https://www.youlikehits.com/addinstagram.php', params=params, cookies={
            'Cookie': cookies_youlikehits
        })
        if 'Payout Changed to' in response.text:
            return "Success"
        else:
            Print(Panel(f"[bold red]Maaf, Kami Gagal Menukarkan Koin Anda Ke Pengikut, Silakan Coba Lakukan Penukaran Secara Mandiri!", width=65, style="bold bright_white", title="[bold bright_white]>> [Exchange Failed] <<"))
            exit()

def Hapus_Postingan(cookies_youlikehits: str) -> str:
    with requests.Session() as session:
        session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'Referer': 'https://www.youlikehits.com/addinstagramlikes.php',
            'Accept-Language': 'en-US,en;q=0.9',
            'Host': 'www.youlikehits.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        }
        response = session.get('https://www.youlikehits.com/addinstagramlikes.php', cookies={
            'Cookie': cookies_youlikehits
        })
        updatepayout = re.search(r'onchange="updatepayout\((\d+)\)"', response.text)
        if updatepayout:
            id_ = updatepayout.group(1)
            params = {
                'step': 'remove',
                'id': id_,
            }
            response2 = session.get('https://www.youlikehits.com/addinstagramlikes.php', params=params, cookies={
                'Cookie': cookies_youlikehits
            }).text
        else:
            return "Mistakes"

def Pengecekan_Penukaran(cookies_youlikehits: str) -> str:
    with requests.Session() as session:
        session.headers = {
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'Host': 'www.youlikehits.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        }
        response = session.get('https://www.youlikehits.com/addinstagram.php', cookies={
            'Cookie': cookies_youlikehits
        })
        if 'SELECTED' in response.text:
            Print(Panel(f"[bold red]Anda Telah Menukarkan Koin Ke Pengikut, Jika Anda Tetap Ingin Melanjutkan Ketik \"[bold green]Y[bold red]\" Lalu Enter.\nTapi Ingat Ini Akan Membatalkan Proses Penukaran!", width=65, style="bold bright_white", subtitle="[bold bright_white]╭────", subtitle_align="left", title="[bold bright_white]>> [Warning] <<"))
            confirm = Console().input("[bold bright_white]   ╰─> ")
            if confirm.lower() == "y":
                return "Cancel"
            else:
                Print(Panel(f"[bold white]Anda Tidak Membatalkan Proses Penukaran Koin, Sekarang Semua Pengikut Akan Segera Tiba Di Akun Anda!", width=65, style="bold bright_white", title="[bold bright_white]>> [Canceled] <<"))
                exit()
        else:
            return "Cancel"

def Tukarkan_Likes(cookies_youlikehits: str, payout: int, link_post: str) -> str:
    with requests.Session() as session:
        session.headers = {
            'Referer': 'https://www.youlikehits.com/addinstagramlikes.php',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Host': 'www.youlikehits.com',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        params = {
            'title': 'YouLikeInsta',
            'url': link_post,
            'step': 'verify',
            'rand': random.random(),
        }
        response = session.get('https://www.youlikehits.com/addinstagramlikes.php', params=params, cookies={
            'Cookie': cookies_youlikehits
        })
        if 'Success!' in response.text:
            session.headers.pop('Content-Type')
            session.headers.update({
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            })
            response2 = session.get('https://www.youlikehits.com/addinstagramlikes.php', cookies={
                'Cookie': cookies_youlikehits
            })
            updatepayout = re.search(r'onchange="updatepayout\((\d+)\)"', response2.text)
            id_ = updatepayout.group(1) if updatepayout else ""
            session.headers.update({
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': '*/*',
            })
            params = {
                'rand': random.random(),
                'step': 'payout',
                'id': id_,
                'payout': payout,
            }
            response3 = session.get('https://www.youlikehits.com/addinstagramlikes.php', params=params, cookies={
                'Cookie': cookies_youlikehits
            })
            if 'Payout Changed to' in response3.text:
                return "Success"
            else:
                Print(Panel(f"[bold red]Maaf, Kami Gagal Menukarkan Koin Anda Ke Likes, Silakan Coba Lakukan Penukaran Secara Mandiri!", width=65, style="bold bright_white", title="[bold bright_white]>> [Exchange Failed] <<"))
                exit()
        else:
            Print(Panel(f"[bold red]Maaf, Sepertinya Link Link Postingan Yang Anda Masukkan Salah\n. Silakan Periksa Lagi!", width=65, style="bold bright_white", title="[bold bright_white]>> [Wrong Link] <<"))
            exit()

def Features() -> None:
    Banner()
    try:
        with open('Penyimpanan/Cookie.json', 'r') as r:
            cookies = json.loads(r.read())
        cookies_youlikehits, cookies_instagram = cookies['Youlikehits'], cookies['Instagram']
        username_youlikehits, email_youlikehits, coin_youlikehits = Login().Periksa_Cookies_Youlikehits(cookies_youlikehits)
        full_name_instagram, username_instagram = Login().Periksa_Cookies_Instagram(cookies_instagram)
        Print(Columns([
            Panel(f"""[bold white]User  :[bold green] @{username_youlikehits}
[bold white]Email :[bold red] {email_youlikehits}""", width=32, style="bold bright_white"),
            Panel(f"""[bold white]User  :[bold green] @{username_instagram}
[bold white]Koin  :[bold red] {coin_youlikehits}""", width=32, style="bold bright_white"),
        ]))
    except Exception as e:
        Print(Panel(f"[bold red]{str(e).title()}!", width=65, style="bold bright_white", title="[bold bright_white]>> [Error] <<"))
        time.sleep(5.5)
        Login().Cookies()

    Print(
        Panel("""[bold green]1[bold white]. Tukarkan Koin Ke Pengikut Instagram
[bold green]2[bold white]. Tukarkan Koin Ke Likes Instagram
[bold green]3[bold white]. Jalankan Misi Follow Instagram
[bold green]4[bold white]. Dapatkan Bonus Koin ([bold green]75 Mision[bold white])
[bold green]5[bold white]. Keluar ([bold red]Exit[bold white])""", width=65, style="bold bright_white", title=f"[bold bold bright_white]>> [Key Features] <<", subtitle="[bold bold bright_white]╭────", subtitle_align="left")
    )
    options = Console().input("[bold bright_white]   ╰─> ")
    if options in ["01", "1"]:
        Print(Panel("""[bold green]1[bold white]. Setiap 1 Pengikut[bold green] 30[bold white] Koin Mode Fast
[bold green]2[bold white]. Setiap 1 Pengikut[bold green] 20[bold white] Koin Mode Slow""", width=65, style="bold bright_white", title="[bold bold bright_white]>> [Coin Amount] <<", subtitle="[bold bold bright_white]╭────", subtitle_align="left"))
        follower_choices = Console().input("[bold bright_white]   ╰─> ")
        Print(Panel("[bold white]Silakan Untuk Memasukkan Username Akun Instagram dan Harus Dipastikan Agar Akun Tidak Terkunci!", width=65, style="bold bright_white", subtitle="[bold bright_white]╭────", subtitle_align="left", title="[bold bright_white]>> [Username] <<"))
        username = Console().input("[bold bright_white]   ╰─> ").replace('@', '')
        Tambah_Konfigurasi(cookies_youlikehits, username)
        Tukarkan_Follower(cookies_youlikehits, 30 if follower_choices == '1' else 20)
        quantity = int(KOIN['COUNT']) // 30 if follower_choices == '1' else int(KOIN['COUNT']) // 20
        Print(Panel(f"""[bold white]Status :[bold green] Successfully!
[bold white]Link :[bold yellow] https://www.instagram.com/{username}
[bold white]Jumlah :[bold green] {quantity}""", width=65, style="bold bright_white", title="[bold bold bright_white]>> [Success] <<"))
        exit()
    elif options in ["02", "2"]:
        Print(Panel("""[bold green]1[bold white]. Setiap 1 Likes[bold green] 30[bold white] Koin Mode Fast
[bold green]2[bold white]. Setiap 1 Likes[bold green] 20[bold white] Koin Mode Slow""", width=65, style="bold bright_white", title="[bold bold bright_white]>> [Coin Amount] <<", subtitle="[bold bold bright_white]╭────", subtitle_align="left"))
        like_choices = Console().input("[bold bright_white]   ╰─> ")
        Print(Panel("[bold white]Silakan Untuk Memasukkan Link Postingan Instagram Yang Ingin Anda Tambahkan Likes!", width=65, style="bold bright_white", subtitle="[bold bright_white]╭────", subtitle_align="left", title="[bold bright_white]>> [Post Links] <<"))
        link_post = Console().input("[bold bright_white]   ╰─> ")
        Tukarkan_Likes(cookies_youlikehits, 30 if like_choices == '1' else 20, link_post)
        quantity = int(KOIN['COUNT']) // 30 if like_choices == '1' else int(KOIN['COUNT']) // 20
        Print(Panel(f"""[bold white]Status :[bold green] Successfully!
[bold white]Link :[bold yellow] {link_post}
[bold white]Jumlah :[bold green] {quantity}""", width=65, style="bold bright_white", title="[bold bold bright_white]>> [Success] <<"))
        exit()
    elif options in ["03", "3"]:
        Pengecekan_Penukaran(cookies_youlikehits)
        Print(Panel("[bold white]Silakan Masukkan Jeda Setiap Misi, Kami Menyarankan Untuk Menggunakan Jeda Diatas 30 Detik Agar Aman!", width=65, style="bold bright_white", subtitle="[bold bright_white]╭────", subtitle_align="left", title="[bold bright_white]>> [Mission Pause] <<"))
        delay = int(Console().input("[bold bright_white]   ╰─> "))
        Tambah_Konfigurasi(cookies_youlikehits, username_instagram)
        Print(Panel(f"[bold white]Anda Bisa Menggunakan[bold yellow] CTRL + C[bold white] Jika Stuck dan Menggunakan[bold red] CTRL + Z[bold white] Jika Ingin Berhenti!", width=65, style="bold bright_white", title="[bold bright_white]>> [Notes] <<"))
        while True:
            try:
                if len(DUMP) == 0:
                    Mission().Dumps(cookies_youlikehits)
                    continue
                else:
                    Mission().Follow(cookies_youlikehits, cookies_instagram, delay)
            except RequestException:
                Print(f"[bold bright_white]   ──>[bold red] KONEKSI ANDA BERMASALAH!     ", end='\r')
                time.sleep(10.0)
                continue
            except KeyboardInterrupt:
                Print("                                 ", end='\r')
                time.sleep(2.5)
                continue
            except Exception as e:
                Print(Panel(f"[bold red]{str(e).title()}!", width=65, style="bold bright_white", title="[bold bright_white]>> [Error] <<"))
                break
        exit()
    elif options in ["04", "4"]:
        Bonus_Koin(cookies_youlikehits)
        Print(Panel(f"[bold green]Selamat![bold red] Anda Berhasil Mendapatkan Bonus Koin, Silakan Untuk Memeriksa Koin Anda!", width=65, style="bold bright_white", title="[bold bright_white]>> [Success] <<"))
        exit()
    elif options in ["05", "5"]:
        os.remove('Penyimpanan/Cookie.json')
        Print(Panel(f"[bold white]Terima Kasih Telah Menggunakan Program Ini, Semoga Anda Puas Dengan Layanan Kami!", width=65, style="bold bright_white", title="[bold bright_white]>> [Exit] <<"))
        exit()
    else:
        Print(Panel(f"[bold red]Maaf, Pilihan Yang Anda Masukkan Tidak Tersedia Di Program Ini, Silakan Coba Lagi!", width=65, style="bold bright_white", title="[bold bright_white]>> [Incorrect Option] <<"))
        time.sleep(5.5)
        Features()

def Bonus_Koin(cookies_youlikehits: str) -> str:
    with requests.Session() as session:
        session.headers = {
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
            'Host': 'www.youlikehits.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        }
        response = session.get('https://www.youlikehits.com/bonuspoints.php', cookies={
            'Cookie': cookies_youlikehits
        })
        session.headers.update({
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
        })
        params = {
            'step': 'get',
        }
        response2 = session.get('https://www.youlikehits.com/bonuspoints.php', params=params, cookies={
            'Cookie': cookies_youlikehits
        })
        if 'You received' in response2.text:
            return "Success"
        else:
            Print(Panel(f"[bold red]Maaf, Tidak Ada Bonus Yang Tersedia Untuk Saat Ini, Silakan Jalankan Misi 75 Misi!", width=65, style="bold bright_white", title="[bold bright_white]>> [Empty Bonus] <<"))
            exit()

class Mission:

    def __init__(self) -> None:
        pass

    def Follow(self, cookies_youlikehits: str, cookies_instagram: str, delay: int) -> None:
        for data in DUMP:
            user_id, username, rand, link = data.split("|")
            if username in SUDAH:
                continue
            for sleep in range(delay, 0, -1):
                time.sleep(1.0)
                Print(f"[bold bright_white]   ──>[bold green] TUNGGU {sleep} DETIK...[bold white]                               ", end = '\r')
            with requests.Session() as session:
                session.headers = {
                    'x-csrftoken': re.search('csrftoken=(.*?);', str(cookies_instagram)).group(1),
                    'Referer': 'https://www.instagram.com/{}/'.format(username),
                    'Accept-Language': 'en-US,en;q=0.9',
                    'User-Agent': 'Instagram 215.0.0.27.359 Android (30/11; 320dpi; 720x1448; realme; RMX3201; RMX3201; mt6765; en_US; 337202351)',
                }
                try:
                    response = session.get('https://www.instagram.com/api/v1/users/web_profile_info/?username={}'.format(username), cookies = {
                        'Cookie': cookies_instagram
                    }).json()
                    userid_follow = response['data']['user']['id']
                except (KeyError, json.decoder.JSONDecodeError, TypeError):
                    self.Skiped(cookies_youlikehits, username)
                    continue
                session.headers.update({
                    'x-instagram-ajax': '1007136769',
                    'x-ig-www-claim': 'hmac.AR0lIitHyhqaelpdO_-emvAj8pjGuGop5PyHOfL0tMhndFzr',
                    'Host': 'www.instagram.com',
                    'x-ig-app-id': '936619743392459',
                    'content-type': 'application/x-www-form-urlencoded',
                    'accept': '*/*',
                    'origin': 'https://www.instagram.com',
                    'x-asbd-id': '198387',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
                })
                data = {
                    'container_module': 'profile',
                    'nav_chain': 'PolarisProfileRoot:profilePage:1:via_cold_start',
                    'user_id': userid_follow,
                }
                response2 = session.post('https://www.instagram.com/api/v1/friendships/create/{}/'.format(userid_follow), data=data, cookies={
                    'cookie': cookies_instagram
                })
                if '"status":"ok"' in response2.text:
                    with requests.Session() as session:
                        session.headers.update({
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
                            'Referer': 'https://www.youlikehits.com/instagram.php',
                            'Accept-Language': 'en-US,en;q=0.9',
                            'Host': 'www.youlikehits.com',
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                            'Sec-Fetch-Site': 'same-origin',
                        })
                        params = {
                            'uname': username,
                        }
                        response2 = session.get('https://www.youlikehits.com/instagramrender.php', params=params, cookies={
                            'Cookie': cookies_youlikehits
                        })
                        session.headers.pop('Sec-Fetch-Site')
                        time.sleep(5.0)
                        session.headers.update({
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'Referer': 'https://www.youlikehits.com/instagram.php',
                            'Host': 'www.youlikehits.com',
                            'Accept': '*/*',
                            'Accept-Language': 'en-US,en;q=0.9',
                        })
                        params = {
                            'id': user_id,
                            'rand': rand,
                        }
                        response = session.get('https://www.youlikehits.com/instagramfollow.php', params=params, cookies={
                            'Cookie': cookies_youlikehits
                        })
                        if 'Login to YouLikeHits' in response.text:
                            Print(Panel(f"[bold red]Maaf, Sepertinya Cookies Akun Youlikehits Anda Sudah Tidak Valid, Silakan Coba Perbarui Cookies Anda!", width=65, style="bold bright_white", title="[bold bright_white]>> [Invalid Cookies] <<"))
                            exit()
                        elif 'You already followed this person before.' in response.text:
                            self.Skiped(cookies_youlikehits, username)
                            continue
                        elif 'Success!' in response.text:
                            self.Koin(session, cookies_youlikehits)
                            Print(f"[bold bright_white]   ──>[bold green] BERHASIL FOLLOW @{username}!     ", end='\r')
                            try:
                                points = re.search('You got (.*?) Points!', response.text).group(1)
                            except:
                                points = "0"
                            Print(Panel(f"""[bold white]Status :[bold green] Successfully!
[bold white]Username :[bold yellow] @{username}
[bold white]Koin :[bold green] {points}[bold white] >[bold red] {KOIN['COUNT']}""", width=65, style="bold bright_white", title="[bold bright_white]>> [Success] <<"))
                            time.sleep(5.0)
                            SUDAH.append(username)
                        elif 'We were not able to verify that you Followed this user.' in response.text:
                            for i in range(10):
                                params = {
                                    'id': user_id,
                                    'rand': rand,
                                }
                                time.sleep(2.5)
                                response2 = session.get('https://www.youlikehits.com/instagramfollow.php', params=params, cookies={
                                    'Cookie': cookies_youlikehits
                                })
                                if 'Success!' in response2.text:
                                    self.Koin(session, cookies_youlikehits)
                                    Print(f"[bold bright_white]   ──>[bold green] BERHASIL FOLLOW @{username}!     ", end='\r')
                                    try:
                                        points = re.search('You got (.*?) Points!', response2.text).group(1)
                                    except:
                                        points = "0"
                                    Print(Panel(f"""[bold white]Status :[bold green] Successfully!
[bold white]Username :[bold yellow] @{username}
[bold white]Koin :[bold green] {points}[bold white] >[bold red] {KOIN['COUNT']}""", width=65, style="bold bright_white", title="[bold bright_white]>> [Success] <<"))
                                    time.sleep(5.0)
                                    SUDAH.append(username)
                                    break
                                else:
                                    continue
                            self.Skiped(cookies_youlikehits, username)
                            continue
                        else:
                            SUDAH.append(username)
                            Print(f"[bold bright_white]   ──>[bold red] GAGAL FOLLOW @{username}!     ", end='\r')
                            time.sleep(2.5)
                            continue
                else:
                    SUDAH.append(username)
                    Print(f"[bold bright_white]   ──>[bold yellow] GAGAL FOLLOW @{username}!     ", end='\r')
                    time.sleep(2.5)
                    continue
        DUMP.clear()
        return None

    def Koin(self, session: requests.Session, cookies_youlikehits: str) -> None:
        session.headers.update({
            'Referer': 'https://www.youlikehits.com/stats.php',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        })
        response = session.get('https://www.youlikehits.com/account.php', cookies={
            'Cookie': cookies_youlikehits
        })
        coin = re.search(r'id="currentpoints".*?>(.*?)<', response.text).group(1)
        KOIN['COUNT'] = coin.replace(",", "")

        return None

    def Skiped(self, cookies_youlikehits: str, user_id: str) -> None:
        SUDAH.append(user_id)
        with requests.Session() as session:
            session.headers = {
                'Accept-Language': 'en-US,en;q=0.9',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Referer': 'https://www.youlikehits.com/instagram.php',
                'Host': 'www.youlikehits.com',
            }
            response = session.get('https://www.youlikehits.com/instagram.php', cookies = {
                'Cookie': cookies_youlikehits
            })
            session.headers.update({
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': '*/*',
            })
            params = {
                'step': 'skip',
                'id': user_id,
            }
            response2 = session.get('https://www.youlikehits.com/instagramfollow.php', params=params, cookies={
                'Cookie': cookies_youlikehits
            })
            if 'Skipped!' in response2.text:
                Print(f"[bold bright_white]   ──>[bold green] BERHASIL MELEWATI @{user_id}!     ", end='\r')
            else:
                Print(f"[bold bright_white]   ──>[bold red] GAGAL MELEWATI @{user_id}!     ", end='\r')
            time.sleep(5.0)
        return None

    def Dumps(self, cookies_youlikehits: str) -> None:
        with requests.Session() as session:
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
                'Host': 'www.youlikehits.com',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            })
            response = session.get('https://www.youlikehits.com/instagram.php', cookies={
                'Cookie': cookies_youlikehits
            })
            followuser = re.findall(r'onclick="followuser\(\'(\d+)\',\'(.*?)\',\'(.*?)\'\);', response.text)
            for data in followuser:
                user_id, username, rand = data[0], data[1], data[2]
                if username in DUMP or username in SUDAH:
                    continue
                if '?igshid' in username:
                    username = username.split("?")[0]
                DUMP.append(f'{user_id}|{username}|{rand}|https://www.instagram.com/{username}/')
            if len(DUMP) == 0:
                Print(f"[bold bright_white]   ──>[bold red] TIDAK ADA MISI!         ", end='\r')
                time.sleep(10.0)
            return None

if __name__ == '__main__':
    try:
        os.system("git pull")
        Features()
    except KeyboardInterrupt:
        exit()
    except Exception as e:
        Print(Panel(f"[bold red]{str(e).title()}!", width=65, style="bold bright_white", title="[bold bright_white]>> [Error] <<"))
        time.sleep(5.5)
        exit()