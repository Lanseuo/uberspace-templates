import os
import pwd


def get_username():
    return pwd.getpwuid(os.getuid())[0]


def renew_letsencrypt():
    print("\nRenew LetsEncrypt")
    os.system("mv /home/{}/.config/letsencrypt/cli.ini /home/{}/.config/letsencrypt/cli.ini.old").format(
        get_username(), get_username())
    os.system("uberspace-letsencrypt")
    os.system("letsencrypt certonly")
    live_certificate_folder = os.listdir(
        "/home/{}/.config/letsencrypt/live").format(get_username())[0]
    os.system("uberspace-add-certificate -k ~/.config/letsencrypt/live/{}/privkey.pem -c ~/.config/letsencrypt/live/{}/cert.pem").format(
        live_certificate_folder, live_certificate_folder)


def ask_domain():
    print("\n")
    domain = ""
    while not domain:
        domain = input("Domain: ")
    return domain


def add_uberspace_domain(domain, method="w"):
    print("\nAdd domain ({}) to Uberspace".format(domain))
    os.system("uberspace-add-domain -d " + domain + " -" + method)
    renew_letsencrypt()


def add_htaccess(domain, https=True, reverse_proxy_port=False):
    print("\nCreate webroot")
    os.system("mkdir /var/www/virtual/{}/".format(get_username()) + domain)

    file_path = "/var/www/virtual/{}/".format(get_username()) + domain + "/.htaccess"
    print("\nAdd .htaccess ({})".format(file_path))
    content = "RewriteEngine On\n"

    if https:
        content += "RewriteCond %{HTTPS} !=on\n"
        content += "RewriteCond %{ENV:HTTPS} !=on\n"
        content += "RewriteRule .* https://%{SERVER_NAME}%{REQUEST_URI} [R=301,L]\n"

    if reverse_proxy_port:
        content += "RewriteRule (.*) http://localhost:" + str(reverse_proxy_port) + "/$1 [P]\n"

    with open(file_path, "w") as f:
        f.write(content)


def ask_and_find_port():
    port = input("\nPort (random available): ") or 61605
    port = int(port)
    found = False

    while not found:
        try:
            subprocess.check_output("netstat -tulpen | grep " + str(port), shell=True)
            port += 1
        except:
            found = True
    print("Application will listen on localhost:" + str(port))
    return port
